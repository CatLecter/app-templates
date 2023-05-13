from db.postgres import PostgresDB


async def provides_postgres() -> PostgresDB:
    return PostgresDB()
