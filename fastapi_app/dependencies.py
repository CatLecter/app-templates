from rodi import Container
from db.postgres import PostgresDB

container = Container()

container.register(
    obj_type=PostgresDB,
    instance=PostgresDB()
)
