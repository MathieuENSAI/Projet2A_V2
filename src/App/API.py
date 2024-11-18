import uvicorn
from fastapi import FastAPI
from .UserController import user_router
from .FollowingController import following_route
from .MovieController import movie_router
from .WatchMovieController import watch_movie_route
from .RecommendationController import recommendation_route
from .init_app import scheduler_service


def run_app():
    app = FastAPI(title="Réseau social ciné", description="Réseau social ciné")

    app.include_router(user_router)

    app.include_router(movie_router)
    
    app.include_router(watch_movie_route)

    app.include_router(following_route)
    
    app.include_router(recommendation_route)

    scheduler_service.start()

    uvicorn.run(app, port=8000, host="localhost")
