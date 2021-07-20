from pydantic import BaseModel, errors;
from typing import Optional;
from pydantic.main import BaseConfig;
from pydantic.fields import Field;
from bson.objectid import ObjectId;

class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

class Dog(MongoModel):
    uid: Optional[int]
    name: str = Field()
    breed: str = Field()
    furr: str = Field()
    size: str = Field()
    uid_client: int = Field()
    deleted: Optional[bool]

class DogBody(MongoModel):
    showDeleted: Optional[bool]
    uid: Optional[int]