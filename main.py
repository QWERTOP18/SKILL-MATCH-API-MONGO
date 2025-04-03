from fastapi import FastAPI
from routers import route_todo
from shemas import SuccessMessage

app = FastAPI()
app.include_router(route_todo.router)

@app.get("/", response_model=SuccessMessage)
def read_root():
    return {"message": "Welcome to FastAPI"}