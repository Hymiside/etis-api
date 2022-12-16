from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models import model
from utils import service
import configs.config


a = configs.config.init_config_pg()

r = APIRouter()
config = model.ConfigPG(
        host="localhost",
        port="5432",
        user="postgres",
        password="putinbest",
        dbname="etis-api"
    )
s = service.Service(config)


@r.post("/signup-tg")
async def signup_tg(req: model.UserTG):
    user_tg = jsonable_encoder(req)
    return JSONResponse(user_tg)


@r.on_event("shutdown")
async def shutdown():
    s.close_pg()
