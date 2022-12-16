from loguru import logger
import psycopg2

from models import model


class Postgres:
    def __init__(self, config: model.ConfigPG):
        self.host = config.host
        self.username = config.user
        self.password = config.password
        self.port = config.port
        self.dbname = config.dbname
        self.conn = None

    def open_connection(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.username,
                    password=self.password,
                    dbname=self.dbname
                )
            except psycopg2.DatabaseError as e:
                logger.error(e)
                raise e
            finally:
                logger.info('Connection opened successfully.')

    def close_connection(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except psycopg2.DatabaseError as e:
                logger.error(e)
                raise e
            finally:
                logger.info('Connection closed successfully.')