import uvicorn
from fastapi import FastAPI
from .UserController import user_router
from .FollowingController import following_route
from .MovieController import movie_router
from .WatchMovieController import watch_movie_route
from .RecommendationController import recommendation_route
from .init_app import scheduler_service

def run_app():
    app = FastAPI(
        title="Réseau social ciné",
        description="""
<p><strong>"Réseau social Cinéma"</strong> is a web service that allows users to interact with their movie preferences and explore films through social connections.</p>
<p>Users can:</p>
<ul>
    <li>Create an account.</li>
    <li>Add movies to their <em>favorites</em> and <em>watchlists</em>.</li>
    <li>Rate movies and track their viewing history.</li>
    <li>Follow other users and view their movie collections.</li>
    <li>Discover films that have been watched by both the user and those they follow.</li>
</ul>
<p>Authenticated users have access to:</p>
<ul>
    <li>Personalized and detailed data, including the ability to rate movies and manage their collections.</li>
    <li>Suggestions for new follows.</li>
</ul>
<p>The platform ensures that only valid, authenticated users can perform actions like rating or following.</p>
<p>Additionally, the project integrates social features, allowing users to engage with others' movie choices, share collections, and collaborate on discovering new films together.</p>
        """,
    )
    app.include_router(user_router)
    app.include_router(movie_router)
    app.include_router(watch_movie_route)
    app.include_router(following_route)
    app.include_router(recommendation_route)

    scheduler_service.start()

    uvicorn.run(app, port=8000, host="localhost")
