#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models import Base, Categories, Units, Positions, Ownerships


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

    repository.session.add(Categories(name="Продукты", description="Категория продуктов"))

    repository.session.add(Units(unit="pcs"))
    repository.session.add(Units(unit="kg"))
    repository.session.add(Units(unit="lb"))

    repository.session.add(Positions(position="Manager"))
    repository.session.add(Positions(position="Admitistrator"))

    repository.session.add(Ownerships(ownership="Sole"))
    repository.session.add(Ownerships(ownership="General"))
    repository.session.add(Ownerships(ownership="Corporation"))
    repository.session.add(Ownerships(ownership="Limited Liability Company"))
    repository.session.add(Ownerships(ownership="Limited Partnership"))
    repository.session.add(Ownerships(ownership="Limited Liability Partnership"))

    repository.session.commit()
