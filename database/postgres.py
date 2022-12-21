from typing import Dict

from loguru import logger
import psycopg2

from models import model


class Postgres:
    def __init__(self, config: model.ConfigPG):
        try:
            self.conn = psycopg2.connect(
                host=config.host,
                port=config.port,
                user=config.user,
                password=config.password,
                dbname=config.dbname
            )
            logger.info('Connection opened successfully.')

        except psycopg2.DatabaseError as e:
            logger.error(e)
            raise e

    def close_connection(self):
        try:
            self.conn.close()
            logger.info('Connection closed successfully.')

        except psycopg2.DatabaseError as e:
            logger.error(e)
            raise e

    def signup_tg(self, user_tg: model.UserTG) -> Dict[str, str]:
        """Кладет данные пользователя из Telegram в БД"""

        try:
            with self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(
                        """insert into users (tg_user_id, username, fullname) values (%s, %s, %s)""",
                        (user_tg.tg_user_id, user_tg.username, user_tg.fullname))
            return {
                "status": "ok",
                "description": "user signed up"
            }

        except psycopg2.DatabaseError as e:
            if e.pgcode == "23505":
                return {
                    "status": "ok",
                    "description": "user already exists"
                }
            else:
                logger.error(e)
                return {
                    "status": "error",
                    "description": "error database: SIGNUP_TG"
                }

    def login_etis(self, user_etis: model.UserETIS) -> Dict[str, str]:
        pass
