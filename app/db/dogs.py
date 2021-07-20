import sqlalchemy;
from config import settings;

metadata = sqlalchemy.MetaData()

dogs = sqlalchemy.Table(
    "dogs",
    metadata,
    sqlalchemy.Column("uid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("breed", sqlalchemy.String),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("furr", sqlalchemy.String),
    sqlalchemy.Column("uid_client", sqlalchemy.Integer),
    sqlalchemy.Column("size", sqlalchemy.String),
    sqlalchemy.Column("deleted", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)