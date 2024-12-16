from dataclasses import dataclass
from typing import AsyncIterator

from aiokafka import AIOKafkaConsumer
from orjson import orjson

from infrastructure.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    consumer: AIOKafkaConsumer

    async def start(self) -> None:
        await self.consumer.start()

    async def close(self) -> None:
        await self.consumer.stop()

    async def start_consuming(self) -> AsyncIterator[dict]:
        async for message in self.consumer:
            loaded = orjson.loads(message.value)
            yield loaded

    async def commit(self) -> None:
        await self.consumer.commit()
