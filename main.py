from fastapi import FastAPI
from routers import route_task, route_auth, route_project
from schemas.schema_util import SuccessMessage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(route_task.router,tags=["task"])
app.include_router(route_auth.router,tags=["auth"])
app.include_router(route_project.router,tags=["project"])





origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_model=SuccessMessage)
def read_root():
    return {"message": "Welcome to FastAPI"}

