#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Base, Categories, Units


DATABASE_PATH = "db.sqlite3"


class Repository:
    def __init__(self, database_path):
        self.engine = create_engine(f"sqlite:///{database_path}")
        self.session = sessionmaker(bind=self.engine)()

        Repository.create_database(self.engine)

    @staticmethod
    def create_database(engine):
        Base.metadata.create_all(engine)


if __name__ == "__main__":
    repository = Repository(DATABASE_PATH)

    # choices demo
    unit = Units(unit="pcs")
    print(unit.unit)

    category = Categories(name="Продукты", description="Категория продуктов")

    repository.session.add(unit)
    repository.session.add(category)

    repository.session.commit()
