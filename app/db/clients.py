import sqlalchemy;
from config import settings;

metadata = sqlalchemy.MetaData()

clients = sqlalchemy.Table(
    "clients",
    metadata,
    sqlalchemy.Column("uid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("cpf", sqlalchemy.Integer),
    sqlalchemy.Column("deleted", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)