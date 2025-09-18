import time
import traceback
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from routers import router1, router2, router3, router4, router5, router6, router7, router8, router9
import logging

# Настройка логирования
# TRACE
# DEBUG
# INFO
# WARNING
# Exception
# ERROR

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=1000000, backupCount=5, encoding="utf-8"),  # В файл
        logging.StreamHandler()  # И в консоль
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.started_at = time.time()
    logger.info("Сервис стартует...")
    # Инициализация ресурсов тут (кэш, пулы и т.п.)
    yield
    # Финализация ресурсов тут (закрыть соединения и т.п.)
    end_time = time.time()
    logger.info(f"App was used for {end_time - app.state.started_at:.2f} seconds. Closing...")


app = FastAPI(
    title="FastAPI Basics",
    description="Описание сервиса здесь",
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(router1.router)
app.include_router(router2.router)
app.include_router(router3.router)
app.include_router(router4.app)
app.include_router(router5.app)
app.include_router(router6.app)
app.include_router(router7.app)
app.include_router(router8.app)
app.include_router(router9.app)


@app.middleware("http")
async def add_timing(request: Request, call_next):
    t0 = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    response.headers["X-Process-Time-ms"] = f"{elapsed_ms:.2f}"
    logger.debug(f"Вызов был обработан за {elapsed_ms} ms")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging
    logger = logging.getLogger("uvicorn.error")

    # Собираем подробности о запросе
    try:
        body = await request.body()
    except Exception:
        body = b"[body read failed]"

    logger.error(
        f"Exception occurred: {exc}\n"
        f"URL: {request.url}\n"
        f"Method: {request.method}\n"
        f"Headers: {dict(request.headers)}\n"
        f"Body: {body[:500]}\n"
        f"Stacktrace:\n{traceback.format_exc()}"
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "name": exc.__class__.__name__,
                "message": str(exc)
            }
        }
    )
