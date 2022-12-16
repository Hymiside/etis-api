from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models import model
from utils import service
from configs import config


r = APIRouter()
cfg = config.init_config_pg()
s = service.Service(cfg)


@r.post("/signup-tg")
async def signup_tg(req: model.UserTG):
    user_tg = jsonable_encoder(req)
    return JSONResponse(user_tg)


@r.on_event("shutdown")
async def shutdown():
    s.close_pg()
