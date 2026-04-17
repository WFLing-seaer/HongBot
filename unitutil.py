def byte2size(bytesize: float, threshold: float = 800) -> tuple[float, str]:
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB"]
    for unit in units:
        if bytesize < threshold:
            return bytesize, unit
        bytesize /= 1024
    return bytesize, "QiB"


def num2si(num: float, threshold: float = 1000) -> tuple[float, str]:
    units = ["", "k", "M", "G", "T", "P", "E", "Z", "Y", "R"]
    for unit in units:
        if num < threshold:
            return num, unit
        num /= 1000
    return num, "Q"


def num2ch(num: float, threshold: float = 10000) -> tuple[float, str]:
    units = ["", "万", "亿", "兆", "京", "垓", "秭", "穰", "沟", "涧", "正", "载", "极"]
    for unit in units:
        if num < threshold:
            return num, unit
        num /= 10000
    return num, "恒河沙"


def num2ch10(num: float, threshold: float = 10) -> tuple[float, str]:
    units = ["", "十", "百", "千", "万", "十万", "百万", "千万", "亿", "十亿", "百亿", "千亿", "万亿", "十万亿"]
    for unit in units:
        if num < threshold:
            return num, unit
        num /= 10
    return num, "百万亿"
