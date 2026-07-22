import logging
from typing import Any, Dict, Optional

import aiomysql

from .config import settings

log = logging.getLogger("db-writer.db")

_pool: Optional[aiomysql.Pool] = None


async def init_pool() -> aiomysql.Pool:
    """앱 시작 시 한 번 호출해서 커넥션 풀을 생성한다."""
    global _pool
    _pool = await aiomysql.create_pool(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        db=settings.MYSQL_DB,
        minsize=settings.MYSQL_POOL_MIN,
        maxsize=settings.MYSQL_POOL_MAX,
        autocommit=True,
        charset="utf8mb4",
    )
    log.info("MySQL pool created (%s:%s/%s)", settings.MYSQL_HOST, settings.MYSQL_PORT, settings.MYSQL_DB)
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        await _pool.wait_closed()
        _pool = None

def get_pool() -> Optional[aiomysql.Pool]:
    """헬스체크(readyz)에서 MySQL 커넥션 풀 상태 확인용"""
    return _pool


def _to_int(value: Any) -> Optional[int]:
    """1783304552358.0 같은 float-looking epoch 값을 정수로 변환."""
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------
# cits_position  (v2x.vehicle.basic)
# ------------------------------------------------------------
_POSITION_COLUMNS = [
    "dataId", "trsmDy", "trmnId", "trsmUtcTime", "trsmYear", "trsmMt", "trsmTm",
    "trsmMs", "vhcleLot", "vhcleLat", "vhcleEvt", "trmnTypeCd", "gpsUtcTime",
    "vhcleDrc", "vhcleSped", "trnsmStatCd", "lcdtRevisnStatCd", "vhcleTypeCd",
    "rgtrId", "regDt",
]

_POSITION_INSERT_SQL = f"""
INSERT INTO cits_position ({', '.join(_POSITION_COLUMNS)})
VALUES ({', '.join(['%s'] * len(_POSITION_COLUMNS))})
ON DUPLICATE KEY UPDATE dataId = dataId
"""



async def insert_position(payload: Dict[str, Any]) -> None:
    values = [
        payload.get("dataId"),
        payload.get("trsmDy"),
        payload.get("trmnId"),
        _to_int(payload.get("trsmUtcTime")),
        payload.get("trsmYear"),
        payload.get("trsmMt"),
        payload.get("trsmTm"),
        payload.get("trsmMs"),
        payload.get("vhcleLot"),
        payload.get("vhcleLat"),
        payload.get("vhcleEvt"),
        payload.get("trmnTypeCd"),
        _to_int(payload.get("gpsUtcTime")),
        payload.get("vhcleDrc"),
        payload.get("vhcleSped"),
        payload.get("trnsmStatCd"),
        payload.get("lcdtRevisnStatCd"),
        payload.get("vhcleTypeCd"),
        payload.get("rgtrId"),
        payload.get("regDt"),
    ]
    async with _pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(_POSITION_INSERT_SQL, values)


# ------------------------------------------------------------
# cits_status  (v2x.vehicle.status)
# ------------------------------------------------------------
_STATUS_COLUMNS = [
    "dataId", "trsmDy", "trmnId", "trsmYear", "trsmMt", "trsmTm", "trsmMs",
    "vhcleLot", "vhcleLat", "fcwsCd", "ldwsCd", "pcwsCd", "dowsCd",
    "lbhlStatCd", "hbhlStatCd", "leftTusgStatCd", "rghtTusgStatCd",
    "hasgStatCd", "alctStatCd", "drlgStatCd", "fglgStatCd", "pklgStatCd",
    "frntWiperStatCd", "vhcleAcr", "laneCd", "rgtrId", "regDt",
]

_STATUS_INSERT_SQL = f"""
INSERT INTO cits_status ({', '.join(_STATUS_COLUMNS)})
VALUES ({', '.join(['%s'] * len(_STATUS_COLUMNS))})
ON DUPLICATE KEY UPDATE dataId = dataId
"""


async def insert_status(payload: Dict[str, Any]) -> None:
    values = [
        payload.get("dataId"),
        payload.get("trsmDy"),
        payload.get("trmnId"),
        payload.get("trsmYear"),
        payload.get("trsmMt"),
        payload.get("trsmTm"),
        payload.get("trsmMs"),
        payload.get("vhcleLot"),
        payload.get("vhcleLat"),
        payload.get("fcwsCd"),
        payload.get("ldwsCd"),
        payload.get("pcwsCd"),
        payload.get("dowsCd"),
        payload.get("lbhlStatCd"),
        payload.get("hbhlStatCd"),
        payload.get("leftTusgStatCd"),
        payload.get("rghtTusgStatCd"),
        payload.get("hasgStatCd"),
        payload.get("alctStatCd"),
        payload.get("drlgStatCd"),
        payload.get("fglgStatCd"),
        payload.get("pklgStatCd"),
        payload.get("frntWiperStatCd"),
        payload.get("vhcleAcr"),
        payload.get("laneCd"),
        payload.get("rgtrId"),
        payload.get("regDt"),
    ]
    async with _pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(_STATUS_INSERT_SQL, values)
