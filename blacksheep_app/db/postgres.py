import os
from datetime import datetime
from uuid import UUID

from dotenv import load_dotenv
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from schemes.users import User

load_dotenv(dotenv_path='./.env')


class PostgresDB:
    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST')
        self.port = os.getenv('POSTGRES_PORT')
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')
        self.database = os.getenv('POSTGRES_DB')
        self.pool = None

    def create_pool(self, min_size: int = 1, max_size: int = 20) -> None:
        if not self.pool:
            self.pool = pool.SimpleConnectionPool(
                cursor_factory=RealDictCursor,
                minconn=min_size,
                maxconn=max_size,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )

    def get_user(self, user_id: UUID) -> dict | None:
        self.create_pool()
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE uuid = %s', (str(user_id),))
                user = cursor.fetchone()
        finally:
            self.pool.putconn(conn)
        return dict(user) or None

    def add_user(self, user: User) -> dict | None:
        self.create_pool()
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users(full_name, phone) VALUES(%s, %s) RETURNING uuid',
                    (user.full_name, user.phone,)
                )
                uuid = cursor.fetchone()
                uuid = uuid['uuid'] if uuid else None
        finally:
            conn.commit()
            self.pool.putconn(conn)
        return self.get_user(uuid) if uuid else None

    def update_user(self, user: User, user_id: UUID) -> dict | None:
        self.create_pool()
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE users SET full_name = (%s), phone = (%s), updated_at = (%s) '
                    'WHERE uuid = (%s) RETURNING uuid',
                    (user.full_name, user.phone, datetime.now(), str(user_id),)
                )
                uuid = cursor.fetchone()
                uuid = uuid['uuid'] if uuid else None
        finally:
            conn.commit()
            self.pool.putconn(conn)
        return self.get_user(uuid) if uuid else None

    def delete_user(self, user_id: UUID) -> str | None:
        self.create_pool()
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM users WHERE uuid = (%s) RETURNING uuid', (str(user_id),))
                delete_user_id = cursor.fetchone()
                delete_user_id = delete_user_id['uuid'] if delete_user_id else None
        finally:
            conn.commit()
            self.pool.putconn(conn)
        return delete_user_id or None
