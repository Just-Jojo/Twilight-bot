"""
MIT License

Copyright (c) 2021 Jojo#7711

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import uuid
import asyncio

import json

import os
from typing import Any


class Config:
    """An asynchronous way to write to and get stuff from files"""

    loop: asyncio.AbstractEventLoop

    def __init__(self, name: str, **options):
        self.name = name
        self.loop = asyncio.get_event_loop()
        self.lock = asyncio.Lock()
        self.sync_load()

    def sync_load(self):
        try:
            with open(self.name, "r") as fp:
                self._data = json.load(fp)
        except FileNotFoundError:
            self._data = {}

    async def load(self):
        async with self.lock:
            await self.loop.run_in_executor(None, self.sync_load)

    def _save_json(self):
        temp = "{}-{}.tmp".format(self.name, uuid.uuid4())
        with open(temp, "w", encoding="utf-8") as tmp:
            json.dump(self._data.copy(), tmp, ensure_ascii=True)
        os.replace(temp, self.name)

    async def save(self):
        async with self.lock:
            await self.loop.run_in_executor(None, self._save_json)

    async def set(self, key: str, value: Any, *args):
        # I'm not gonna trust myself to make sure
        # that this key is a string lol
        self._data[str(key)] = value
        await self.save()

    async def remove(self, key: str):
        del self._data[str(key)]
        await self.save()

    def get(self, key: str, *args) -> Any:
        return self._data.get(str(key), *args)

    def __getitem__(self, key: str) -> Any:
        return self._data[str(key)]

    def __contains__(self, key: str) -> bool:
        return str(key) in self._data

    def __len__(self):
        return len(self._data)

    def keys(self):
        return self._data.keys()
