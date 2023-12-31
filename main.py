import asyncio
import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    #
    SyncOrm.select_workers_condition_relationship()
    SyncOrm.select_workers_condition_relationship_contains_eager()
    SyncOrm.select_workers_relationship_contains_eager_with_limit()
    # DTO
    SyncOrm.convert_workers_to_dto()
    SyncOrm.convert_workers_to_dto_with_rel()
    SyncOrm.convert_workers_to_dto_with_dto_join()
    # M_to_M
    SyncOrm.add_vacancies_and_replies()
    SyncOrm.select_resumes_with_all_relationships()


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
    #
    await AsyncOrm.select_workers_condition_relationship()
    await AsyncOrm.select_workers_condition_relationship_contains_eager()
    await AsyncOrm.select_workers_relationship_contains_eager_with_limit()
    # DTO
    await AsyncOrm.convert_workers_to_dto()
    await AsyncOrm.convert_workers_to_dto_with_rel()
    await AsyncOrm.convert_workers_to_dto_with_dto_join()
    # M_to_M
    await AsyncOrm.add_vacancies_and_replies()
    await AsyncOrm.select_resumes_with_all_relationships()


def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/workers", tags=["Кандидат"])
    async def get_workers():
        workers = SyncOrm.convert_workers_to_dto_with_rel()
        return workers

    @app.get("/resumes", tags=["Резюме"])
    async def get_resumes():
        resumes = await AsyncOrm.select_resumes_with_all_relationships()
        return resumes

    return app


app = create_fastapi_app()


def uvicorn_run():
    print()
    uvicorn.run(
        app="main:app",
        reload=True,
    )


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

    if "--webserver" in sys.argv:
        uvicorn_run()
