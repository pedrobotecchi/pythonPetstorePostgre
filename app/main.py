from fastapi import FastAPI;
from routers import employees, clients, dogs, products, sales;
from config import settings;
import databases;

app = FastAPI();
database = databases.Database(settings.DATABASE_URL);

@app.on_event("startup")
async def startup():
    await database.connect();

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect();

app.include_router(employees.router);
app.include_router(clients.router);
app.include_router(dogs.router);
app.include_router(products.router);
app.include_router(sales.router);

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

def main() :
    return app;