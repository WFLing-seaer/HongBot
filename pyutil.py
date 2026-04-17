"""from collections.abc import Generator
from itertools import chain, product
from typing import Literal, cast, overload

if __package__:
    from .pyparser import Final_verbose, Initial_verbose, WildcardSyll, pyparse_cached
else:
    from pyparser import Final_verbose, Initial_verbose, WildcardSyll, pyparse_cached

from pypinyin import Style, pinyin
from pypinyin_dict.phrase_pinyin_data import large_pinyin

large_pinyin.load()

SYL2DOUBLE: dict[Initial_verbose | Final_verbose, bytes] = {
    # 基于自然码改写；用于MLTrie，保证一个音节固定映射为三个ASCII
    "zh": b"v",
    "ch": b"i",
    "sh": b"u",
    "er": b"E",
    "hm": b"M",
    "hng": b"N",
    "ng": b"F",
    "ii": b"Z",
    "ri": b"C",
    "iou": b"q",
    "ia": b"w",
    "ua": b"W",
    "uan": b"r",
    "van": b"R",
    "ve": b"t",
    "ing": b"y",
    "uai": b"Y",
    "uo": b"O",
    "uen": b"p",
    "ven": b"P",
    "iong": b"s",
    "ong": b"S",
    "iang": b"d",
    "uang": b"D",
    "en": b"f",
    "eng": b"g",
    "ueng": b"G",
    "ang": b"h",
    "an": b"j",
    "ao": b"k",
    "ai": b"l",
    "ei": b"z",
    "ie": b"x",
    "iao": b"c",
    "uei": b"V",
    "ou": b"b",
    "ien": b"n",
    "ian": b"m",
}


@overload
def wsyll2mltrie(wsyll: WildcardSyll, pass_none: Literal[False]) -> list[bytes]:
    pass


@overload
def wsyll2mltrie(wsyll: WildcardSyll, pass_none: Literal[True] = True) -> list[bytes | None]:
    pass


def wsyll2mltrie(wsyll: WildcardSyll, pass_none: bool = True) -> list:
    # MLTrie风格的拼音键用倒转音节表示；倒转序为韵母-声母-声调
    return [
        (
            (None if pass_none else b".")
            if wsyll.final == {None}
            else b"".join(SYL2DOUBLE.get(opt, cast(str, opt).encode("ascii")) for opt in wsyll.final)
        ),
        (
            (None if pass_none else b".")
            if wsyll.initial == {None}
            else b"".join(SYL2DOUBLE.get(opt, cast(str, opt).encode("ascii")) for opt in wsyll.initial)
        ),
        ((None if pass_none else b".") if wsyll.tone == {None} else b"".join(str(opt).encode("ascii") for opt in wsyll.tone)),
    ]


def get_mltrie_styled_pinyin(text: str, max_pinyins: int = 1024, tail: int = 5, head: int = 3) -> Generator[bytes]:
    pinyins = pinyin(
        text,
        heteronym=True,
        style=Style.TONE3,
        neutral_tone_with_five=True,
        errors=(lambda t: [""] * len(t)),  # type: ignore pypinyin对errors的类型注解有问题，注解为str|(str)->str，然而根据文档还应当接受(str)->list[str]和(str)->list[list[str]]。
    )
    for i in chain(
        range(len(text) - 1, len(text) - min(tail, len(text)) - 1, -1),
        range(0, min(head, len(text) - min(tail, len(text)))),
        range(len(text) - min(tail, len(text)) - 1, min(head, len(text) - min(tail, len(text))) - 1, -1),
    ):
        pinyins[i] = pinyins[i][:max_pinyins]
        max_pinyins = max(1, max_pinyins // len(pinyins[i]))
    for p in product(*pinyins):
        yield b"".join(
            chain(
                *(
                    (
                        wsyll2mltrie(pyparse_cached("rri4" if w == "ri4" else w, allow_force_initial=False)[0], False)
                        if w
                        else (b".", b".", b".")
                    )
                    for w in reversed(p)
                )
            )  # 对ri4特判是因为，它是唯一一个可能混淆音节&韵母的
        )
"""
