from fastapi import APIRouter;
from fastapi.param_functions import Depends;
from pymongo import MongoClient;
from starlette.responses import JSONResponse;
from .dogs import get_dogs_byClient, delete_dogs_byClient;
from auth.auth import AuthHandler;
from models.clients import *;
from db.clients import clients as clientsDB;
import main;

router = APIRouter();

auth_handler = AuthHandler();

# Get all clients
@router.get('/clients')
async def get_all_clients(body : ClientBody, token = Depends(auth_handler.auth_wrapper)):
    output = [];

    if (body.showDeleted) :
        query = clientsDB.select();
        clients = await main.database.fetch_all(query);
        for q in clients:
            dogs = await get_dogs_byClient(q.get('uid'));
            output.append({'client' : q, 'dogs' : dogs});

        return (output);
    
    query = clientsDB.select().where(clientsDB.c.deleted == None);
    clients = await main.database.fetch_all(query);
    for q in clients:
        dogs = await get_dogs_byClient(q.get('uid'));
        output.append({'client' : q, 'dogs' : dogs});

    return (output);

# Get an specific client
@router.get('/clients/{uid}')
async def get_client(uid: int, token = Depends(auth_handler.auth_wrapper)):
    output = [];
    query = clientsDB.select().where(clientsDB.c.uid == uid);
    client = await main.database.fetch_one(query);
    dogs = await get_dogs_byClient(client.get('uid'));
    output.append({'client': client, 'dogs': dogs });

    return (output);

# Post a client
@router.post('/clients/insert', response_model=Client)
async def post_client(clientInfo : Client, token = Depends(auth_handler.auth_wrapper)):

    foundClientInDB = await search_client_byCPF(clientInfo.cpf);
    if(not foundClientInDB):
        query = clientsDB.insert().values(name = clientInfo.name, phone = clientInfo.phone ,address = clientInfo.phone, cpf = clientInfo.cpf);
        await main.database.execute(query);
        return clientInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee already inserted"})

# Update an specific client
@router.patch('/clients', response_model=Client)
async def update_client(clientInfo : Client, token = Depends(auth_handler.auth_wrapper)):

    foundClientInDB = await search_client_byID(clientInfo.uid);
    if(foundClientInDB):
        query = clientsDB.update().where(clientsDB.c.uid == clientInfo.uid).values(name = clientInfo.name, phone = clientInfo.phone ,address = clientInfo.phone, cpf = clientInfo.cpf)
        await main.database.execute(query); 
        return clientInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Remove an specific client
@router.delete('/clients')
async def delete_employee(body: ClientBody, token = Depends(auth_handler.auth_wrapper)):

    foundClientInDB = await search_client_byID(body.uid);
    if(foundClientInDB):
        query = clientsDB.update().where(clientsDB.c.uid == body.uid).values(deleted = True);
        await main.database.execute(query); 
        delete_dogs_byClient(body.uid);

        return True;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Helper functions
async def search_client_byCPF(cpf) :
    output = False;
    query = clientsDB.select().where(cpf == clientsDB.c.cpf);
    clients = await main.database.fetch_one(query);
    if(clients) :
        output = True;

    return output;

# Helper functions
async def search_client_byID(uid) :
    output = False;
    query = clientsDB.select().where(uid == clientsDB.c.uid);
    clients = await main.database.fetch_one(query);
    if(clients) :
        output = True;

    return output;

