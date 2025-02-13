from src.Model.User import User 
from src.Model.Movie import Movie 
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.DAO.MovieRepo import MovieRepo

class NoteService :

    def __init__(self, movie_repo:MovieRepo, seen_movie_repo :SeenMovieRepo):
        self.movie_repo=movie_repo
        self.seen_movie_repo=seen_movie_repo
    
    def note_movie(self, id_user:int, id_movie:int, note:int):
        vote_movie = self.seen_movie_repo.note_movie(id_user, id_movie, note)
        if vote_movie:
            movie = self.movie_repo.update_vote(id_movie, vote_movie["vote_avg"], vote_movie["vote_count"])
            return movie
        return None
    
    def remove_note_movie(self, id_user:int, id_movie:int):
        vote_movie =self.seen_movie_repo.remove_note_movie(id_user, id_movie)
        if vote_movie:
            movie = self.movie_repo.update_vote(id_movie, vote_movie["vote_avg"], vote_movie["vote_count"])
            return movie
        return False

if __name__ == "__main__" :
    import dotenv
    from src.DAO.DBConnector import DBConnector
    dotenv.load_dotenv()
    db_connector = DBConnector()
    movie_repo = MovieRepo(db_connector)
    seen_movie_repo = SeenMovieRepo(db_connector)
    
    note_service = NoteService(movie_repo, seen_movie_repo)
    print(note_service.note_movie(1, 700, 8))

    