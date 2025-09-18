from fastapi import FastAPI

app = FastAPI(title="My App")


@app.get("/")
def index():
    return {"message": "Hello World!"}
