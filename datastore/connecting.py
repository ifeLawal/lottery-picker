# https://docs.sqlalchemy.org/en/14/tutorial/engine.html
# import sqlalchemy
# sqlalchemy(__name__)
import os

from sqlalchemy import create_engine
from datastore.models.mega_millions import DataAccessObject, dao

class DatabaseConnector:
    # {
#     "drivername": "sqlite",
#     # 'host': 'localhost',
#     # 'port': '5432',
#     # 'username': 'YOUR_USERNAME',
#     # 'password': 'YOUR_PASSWORD',
#     "database": "/path/to/your_db.sqlite",
# }

    basedir = os.path.abspath(os.path.dirname(__file__))
    
    def __init__(self, db_type="sqlite", db_api="pysqlite"):
      self.db_type = db_type
      self.db_api = db_api

    def clean_tables_and_get_data_access_object(self, name) -> DataAccessObject:
        db_location = os.path.join(self.basedir, f"{name}.db")
        conn_string = f"{self.db_type}+{self.db_api}:///{db_location}"
        dao.set_conn_string(conn_string=conn_string)
        dao.db_clear() 
        dao.db_init(conn_string=conn_string)
        return dao


    def get_data_access_object(self, name) -> DataAccessObject:
        db_location = os.path.join(self.basedir, f"{name}.db")
        conn_string = f"{self.db_type}+{self.db_api}:///{db_location}"
        dao.set_conn_string(conn_string=conn_string)
        dao.db_init(conn_string=conn_string)
        return dao

    def get_engine(self, name):
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_type = "sqlite"
        db_api = "pysqlite"
        db_location = os.path.join(basedir, f"{name}.db")
        engine = create_engine(
            f"{db_type}+{db_api}:///{db_location}", echo=True, future=True
        )
        # engine = create_engine(URL(**DATABASE))
        return engine