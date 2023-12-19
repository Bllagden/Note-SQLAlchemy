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
    SyncCore.insert_workers(["AAA", "BBB"])
    SyncCore.select_workers()
    SyncCore.update_worker_1()
    SyncCore.update_worker_2()
    SyncCore.insert_resumes()
    SyncCore.select_resumes_avg_compensation()
    SyncCore.insert_additional_resumes()


async def async_core_main():
    print("\nAsync Core\n")
    await AsyncCore.delete_tables()
    await AsyncCore.create_tables()
    await AsyncCore.insert_workers(["AAA", "BBB"])
    await AsyncCore.select_workers()
    await AsyncCore.update_worker_1()
    await AsyncCore.update_worker_2()
    await AsyncCore.insert_resumes()
    await AsyncCore.select_resumes_avg_compensation()
    await AsyncCore.insert_additional_resumes()


def sync_orm_main():
    print("\nSync Orm\n")
    SyncOrm.delete_tables()
    SyncOrm.create_tables()
    SyncOrm.insert_workers(["AAA", "BBB"])
    SyncOrm.select_workers()
    SyncOrm.update_worker_1()
    SyncOrm.insert_resumes()
    SyncOrm.select_resumes_avg_compensation()
    SyncOrm.insert_additional_resumes()
    # end core
    SyncOrm.join_cte_subquery_window_func()
    # relationship
    SyncOrm.select_workers_lazy_relationship()
    SyncOrm.select_workers_joined_relationship()
    SyncOrm.select_workers_selectin_relationship()
    SyncOrm.select_worker_selectin_relationship()


async def async_orm_main():
    print("\nAsync Orm\n")
    await AsyncOrm.delete_tables()
    await AsyncOrm.create_tables()
    await AsyncOrm.insert_workers(["AAA", "BBB"])
    await AsyncOrm.select_workers()
    await AsyncOrm.update_worker_1()
    await AsyncOrm.insert_resumes()
    await AsyncOrm.select_resumes_avg_compensation()
    await AsyncOrm.insert_additional_resumes()
    # end core
    await AsyncOrm.join_cte_subquery_window_func()
    # relationship
    await AsyncOrm.select_workers_joined_relationship()
    await AsyncOrm.select_workers_selectin_relationship()
    await AsyncOrm.select_worker_selectin_relationship()


if __name__ == "__main__":
    """python main.py --sync --orm"""
    if "--sync" in sys.argv and "--core" in sys.argv:
        sync_core_main()
    elif "--async" in sys.argv and "--core" in sys.argv:
        asyncio.run(async_core_main())
    elif "--sync" in sys.argv and "--orm" in sys.argv:
        sync_orm_main()
    elif "--async" in sys.argv and "--orm" in sys.argv:
        asyncio.run(async_orm_main())
