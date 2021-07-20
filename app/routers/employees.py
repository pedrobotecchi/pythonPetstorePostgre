from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from pymongo import MongoClient
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.sqltypes import Date;
from starlette.responses import JSONResponse;
from auth.auth import AuthHandler;
from models.employee import *;
from db.employees import employees as employeesDB;
import main

router = APIRouter();

auth_handler = AuthHandler();

# Login
@router.post('/employees/authenticated')
async def login(authInfo : AuthModel):
    # Check if user is in DB:
    foundUser = await search_employee_byUSER(authInfo.username);
    if( foundUser ) :
        # get User password and compare:
        password = foundUser.get('password');
        if ( not auth_handler.verify_password(authInfo.password, password)) :
            raise HTTPException(status_code=401, detail='Invalid Username and/or password');
        
        await update_lastlogin(foundUser.get('uid'));

        token = auth_handler.encode_token(authInfo.username);
        return { 'token' : token }

    raise HTTPException(status_code=401, detail='User not found');

# Get all employees
@router.get('/employees')
async def get_all_employees(body : EmployeeBody, token = Depends(auth_handler.auth_wrapper)):
    if (body.showDeleted) :
        query = employeesDB.select();
        return await main.database.fetch_all(query);
    
    query = employeesDB.select().where(employeesDB.c.deleted == None);
    return await main.database.fetch_all(query);

# Get an specific employee
@router.get('/employees/{uid}')
async def get_employee(uid: int, token = Depends(auth_handler.auth_wrapper)):
    query = employeesDB.select().where(uid == employeesDB.c.uid);
    return await main.database.fetch_one(query);

# Post an employee
@router.post('/employees/signup', response_model=Employee)
async def post_employee(employeeInfo : Employee, token = Depends(auth_handler.auth_wrapper)):
    foundEmployeeInDB = await search_employee_byUSER(employeeInfo.username);
    if(not foundEmployeeInDB):
        query = employeesDB.insert().values(username = employeeInfo.username, password = employeeInfo.password, name = employeeInfo.name);
        await main.database.execute(query);
        return employeeInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee already inserted"})

# Update an specific employee
@router.patch('/employees', response_model=Employee)
async def update_employee(employeeInfo : Employee, token = Depends(auth_handler.auth_wrapper)):   
    foundEmployeeInDB = await search_employee_byID(employeeInfo.uid);
    if(foundEmployeeInDB):
        query = employeesDB.update().where(employeesDB.c.uid == employeeInfo.uid).values(name = employeeInfo.name, username = employeeInfo.username, password = employeeInfo.password)
        await main.database.execute(query); 
        return employeeInfo;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Remove an specific employee
@router.delete('/employees')
async def delete_employee(body: EmployeeBody, token = Depends(auth_handler.auth_wrapper)):
    foundEmployeeInDB = await search_employee_byID(body.uid);
    if(foundEmployeeInDB):
        query = employeesDB.update().where(employeesDB.c.uid == body.uid).values(deleted = True)
        await main.database.execute(query);
        return True;

    return JSONResponse(status_code=200, content={"Error": "Employee not found in DB inserted"})

# Helper functions
async def search_employee_byUSER(user) :
    query = employeesDB.select().where(user == employeesDB.c.username);
    employees = await main.database.fetch_one(query);

    return employees;

async def search_employee_byID(uid) :
    output = False;
    query = employeesDB.select().where(uid == employeesDB.c.uid);
    employees = await main.database.fetch_one(query);
    if(employees) :
        output = True;

    return output;

async def get_user_passsword(username) :
    query = employeesDB.select().where(username == employeesDB.c.username);
    employees = await main.database.fetch_one(query);

    return employees.get('password');

async def update_lastlogin(uid) :
    now = datetime.now();
    query = employeesDB.update().where(uid == employeesDB.c.uid).values(lastlogin = now);
    await main.database.execute(query);