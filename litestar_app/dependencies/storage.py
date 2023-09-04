from engines.storage import DBEngine


async def provides_postgres() -> DBEngine:
    return DBEngine()
