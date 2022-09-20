import logging
import os
import shutil
from pathlib import Path

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base


Base = declarative_base()
db = SQLAlchemy()
ma = Marshmallow()


# def create_all_tables(engine_name):
#     engine = get_engine(name=engine_name)
#     Base.metadata.create_all(engine)


# def drop_table_with_name(engine_name, table_name):
#     engine = get_engine(name=engine_name)
#     metadata = MetaData(engine)
#     table = Table(table_name, metadata, autoload=True)
#     if table is not None:
#         logging.info(f"Deleting {table_name} table")
#         Base.metadata.drop_all(bind=engine, tables=[table], checkfirst=True)
#     # Base.metadata.drop_all(bind=engine, tables=[Covers.__table__])


# def drop_all(engine_name):
#     engine = get_engine(name=engine_name)
#     Base.metadata.drop_all(engine)
