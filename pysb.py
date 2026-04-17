import base64
import pickle
from typing import Any
from uuid import uuid4

import aiohttp

TARGET_ADDR = "ka.li"
TARGET_PORT = 9901


class SandBox:
    def __init__(self):
        self.uuid = str(uuid4())

    async def commit(self, code: str, variables: dict[str, Any]):
        code_encoded = base64.b64encode(code.encode()).decode()
        vars_encoded = base64.b64encode(pickle.dumps(variables)).decode()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://{TARGET_ADDR}:{TARGET_PORT}/pysb/commit?code={code_encoded}&vars={vars_encoded}&uuid={self.uuid}"
            ) as resp:
                return await resp.json()

    async def run(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{TARGET_ADDR}:{TARGET_PORT}/pysb/run?uuid={self.uuid}") as resp:
                return await resp.json()

    async def discard(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{TARGET_ADDR}:{TARGET_PORT}/pysb/discard?uuid={self.uuid}") as resp:
                return await resp.json()
