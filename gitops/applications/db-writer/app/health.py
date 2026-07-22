from fastapi import FastAPI, Response, status

from . import db

app = FastAPI()

# consumer.py에서 RabbitMQ 연결 성공 시 설정해줄 전역 변수
rabbitmq_connection = None


def set_rabbitmq_connection(conn) -> None:
    """consumer.py에서 RabbitMQ 연결 객체를 등록"""
    global rabbitmq_connection
    rabbitmq_connection = conn


@app.get("/healthz")
async def healthz():
    """프로세스 생존 여부만 확인 (가볍게, 실패 시 K8s가 컨테이너 재시작)"""
    return {"status": "ok"}


@app.get("/readyz")
async def readyz(response: Response):
    try:
        pool = db.get_pool()
        if pool is None:
            raise Exception("pool not initialized")
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
    except Exception as e:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready", "reason": f"mysql check failed: {e}"}

    if rabbitmq_connection is None or rabbitmq_connection.is_closed:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready", "reason": "rabbitmq not connected"}

    return {"status": "ready"}
