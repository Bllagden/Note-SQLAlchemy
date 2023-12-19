import asyncio
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "src"))
# C:\GLOBAL_PATH_TO_PROJECT\root\src   (добавление src в список путей на 2 место)
# for i in sys.path: print(i)

from queries import AsyncCore, AsyncOrm, SyncCore, SyncOrm  # noqa: E402


def sync_core_main():
    print("\nSync Core\n")
    SyncCore.delete_tables()
    SyncCore.create_tables()


async def async_core_main():
    print("\nAsync Core\n")
    await AsyncCore.delete_tables()
    await AsyncCore.create_tables()


def sync_orm_main():
    print("\nSync Orm\n")
    SyncOrm.delete_tables()
    SyncOrm.create_tables()


async def async_orm_main():
    print("\nAsync Orm\n")
    await AsyncOrm.delete_tables()
    await AsyncOrm.create_tables()


if __name__ == "__main__":
    # sync_core_main()
    # asyncio.run(async_core_main())
    # sync_orm_main()
    asyncio.run(async_orm_main())
