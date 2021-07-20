from datetime import date
from fastapi import APIRouter;
from fastapi.param_functions import Depends;
from starlette.responses import JSONResponse;
from auth.auth import AuthHandler;
from models.sales import *;
from db.sales import sales as salesDB;
import main

router = APIRouter();

auth_handler = AuthHandler();

# Get all sales
@router.get('/sales')
async def get_all_sales( token = Depends(auth_handler.auth_wrapper)):
    query = salesDB.select();
    return await main.database.fetch_all(query);

# Get an specific sale
@router.get('/sales/{uid}')
async def get_sale(uid: int, token = Depends(auth_handler.auth_wrapper)):
    query = salesDB.select().where(uid == salesDB.c.uid);
    return await main.database.fetch_all(query);

# Post a sale
@router.post('/sales/sell', response_model=Sale)
async def post_sale(saleInfo : Sale, token = Depends(auth_handler.auth_wrapper)):
    saleDt = datetime.strptime(saleInfo.saleDt, '%d-%m-%Y')
    #saleDt = date(saleInfo.saleDt);
    query = salesDB.insert().values(amount = saleInfo.amount, uid_client = saleInfo.uid_client , uid_employee = saleInfo.uid_employee, saledt = saleDt);
    await main.database.execute(query);
    return saleInfo;

# Update an specific sale
@router.patch('/sales', response_model=Sale)
async def update_sale(saleInfo : Sale, token = Depends(auth_handler.auth_wrapper)):
    foundSaleInDB = await search_sale_byID(saleInfo.uid);
    if(foundSaleInDB):
        saleDt = datetime.strptime(saleInfo.saleDt, '%d-%m-%Y');
        query = salesDB.update().where(salesDB.c.uid == saleInfo.uid).values(amount = saleInfo.amount, uid_client = saleInfo.uid_client , uid_employee = saleInfo.uid_employee, saledt = saleDt)
        await main.database.execute(query); 
        return saleInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Remove an specific sale
@router.delete('/sales')
async def delete_sale(body: SaleBody, token = Depends(auth_handler.auth_wrapper)):
    foundSaleInDB = await search_sale_byID(body.uid);
    if(foundSaleInDB):
        query = salesDB.update().where(salesDB.c.uid == body.uid).values(deleted = True);
        await main.database.execute(query); 
        return True;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Helper functions
async def search_sale_byID(uid) :
    output = False;
    query = salesDB.select().where(uid == salesDB.c.uid);
    sale = await main.database.fetch_one(query);
    if(sale) :
        output = True;

    return output;

