from fastapi import APIRouter
from fastapi.param_functions import Depends, Query
from pymongo import MongoClient;
from starlette.responses import JSONResponse;
from auth.auth import AuthHandler;
from models.dogs import *;
from db.dogs import dogs as dogsDB;
import main

router = APIRouter();

auth_handler = AuthHandler();

# Get all dogs
@router.get('/dogs')
async def get_all_dogs(body : DogBody, token = Depends(auth_handler.auth_wrapper)):
    if (body.showDeleted) :
        query = dogsDB.select();
        return await main.database.fetch_all(query);
    
    query = dogsDB.select().where(dogsDB.c.deleted == None);
    return await main.database.fetch_all(query);

# Get an specific dog
@router.get('/dogs/{uid}')
async def get_dog(uid: int, token = Depends(auth_handler.auth_wrapper)):
    query = dogsDB.select().where(uid == dogsDB.c.uid);
    return await main.database.fetch_one(query);

# Post a dog
@router.post('/dogs/insert', response_model=Dog)
async def post_client(dogInfo : Dog, token = Depends(auth_handler.auth_wrapper)):
    
    foundDogInDB = await search_dog(dogInfo.name, dogInfo.uid_client);
    if(not foundDogInDB):
        query = dogsDB.insert().values(name = dogInfo.name, breed = dogInfo.breed ,furr = dogInfo.furr, uid_client = dogInfo.uid_client, size = dogInfo.size);
        await main.database.execute(query);
        return dogInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee already inserted"})

# Update an specific dog
@router.patch('/dogs', response_model=Dog)
async def update_client(dogInfo : Dog, token = Depends(auth_handler.auth_wrapper)):
    foundDogInDB = await search_dog_byID(dogInfo.uid);
    if(foundDogInDB):
        query = dogsDB.update().where(dogsDB.c.uid == dogInfo.uid).values(name = dogInfo.name, breed = dogInfo.breed ,furr = dogInfo.furr, uid_client = dogInfo.uid_client, size = dogInfo.size)
        await main.database.execute(query); 
        return dogInfo;

    return JSONResponse(status_code=200, content={"Error": "Dog not found in DB inserted"})

# Remove an specific client
@router.delete('/dogs')
async def delete_dog(body: DogBody, token = Depends(auth_handler.auth_wrapper)):
    foundDogInDB = await search_dog_byID(body.uid);
    if(foundDogInDB):
        query = dogsDB.update().where(dogsDB.c.uid == body.uid).values(deleted = True);
        await main.database.execute(query); 
        return True;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Helper functions
async def search_dog(dogName, uid_client) :
    output = False;
    #query = f'SELECT * FROM dogs WHERE name={dogName} and uid_client={uid_client}';
    query = dogsDB.select().where(dogsDB.c.name == dogName).where(dogsDB.c.uid_client == uid_client);
    dog = await main.database.execute(query);
    if(dog) :
        output = True;

    return output;

# Helper functions
async def search_dog_byID(uid) :
    output = False;
    query = dogsDB.select().where(uid == dogsDB.c.uid);
    dog = await main.database.fetch_one(query);
    if(dog) :
        output = True;

    return output;

async def get_dogs_byClient(uid_client):
    output = [];
    query = dogsDB.select().where(uid_client == dogsDB.c.uid_client);
    dogs = await main.database.fetch_all(query);
    for d in dogs:
        output.append(d);
    
    return output;

async def delete_dogs_byClient(uid_client) :
    query = dogsDB.select().where(uid_client == dogsDB.c.uid_client);
    dog = await main.database.fetch_all(query);
    for q in dog :
        await delete_dog(q.get('uid'));

    return True;