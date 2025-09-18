from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException, APIRouter

app = APIRouter(tags=["v4"])


class UserIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str | None = Field(None, max_length=100)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None


_db_users: dict[int, UserOut] = {}
_next_id = 1


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    global _next_id
    new = UserOut(id=_next_id, email=user.email, full_name=user.full_name)
    _db_users[_next_id] = new
    _next_id += 1
    return new


@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int):
    user = _db_users.get(user_id)
    if not user:
        raise HTTPException(404, f"пользователь {user_id} не найден")
    return user
