import base64
import pickle
import struct
from glob import glob
from itertools import chain
from pathlib import Path

import bson
import marisa_trie
import numpy as np
import ujson as json

SRC = "./lexicons/Lexicon"
DST = "./lexicons/Lexicon_compiled"


def compile_e1l1w(fname: str, data: str) -> tuple[str, bytes]:
    datas = data.rstrip().split("\n")
    if fname.startswith("_"):
        lname = datas.pop(0)
    else:
        lname = fname

    trie = marisa_trie.Trie([word.lower() for word in datas if word.strip()])
    return lname + ".mrswl", pickle.dumps(trie)


def compile_1l1w(fname: str, data: str) -> tuple[str, bytes]:
    datas = data.rstrip().split("\n")
    if fname.startswith("_"):
        lname = datas.pop(0)
    else:
        lname = fname

    trie = marisa_trie.Trie([word for word in datas if word.strip()])
    return lname + ".mrswl", pickle.dumps(trie)


def compile_cset(fname: str, data: str) -> tuple[str, bytes]:
    datas = data.rstrip().split("\n")
    if len(datas) == 2:
        lname = datas.pop(0)
    else:
        lname = fname

    datas = datas[0] if datas else ""
    return lname + ".cset", datas.encode("UTF8")


def compile_xxxsv(fname: str, data: str, det: str) -> tuple[str, bytes]:
    datas = data.rstrip().split("\n")
    if fname.startswith("_"):
        lname = datas.pop(0)
    else:
        lname = fname
    rows = [line.split(det) for line in datas if line.strip()]

    flattened = [*chain(*(row for row in rows))]

    long = len(flattened) > 65535

    trie = marisa_trie.Trie(flattened)

    vrows = [[trie[val] for val in row] for row in rows]
    # 对齐每行保证长度相同
    maxllen = max(len(row) for row in vrows)
    vrows = [row + [4294967295 if long else 65535] * (maxllen - len(row)) for row in vrows]
    varray = np.array(vrows, dtype=(np.uint32 if long else np.uint16))

    marisa_bytes = pickle.dumps(trie)
    marisa_len = struct.pack(">Q", len(marisa_bytes))
    return lname + ".mnpy", marisa_len + marisa_bytes + varray.dumps()


def compile_xxhxsv(fname: str, data: str, det: str) -> tuple[str, bytes]:
    datas = data.rstrip().split("\n")
    if fname.startswith("_"):
        lname = datas.pop(0)
    else:
        lname = fname

    rows = [line.split(det) for line in datas if line.strip()]

    header = rows.pop(0)

    flattened = [*chain(*(row for row in rows))]

    long = len(flattened) > 65535

    trie = marisa_trie.Trie(flattened)

    vrows = [[trie[val] for val in row] for row in rows]
    # 对齐每行保证长度相同
    maxllen = max(len(row) for row in vrows)
    vrows = [row + [4294967295 if long else 65535] * (maxllen - len(row)) for row in vrows]
    varray = np.array(vrows, dtype=(np.uint32 if long else np.uint16))

    marisa_bytes = pickle.dumps(trie)
    marisa_len = struct.pack(">Q", len(marisa_bytes))

    header_bytes = pickle.dumps(header)
    header_len = struct.pack(">Q", len(header_bytes))
    return lname + ".mhnpy", marisa_len + header_len + marisa_bytes + header_bytes + varray.dumps()


def compile_dcsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxxsv(fname, data, ",")


def compile_mcsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxxsv(fname, data, ",")


def compile_dhcsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxhxsv(fname, data, ",")


def compile_mhcsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxhxsv(fname, data, ",")


def compile_dssv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxxsv(fname, data, " ")


def compile_mssv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxxsv(fname, data, " ")


def compile_dhssv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxhxsv(fname, data, " ")


def compile_mhssv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxhxsv(fname, data, " ")


def compile_dtsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxxsv(fname, data, "\t")


def compile_mtsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxxsv(fname, data, "\t")


def compile_dhtsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxhxsv(fname, data, "\t")


def compile_mhtsv(fname: str, data: str) -> tuple[str, bytes]:
    return compile_xxhxsv(fname, data, "\t")


def compile_logic(fname: str, data: str, ext: str) -> tuple[str, bytes]:
    datas = data.rstrip().split("\n")
    if fname.startswith("_"):
        lname = datas.pop(0)
    else:
        lname = fname

    datas = "".join(datas)
    json_data = json.loads(datas)
    bson_data = bson.encode(json_data)
    return lname + ext, bson_data


def compile_csset(fname: str, data: str) -> tuple[str, bytes]:
    return compile_logic(fname, data, ".csset")


def compile_cuset(fname: str, data: str) -> tuple[str, bytes]:
    return compile_logic(fname, data, ".cuset")


def compile_mmrs(fname: str, data: str) -> tuple[str, bytes]:
    return compile_logic(fname, data, ".mmrs")


def main():
    dst_path = Path(DST)
    dst_path.mkdir(exist_ok=True)

    extensions = [
        "*.e1l1w",
        "*.1l1w",
        "*.cset",
        "*.csset",
        "*.cuset",
        "*.mmrs",
        "*.dcsv",
        "*.dhcsv",
        "*.mcsv",
        "*.mhcsv",
        "*.dssv",
        "*.dhssv",
        "*.mssv",
        "*.mhssv",
        "*.dtsv",
        "*.dhtsv",
        "*.mtsv",
        "*.mhtsv",
    ]
    valids = []
    for ext in extensions:
        valids.extend(glob(str(Path(SRC) / ext)))

    selected = {}
    for fp in valids:
        path = Path(fp)
        base_name = path.stem
        ext = path.suffix

        if base_name not in selected:
            selected[base_name] = (path, ext)

    for base_name, (fp, ext) in selected.items():
        try:
            print(f"正在编译 {fp} ……")
            data = fp.read_text(encoding="utf-8")
            match ext:
                case ".e1l1w":
                    lname, compiled_data = compile_e1l1w(fp.stem, data)
                case ".1l1w":
                    lname, compiled_data = compile_1l1w(fp.stem, data)
                case ".cset":
                    lname, compiled_data = compile_cset(fp.stem, data)
                case ".csset":
                    lname, compiled_data = compile_csset(fp.stem, data)
                case ".cuset":
                    lname, compiled_data = compile_cuset(fp.stem, data)
                case ".mmrs":
                    lname, compiled_data = compile_mmrs(fp.stem, data)
                case ".dcsv":
                    lname, compiled_data = compile_dcsv(fp.stem, data)
                case ".dhcsv":
                    lname, compiled_data = compile_dhcsv(fp.stem, data)
                case ".mcsv":
                    lname, compiled_data = compile_mcsv(fp.stem, data)
                case ".mhcsv":
                    lname, compiled_data = compile_mhcsv(fp.stem, data)
                case ".dssv":
                    lname, compiled_data = compile_dssv(fp.stem, data)
                case ".dhssv":
                    lname, compiled_data = compile_dhssv(fp.stem, data)
                case ".mssv":
                    lname, compiled_data = compile_mssv(fp.stem, data)
                case ".mhssv":
                    lname, compiled_data = compile_mhssv(fp.stem, data)
                case ".dtsv":
                    lname, compiled_data = compile_dtsv(fp.stem, data)
                case ".dhtsv":
                    lname, compiled_data = compile_dhtsv(fp.stem, data)
                case ".mtsv":
                    lname, compiled_data = compile_mtsv(fp.stem, data)
                case ".mhtsv":
                    lname, compiled_data = compile_mhtsv(fp.stem, data)
                #    ... # 没写完。QaQ
                case _:
                    continue
            lnamep = lname.rsplit(".", 1)
            encoded_name = base64.b16encode(lnamep[0].encode("utf-8")).decode("ascii").upper()
            output_path = dst_path / (encoded_name + "." + lnamep[1])

            output_path.write_bytes(compiled_data)

            print(f"已编译到 {output_path}\n")

        except Exception as e:
            print(f"编译 {fp} 失败: {e}")
            raise


if __name__ == "__main__":
    main()
