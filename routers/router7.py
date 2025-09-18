import time
from typing import Annotated

from fastapi import BackgroundTasks, APIRouter, Query
from starlette.concurrency import run_in_threadpool

app = APIRouter(tags=["v7"])


def blocking_write(path: str, line: str):
    time.sleep(5)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"Вызов только сейчас закончился! Строка `{line}` записана!")


@app.post("/bg/log", summary="Записать строку в фоне после ответа")
def background_log(
        line: Annotated[str, Query(..., description="Строка лога")],
        bg: BackgroundTasks,
):
    bg.add_task(blocking_write, "bg.log", line)
    return {"accepted": True}


def cpu_bound(n: int) -> int:
    if n <= 1:
        return n
    return cpu_bound(n - 1) + cpu_bound(n - 2)


@app.get("/cpu/slow", summary="CPU-задача: синхронный эндпоинт → уходит в threadpool FastAPI")
def cpu_slow(n: Annotated[int, Query(ge=1, le=40)] = 32):
    return {"fib": cpu_bound(n)}


@app.get("/cpu/offload", summary="CPU-задача явно вынесена в поток")
async def cpu_offload(n: Annotated[int, Query(ge=1, le=40)] = 32):
    res = await run_in_threadpool(cpu_bound, n)
    return {"fib": res}


@app.get("/io/offload", summary="Блокирующий IO вынесен в поток")
async def io_offload():
    def blocking_io():
        time.sleep(1.0)
        return "ok"

    out = await run_in_threadpool(blocking_io)
    return {"io": out}
