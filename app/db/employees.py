import sqlalchemy;
from config import settings;

metadata = sqlalchemy.MetaData()

employees = sqlalchemy.Table(
    "employees",
    metadata,
    sqlalchemy.Column("uid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("lastlogin", sqlalchemy.DATE),
    sqlalchemy.Column("deleted", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)