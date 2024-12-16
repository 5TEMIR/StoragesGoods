import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.core.config import settings
from project.api.storage_routes import storage_router
from project.api.goodsgroup_routes import goodsgroup_router
from project.api.producer_routes import producer_router
from project.api.storagemethod_routes import storage_method_router
from project.api.supplier_routes import supplier_router
from project.api.client_routes import client_router
from project.api.good_routes import good_router
from project.api.storageplace_routes import storage_place_router
from project.api.receipt_routes import receipt_router
from project.api.expense_routes import expense_router
from project.api.goodstransfer_routes import goods_transfer_router
from project.api.goodsreceipt_routes import goods_receipt_router
from project.api.goodsexpense_routes import goods_expense_router

from project.api.user_routes import user_router
from project.api.auth_routes import auth_router
from project.api.healthcheck import healthcheck_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV.lower() == "prod":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }
    if settings.LOG_LEVEL in ["DEBUG", "INFO"]:
        app_options["debug"] = True

    app = FastAPI(root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(storage_router, tags=["Storage"])
    app.include_router(goodsgroup_router, tags=["GoodsGroup"])
    app.include_router(producer_router, tags=["Producer"])
    app.include_router(storage_method_router, tags=["StorageMethod"])
    app.include_router(supplier_router, tags=["Supplier"])
    app.include_router(client_router, tags=["Client"])
    app.include_router(good_router, tags=["Good"])
    app.include_router(storage_place_router, tags=["StoragePlace"])
    app.include_router(receipt_router, tags=["Receipt"])
    app.include_router(expense_router, tags=["Expense"])
    app.include_router(goods_transfer_router, tags=["GoodsTransfer"])
    app.include_router(goods_receipt_router, tags=["GoodsReceipt"])
    app.include_router(goods_expense_router, tags=["GoodsExpense"])

    app.include_router(user_router, tags=["User"])
    app.include_router(auth_router, tags=["Auth"])
    app.include_router(healthcheck_router, tags=["Health check"])

    return app


app = create_app()


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    logger.debug(f"{settings.postgres_url}=")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
