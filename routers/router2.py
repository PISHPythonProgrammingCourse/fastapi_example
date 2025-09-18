import logging

from fastapi import APIRouter

from models.item import Item

router = APIRouter(tags=["v2"])

logger = logging.getLogger(__name__)


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    logger.info(f"Item: {item_id}", type(item_id))
    return {"item_id": item_id}


@router.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
        user_id: int,  # Объявляем тип -> получаем автоматическую валидацию и конвертацию
        item_id: str,
):
    return {"user_id": user_id, "item_id": item_id}


@router.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):  # Значения по умолчанию
    return {"skip": skip, "limit": limit}


@router.post("/post_items/")
async def create_item(item: Item):  # FastAPI сам прочитает тело запроса и проверит его
    # item уже является объектом с данными и методами
    item_dict = item.model_dump()
    if item.tax:
        total = item.price + item.tax
        item_dict.update({"total": total})
    return item_dict
