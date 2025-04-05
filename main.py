from fastapi import FastAPI
from app.routers import route_task, route_auth, route_project, route_user, route_questions, route_project_user
from app.schemas.schema_util import SuccessMessage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(route_task.router,tags=["task"])
app.include_router(route_auth.router,tags=["user"])
app.include_router(route_user.router,tags=["user"])
app.include_router(route_project.router,tags=["project"])
app.include_router(route_questions.router,tags=["questions"])
app.include_router(route_project_user.router,tags=["project_user"])



# CORS設定
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

