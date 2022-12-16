from database import postgres
from models import model


class Service:
    def __init__(self, config: model.ConfigPG):
        self.pg = postgres.Postgres(config)
        self.pg.open_connection()

    def close_pg(self):
        self.pg.close_connection()
