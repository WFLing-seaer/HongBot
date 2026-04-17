import contextlib
import logging
import time
from collections.abc import Callable, Coroutine, Iterable

from regex import Match, Pattern


class NotModified(ValueError):
    pass


class PosteriorReject(ValueError):  # 后验拒绝，指的是虽然正则匹配成功但是在函数内检查后发现不应该匹配的
    pass


logger = logging.getLogger("reutil")


async def asub(
    pattern: Pattern[str],
    repl: Callable[[Match], Coroutine[None, None, str]],
    text: str,
    count: int = 0,
    raise_on_not_modified: bool = False,
) -> str:
    results: list[str] = []
    last_end = 0
    n = 0

    matches: list[tuple[int, int, Match]] = []
    for mch in pattern.finditer(text):
        start, end = mch.span(0)
        matches.append((start, end, mch))

    if not matches and raise_on_not_modified:
        raise NotModified

    really_modified = False
    for start, end, mch in matches:
        if count > 0 and n >= count:
            break
        if start > last_end:
            results.append(text[last_end:start])

        try:
            replacement = await repl(mch)
            really_modified = True
        except PosteriorReject:
            replacement = mch.group(0)
        except Exception:
            raise

        results.append(replacement)
        last_end = end
        n += 1

    if not really_modified and raise_on_not_modified:
        raise NotModified

    if last_end < len(text):
        results.append(text[last_end:])

    return "".join(results)


async def series_asub(
    patterns: Iterable[Pattern[str]],
    repl: Iterable[Callable[[Match], Coroutine[None, None, str]]],
    text: str,
    count: int = 0,
    raise_on_not_modified: bool = False,
) -> str:
    modified = False
    for pattern, replacing in zip(patterns, repl):
        with contextlib.suppress(NotModified):
            text0 = text
            time0 = time.perf_counter()
            text = await asub(pattern, replacing, text, count, True)
            time_elapsed = time.perf_counter() - time0
            modified = True
            logger.info(f"REutil SASUB 应用:\n{repr(text0)}\n↓ {replacing.__name__} {time_elapsed:.3f}s\n{repr(text)}")
    if not modified and raise_on_not_modified:
        logger.info(f"REutil SASUB 未修改:{repr(text)}")
        raise NotModified
    return text
