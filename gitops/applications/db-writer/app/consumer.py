import asyncio
import json
import logging

import aio_pika
from aio_pika import IncomingMessage

from . import db
from .config import settings

import uvicorn
from . import health

log = logging.getLogger("db-writer.consumer")


async def _handle_position(message: IncomingMessage) -> None:
    async with message.process(ignore_processed=True):
        try:
            payload = json.loads(message.body)
            await db.insert_position(payload)
            log.debug("position insert OK dataId=%s", payload.get("dataId"))
        except json.JSONDecodeError:
            log.error("position 큐 JSON 파싱 실패, 메시지 버림: %r", message.body[:200])
            await message.reject(requeue=False)
        except Exception:
            log.exception("position insert 실패, 메시지 버림 (dataId=%s)",
                           _safe_data_id(message.body))
            await message.reject(requeue=False)


async def _handle_status(message: IncomingMessage) -> None:
    async with message.process(ignore_processed=True):
        try:
            payload = json.loads(message.body)
            await db.insert_status(payload)
            log.debug("status insert OK dataId=%s", payload.get("dataId"))
        except json.JSONDecodeError:
            log.error("status 큐 JSON 파싱 실패, 메시지 버림: %r", message.body[:200])
            await message.reject(requeue=False)
        except Exception:
            log.exception("status insert 실패, 메시지 버림 (dataId=%s)",
                           _safe_data_id(message.body))
            await message.reject(requeue=False)


def _safe_data_id(body: bytes) -> str:
    try:
        return json.loads(body).get("dataId", "?")
    except Exception:
        return "?"


async def run() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    await db.init_pool()

    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
        virtualhost=settings.RABBITMQ_VHOST,
    )

    health.set_rabbitmq_connection(connection)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=settings.PREFETCH_COUNT)

        queue_position = await channel.declare_queue(settings.QUEUE_POSITION, passive=True)
        queue_status = await channel.declare_queue(settings.QUEUE_STATUS, passive=True)

        log.info("컨슈머 시작: %s -> cits_position, %s -> cits_status",
                  settings.QUEUE_POSITION, settings.QUEUE_STATUS)

        await queue_position.consume(_handle_position)
        await queue_status.consume(_handle_status)

        config = uvicorn.Config(health.app, host="0.0.0.0", port=8000, log_level="warning")
        server = uvicorn.Server(config)

        try:
            await server.serve()
        finally:
            await db.close_pool()


def main() -> None:
    asyncio.run(run())

# 최종 자동배포 검증 2번째 
# 최종 자동배포 검증 3번째
# 쵀종 자동배포 검증 4번째
if __name__ == "__main__":
    main()
# 자동배포 테스트 Tue Jul 14 02:00:33 AM UTC 2026

 
# pipeline test 
# pipeline test 2 Mon Jul 20 08:41:08 AM UTC 2026
# pipeline test 3 Mon Jul 20 08:42:39 AM UTC 2026
# pipeline test 4 Mon Jul 20 08:46:27 AM UTC 2026
