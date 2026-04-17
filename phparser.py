import base64
import numbers
import pickle
import secrets
import time
import uuid
from collections import deque
from collections.abc import Callable, Coroutine, Iterator
from dataclasses import dataclass
from functools import partial
from itertools import pairwise, repeat
from logging import getLogger
from random import Random
from typing import Any, Literal, Protocol, cast, runtime_checkable

import aiohttp
import ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING
import numpy as np
import orjson
import regex
from anyio import Path
from cachetools import TTLCache
from regex import Match as _Match
from regex import Pattern as _Pattern
from regex import escape

from . import lexloaders
from .cacheutil import Cache
from .fontutil import fonts
from .MLTrie import SourceEmptyError
from .numutil import Value, numfmt, numify, numsify, numsimp
from .randutil import rngs, rsgs
from .textutil import find_outmost_bracket

# region init

type Match = _Match[str]
type Pattern = _Pattern[str]
type Translator = Callable[[Match], Coroutine[None, None, SupportsStr]]

calc_cache: Cache[Any] = Cache("T.Calc")
result_cache: Cache[SupportsStr] = Cache("T.Ret")

translators: list[tuple[Pattern, Translator]] = []

logger = getLogger("translators")

_RESET_COUNT = 0

OTP: deque[str] = deque(maxlen=10)
OTP_EXPIRE: deque[float] = deque(maxlen=10)

random = Random(ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING.ANSWER)
nrandom = np.random.default_rng(ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING.ANSWER)

CALL_STACK: list[str] = []

LINGERS: TTLCache[str, dict[str, SupportsStr]] = TTLCache(maxsize=1024, ttl=86400)


class BreakOut(Exception):
    pass


class PosteriorReject(Exception):
    pass


class WhatTheFuckIsThis(Exception):
    pass


class PUACharDrained(Exception):
    pass


@runtime_checkable
class SupportsStr(Protocol):
    def __str__(self) -> str: ...


EPACSE = {n: n - 0xE000 for n in range(0xE000, 0xE080)}
NESTED_INLINE_EPACSE: dict[str, str] = {}

# endregion

# region funs


def breakout(mch: Match, abbr: str, msg: str) -> str:
    match CurrentStat.err_level:
        case "ignore":
            return ""
        case "abort":
            return egroup(mch, 0)
        case "inline":
            return abbr
        case "raise":
            raise BreakOut(msg.replace("{d}", egroup(mch, 0)))


def translator(pattern: str) -> Callable[[Translator], Translator]:
    def deco(func: Translator) -> Translator:
        translators.append((regex.compile(pattern, flags=80), func))  # 80: DOTALL | VERBOSE
        return func

    return deco


def helps() -> str:
    return "\n".join(trans[1].__doc__ or "" for trans in translators)


# 目前已占用的PUA: 0xE000-0xE07F(ASCII转义) 0xE104-0xE500(嵌套指令打包)
async def translate(text: str, final: bool = False) -> SupportsStr:
    if len(text) > 65535:
        raise BreakOut("[E31] 尝试转换的文本过长。输入不得大于65535字符")

    if CurrentStat.allow_pua_warning:
        CurrentStat.pua_warning |= bool(regex.search("[\ue000-\ue07f\ue104-\ue500]", text))
    else:
        CurrentStat.pua_warning = False

    logger.info(f"TRANSLATE {text} ↓↓↓")

    text = regex.sub("\\\\([\x00-\x7f])", lambda m: chr(ord(m.group(1)) + 0xE000), text)

    fields_index: list[tuple[int, int]] = find_outmost_bracket((SYM_HEAD, SYM_TAIL), text)
    fields = deque(text[i + len(SYM_HEAD) : j - len(SYM_TAIL)] for i, j in fields_index)
    if not fields:
        ret = text

    global NESTED_INLINE_EPACSE
    nested_cmd_chr_it: Iterator[str] = map(chr, range(0xE104, 0xE500))

    for i, field in enumerate(fields):
        print(f"debug: {i=} {field=}")
        nested_cmds: list[tuple[int, int]] = [(0, 0)] + find_outmost_bracket((SYM_HEAD, SYM_TAIL), field) + [(len(field), 114514)]
        cmd_segs = []
        nested_cmd_map: dict[str, str] = {}
        for segi, segj in pairwise(nested_cmds):
            if segi[0] != segi[1]:
                try:
                    nested_cmd_chr = next(nested_cmd_chr_it)
                except StopIteration:
                    raise PUACharDrained
                nested_cmd_map[nested_cmd_chr] = field[segi[0] : segi[1]]
                cmd_segs.append(nested_cmd_chr)
            cmd_segs.append(field[segi[1] : segj[0]])

        field = "".join(cmd_segs)
        print(f"debug: new {field=}")
        NIEPACSE_backup = NESTED_INLINE_EPACSE.copy()
        NESTED_INLINE_EPACSE |= nested_cmd_map
        print(f"debug: {NIEPACSE_backup=} {NESTED_INLINE_EPACSE=}")

        for pat, fun in translators:
            mch = pat.fullmatch(field, concurrent=True, timeout=5)
            if mch:
                CALL_STACK.append(f"{fun.__name__}[")
                try:
                    field = str(await fun(mch))
                    CALL_STACK.append("]")
                    break
                except PosteriorReject:
                    CALL_STACK.pop()
                    continue
        fields[i] = field
        NESTED_INLINE_EPACSE = NIEPACSE_backup
    text_lst = []
    last_j = 0
    for i, j in fields_index:
        text_lst.append(text[last_j:i])
        text_lst.append(fields.popleft())
        last_j = j
    text_lst.append(text[last_j:])
    ret = "".join(text_lst)

    if isinstance(ret, str):
        ret = ret.translate(EPACSE)
    logger.info(f"TRANSLATE {text} → {ret} ↑↑↑")

    if final:
        ret = epacse(ret)

    return ret


def fusr_to_nfmt_fmt(fusr: str) -> Literal["c", "C", "u", "n", "r", "R"]:
    return cast(
        Literal["c", "C", "u", "n", "r", "R"], {"cn": "c", "CN": "C", "u": "u", "U": "u", "unicode": "u", "ro": "r", "RO": "R"}.get(fusr, "n")
    )


def reset(intial_result_cache: dict[str, SupportsStr] | None = None):
    global calc_cache, result_cache, random, nrandom, CurrentStat, _RESET_COUNT, CENSOR, CALL_STACK
    _RESET_COUNT += 1
    calc_cache.clear()

    if CurrentStat.linger_name and CurrentStat.linger_names:
        LINGERS[CurrentStat.linger_name] = {k: v for k, v in result_cache.caches["Ret"].items() if k in CurrentStat.linger_names}
    result_cache.clear()
    if intial_result_cache:
        result_cache.caches["Ret"] = intial_result_cache
    random = Random(ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING.ANSWER + _RESET_COUNT)
    nrandom = np.random.default_rng(ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING.ANSWER + _RESET_COUNT)
    CurrentStat = _Stat()
    CALL_STACK.clear()
    lexloaders.BatchedFunc.reset_all_pools()


def set_new_otp(exp=60):
    global OTP, OTP_EXPIRE
    if OTP_EXPIRE and OTP_EXPIRE[-1] > time.monotonic():
        # 已经有正在使用的验证码，直接刷新有效时长，不更新验证码
        OTP_EXPIRE[-1] = time.monotonic() + exp
    else:
        OTP.append("".join(secrets.choice("0123456789ABCDEFGHKLMNPRSTUWXY") for _ in range(6)))
        OTP_EXPIRE.append(time.monotonic() + exp)
    return OTP[-1]


def check_otp(otp: str) -> int:
    otp = otp.upper()
    for valid, exp in zip(OTP, OTP_EXPIRE):
        if otp == valid:
            if time.monotonic() < exp:
                return 0  # 成功
            else:
                return 1  # 过期
    return 2  # 无效


def group(mch: Match, group: str | int) -> str:
    return mch.group(group) or ""


def egroup(mch: Match, group: str | int) -> str:
    return (g := mch.group(group)) and epacse(g) or ""


def epacse(s: str):
    for c, r in NESTED_INLINE_EPACSE.items():
        s = s.replace(c, r)
    return s.translate(EPACSE)


async def tegroup(mch: Match, group: str | int) -> SupportsStr:
    return await translate(egroup(mch, group))


async def stegroup(mch: Match, group: str | int) -> str:
    return str(await tegroup(mch, group))


# endregion

# region symbols

SYM_HEAD = "[["
SYM_TAIL = "]]"
SYM_MODIFY = "@"
SYM_LENGTH = "="
SYM_CACHE = ">"

CS_RANGE = "-~－～—到至"  # CharSet
CS_SEGSEP = ";；|/"
CS_SEP = "，、；？,.; \n"
CS_INLINE = "\ue104-\ue500"


RSYM_HEAD = escape(SYM_HEAD)
RSYM_TAIL = escape(SYM_TAIL)
RSYM_MODIFY = escape(SYM_MODIFY)
RSYM_LENGTH = escape(SYM_LENGTH)
RSYM_CACHE = escape(SYM_CACHE)

RCS_RANGE = escape(CS_RANGE)
RCS_SEGSEP = escape(CS_SEGSEP)
RCS_SEP = "\\s\\，\\、\\；\\？\\,\\;"  # 此处不用escape是因为\s会被escape转义失效
RCG_ELLIPSIS = "\\.\\.\\.|\\.\\.\\.\\.\\.\\.|\\…|\\…\\…|\\。\\。\\。|\\-|\\~|\\－|\\～|\\—|\\*"
RCS_INLINE = escape(CS_INLINE)

RCS_CJK = (
    "\u3007\u4e00-\u9fff\ufa0e\ufa0f\ufa11\ufa13\ufa14\ufa1f\ufa21\ufa23\ufa24\ufa27-\ufa29\u3300-\u4dbf"
    "\U00020000-\U0002a6df\U0002a700-\U0002b739\U0002b740-\U0002b81d\U0002b820-\U0002cea1\U0002ceb0-\U0002ebe0\U00030000-\U0003134a\U00031350-\U000323af\U0002ebf0-\U0002ee5d\U000323b0-\U0003347f"
)

# endregion


# region configs
@dataclass
class _Stat:
    err_level: Literal["ignore", "abort", "inline", "raise"] = "raise"
    # ignore: 替换成"" abort: 保持原样 inline: 行内替换为缩写 raise: 抛出

    allow_underscore_in_cache_name: bool = False

    max_calc_output_length = 512

    censor: bool = True

    linger_names: set[str] | None = None
    linger_name: str | None = None

    allow_pua_warning = True
    pua_warning: bool = False


CurrentStat = _Stat()

# endregion

# region checkers


def check_cache_name(cn: str):
    if cn and "_" in cn and not CurrentStat.allow_underscore_in_cache_name:
        return partial(
            breakout,
            abbr="[E32缓存名无效]",
            msg="{d} - 缓存名中不允许出现下划线，因其可能导致意外的后果。如果一定要使用下划线，请使用[[config<enable_cache_name_with_underscore>]]。 (E32)",
        )


# endregion


# region translators
@translator("nocensor\\s*(?P<otp>([0-9A-Z]{6}))?")
async def Nocensor(mch: Match) -> SupportsStr:
    """临时关闭屏蔽词系统"""
    logger.info(f"Nocensor ← {mch.groupdict()}")
    otp = group(mch, "otp")
    if otp:
        if (chk := check_otp(otp)) == 0:
            CurrentStat.censor = False
            return ""
        elif chk == 1:
            return breakout(mch, "[E21.1验证码过期]", f"{{d}} - 此验证码已过期。当前验证码为【{set_new_otp()}】。 (E21.1)")
        elif chk == 2:
            return breakout(mch, "[E21.2验证码无效]", f"{{d}} - 此验证码无效。当前验证码为【{set_new_otp()}】。 (E21.2)")
        else:
            raise WhatTheFuckIsThis
    else:
        return breakout(
            mch,
            "[E21.3验证码缺失]",
            f"{{d}} - 需要验证码才能执行此操作。当前验证码为【{(val_otp:=set_new_otp())}】。请使用[[nocensor {val_otp}]]。 (E21.3)\n警告：使用此指令造成的一切后果由调用者承担，本机不负任何责任！",
        )


@translator("RST")
async def Reset(_: Match) -> SupportsStr:
    """重置 「Reset」
    语法：RST"""
    logger.info("Reset")
    reset()
    return ""


@translator("(?P<main>.*?)>>>(?P<name>.+)")
async def LingerAssign(mch: Match) -> SupportsStr:
    """驻留赋值 「LingerAssign」
    语法：{变量名}>>>{驻留名}"""
    varnames = await stegroup(mch, "main")
    linger_name = egroup(mch, "name")
    if CurrentStat.linger_name and CurrentStat.linger_name != linger_name:
        return breakout(
            mch, "[E71驻留名冲突]", f"{{d}} - 当前已设置了名为{CurrentStat.linger_name}的驻留。同一个填字中仅能使用一个驻留名。 (E71)"
        )
    else:
        CurrentStat.linger_name = linger_name
    if not CurrentStat.linger_names:
        CurrentStat.linger_names = set()
    if varnames:
        for varname in varnames.split():
            CurrentStat.linger_names.add(varname)
    else:
        CurrentStat.linger_names |= result_cache.caches["Ret"].keys()
    return ""


@translator("<<<(?P<name>.+)")
async def LingerRef(mch: Match) -> SupportsStr:
    """驻留引用 「LingerRef」
    语法：<<<{驻留名}"""
    lingername = egroup(mch, "name")
    if lingername not in LINGERS.keys():
        return breakout(mch, "[E72驻留名无效]", f"{{d}} - 驻留名{lingername}不存在。 (E72)")
    result_cache.caches["Ret"].update(LINGERS[lingername])
    return ""


@translator(f"(?P<main>.+?):(?P<start>[\\-0-9{RCS_INLINE}]+)?:(?P<stop>[\\-0-9\\@{RCS_INLINE}]+)?(:(?P<step>[\\-0-9{RCS_INLINE}]+))?")
async def Slice(mch: Match) -> SupportsStr:
    """切片 「Slice」
    语法：{值}:{起始}:{结束}[:步长]"""
    logger.info(f"Slice ← {mch.groupdict()}")
    main = await stegroup(mch, "main")
    _start = cast(str, await tegroup(mch, "start")) or None
    _stop = cast(str, await tegroup(mch, "stop")) or None
    _step = cast(str, await tegroup(mch, "step")) or None
    try:
        if _stop == "@":
            if not _start:
                raise PosteriorReject
            start = int(_start)
            ret = main[start]
        else:
            if not _start and not _stop and not _step:
                raise PosteriorReject
            start = _start and int(_start)
            stop = _stop and int(_stop)
            step = _step and int(_step)
            ret = main[start:stop:step]
    except ValueError:
        return breakout(mch, "[E31.1切片参数无效]", "{d} - 切片参数无效。 (E31.1)")
    except IndexError:
        return breakout(mch, "[E31.2切片越界]", "{d} - 切片越界。 (E31.2)")
    logger.info(f"Slice → {ret}")
    return ret


@translator("config<(?P<item>.+)>")
async def Config(mch: Match) -> SupportsStr:
    """配置项 「Config」
    语法：config<配置项>"""
    logger.info(f"Config ← {mch.groupdict()}")

    item = egroup(mch, "item")

    match item.lower():
        case "enable_cache_name_with_underscore":
            CurrentStat.allow_underscore_in_cache_name = True
        case "disable_cache_name_with_underscore":
            CurrentStat.allow_underscore_in_cache_name = False
        case "error_level_ignore":
            CurrentStat.err_level = "ignore"
        case "error_level_abort":
            CurrentStat.err_level = "abort"
        case "error_level_inline":
            CurrentStat.err_level = "inline"
        case "error_level_raise":
            CurrentStat.err_level = "raise"
        case "max_calculate_output_normal":
            CurrentStat.max_calc_output_length = 512
        case "max_calculate_output_long":
            CurrentStat.max_calc_output_length = 1024
        case "max_calculate_output_unlimited":
            CurrentStat.max_calc_output_length = 1145141919810
        case "disable_pua_warning":
            CurrentStat.allow_pua_warning = False
        case "enable_pua_warning":
            CurrentStat.allow_pua_warning = True
        case _:
            return breakout(mch, "[E33.1配置无效]", f"{{d}} - {item} 不是有效的配置项名称。 (E33.1)")

    return ""


@translator(
    "".join(chr(ord(c) - 42) for c in "畉咧〫宱寃叴个刱皮绲枫签桲"),
)
async def TheAnswer(_: Match) -> SupportsStr:
    """..."""
    return ANSWER_TO_THE_ULTIMATE_QUESTION_OF_LIFE_THE_UNIVERSE_AND_EVERYTHING.ANSWER


@translator("=\\s?(?P<main>.+)")
async def Calculate(mch: Match) -> SupportsStr:
    """计算 「Calculate」
    语法：={表达式}"""

    logger.info(f"Calculate ← {mch.groupdict()}")

    main = egroup(mch, "main")
    cache_vars = result_cache.caches.get("Ret", {})

    inner_cache_vars = {
        f"Inner_{field}_{name}": calc_cache.get(field, name, "") for field in calc_cache.caches for name in calc_cache.caches[field]
    }

    async with aiohttp.ClientSession() as sess:
        await sess.get(
            f"http://ka.li:9901/pysb/commit?uuid={(uid:=uuid.uuid4().hex)}"
            f"&code={base64.urlsafe_b64encode(main.encode("utf8")).decode("ascii")}"
            f"&vars={base64.urlsafe_b64encode(pickle.dumps(cache_vars | inner_cache_vars)).decode("ascii")}"
        )

        async with sess.get(f"http://ka.li:9901/pysb/run?uuid={uid}") as resp:
            if resp.status != 200:
                return breakout(mch, f"[E51.{resp.status}计算失败]", f"{{d}} - 计算服务器错误 (E51.{resp.status})")

            data = orjson.loads(await resp.text())

    if data["stat"] != "OK":
        return breakout(mch, f"[E51.{data["stat"]}计算失败]", f"{{d}} - 计算失败：{data} (E51.{data["stat"]})")

    output = pickle.loads(base64.b64decode(data["output"].encode("ascii")))[0]
    logger.info(f"Calc Server output: {output}")
    errno, retstr, retvars = output
    errno: int
    retstr: str
    retvars: dict[str, Any]

    if errno != 0:
        return breakout(mch, f"[E52.{errno}计算错误]", f"{{d}} - 计算错误：{retstr} (E52.{errno})")

    result_cache.caches["Ret"].update({k: v for k, v in retvars.items() if not k.startswith("Inner_")})

    for k, v in retvars.items():
        if k.startswith("Inner_"):
            field, name = k[6:].split("_", 1)
            calc_cache[field:name] = v

    if len(retstr) > CurrentStat.max_calc_output_length:
        return breakout(mch, "[E41结果过长]", f"{{d}} - 计算结果过长（{len(retstr)}字符）。(E41)")
    logger.info(f"Calculate → {retstr}")
    return retstr


@translator("<<((?P<field>.+?):)?(?P<name>.+)")
async def InnerValRef(mch: Match) -> SupportsStr:
    """内部值引用 「InnerValRef」
    语法：<<[{作用域}:]{缓存名}"""

    logger.info(f"InnerValRef ← {mch.groupdict()}")

    field: str = await stegroup(mch, "field")
    name: str = await stegroup(mch, "name")

    if bo := check_cache_name(name):
        return bo(mch)

    logger.info(f"caches: {calc_cache.caches}")

    for _, trans in translators:
        _field = field or trans.__name__
        if ret := calc_cache.get(_field, name, None):
            ret = str(ret)
            logger.info(f"InnerValRef → {ret}")
            return ret
        if field:
            break
    ret = egroup(mch, 0)
    logger.info(f"InnerValRef → {ret}")
    return ret


@translator("<(?P<name>.+)")
async def Reference(mch: Match) -> SupportsStr:
    """引用 「Reference」
    语法：<{缓存名}"""
    logger.info(f"Reference ← {mch.groupdict()}")
    ret = result_cache.get("Ret", await stegroup(mch, "name"))
    if ret is None:
        raise PosteriorReject
    logger.info(f"Reference → {ret}")
    return ret


@translator("(?P<main>.+?)>>((?P<field>.+?):)?(?P<name>[^>]+?)(?P<output>>?)")
async def InnerValAssign(mch: Match) -> SupportsStr:
    """内部值赋值 「InnerValAssign」
    语法：{值}>>{作用域}:{缓存名}[>]"""
    logger.info(f"InnerValAssign ← {mch.groupdict()}")
    field: str = await stegroup(mch, "field")

    if not field:
        return breakout(mch, "[E34参数缺失]", "在为内部值赋值的时候，必须指定作用域。(E34)")

    main: str = await stegroup(mch, "main") or ""
    name: str = await stegroup(mch, "name") or ""
    output: bool = bool(group(mch, "output"))

    if bo := check_cache_name(name):
        return bo(mch)

    try:
        val: int | float | complex | str = numsimp(numify(main, True)[2])
    except ValueError:
        val = main

    calc_cache[field:name] = val

    return str(val) if output else ""


@translator(f"""
    (?P<data>.+?)\\s?
    \\$
    (?P<font>[^{RSYM_TAIL}{RCS_SEP}{RCS_SEGSEP}]+?)
    ({RSYM_MODIFY}
        (?P<charset>.+?)
    )?
    (\\s?{RSYM_CACHE}
        (?P<cname>.+?)
    )?
""")
async def Font(mch: Match) -> SupportsStr:
    """字体 「Font」
    语法：{字符串} ${字体}[>{缓存名}]"""

    logger.info(f"Font ← {mch.groupdict()}")

    cache_name: str = await stegroup(mch, "cname")
    data: str = await stegroup(mch, "data")
    font_name: str = await stegroup(mch, "font")
    charset: str = await stegroup(mch, "charset")
    if bo := check_cache_name(cache_name):
        return bo(mch)

    font: dict[int, int] | dict[int | str, int | str] | dict[str, str] | None = fonts.fuzzy(font_name.lower(), threshold=60)
    if font is None:
        return breakout(mch, "[E61字体无效]", f"{{d}} - 「{font_name}」不是有效的字体名称，也无法被模糊匹配到有效的字体名称。(E61)")

    for k, v in font.items():
        if (not isinstance(k, str)) or (k not in charset):
            continue
        data = data.replace(k, cast(str, v))
    # 此处的cast是为了直接复用带有str:str的翻译表。

    ret = data.translate({k: v for k, v in font.items() if isinstance(k, int) and (not charset or chr(k) in charset)})
    result_cache["Ret":cache_name] = ret
    logger.info(f"Font → {ret}")

    return ret


@translator(f"""
    (?P<left>[^{RSYM_HEAD}{RSYM_TAIL}{RSYM_MODIFY}=\\s]+?)
    \\s*(?P<sep>([{RCS_RANGE}]|——))\\s*
    (?P<right>[^{RSYM_HEAD}{RSYM_TAIL}{RSYM_MODIFY}\\s:]+?(?<!({RCG_ELLIPSIS})))
    (
        (:
            (?P<fspec>(?!(cn|CN|u|U|unicode|nul|ro|RO))
                (
                    (?P<fill>[^{{}}<>;]?)
                    (?P<align>[<>=^])
                )?
                (?P<sign>[-+ ]?)
                \\#?
                0?
                [0-9]*
                [_,]?
                (\\.(?P<perc>[0-9]*))?
                (?P<ftype>[bcdeEfFgGnosxX%]?)
            )?
            (
                [{RCS_SEGSEP}]?
                (?P<fusr>(cn|CN|u|U|unicode|nul|ro|RO))
            )?
        )?
        (\\s?{RSYM_MODIFY}
            (?P<rand>({"|".join(map(escape,rngs.names))}))
        )?
        (\\s?[{RSYM_CACHE}]
            (?P<cname>.+?)
        )?
    ){{3}}""")
async def Range(mch: Match) -> SupportsStr:
    """随机数 「Range」
    语法：{下界}-{上界}[:[{Python式格式};]{转换格式}][@{分布}][>{缓存名}]"""

    logger.info(f"Range ← {mch.groupdict()}")

    cache_name: str = await stegroup(mch, "cname")
    rand_type: str = await stegroup(mch, "rand")

    if bo := check_cache_name(cache_name):
        return bo(mch)

    cached_rand: float | None = calc_cache.get("Range", cache_name, None) if cache_name else None
    rand: float = rngs.get(rand_type, random.random)() if cached_rand is None else cached_rand
    calc_cache["Range":cache_name] = rand

    lit_value1, lit_value2 = (await tegroup(mch, "left")), (await tegroup(mch, "right"))
    if isinstance(lit_value1, Value) and isinstance(lit_value2, Value):
        v_ftype = ""
        v_otype = "n"
        value1, value2 = lit_value1, lit_value2
    else:
        try:
            v_ftype, v_otype, (value1, value2), _ = numsify((str(lit_value1), str(lit_value2)))
        except OverflowError:
            if rand_type:
                return breakout(mch, "[E11尚未支持]", "{d} - 尚不支持在分布上进行无界选择，还望谅解。(E11)")
            return breakout(mch, "[E35.1边界无效]", "{d} - 边界不可以是Inf或NaN。(E35.1)")
        except ValueError:
            if egroup(mch, "sep") == "-":
                # 一般是带有负数的choice被识别成Range了，此时抛个后验拒绝让choice能吃到
                raise PosteriorReject
            return breakout(mch, "[E36.1解析不能]", f"{{d}} - 输入的边界「{lit_value1}」「{lit_value2}」无法被解析为范围。(E36.1)")

    c_ftype: str = egroup(mch, "ftype")
    c_otype: str = egroup(mch, "fusr") or "nul"

    ftype = c_ftype or v_ftype or "s"
    otype = c_otype or v_otype or "nul"

    cf_fspec: str = egroup(mch, "fspec") or ""
    cf_fill: str = egroup(mch, "fill") or ""
    cf_align: str = egroup(mch, "align") or ""
    cf_sign: str = egroup(mch, "sign") or ""
    cf_perc: int = int(egroup(mch, "perc") or 0)

    if isinstance(value1, int) and isinstance(value2, int):
        chosen = value1 + int((value2 - value1 + 1) * rand)
    else:
        chosen = value1 + (value2 - value1) * rand

    chosen: int | float | complex = numsimp(chosen)
    if cf_fspec or (otype != "nul"):
        try:
            ret: str | int | float | complex = numfmt(
                fusr_to_nfmt_fmt(otype),
                cf_fspec,
                cf_fill,
                cf_align,
                cf_sign,
                cf_perc,
                ftype,
                chosen,
            )
        except UnicodeError:
            return breakout(
                mch, "[E42.1码点无效]", f"{{d}} - 随机结果「{chosen}」不是一个有效的Unicode码点。对于u模式，上下界不应超出0~1114111。(E42.1)"
            )
        except ValueError:
            return breakout(
                mch,
                "[E33.2格式无效]",
                f"{{d}} - 输入/推定的格式 {cf_fspec or "NUL"} -> {otype} 不可用于格式化「{chosen}」（{type(chosen).__name__}）。(E33.2)",
            )
    else:
        ret = chosen

    result_cache["Ret":cache_name] = ret
    logger.info(f"Range → {ret}")

    return ret


@translator("\\#(?P<val>.+?)([:;](?P<fmt>(c|cn|CN|u|U|unicode|n|norm|normal|ro|RO|x|X|d|f)))?")
async def ImmediateNumbers(mch: Match) -> SupportsStr:
    """立即数 「ImmediateNumbers」
    语法：#{数值}"""
    logger.info(f"ImmediateNumbers ← {mch.groupdict()}")

    _fmt = await stegroup(mch, "fmt")
    fmt: Literal["c", "u", "n", "r", "x", "X", None] = cast(
        dict[str | None, Literal["c", "u", "n", "r", "x", "X", None]],
        {
            "c": "c",
            "cn": "c",
            "CN": "c",
            "u": "u",
            "U": "u",
            "unicode": "u",
            "n": "n",
            "norm": "n",
            "normal": "n",
            "ro": "r",
            "RO": "r",
            "x": "x",
            "X": "X",
            "d": "n",
            "f": "n",
            None: None,
            "": None,
        },
    )[_fmt]

    val = await tegroup(mch, "val")

    if (fmt == "n") and isinstance(val, numbers.Number):
        ret = val
    else:
        try:
            ret = numify(str(val), lvl=fmt)[2]
        except ValueError:
            return breakout(mch, "[E36.2数值无效]", f"{{d}} - {_fmt or "默认"}模式下无效的数值。(E36.2)")

    logger.info(f"ImmediateNumbers → {ret}")
    return ret


@translator(f"""
    (?P<data>
        [^{RSYM_MODIFY}\\s\\?]+?
        (?<!({RCG_ELLIPSIS}))
    )
    (:
        (?P<fspec>(?!(cn|CN|u|U|unicode|ro|RO))
            (
                (?P<fill>[^{{}}<>;]?)
                (?P<align>[<>=^])
            )?
            (?P<sign>[-+ ]?)
            \\#?
            0?
            [0-9]*
            [_,]?
            (\\.(?P<perc>[0-9]*))?
            (?P<ftype>[bcdeEfFgGnosxX%]?)
        )?
        (
            [{RCS_SEGSEP}]?
            (?P<fusr>(cn|CN|u|U|unicode|ro|RO))
        )?
    )
    (\\s?[{RSYM_CACHE}]
        (?P<cname>.+?)
    )?
""")
async def Format(mch: Match) -> SupportsStr:
    """格式化 「Format」
    语法：{数据}[:[{Python式格式};]{转换格式}][>{缓存名}]"""

    logger.info(f"Format ← {mch.groupdict()}")

    cache_name: str = await stegroup(mch, "cname")

    if bo := check_cache_name(cache_name):
        return bo(mch)

    data: str = await stegroup(mch, "data")
    if not data:
        return ""
    cf_fspec: str = egroup(mch, "fspec") or ""
    cf_fill: str = egroup(mch, "fill") or ""
    cf_align: str = egroup(mch, "align") or ""
    cf_sign: str = egroup(mch, "sign") or ""
    cf_perc: int = int(egroup(mch, "perc") or 0)
    c_ftype: str = egroup(mch, "ftype")
    c_otype: str = egroup(mch, "fusr") or "nul"

    try:
        v_ftype, v_otype, value, _ = numify(data, True)
    except TypeError, ValueError:
        return breakout(mch, "[E36.3解析不能]", f"{{d}} - 输入的值「{data}」无法被解析为数值。(E36.3)")

    value = numsimp(value)

    ftype = c_ftype or v_ftype or "s"
    otype = c_otype or v_otype or "nul"

    try:
        ret: str = numfmt(
            fusr_to_nfmt_fmt(otype),
            cf_fspec,
            cf_fill,
            cf_align,
            cf_sign,
            cf_perc,
            ftype,
            value,
        )
    except UnicodeError:
        return breakout(
            mch, "[E42.2码点无效]", f"{{d}} - 输入值「{value}」不是一个有效的Unicode码点。对于u模式，码点数值不应超出0~1114111。(E42.2)"
        )
    except ValueError:
        return breakout(
            mch,
            "[E33.2格式无效]",
            f"{{d}} - 输入/推定的格式 {cf_fspec or "NUL"} -> {otype} 不可用于格式化「{value}」（{type(value).__name__}）。(E33.2)",
        )

    result_cache["Ret":cache_name] = ret
    logger.info(f"Format → {ret}")

    return ret


@translator(
    f"(?P<main>[^*]+?)(?P<ast>\\*\\*|\\*)(?P<num>[^{RSYM_TAIL}]+?)(\\s?{RSYM_CACHE}(?P<loopvar>[^{RSYM_TAIL}]+?))?(\\s?{RSYM_MODIFY}(?P<offset>[^{RSYM_TAIL}]+?))?"
)
async def Repeat(mch: Match) -> SupportsStr:
    """重复 「Repeat」\
    语法：{字符串} *[*]{次数}"""
    lazy = mch.group("ast") == "**"
    loopvar: str = egroup(mch, "loopvar")
    try:
        offset: int = int(cast(str, ((await tegroup(mch, "offset")) or 0)))
    except ValueError:
        return breakout(mch, "[E36.5解析不能]", f"{{d}} - 偏移量「{egroup(mch, 'offset')}」无法被解析为整数。(E36.5)")

    _head = egroup(mch, "main")
    _mch = regex.fullmatch(f"(?P<main>[\\s\\S]+?)(?P<sep>[{RCS_SEP}]+)?", _head)
    if not _mch:
        raise PosteriorReject
    logger.info(f"Repeat ← {_mch.groupdict()} {lazy=} {loopvar=}")
    main: str = _mch.group("main") or ""
    sep: str = _mch.group("sep") or ""

    try:
        num: int = int(cast(str, (await tegroup(mch, "num"))) or 1)
    except ValueError:
        return breakout(mch, "[E36.4解析不能]", f"{{d}} - 次数「{egroup(mch, 'num')}」无法被解析为整数。(E36.4)")

    if num > 4096:
        return breakout(mch, "[E22.1次数无效]", f"{{d}} - 次数「{num}」超出范围。最大次数为4096。(E22.2)")
    if len(main) * num > 131072:
        return breakout(
            mch,
            "[E22.2次数无效]",
            f"{{d}} -次数「{num}」超出范围。在该输入长度（{len(main)}字符）下，最多重复次数为{131072//len(main)}次。(E22.2)",
        )

    if lazy:
        ret_lst = []
        for lv in range(offset, num + offset):
            result_cache["Ret":loopvar] = lv
            ret_lst.append(str(await translate(main)))
    else:
        result_cache["Ret":loopvar] = offset
        ret_lst = repeat(str(await translate(main)), num)
        result_cache["Ret":loopvar] = offset + num - 1
    ret = sep.join(ret_lst)
    logger.info(f"Repeat → {ret}")
    return ret


@translator(f"""
    (?P<main>[^>=]+?(?P<sep>[{RCS_SEP}])[^>=]+(?:(?P=sep)[^>=]+)*)
    (
        (\\s?{RSYM_MODIFY} (?P<rand>({"|".join(rsgs.names)})) )?
        (\\s?{RSYM_CACHE} (?P<cname>[^{RSYM_LENGTH}{RSYM_TAIL}]+?) )?
        (\\s?{RSYM_LENGTH} (?P<length>.+?) )?
    ){{3}}
""")
async def Choice(mch: Match) -> SupportsStr:
    """选择 「Choice」 语法：{选项1} {选项2} {选项3}...[>{缓存名}][@{分布}][={选择数}]"""
    logger.info(f"Choice ← {mch.groupdict()}")
    cache_name: str = await stegroup(mch, "cname")
    if bo := check_cache_name(cache_name):
        return bo(mch)
    length: int = max(1, int(cast(str, await tegroup(mch, "length")) or 1))
    rand_type: str = await stegroup(mch, "rand")

    sep: str = group(mch, "sep") or ""
    main: str = group(mch, "main") or ""
    splitted = [epacse(seg) for seg in main.split(sep) if seg]
    logger.info(f"Choice ↔ {splitted}")

    if len(splitted) <= 1:
        raise PosteriorReject
    length = min(length, len(splitted))
    _cache_name = f"{cache_name}${length}"

    weights = None
    if cache_name:
        weights: list[float] | None = calc_cache.get("Choice", _cache_name)
        if weights is None and length == 1:
            _rand: float | None = calc_cache.get("Range", cache_name)
            if _rand is not None:
                weights = [0.0] * len(splitted)
                weights[int(_rand * len(splitted))] = 1.0
    if weights is None:
        if rand_type:
            weights = list(rsgs[rand_type](len(splitted)))
        else:
            weights = [1 / len(splitted)] * len(splitted)

    options: list[str] = []
    opt_weights: list[float] = []
    for item in splitted:
        _parts = item.split(SYM_MODIFY, 1)
        if len(_parts) > 1:
            try:
                opt_weights.append(float(_parts[1]))
            except ValueError:
                raise PosteriorReject
            options.append(_parts[0])
        else:
            opt_weights.append(1.0)
            options.append(_parts[0])

    weights = [w * ow for w, ow in zip(weights, opt_weights)]
    swght = sum(weights)
    weights = [w / swght for w in weights]

    if cache_name:
        calc_cache["Choice":_cache_name] = weights

    chosens: list[str] = list(nrandom.choice(options, length, False, weights))
    chosens = [str(await translate(opt)) for opt in chosens]
    ret = sep.join(chosens)
    result_cache["Ret":cache_name] = ret
    logger.info(f"Choice → {ret}")
    return ret


@translator(f"""
    (?P<typ>(动画|漫画|游戏|文学|原创|网络|其他|影视|诗词|网易云|哲学|抖机灵)?)
    一言
    (?P<req>(出处|作者)?)
    (\\s?[{RSYM_CACHE}]
        (?P<cname>.+?)
    )?
""")
async def Hitokoto(mch: Match) -> SupportsStr:
    """一言 「Hitokoto」
    语法：[类型]一言[出处|作者|/]"""
    logger.info(f"Thitokoto ← {mch.groupdict()}")
    typ = await stegroup(mch, "typ") or "动画"
    req = await stegroup(mch, "req")
    cache_name = await stegroup(mch, "cname")

    if bo := check_cache_name(cache_name):
        return bo(mch)

    typ_id = {
        "动画": "a",
        "漫画": "b",
        "游戏": "c",
        "文学": "d",
        "原创": "e",
        "网络": "f",
        "其他": "g",
        "影视": "h",
        "诗词": "i",
        "网易云": "j",
        "哲学": "k",
        "抖机灵": "l",
    }[typ]

    _cname = f"{cache_name}${typ_id}"

    if req:
        hitokoto: dict[str, str] | None = calc_cache.get("Hitokoto", _cname)
    else:
        hitokoto = None

    if not hitokoto:
        h_file = Path(f"./modules/tianzi/lexicons/Hitokoto/{typ_id}.json")
        h_items = orjson.loads(await h_file.read_text(encoding="utf8"))
        hitokoto = random.choice(h_items)

    calc_cache["Hitokoto":_cname] = hitokoto

    match req:
        case "出处":
            ret = hitokoto["from"] or "……"
        case "作者":
            ret = hitokoto["from_who"] or "佚名"
        case _:
            ret = hitokoto["hitokoto"]

    result_cache["Ret":cache_name] = ret
    logger.info(f"Hitokoto → {ret}")
    return ret


@translator(f"""
    (?P<lex>({"|".join(lexloaders.LexLoader.loaded.keys())}))
    \\s?
    (
        (:(?P<pinyin>.+?))?
        ({RSYM_LENGTH}(?P<length>.+?))?
        ({RSYM_CACHE}(?P<cname>[^{RSYM_LENGTH}{RSYM_TAIL}]+?))?
    ){{3}}
    (?P<nocache>(,(nc|NC|nocache|rstcache|clearcache|resetcache))?)
    """)
async def Lex(mch: Match) -> SupportsStr:
    """词库 「Lex」
    语法：{词库名}[={长度}][>{缓存名}]"""
    logger.info(f"Lex ← {mch.groupdict()}")

    nocache: bool = bool(mch.group("nocache"))
    if nocache:
        lexloaders.BatchedFunc.reset_all_pools()

    lex_name: str = await stegroup(mch, "lex")
    _length: str = await stegroup(mch, "length")
    length: int | None = int(cast(str, _length)) if _length else None
    cache_name: str = await stegroup(mch, "cname") or ""
    pinyin: str | None = await stegroup(mch, "pinyin") or None

    if bo := check_cache_name(cache_name):
        return bo(mch)
    try:
        ret = await lexloaders.LexLoader.loaded[lex_name][length:pinyin]
    except lexloaders.UnsupportedOperation as e:
        return breakout(mch, "[E01填词失败]", f"{{d}} - 意外的填词失败：{repr(e)} (E01)")
    except SourceEmptyError:
        return breakout(mch, "[E62填词失败]", "{d} - 没有符合条件的词。(E62)")

    result_cache["Ret" : egroup(mch, "cname")] = ret
    logger.info(f"Lex → {repr(ret)}")
    return ret


@translator("(?P<main>[^>]+?)>(?P<name>[^>]+)(?P<output>>?)")
async def Assign(mch: Match) -> SupportsStr:
    """赋值 「Assign」
    语法：{值}>{缓存名}[>]"""
    logger.info(f"Assign ← {mch.groupdict()}")
    val = await tegroup(mch, "main")
    cache_name = egroup(mch, "name")

    if bo := check_cache_name(cache_name):
        return bo(mch)

    result_cache["Ret":cache_name] = val
    return val if group(mch, "output") else ""
