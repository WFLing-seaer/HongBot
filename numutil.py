import contextlib
from cmath import isinf, isnan
from collections.abc import Iterable
from typing import Literal, cast
from unicodedata import normalize

import cn2an
import rn2an

Value = int | float | complex
type Real = int | float
type Numeral = tuple[Literal["d", "x", "X", "f", "", "s"], Literal["n", "c", "u"], Value, int]  # ftype output_mode value priority
type Numerals = tuple[Literal["d", "x", "X", "f", "", "s"], Literal["n", "c", "u"], list[Value], int]


def numify(
    text: str, suppress_overflow: bool = False, lvl: Literal[0, 1, 2, 3, 4, 5, 6] | Literal["c", "u", "n", "r", "x", "X"] | None = None
) -> Numeral:
    text = normalize("NFKC", text)
    with contextlib.suppress(ValueError):
        if (lvl is None) or (lvl == 0) or (lvl == "n"):
            return "d", "n", int(text), 0
    with contextlib.suppress(ValueError):
        if ((lvl is None) or (lvl == 1) or (lvl == "x")) and text.islower():
            return "x", "n", int(text, 16), 1
    with contextlib.suppress(ValueError):
        if (lvl is None) or (lvl == 2) or (lvl == "n"):
            val = float(text)
            if (not suppress_overflow) and (isinf(val) or isnan(val)):
                raise OverflowError
            return "f", "n", val, 2
    with contextlib.suppress(ValueError):
        if (lvl is None) or (lvl == 3) or (lvl == "n"):
            val = complex(text)
            if (not suppress_overflow) and (isinf(val.real) or isnan(val.real) or isinf(val.imag) or isnan(val.imag)):
                raise OverflowError
            return "", "n", val, 3
    with contextlib.suppress(ValueError):
        if (lvl is None) or (lvl == 4) or (lvl == "c"):
            with contextlib.suppress(ValueError):
                return "d", "c", int(text), 4  # 因为cn2an会把原本就是阿拉伯数字的整数转成浮点数，因此此处通过int将这种情况短路掉
            return "d", "c", cn2an.cn2an(text, "smart"), 4
    with contextlib.suppress(ValueError):
        if (lvl is None) or (lvl == 5) or (lvl == "r"):
            return "f", "n", rn2an.rn2an(text), 5
    with contextlib.suppress(ValueError):
        if (lvl is None) or (lvl == 1) or (lvl == "X"):
            return "X", "n", int(text, 16), 1
    with contextlib.suppress(TypeError):
        if (lvl is None) or (lvl == 6) or (lvl == "u"):
            return "s", "u", ord(text), 6
    raise ValueError


def as_numeral(n: Value, _minlvl: int | None = None) -> Numeral:
    if isinstance(n, int) or (_minlvl is not None and _minlvl < 2):
        return "d", "n", int(n.real), _minlvl or 0
    if isinstance(n, float) or (_minlvl == 2 or _minlvl == 4 or _minlvl == 5):
        return "f", "n", float(n.real), _minlvl or 2
    if isinstance(n, complex) or _minlvl == 3:
        return "", "n", n, _minlvl or 3
    if _minlvl and _minlvl == 6:
        return "s", "u", int(n), 6


def numsify(texts: Iterable[str], suppress_overflow: bool = False) -> Numerals:
    lvl = max(numify(i, suppress_overflow)[3] for i in texts)
    nums = [numify(i, suppress_overflow, cast(Literal[0, 1, 2, 3, 4, 5, 6], lvl)) for i in texts]
    return (nums[0][0], nums[0][1], [i[2] for i in nums], lvl)


def fmtunify(*nums: Numeral) -> Numerals:
    lvl = max(num[3] for num in nums)
    n = [as_numeral(num[2], lvl) for num in nums]
    return (n[0][0], n[0][1], [i[2] for i in n], lvl)


def numsimp(n: Value) -> Value:
    if isinstance(n, complex):
        n = n if n.imag else n.real
    if isinstance(n, float):
        n = int(n) if not (isnan(n) or isinf(n)) and (n == int(n)) else n
    return n


def numfmt(
    output_mode: Literal["c", "C", "u", "n", "r", "R"], fmt_spec: str, fill: str, align: str, sign: str, perc: int, ftype: str, value: Value
) -> str:
    match output_mode:
        case "c" | "C":
            if isinstance(value, complex):
                raise ValueError
            # 执行对中文数字的格式化。这个好像没有现成的库可以用，只能自己写
            if ftype == "%":
                value *= 100
            value = round(value, perc)
            an2cn_format = "direct" if ftype == "s" else {"c": "low", "C": "up"}[output_mode]
            ret = cn2an.an2cn(str(value), an2cn_format)
            if sign == "+":
                ret = "正" + ret if ret[0] != "负" else ret
            elif sign == " ":
                ret = "\u3000" + ret if ret[0] != "负" else ret
            ret = f"{{r:{fill}{align}}}".format(r=ret)
            if perc:
                if "点" not in ret:
                    ret += "点"
                ret += "零" * (perc - len(ret.split("点")[-1]))
            if ftype == "%":
                if an2cn_format == "up":
                    ret = "佰分之" + ret
                else:
                    ret = "百分之" + ret
            return ret
        case "u":
            if not isinstance(value, int):
                raise ValueError
            if not (0 <= value <= 0x10FFFF):
                raise UnicodeError
            ret = chr(value)
        case "r":
            if isinstance(value, complex):
                raise ValueError
            ret = rn2an.an2rnA(value)
        case "R":
            if isinstance(value, complex):
                raise ValueError
            ret = rn2an.an2rn(value)
        case "n":
            ret = str(value)
    if fmt_spec:
        ret = f"{{v:{fmt_spec}}}".format(v=value)
    return ret
