from __future__ import annotations

import contextlib
import functools
import pathlib
import pickle
import random
import types
from abc import ABC, abstractmethod
from base64 import b16decode
from collections import OrderedDict, namedtuple
from collections.abc import Callable, Coroutine, Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from traceback import print_exc
from typing import Any, Generic, Never, TypeVar, cast
from uuid import UUID, uuid4
from weakref import WeakValueDictionary

import asyncache
import bson
import marisa_trie
from anyio import Path
from cachetools import Cache, TTLCache

# from .pyparser import pyparse
# from .pyutil import wsyll2mltrie
from .textutil import glued
from .unitutil import byte2size, num2ch

logger = getLogger("lexloader")

T = TypeVar("T")


class EmptyResponse(ValueError):
    pass


class PoolDrained(ValueError):
    pass


class UnsupportedFileType(ValueError):
    pass


class UnsupportedOperation(NotImplementedError):
    pass


class RefillDisabledError(OverflowError):
    pass


class BatchedFunc(Generic[T]):

    registered: set[BatchedFunc] = set()

    def __init__(self, func: Callable[..., Coroutine[None, None, Iterable[T]]], batch_size: int, max_size: int, no_refill: bool = False):
        self.func = func
        self.batch_size = batch_size
        self.max_size = max_size
        self.no_refill = no_refill
        self.cache: OrderedDict[tuple[tuple[Any, ...], frozenset[tuple[str, Any]]], Iterator[T]] = OrderedDict()

        functools.update_wrapper(self, func)

        BatchedFunc.registered.add(self)

    async def __call__(self, *args: Any, **kwargs: Any) -> T:
        kwargs.pop("num", None)  # 忽略num参数
        key: tuple[tuple[Any, ...], frozenset[tuple[str, Any]]] = (args, frozenset(kwargs.items()))

        try:
            self.cache.move_to_end(key)
            return next(self.cache[key])
        except (KeyError, StopIteration) as e:
            if self.no_refill and isinstance(e, StopIteration):
                raise RefillDisabledError

            result = await self.func(*args, **kwargs, num=self.batch_size)
            spawned = iter(result)

            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)

            self.cache[key] = cast(Iterator[T], spawned)
            self.cache.move_to_end(key)

            try:
                return next(spawned)
            except StopIteration:
                raise PoolDrained

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        return types.MethodType(self, obj)

    def get_pool(self) -> OrderedDict[tuple[tuple[Any, ...], frozenset[tuple[str, Any]]], Iterator[T]]:
        return self.cache

    def reset_pool(self) -> None:
        self.cache.clear()

    @classmethod
    def reset_all_pools(cls) -> None:
        for batched in cls.registered:
            batched.reset_pool()


def abatched(batch_size: int, max_size: int, no_refill: bool = False):
    def deco(func: Callable[..., Coroutine[None, None, Iterable[T]]]) -> BatchedFunc[T]:
        return BatchedFunc[T](func, batch_size, max_size, no_refill)

    return deco


class CacheHub:
    def __init__(self):
        self.participants: WeakValueDictionary[UUID, TTLCache] = WeakValueDictionary()

    def register(self, participant: Any):
        self.participants[uuid4()] = participant

    def expire(self):
        logger.info("LexLoader Cache EXPIRE Triggered")
        for participant in self.participants.values():
            participant.expire()

    def expire_now(self):
        logger.info("LexLoader Cache EXPIRE_NOW Triggered")
        for participant in self.participants.values():
            participant.clear()

    def __call__(self, cache: TTLCache):
        self.register(cache)
        return cache


cache_hub = CacheHub()


class LexLoader(ABC):
    loaded: WeakValueDictionary[str, LexLoader] = WeakValueDictionary()

    Tname = "词表"

    @dataclass
    class Meta:
        name: str = ""
        filename: str = ""
        description: str = ""
        updated: datetime = datetime(1970, 1, 1)
        filesize: int = 0
        memusage: int = 0
        shape: tuple[int, int] = (0, 0)  # 先行数后列数
        extra: dict[str, Any] | None = None

    DataMeta = namedtuple("DataMeta", ["memusage", "shape", "extra"])

    def __init__(self, path: Path):
        self.path = path
        self.meta = LexLoader.Meta()
        self.meta.name = b16decode(path.stem.encode("ASCII")).decode("UTF8")
        LexLoader.loaded[self.meta.name] = self
        self.meta.filename = f"{path.stem[:8]}{"……" if len(path.stem) > 8 else ""}{path.suffix}"

    async def show_meta(self) -> str:
        if self.meta.extra is None:
            stat = await self.path.stat()
            self.meta.filesize = stat.st_size
            self.meta.updated = datetime.fromtimestamp(stat.st_mtime)
            meta_update_data = await self.get_datameta()
            self.meta.memusage = meta_update_data.memusage
            self.meta.shape = meta_update_data.shape
            self.meta.extra = meta_update_data.extra

        filesize_val, filesize_unit = byte2size(self.meta.filesize)
        memusage_val, memusage_unit = byte2size(self.meta.memusage)
        size_rows_val, size_rows_unit = num2ch(self.meta.shape[0])
        size_rows_val = f"{size_rows_val:.1f}" if size_rows_unit else f"{size_rows_val:d}"
        desc_cmp = f"“ {self.meta.description.replace("\n", "  \n")} ”\n" if self.meta.description else ""
        extra_cmp = f"\n  其他信息：\n  {"\n  ".join(f"{k}：{v}" for k, v in self.meta.extra.items())}" if self.meta.extra else ""

        return (
            f"词表\u200b「{self.meta.name}」\u200b{size_rows_val}\u2060{size_rows_unit}\u2060词\u2060头\n"
            f"  文件：{self.meta.filename} {self.Tname}\n"
            f"  {filesize_val:.2f}\u2060{filesize_unit}\u00a0SSD {memusage_val:.2f}\u2060{memusage_unit}\u00a0RAM\n"
            f"  上次更新：{self.meta.updated.strftime('%Y-%m-%d %H:%M:%S')}"
            f"  {desc_cmp}{extra_cmp}"
        )

    @classmethod
    async def search_word(cls, word: str) -> list[LexLoader]:
        return [lex for lex in cls.loaded.values() if await lex.contains(word)]

    @abstractmethod
    async def data(self) -> Any:
        pass

    @abstractmethod
    async def get_datameta(self) -> DataMeta:
        pass

    @abstractmethod
    async def __getitem__(self, key: slice[int | None, str | None]) -> str:
        pass

    @abstractmethod
    async def contains(self, key: str) -> bool:
        pass

    async def __contains__(self, *_) -> Never:
        raise TypeError("LexLoader不允许使用同步的in操作。应当使用异步的ll.contains(word)。")


class LexLoader_mrswl(LexLoader):
    Tname = glued("使用MARISA压缩的词表")

    @asyncache.cached(cache_hub(TTLCache(maxsize=1, ttl=120)))
    async def data(self) -> marisa_trie.Trie:
        return pickle.loads(await self.path.read_bytes())

    @asyncache.cached(Cache(maxsize=1))
    async def get_datameta(self) -> LexLoader.DataMeta:
        data = await self.data()
        return LexLoader.DataMeta(memusage=len(pickle.dumps(data)), shape=(len(data), 1), extra={})

    @abatched(128, 32)
    async def get(self, num: int, length: int | None = None, prefix: str = ""):
        logger.info(f"LL.MRSWL.GET {self.meta.name} {num=} {length=} {prefix=}")
        if prefix.startswith("…") or prefix.startswith("..."):
            raise UnsupportedOperation("MARISA压缩的词表不支持使用拼音反查。")
        prefix = prefix.rstrip(".…")
        data = await self.data()
        if length is None and not prefix:
            total = len(data)
            chosen = random.sample(range(total), min(num, total))
            return [data.restore_key(i) for i in chosen]
        reservoir: list[str] = []
        count = 0
        for word in data.iterkeys(prefix):
            if length is not None and len(word) != length:
                continue
            count += 1
            if len(reservoir) < num:
                reservoir.append(word)
            elif (i := random.random() * count) < num:
                reservoir[int(i)] = word
        random.shuffle(reservoir)
        return reservoir

    async def __getitem__(self, key: slice[int | None, str | None]) -> str:
        logger.info(f"LL.MRSWL.GI {self.meta.name} {key=}")
        try:
            return await self.get(length=key.start, prefix=key.stop or "")
        except Exception:
            print_exc()
            raise

    async def contains(self, key: str) -> bool:
        return key in await self.data()


class LexLoader_cset(LexLoader):
    Tname = glued("字库")

    @asyncache.cached(cache_hub(TTLCache(maxsize=1, ttl=120)))
    async def data(self) -> str:
        return (await self.path.read_text(encoding="utf-8")).strip()

    @asyncache.cached(Cache(maxsize=1))
    async def get_datameta(self) -> LexLoader.DataMeta:
        data = await self.data()
        return LexLoader.DataMeta(
            memusage=len(data.encode("utf-8")),
            shape=(len(data), 1),
            extra={"关于长度": "字库的限定长度用于指定想要多少个字，等效于[[[[xxx]] **len]]"},
        )

    @abatched(128, 32)
    async def get(self, num: int, length: int | None = None):
        data = await self.data()
        chosen = random.sample(range(len(data)), min(num, len(data)))
        cstr = [data[i] for i in chosen]
        length = max(length or 1, 1)
        return ["".join(cstr[i : i + length]) for i in range(0, len(cstr), length)]

    async def __getitem__(self, key: slice[int | None, str | None]) -> str:
        """if key.stop is not None:
        raise UnsupportedOperation("字库不支持使用拼音反查或前后缀操作。")"""
        return await self.get(length=key.start)

    async def contains(self, key: str) -> bool:
        return (len(key) == 1) and (key in await self.data())


class LexLoader_csset(LexLoader_cset):
    Tname = glued("逻辑字库子集")

    @asyncache.cached(cache_hub(TTLCache(maxsize=1, ttl=120)))
    async def data(self) -> str:
        try:
            self.bs
        except AttributeError:
            self.bs = bson.decode(await self.path.read_bytes())
            parent_name = self.bs["name"]
            self.parent = LexLoader.loaded[parent_name]
            self.start_idx = self.bs["start"]
            self.end_idx = self.bs["end"]

        return (await self.parent.data())[self.start_idx : self.end_idx]


def lexload(path: Path | str) -> LexLoader:
    path = Path(path)
    match path.suffix:
        case ".mrswl":
            return LexLoader_mrswl(path)
        case ".cset":
            return LexLoader_cset(path)
        case ".csset":
            return LexLoader_csset(path)
        case _:
            raise UnsupportedFileType

            # 注意: LexLoader中对于已创建的词库的引用是弱引用，因此不应当丢弃lexload的返回值


default_load_directory = pathlib.Path("R:/Aha/modules/tianzi/lexicons/Lexicon_compiled/")
default_loaded_lexicons = []

for file_path in default_load_directory.iterdir():
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
    if file_path.is_file():
        with contextlib.suppress(UnsupportedFileType):
            loader = lexload(str(file_path))
            default_loaded_lexicons.append(loader)
