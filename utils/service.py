from typing import Dict

from database import postgres
from models import model


class Service:
    def __init__(self, config: model.ConfigPG):
        self.pg = postgres.Postgres(config)

    def close_pg(self):
        self.pg.close_connection()

    def signup_tg(self, user_tg: model.UserTG) -> (Dict[str, str], int):
        """"""
        res = self.pg.signup_tg(user_tg)
        if res["status"] == "error":
            return res, 500
        return res, 200
