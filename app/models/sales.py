from pydantic import BaseModel;
from typing import Optional;
from pydantic.fields import Field;
from pydantic.main import BaseConfig;
from datetime import datetime;
from os import error;
from bson.objectid import ObjectId
from sqlalchemy.sql.sqltypes import Date;

class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

class Sale(MongoModel):
    uid: Optional[int]
    amount: float = Field()
    uid_client: int = Field()
    uid_employee: int = Field()
    saleDt: str = Field()
    deleted: Optional[bool]

class SaleBody(MongoModel):
    uid: Optional[int]
    showDeleted: Optional[bool]