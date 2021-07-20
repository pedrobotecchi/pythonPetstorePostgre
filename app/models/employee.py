from os import error
from pydantic import BaseModel
from typing import Optional
from pydantic.main import BaseConfig
from bson.objectid import ObjectId
from pydantic.fields import Field
from datetime import datetime

class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }

class AuthModel(MongoModel):
    username: str = Field()
    password: str = Field()


class Employee(MongoModel):
    uid: Optional[int]
    name: str = Field()
    username: str = Field()
    password: str = Field()
    deleted: Optional[bool]
    lastlogin: Optional[datetime]

# body class
class EmployeeBody(MongoModel):
    uid: Optional[int]
    showDeleted: Optional[bool]