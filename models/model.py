from pydantic import BaseModel, EmailStr


class UserTG(BaseModel):
    tg_user_id: int
    username: str | None
    fullname: str | None


class UserETIS(BaseModel):
    tg_user_id: int
    email: EmailStr
    password: str


class ConfigPG(BaseModel):
    host: str
    port: str
    user: str
    password: str
    dbname: str
