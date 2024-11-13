from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging
from src.DAO.GenreRepo import GenreRepo
from src.Service.MovieFromTMDService import MovieFromTMDService

class SchedulerService(BackgroundScheduler):

    def __init__(self, movie_TMDB:MovieFromTMDService, genre_repo:GenreRepo):
        super().__init__()
        self.movie_TMDB = movie_TMDB
        self.genre_repo = genre_repo
        
    def update_movie_genre(self):
        
        try :
            movies_genres = self.movie_TMDB.get_id_name_genre()
        except Exception as error:
            logging.error(error)

        return self.genre_repo.insert_into_db([movie_genre.__dict__ for movie_genre in movies_genres]) if movies_genres else False
    
    # def update_last_week_released_movies(self):
    #     end_release_date = datetime.today()
    #     start_release_date = end_release_date - timedelta(weeks=1)
    #     try :
    #         last_week_released_movies = self.movie_TMDB.get_by_release_period(start_release_date, end_release_date)
    #     except Exception as error:
    #         logging.error(error)


    def start(self):
        self.add_job(self.update_movie_genre, 'interval', seconds=5)
        super().start()

if __name__ == "__main__" :
    import dotenv
    from src.DAO.DBConnector import DBConnector
    dotenv.load_dotenv()
    db_connector = DBConnector()
    genre_repo = GenreRepo(db_connector)
    movie_TMDB = MovieFromTMDService()
    scheduler_service = SchedulerService(movie_TMDB, genre_repo)
    print(scheduler_service.update_movie_genre())