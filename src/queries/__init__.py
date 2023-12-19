from .core.async_core import AsyncCore  # noqa: F401
from .core.sync_core import SyncCore  # noqa: F401
from .orm.async_orm import AsyncOrm  # noqa: F401
from .orm.sync_orm import SyncOrm  # noqa: F401

# core
# низкоуровневый SQL-инструментарий SQLAlchemy (набор SQL-подобных выражений);
# позволяет составлять SQL-запросы с использованием Python-синтаксиса и функций.

# orm
# высокоуровневый интерфейс SQLAlchemy ORM (cвязывает Python-классы с записями в БД);
# позволяет взаимодействовать с данными как с обычными Python-объектами.
