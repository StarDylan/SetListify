from fastapi import APIRouter
from pydantic import BaseModel
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


class UserIdResponse(BaseModel):
    user_id: int

@router.post("/create")
def create_user(password: str) -> UserIdResponse:
    """ """
    with db.engine.begin() as connection:
        user_result = connection.execute(sqlalchemy.text("INSERT INTO users(password)\
                                           VALUES (:password)\
                                           RETURNING id"),
                                           [{
                                               "password":password
                                           }]).one()
    return user_result.id

class Platform(BaseModel):
    platform: str
    album: str
    artist: str
    link: str

@router.post("/platform")
def set_platform(user_id: int, password: str, platform: Platform):
    """ """
    with db.engine.begin() as connection:
        user_result = connection.execute(sqlalchemy.text("""UPDATE users
        SET platform_id = sq.sel_platform
        FROM
        (SELECT id as sel_platform
            FROM platforms
            WHERE platform_name=:platform) as sq
        WHERE id=:user_id AND password=:password"""),
        [{
            "user_id":user_id,
            "password":password,
            "platform":platform
        }])
    
@router.post("/delete/{user_id}")
def delete_user(user_id: int, password: str):
    """ """
    with db.engine.begin() as connection:
        user_result = connection.execute(sqlalchemy.text(
            """DELETE
                FROM users
                WHERE id=:user_id AND password=:password
            """),
        [{
            "user_id":user_id,
            "password":password
        }]
        )

    raise NotImplementedError()

