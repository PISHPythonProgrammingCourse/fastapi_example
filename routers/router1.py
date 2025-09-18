import time

from fastapi import APIRouter

router = APIRouter(prefix="/v1", tags=["v1"])

c = 0


@router.get("/ping")
def v1_ping():
    return {"pong": True, "v": 1}


@router.post("/counter")
def counter():
    global c
    c += 1
    # time.sleep(2)
    return {"c": c}
