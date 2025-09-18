import pathlib

from fastapi import HTTPException
from fastapi import UploadFile, File, APIRouter
from fastapi.responses import FileResponse

app = APIRouter(tags=["v5"])

UPLOAD_DIR = pathlib.Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload")
async def upload(
        file: UploadFile = File(..., description="любой файл"),
        note: str = "",
):
    path = UPLOAD_DIR / file.filename
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"saved_to": str(path), "note": note, "content_type": file.content_type}


@app.get("/download/{name}")
def download(name: str):
    path = UPLOAD_DIR / name
    if not path.exists():
        raise HTTPException(404, "файл не найден")
    return FileResponse(path)


@app.get("/download2/{name}")
def download2(name: str):
    path = UPLOAD_DIR / name
    if not path.exists():
        raise HTTPException(404, "файл не найден")
    return FileResponse(
        path=path,
        filename=name,
        media_type="*/*",
    )
