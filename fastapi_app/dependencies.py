from engines.storage import DBEngine
from engines.storage_with_orm import ORMEngine
from rodi import Container

container = Container()

container.register(obj_type=DBEngine, instance=DBEngine())
container.register(obj_type=ORMEngine, instance=ORMEngine())
