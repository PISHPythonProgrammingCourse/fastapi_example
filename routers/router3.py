from fastapi import APIRouter

from enum import Enum
from typing import Annotated
from fastapi import Query

router = APIRouter(tags=["v3"])


class Color(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"


@router.get("/hello", summary="Приветствие", response_description="Сообщение-приветствие")
def hello(name: Annotated[str | None, Query(description="Имя пользователя", example="Алиса")] = None):
    """
    Здесь мы можем написать документацию к роуту
    """
    msg = f"Привет, {name}!" if name else "Привет!"
    return {"message": msg}


@router.get("/color")
def color(c: Color = Color.red):
    return {"color": c}
