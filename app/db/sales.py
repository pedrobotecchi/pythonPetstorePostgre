import sqlalchemy;
from config import settings;

metadata = sqlalchemy.MetaData()

sales = sqlalchemy.Table(
    "sales",
    metadata,
    sqlalchemy.Column("uid", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("amount", sqlalchemy.Float),
    sqlalchemy.Column("uid_client", sqlalchemy.Integer),
    sqlalchemy.Column("uid_employee", sqlalchemy.Integer),
    sqlalchemy.Column("saledt", sqlalchemy.Date),
    sqlalchemy.Column("deleted", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL, pool_size=3, max_overflow=0
)
metadata.create_all(engine)