import time
from fastapi import Depends, HTTPException, APIRouter
from functools import lru_cache

from utils.authorization import authorize

app = APIRouter(
    tags=["v9"],
    dependencies=[Depends(authorize)]
)

_last_called: dict[str, float] = {}


def rate_limit(key: str, min_interval_s: float = 1.0):
    now = time.monotonic()
    prev = _last_called.get(key, 0.0)
    if now - prev < min_interval_s:
        raise HTTPException(429, f"слишком часто, подожди {min_interval_s}с")
    _last_called[key] = now
    return True


# noinspection PyUnusedLocal
@app.get("/limited")
def limited(ok=Depends(lambda: rate_limit("limited", 3))):
    return {"ok": True, "ts": time.time()}


@lru_cache(maxsize=128)
def slow_square(n: int) -> int:
    time.sleep(2)
    return n * n


@app.get("/square/{n}")
def square(n: int):
    raise ValueError("abc")
    return {"n": n, "square": slow_square(n)}
