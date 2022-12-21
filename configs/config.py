from dotenv import dotenv_values

from models import model


def init_config_pg() -> model.ConfigPG:
    env_values = dotenv_values(".env")
    config = model.ConfigPG(
        host=env_values["HOST"],
        port=env_values["PORT"],
        user=env_values["USER"],
        password=env_values["PASSWORD"],
        dbname=env_values["DBNAME"]
    )
    return config
