import typing

from databases import DatabaseURL, Database as DatabaseBackend
from sqlalchemy import MetaData
import orm, orm.models


class Database:
    def __init__(self, url: DatabaseURL):
        url = DatabaseURL(url)

        if url.scheme == "postgres":
            # The default postgres backend for databases does not return
            # RowProxy objects, unlike all the other backends.
            # Therefore, we use aiopg so that we have dialect-agnostic results.
            url = url.replace(scheme="postgres+aiopg")

        self.url = url
        self.database = DatabaseBackend(url)
        self.metadata = MetaData()

        class DatabaseModelMetaclass(orm.models.ModelMetaclass):
            def __new__(
                cls: type,
                name: str,
                bases: typing.Sequence[type],
                attrs: dict,
            ) -> type:
                attrs["__database__"] = self.database
                attrs["__metadata__"] = self.metadata

                return super(DatabaseModelMetaclass, cls).__new__(
                    cls, name, bases, attrs
                )

        class DatabaseModel(orm.Model, metaclass=DatabaseModelMetaclass):
            __abstract__ = True

        self.Model = DatabaseModel
