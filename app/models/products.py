from pydantic import BaseModel;
from typing import Optional;
from pydantic.fields import Field;
from pydantic.main import BaseConfig;
from os import error;
from bson.objectid import ObjectId;

class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

class Product(MongoModel):
    uid: Optional[int]
    name: str = Field()
    amount: float = Field()
    description: str = Field()
    deleted: Optional[bool]

class ProductBody(MongoModel):
    uid: Optional[int]
    showDeleted: Optional[bool]
