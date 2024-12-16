from typing import AsyncIterable

from aiokafka import AIOKafkaConsumer
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from config import Config, get_config
from infrastructure.db.sqlalchemy.setup import create_engine, create_session_pool
from infrastructure.message_brokers.kafka import KafkaMessageBroker
from infrastructure.uow.sqlalchemy import SQLAlchemyUnitOfWork


class BaseProvider(Provider):
    @provide(scope=Scope.APP)
    def config(self) -> Config:
        return get_config()

    @provide(scope=Scope.APP)
    def sqlalchemy_engine(self, config: Config) -> AsyncEngine:
        return create_engine(config.pg)

    @provide(scope=Scope.APP)
    def session_pool(self, sqlalchemy_engine: AsyncEngine) -> sessionmaker:
        return create_session_pool(sqlalchemy_engine)

    @provide(scope=Scope.REQUEST)
    def sqlalchemy_uow(self, session_factory: sessionmaker) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(_session=session_factory())

    @provide(scope=Scope.APP)
    async def kafka_broker(self, config: Config) -> AsyncIterable[KafkaMessageBroker]:
        consumer = AIOKafkaConsumer(
            config.rp.CONSUME_TOPIC,
            bootstrap_servers=config.rp.RP_SERVER,
            group_id=config.rp.CONSUME_GROUP,
            enable_auto_commit=False,
            auto_offset_reset="latest",
            sasl_mechanism=config.rp.SASL_MECHANISM,
            security_protocol=config.rp.SECURITY_PROTOCOL,
            sasl_plain_username=config.rp.RP_USER,
            sasl_plain_password=config.rp.RP_PASS,
        )
        broker = KafkaMessageBroker(consumer)
        await broker.start()
        yield broker
        await broker.close()
