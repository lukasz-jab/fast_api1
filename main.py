from typing import List
from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException

from models import Gender, Role, User, UserUpdateRequest

app = FastAPI()


db: List[User] = [
    User(
        #id=uuid4(),
        id=UUID("b11f0225-775b-4ed6-9167-2365921cd308"),
        first_name = "Hannah",
        last_name = "Mambo",
        gender = Gender.female,
        roles = [Role.student]

    ),
    User(
        #id=uuid4(),
        id=UUID("464cbe90-45d8-4e8f-812b-0551f0938d9e"),
        first_name = "Mark",
        last_name = "Bambo",
        gender = Gender.male,
        roles = [Role.user, Role.admin]

    )
]
@app.get("/")
async def root():
    return {"Main Page"}


@app.get("/api/v1/users")
async def fetch_users():
    return db 


@app.post("/api/v1/users")   
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user_id == user.id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exist."
    )


@app.put("/api/v1/users/{user_id}")
async def  update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user_id == user.id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exist."
    )