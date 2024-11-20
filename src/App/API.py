import uvicorn
from fastapi import FastAPI
from .UserController import user_router
from .FollowingController import following_route
from .MovieController import movie_router
from .WatchMovieController import watch_movie_route
from .RecommendationController import recommendation_route
from .init_app import scheduler_service


def run_app():
    app = FastAPI(title="Réseau social ciné", 
                description="""<p>
                Réseau social Cinéma is a web service that allows users to interact with their movie preferences and explore films through social connections.
                Users can create an account, add movies to their favorites and watchlists, rate movies, and track their viewing history.
                The system also supports following other users, viewing their movie collections, and discovering films that have been watched by both the user and those they follow. 
                Authenticated users have access to personalized and detailed data, including the ability to rate movies and manage their collections. 
                Users can receive suggestions for new follows, and the platform ensures that only valid, authenticated users can perform actions like rating or following. Additionally, the project integrates social features, allowing users to engage with others' movie choices, share collections, and collaborate on discovering new films together.
                </p>""")

    app.include_router(user_router)

    app.include_router(movie_router)
    
    app.include_router(watch_movie_route)

    app.include_router(following_route)
    
    app.include_router(recommendation_route)

    scheduler_service.start()

    uvicorn.run(app, port=8000, host="localhost")
