import logging

from infrastructure.message_brokers.base import BaseMessageBroker


async def consume_in_background(
    broker: BaseMessageBroker,
) -> None:
    logger = logging.getLogger("AccessConsumer")
    async for message in broker.start_consuming():
        try:
            logging.info(message)
            await broker.commit()
        except Exception as e:
            logger.error(f"Error while consuming message: {e}")
            break
