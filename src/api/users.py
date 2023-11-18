from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from src import database as db
from argon2 import PasswordHasher


ph = PasswordHasher()

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

def validatePassword(user_id, password):
    with db.engine.begin() as connection:
        result  = connection.execute(sqlalchemy.text(
            """SELECT password
                FROM users
                WHERE id=:user_id
            """),
        [{
            "user_id":user_id
        }]
        )

    hash = result.scalar_one_or_none()
    if hash is None:
        print("User doesn't exist.")
    try:
        return ph.verify(hash=hash, password=password)
    except Exception:
        return False

class PasswordRequest(BaseModel):
    password: str

class UserIdResponse(BaseModel):
    user_id: int

@router.post("/create")
def create_user(pw: PasswordRequest) -> UserIdResponse:
    """ """
    # salt is handled by library
    hashed = ph.hash(pw.password)
    with db.engine.begin() as connection:
        user_result = connection.execute(sqlalchemy.text("INSERT INTO users(password)\
                                           VALUES (:password)\
                                           RETURNING id"),
                                           [{
                                               "password":hashed
                                           }]).one()
    return user_result.id

class Platform(BaseModel):
    platform: str

@router.post("/platform")
def set_platform(user_id: int, password: PasswordRequest, platform: str):
    """ """
    if not validatePassword(user_id, password.password):
        return "Incorrect Password"

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
        UPDATE users
        SET platform_id = sq.sel_platform
        FROM
        (SELECT id as sel_platform
            FROM platforms
            WHERE platform_name=:platform) as sq
        WHERE id=:user_id
        """),
        [{
            "user_id":user_id,
            "platform":platform
        }])

        if result.rowcount == 0:
            return "Invalid password or platform"
    

    return "OK"
@router.post("/delete/{user_id}")
def delete_user(user_id: int, password: PasswordRequest):
    """ """
    with db.engine.begin() as connection:
        salt_rsp = connection.execute(sqlalchemy.text(
            """
            SELECT salt
            FROM users
            WHERE id = :user_id
            """
        ),
        [{
            "user_id":user_id
        }]
        ).scalar_one_or_none()

        if salt_rsp is None:
            return "User does not exist"
        
        
        hashed = hashPassword(password, salt_rsp)

        result = connection.execute(sqlalchemy.text(
  
    if not validatePassword(user_id, password.password):
        return "Incorrect Password"

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            """DELETE
                FROM users
                WHERE id=:user_id
            """),
        [{
            "user_id":user_id,
        }]
        )

        if result.rowcount == 0:
            return "Invalid password"
    
    return "OK"
