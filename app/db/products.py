import sqlalchemy;
from config import settings;

metadata = sqlalchemy.MetaData()

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("uid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("amount", sqlalchemy.Float),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("deleted", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)