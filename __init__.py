import logging
import re
import time
import traceback
from collections import deque
from typing import cast

import regex
from fuzzywuzzy import process

from core.api import API
from core.router import on_message, on_notice
from models import api
from models.msg import Forward, MessageChain, MsgChain, Node, Text
from utils.string import InlineStr

from . import lexloaders
from .censor import censor
from .phparser import BreakOut, reset, translate

# from .pyparser import CannotParse, WildcardPinyinChain
# from .pyparser import pyparse as pinyinparse

logger = logging.getLogger("tianzi")

last_sent: deque[tuple[str, str]] = deque(maxlen=3)

group_last_command: dict[str, str] = {}

OTHER_BOT_QQ = {
    "1994709738": 1,
    "3491521267": 1,
    "3635837386": 1,  # Lvory
    "3402897586": 2,
    "3498314126": 2,  # 豆鸽
}
OTHER_BOT_RE = {
    re.compile("发 填字[\\s\\S]+"): 1,
    re.compile("回 [\\s\\S]+"): 2,
}
last_inter_bot_interact: deque[set[int]] = deque(maxlen=36)
last_loopbreak_time = 0
last_inter_bot_interact_time = 0


CRASHACTER = regex.compile(
    "[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f\u1fff\u200b-\u200f\u2028-\u202e\u2060-\u206f\uf900-\ufaff\U000107c0-\U000107ff\U000108b0-\U000108df]"
)


async def tianzi_core(raw: str, initial_var: dict | None = None) -> str:
    try:
        reset(initial_var)
        translated: str = str(await translate(raw, final=True))
    except BreakOut as bo:
        translated = bo.args[0]
    except TimeoutError:
        translated = "正则超时。您的输入可能太长或太复杂。"
    except Exception as e:
        translated = f"意外的错误：{repr(e)}，栈如下：\n{traceback.format_exc()}\n请联系找北。"
    if phparser.CurrentStat.censor:
        translated = censor(translated)
    ret_msg = regex.sub(CRASHACTER, lambda char: f"U+{hex(ord(char.group(0)))[2:].upper()}", translated.removeprefix("\n").removeprefix(" "))
    logger.info(f"CALL STACK: {"".join(phparser.CALL_STACK)}")

    return ret_msg


@on_message("不发 填字[\\s\n][\\s\\S]+")
async def tianzi_test(event: api.Message):
    raw = event.get_msg_inline().removeprefix("不发 填字").removeprefix("（测）")
    ret_msg = InlineStr(await tianzi_core(raw))

    triggered_by = OTHER_BOT_QQ.get(event.user_id, None)
    triggers = next((v for (k, v) in OTHER_BOT_RE.items() if k.fullmatch(ret_msg)), None)
    global last_loopbreak_time, last_inter_bot_interact_time
    if triggered_by and (curr_t := time.monotonic()) - last_loopbreak_time < 15:
        await event.send("Bot互交互深度超限后的15秒内不可再使用其他bot调用薨机。")
        return
    if triggered_by and triggers:
        last_inter_bot_interact_time = curr_t
        last_inter_bot_interact.append({triggered_by, triggers})
        if last_inter_bot_interact.count(last_inter_bot_interact[-1]) >= 5:
            last_loopbreak_time = curr_t
            await event.send("Bot互交互深度超出限制。")
            return
    elif time.monotonic() - last_inter_bot_interact_time > 15:
        last_inter_bot_interact.clear()

    if ret_msg.startswith("名 "):
        await event.send("名 薨机")
        return
    if ret_msg.startswith("发 我叫"):
        await event.send("发 我叫 薨机")
        return
    if phparser.CurrentStat.pua_warning:
        await event.send(
            "警告：输入/处理过程中涉及保留的PUA字符，可能导致意外的行为。请不要使用PUA字符，或者如果您明白自己在做什么的话，请使用[[config<disable_pua_warning>]]消除本警告。如果您认为这是误报，请@找北。"
        )
    if ret_msg:
        mid = await event.send(ret_msg.to_list())
        last_sent.append((str(event.message_id), mid))
        group_last_command[str(event.group_id)] = raw
        if ret_msg.startswith("不发 填字") and ret_msg != "不发 填字 自己吓自己~" and ret_msg != "不发 填字 自己吓自己～":
            await event.send("自己吓自己~")


@on_message("不发 填字同上([\\s][\\s\\S]+)?")
async def tianzi_repeat(event: api.Message):
    variants_str = str(event.get_msg_inline())[7:].strip().split("\n")
    try:
        variants = {(sp := ln.split("=", maxsplit=1))[0]: sp[1] for ln in variants_str if ln}
    except IndexError:
        await event.send("填字同上指定变量格式错误：应当使用每行一个的「变量名=值」格式。")
        return
    if str(event.group_id) in group_last_command:
        ret_msg = await tianzi_core(group_last_command[str(event.group_id)], variants)

        triggered_by = OTHER_BOT_QQ.get(event.user_id, None)
        triggers = next((v for (k, v) in OTHER_BOT_RE.items() if k.fullmatch(ret_msg)), None)
        global last_loopbreak_time, last_inter_bot_interact_time
        if triggered_by and (curr_t := time.monotonic()) - last_loopbreak_time < 15:
            await event.send("Bot互交互深度超限后的15秒内不可再使用其他bot调用薨机。")
            return
        if triggered_by and triggers:
            last_inter_bot_interact_time = curr_t
            last_inter_bot_interact.append({triggered_by, triggers})
            if last_inter_bot_interact.count(last_inter_bot_interact[-1]) >= 5:
                last_loopbreak_time = curr_t
                await event.send("Bot互交互深度超出限制。")
                return
        elif time.monotonic() - last_inter_bot_interact_time > 15:
            last_inter_bot_interact.clear()

        if ret_msg.startswith("名 "):
            await event.send("名 薨机")
            return
        if ret_msg.startswith("发 我叫"):
            await event.send("发 我叫 薨机")
            return
        if ret_msg:
            mid = await event.send(ret_msg)
            last_sent.append((str(event.message_id), mid))


@on_message("不发 填字同上是(啥|什么)")
async def tianzi_repeat_what(event: api.Message):
    if str(event.group_id) in group_last_command:
        await event.send(group_last_command[str(event.group_id)])
    else:
        await event.send("上次重启之后本群还没有进行过填字。")


@on_message("不发 填字调用栈")
async def tianzi_callstack(event: api.Message):
    await event.send("".join(phparser.CALL_STACK))


@on_message("不发 帮助 填字")
async def help_tianzi(event: api.Message):
    await event.send(phparser.helps())


@on_notice("group_recall")
async def del_tianzi(event: api.Notice):
    rid = event.message_id
    for recv_mid, sent_mid in last_sent:
        if recv_mid == rid:
            await API.delete_msg(message_id=sent_mid)
            break


@on_message("不发 查词[库典].*")
async def get_lex_meta(event: api.Message):
    name = event.message_str[6:].lstrip()
    if name:
        try:
            meta = await lexloaders.LexLoader.loaded[name].show_meta()
        except KeyError:
            fuzz = cast(list[tuple[str, int]], process.extract(name, list(lexloaders.LexLoader.loaded.keys()), limit=2))
            if fuzz and fuzz[0][1] >= 70:
                if len(fuzz) == 2 and fuzz[1][1] == fuzz[0][1]:
                    hint = f"猜你想找：「{fuzz[0][0]}」「{fuzz[1][0]}」"
                else:
                    hint = f"猜你想找：「{fuzz[0][0]}」"
            else:
                hint = ""
            meta = f"词库不存在。{hint}"
        await event.send(meta)
    else:
        await event.send("由于本功能会导致意外的挂起与可能的长时间死机，因此本功能将禁用直到死机问题被解决。")
        return
        names = list(lexloaders.LexLoader.loaded.keys())
        namesegs = [
            Node(nickname=f"词典{i+1}~{i+50}", content=MessageChain(Text(text="\n".join(names[i : i + 50])))) for i in range(0, len(names), 50)
        ]
        await event.send(Forward(content=MsgChain(namesegs)))


@on_message("不发 查词 .+")
async def find_lex(event: api.Message):
    word = event.message_str[6:].strip()
    lexs = await lexloaders.LexLoader.search_word(word)
    if not lexs:
        ret = f"{word} - 不见于任何词典"
    else:
        lex_names = [lex.meta.name for lex in lexs]
        ret = f"{word} - 见于以下{len(lexs)}个词典：「{"」「".join(lex_names)}」"
    await event.send(ret)


"""@on_message("不发 拼解 .+")
async def pinyin_parse(event: api.Message):
    word = event.message_str[6:].strip()
    try:
        ret: WildcardPinyinChain = pinyinparse(word)
    except CannotParse:
        await event.send(f"{word} - 无法解析")
        return
    await event.send(" ".join(map(str, ret)))"""
