from logging import getLogger

logger = getLogger("textutil")


def glued(s: str) -> str:
    return "\u2060".join(s).replace("\u2060\n", "\n").replace("\n\u2060", "\n").replace("\u2060 \u2060", "\u00a0")


def find_outmost_bracket(bracket: tuple[str, str], s: str):
    subs: list[tuple[int, int]] = []

    left_bracket = bracket[0]
    right_bracket = bracket[1]
    left_len = len(left_bracket)
    right_len = len(right_bracket)
    i = 0

    while i < len(s):
        if i + left_len > len(s) or s[i : i + left_len] != left_bracket:
            i += 1
            continue
        else:
            stack = 1
            start = i
            i += left_len
            while i < len(s) and stack > 0:
                if i + right_len <= len(s) and s[i : i + right_len] == right_bracket:
                    stack -= 1
                    if stack == 0:
                        subs.append((start, i + right_len))
                        i += right_len
                        break
                    i += right_len
                elif i + left_len <= len(s) and s[i : i + left_len] == left_bracket:
                    stack += 1
                    i += left_len
                else:
                    i += 1
            if stack > 0:
                break

    return subs


if __name__ == "__main__":
    print(find_outmost_bracket(("[[", "]]"), "[[a]]"))
