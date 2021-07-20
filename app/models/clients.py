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

class Client(MongoModel):
    name: str = Field()
    cpf: str = Field()
    address: str = Field()
    phone: str = Field()
    uid : Optional[int]
    deleted: Optional[bool]

class ClientBody(MongoModel):
    showDeleted: Optional[bool]
    uid : Optional[int]