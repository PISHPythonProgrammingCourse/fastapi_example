from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None  # Необязательное поле
    price: float
    tax: float | None = None
