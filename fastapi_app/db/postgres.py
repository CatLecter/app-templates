from datetime import datetime
from uuid import UUID

from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from schemes import User
from settings import settings


class PostgresDB:
    def __init__(self):
        self.host = settings.pg_host
        self.port = settings.pg_port
        self.user = settings.pg_user
        self.password = settings.pg_password
        self.database = settings.pg_db
        self.pool = {}

    def create_pool(self, min_size: int = 1, max_size: int = 50) -> None:
        if self.pool.get('pool') is None:
            self.pool['pool'] = pool.SimpleConnectionPool(
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
        conn = self.pool['pool'].getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE uuid = %s', (str(user_id),))
                user = cursor.fetchone()
        finally:
            self.pool['pool'].putconn(conn)
        return dict(user) if user else None

    def add_user(self, user: User) -> dict | None:
        self.create_pool()
        conn = self.pool['pool'].getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users(full_name, phone) VALUES(%s, %s) RETURNING uuid',
                    (
                        user.full_name,
                        user.phone,
                    ),
                )
                uuid = cursor.fetchone()
                uuid = uuid['uuid'] if uuid else None
        finally:
            conn.commit()
            self.pool['pool'].putconn(conn)
        return self.get_user(uuid) if uuid else None

    def update_user(self, user: User, user_id: UUID) -> dict | None:
        self.create_pool()
        conn = self.pool['pool'].getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE users SET full_name = (%s), phone = (%s), updated_at = (%s) '
                    'WHERE uuid = (%s) RETURNING uuid',
                    (
                        user.full_name,
                        user.phone,
                        datetime.now(),
                        str(user_id),
                    ),
                )
                uuid = cursor.fetchone()
                uuid = uuid['uuid'] if uuid else None
        finally:
            conn.commit()
            self.pool['pool'].putconn(conn)
        return self.get_user(uuid) if uuid else None

    def delete_user(self, user_id: UUID) -> str | None:
        self.create_pool()
        conn = self.pool['pool'].getconn()
        try:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM users WHERE uuid = (%s) RETURNING uuid', (str(user_id),))
                delete_user_id = cursor.fetchone()
                delete_user_id = delete_user_id['uuid'] if delete_user_id else None
        finally:
            conn.commit()
            self.pool['pool'].putconn(conn)
        return delete_user_id or None

    def close_pool(self) -> None:
        if self.pool.get('pool') is not None:
            self.pool['pool'].closeall()
            self.pool = {}
