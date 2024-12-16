import logging

import sentry_sdk
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.api.docs import secure_docs
from app.api.lifespan import lifespan
from app.api.middlewares import register_middlewares

from app.api.admin.handlers import router as admin_router

from config import get_config

from logic.providers.base import BaseProvider
from logic.providers.invoices import InvoicesProvider
from logic.providers.legal_entities import LegalEntitiesProvider


def create_app() -> FastAPI:
    config = get_config()
    logging.basicConfig(level=config.app.LOG_LEVEL)
    if config.app.is_dev or config.app.is_production:
        sentry_sdk.init(
            dsn=config.app.SENTRY_DSN,
            environment=config.app.MODE,
            traces_sample_rate=1.0,
        )

    fastapi_params = dict(
        title=config.app.TITLE,
        description=config.app.DESCRIPTION,
        version=config.app.VERSION,
        lifespan=lifespan
    )

    if config.app.is_production:
        app = FastAPI(
            **fastapi_params,
            docs_url=None,
            redoc_url=None,
            openapi_url=None,
            debug=True,
        )
        secure_docs(
            app=app,
            admin_username=config.app.ADMIN_USERNAME,
            admin_password=config.app.ADMIN_PASSWORD,
            **fastapi_params
        )
    else:
        app = FastAPI(**fastapi_params, debug=True)

    register_middlewares(app, profiler_enabled=config.app.PROFILING_ENABLED)

    container = make_async_container(
        BaseProvider(),
        LegalEntitiesProvider(),
        InvoicesProvider(),
    )
    setup_dishka(container, app)

    app.include_router(admin_router)

    return app
