from fastapi import FastAPI
from routers import route_todo, route_auth
from shemas import SuccessMessage

app = FastAPI()
app.include_router(route_todo.router,tags=["todos"])
app.include_router(route_auth.router,tags=["auth"])

@app.get("/", response_model=SuccessMessage)
def read_root():
    return {"message": "Welcome to FastAPI"}

