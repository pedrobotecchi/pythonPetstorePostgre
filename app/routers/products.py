from fastapi import APIRouter;
from fastapi.param_functions import Depends;
from pymongo import MongoClient;
from starlette.responses import JSONResponse;
from auth.auth import AuthHandler;
from models.products import *;
from db.products import products as productsDB;
import main

router = APIRouter();

auth_handler = AuthHandler();


# Get all products
@router.get('/products')
async def get_all_products(body: ProductBody, token = Depends(auth_handler.auth_wrapper)):
    if (body.showDeleted) :
        query = productsDB.select();
        return await main.database.fetch_all(query);
    
    query = productsDB.select().where(productsDB.c.deleted == None);
    return await main.database.fetch_all(query);

# Get an specific product
@router.get('/products/{uid}')
async def get_product(uid: int, token = Depends(auth_handler.auth_wrapper)):
    query = productsDB.select().where(uid == productsDB.c.uid);
    return await main.database.fetch_one(query);

# Post a product
@router.post('/products/insert', response_model=Product)
async def post_product(productInfo : Product, token = Depends(auth_handler.auth_wrapper)):
    foundProductInDB = await search_product_byName(productInfo.name);
    if(not foundProductInDB):
        query = productsDB.insert().values(name = productInfo.name, amount = productInfo.amount ,description = productInfo.description );
        await main.database.execute(query);
        return productInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee already inserted"})

# Update an specific product
@router.patch('/products', response_model=Product)
async def update_product(productInfo : Product, token = Depends(auth_handler.auth_wrapper)):
    foundProductInDB = await search_product_byID(productInfo.uid);
    if(foundProductInDB):
        query = productsDB.update().where(productsDB.c.uid == productInfo.uid).values(name = productInfo.name, amount = productInfo.amount ,description = productInfo.description)
        await main.database.execute(query); 
        return productInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Remove an specific product
@router.delete('/products')
async def delete_product(body: ProductBody, token = Depends(auth_handler.auth_wrapper)):
    foundProductInDB = await search_product_byID(body.uid);
    if(foundProductInDB):
        query = productsDB.update().where(productsDB.c.uid == body.uid).values(deleted = True);
        await main.database.execute(query); 
        return True;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Helper functions
async def search_product_byName(name) :
    output = False;
    query = productsDB.select().where(name == productsDB.c.name);
    product = await main.database.fetch_one(query);
    if(product) :
        output = True;

    return output;

# Helper functions
async def search_product_byID(uid) :
    output = False;
    query = productsDB.select().where(uid == productsDB.c.uid);
    product = await main.database.fetch_one(query);
    if(product) :
        output = True;

    return output;

