import uvicorn
from fastapi import FastAPI
from .MovieController import movie_router
from .UserController import user_router
from .init_app import scheduler_service


def run_app():
    app = FastAPI(title="Projet Info 2A", description="Example project for ENSAI students")

    app.include_router(user_router)

    app.include_router(movie_router)

    scheduler_service.start()

    uvicorn.run(app, port=8000, host="localhost")
