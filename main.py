import asyncio
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "src"))
# C:\GLOBAL_PATH_TO_PROJECT\root\src   (добавление src в список путей на 2 место)
# for i in sys.path: print(i)

from queries import AsyncCore, AsyncOrm, SyncCore, SyncOrm  # noqa: E402


def sync_core_main():
    pass


async def async_core_main():
    pass


def sync_orm_main():
    pass


async def async_orm_main():
    pass


if __name__ == "__main__":
    pass
