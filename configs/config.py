from dotenv import dotenv_values

from models import model


def init_config_pg() -> model.ConfigPG:
    env = dotenv_values(".env")
    config = model.ConfigPG(
        host=env["HOST"],
        port=env["PORT"],
        user=env["USER"],
        password=env["PASSWORD"],
        dbname=env["DBNAME"]
    )
    return config
