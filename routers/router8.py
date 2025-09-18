import asyncio
from typing import Annotated

from fastapi import HTTPException, APIRouter, Query

app = APIRouter(tags=["v8"])


@app.get("/bad/async-sleep", summary="ПЛОХО: time.sleep внутри async‑роута")
async def bad_async_sleep(seconds: Annotated[float, Query(ge=0, le=10)] = 2.0):
    import time as _t
    _t.sleep(seconds)  # блокирует event loop!
    return {"slept": seconds}


@app.get("/good/async-sleep", summary="ХОРОШО: asyncio.sleep")
async def good_async_sleep(seconds: Annotated[float, Query(ge=0, le=10)] = 2.0):
    await asyncio.sleep(seconds)
    return {"slept": seconds}


@app.get("/with/inner-timeout", summary="Внутренний таймаут задачи (asyncio.wait_for)")
async def with_inner_timeout(delay: Annotated[float, Query(ge=0, le=10)] = 3.0,
                             timeout: Annotated[float, Query(ge=0.1, le=10)] = 1.5):
    async def slow_op():
        await asyncio.sleep(delay)
        return "done"

    try:
        res = await asyncio.wait_for(slow_op(), timeout=timeout)
        return {"result": res, "delay": delay, "timeout": timeout}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail=f"таймаут {timeout}s")
