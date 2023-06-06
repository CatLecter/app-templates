from lagom import Container, Singleton
from lagom.integrations.fast_api import FastApiIntegration

from db.postgres import PostgresDB

container = Container()
container[PostgresDB] = Singleton(PostgresDB)

deps = FastApiIntegration(container, request_singletons=[PostgresDB])
