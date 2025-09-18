from typing import Annotated

from fastapi import UploadFile, File, APIRouter, Query
from fastapi.responses import Response, StreamingResponse
from PIL import Image, ImageDraw
import io

app = APIRouter(tags=["v6"])


@app.post("/image/echo", summary="Вернуть загруженную картинку как есть")
async def image_echo(file: UploadFile = File(..., description="Файл изображения")):
    data = await file.read()
    media = file.content_type or "image/jpeg"
    return Response(content=data, media_type=media)


@app.get("/image/generated", summary="Сгенерировать картинку на лету (PNG)")
def image_generated(text: Annotated[str, Query(description="Надпись на изображении")] = "Hello"):
    img = Image.new("RGB", (400, 160), color=(40, 44, 52))
    draw = ImageDraw.Draw(img)
    draw.text((20, 60), text, fill=(248, 248, 242))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
