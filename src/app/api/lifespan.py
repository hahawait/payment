from contextlib import asynccontextmanager

import aiojobs
from fastapi import FastAPI

from app.api.background import consume_in_background
from config import Config
from infrastructure.message_brokers.kafka import KafkaMessageBroker
from infrastructure.uow.sqlalchemy import SQLAlchemyUnitOfWork


@asynccontextmanager
async def lifespan(app: FastAPI) -> FastAPI:
    container = app.state.dishka_container
    scheduler = aiojobs.Scheduler()
    # broker = await container.get(KafkaMessageBroker)
    config = await container.get(Config)
    if config.app.is_dev or config.app.is_production:
        async with container() as request_container:
            uow = await request_container.get(SQLAlchemyUnitOfWork)
        # job = await scheduler.spawn(consume_in_background(broker, uow))
    yield
    # if config.app.is_dev or config.app.is_production:
    #     await job.close()
    await scheduler.close()
    await container.close()
