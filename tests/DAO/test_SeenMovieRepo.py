from typing import TYPE_CHECKING, Literal, Optional, Union
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.Model.SeenMovie import SeenMovie
from src.Model.Movie import Movie 
from src.Model.User import User

if TYPE_CHECKING:
    from src.Model.SeenMovie import SeenMovie

class MockDBConnector:
    def __init__(self):
            self.db = [
        {
            "id_user": 3,
            "id_movie": 1,
            "seen": True,
            "to_watch_later": False,
            "watch_count": 3,
            "vote": 8,
            "favorite": True,
            "username": "", 
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None, 
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 4,
            "id_movie": 3,
            "seen": True,
            "to_watch_later": True,
            "watch_count": 1,
            "vote": 6,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 2,
            "id_movie": 4,
            "seen": False,
            "to_watch_later": True,
            "watch_count": 0,
            "vote": None,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 5,
            "id_movie": 2,
            "seen": True,
            "to_watch_later": False,
            "watch_count": 2,
            "vote": 7,
            "favorite": True,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 1,
            "id_movie": 5,
            "seen": False,
            "to_watch_later": True,
            "watch_count": 0,
            "vote": None,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 3,
            "id_movie": 5,
            "seen": True,
            "to_watch_later": False,
            "watch_count": 1,
            "vote": 9,
            "favorite": True,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 4,
            "id_movie": 2,
            "seen": True,
            "to_watch_later": False,
            "watch_count": 2,
            "vote": 5,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 2,
            "id_movie": 3,
            "seen": False,
            "to_watch_later": True,
            "watch_count": 0,
            "vote": None,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 5,
            "id_movie": 1,
            "seen": True,
            "to_watch_later": False,
            "watch_count": 4,
            "vote": 10,
            "favorite": True,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 1,
            "id_movie": 6,
            "seen": False,
            "to_watch_later": True,
            "watch_count": 0,
            "vote": None,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 3,
            "id_movie": 4,
            "seen": True,
            "to_watch_later": False,
            "watch_count": 2,
            "vote": 6,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 4,
            "id_movie": 1,
            "seen": True,
            "to_watch_later": False,
            "watch_count": 3,
            "vote": 8,
            "favorite": True,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None
        },
        {
            "id_user": 5,
            "id_movie": 3,
            "seen": False,
            "to_watch_later": True,
            "watch_count": 0,
            "vote": None,
            "favorite": False,
            "username": "",
            "salt": None,
            "pass_word": "",
            "original_language": None,
            "original_title": None,
            "release_date": None,
            "title": None,
            "vote_average": None,
            "vote_count": None,
            "overview": None}]

    def sql_query(
        self,
        query: str,
        data: Optional[Union[tuple, list, dict]] = None,
        return_type: Union[Literal["one"], Literal["all"]] = "none",
    ):
        match query:
            case """SELECT * from projet_info.seenmovies 
               WHERE id_user =%(id_user)s
               AND id_movie =%(id_movie)s;""":
                if not data:
                    raise Exception
                id_user = data["id_user"]
                id_movie = data["id_movie"]
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["id_movie"] == id_movie:
                        return seenmovie
                return None
                
            case """INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, to_watch_later, watch_count, vote, favorite)
                VALUES (%(id_user)s, %(id_movie)s, %(seen)s, %(to_watch_later)s, %(watch_count)s, %(vote)s, %(favorite)s)
                ON CONFLICT(id_user, id_movie) DO UPDATE
                SET watch_count = seenmovies.watch_count + 1,
                    seen = EXCLUDED.seen,
                    to_watch_later = EXCLUDED.to_watch_later,
                    vote = EXCLUDED.vote,
                    favorite = EXCLUDED.favorite
                RETURNING *;""":
                if not data:
                    raise Exception
                self.db.append({"id_user": data['id_user'], "id_movie" : data['id_movie'], 
                                "seen": data['seen'], "to_watch_later": data['to_watch_later'],
                                "watch_count" : data['watch_count'],"vote": data['vote'], "favorite": data['favorite']})
                return(self.db[-1])
            
            case  """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.movie AS m
            ON sm.id_movie = m.id
            WHERE sm.id_user = %(id_user)s
            AND sm.seen = TRUE;
            """:
                if not data:
                    raise Exception
                id_user = data["id_user"]
                list_seenmovies = []
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["seen"] is True:
                        movie = Movie(id=seenmovie["id_movie"],**seenmovie)
                        list_seenmovies.append(movie)
                return list_seenmovies

            case """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.movie AS m
            ON sm.id_movie = m.id
            WHERE sm.id_user = %(id_user)s
            AND sm.to_watch_later = TRUE;
            """:
                if not data:
                    raise Exception
                id_user = data["id_user"]
                list_seenmovies = []
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["to_watch_later"] is True:
                        movie = Movie(id=seenmovie["id_movie"],**seenmovie)
                        list_seenmovies.append(movie)
                return list_seenmovies
            
            case """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.movie AS m
            ON sm.id_movie = m.id
            WHERE sm.id_user = %(id_user)s
            AND sm.favorite = TRUE;
            """:
                if not data:
                    raise Exception
                id_user = data["id_user"]
                list_seenmovies = []
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["favorite"] is True:
                        movie = Movie(id=seenmovie["id_movie"],**seenmovie)
                        list_seenmovies.append(movie)
                return list_seenmovies
            
            case """SELECT *
            FROM projet_info.seenmovies AS sm
            JOIN projet_info.user AS m
            ON sm.id_user = m.id_user
            WHERE sm.id_movie = %(id_movie)s
            AND sm.seen = TRUE;
            """:
                if not data:
                    raise Exception
                id_movie = data["id_movie"]
                list_users = []
                for seenmovie in self.db:
                    if seenmovie["id_movie"] == id_movie and seenmovie["seen"] is True:
                        user = User(**seenmovie)
                        list_users.append(user)
                return list_users
            case """
            SELECT AVG(vote) AS vote_avg, COUNT(vote) AS vote_count 
            FROM projet_info.seenmovies
            WHERE id_movie = %(id_movie)s;
            """ :
                id_user = data["id_user"]
                id_movie = data["id_movie"]
                vote = data["vote"]
                for seenmovie in self.db: 
                    if seenmovie["id_movie"] == id_movie and seenmovie[id_user] == [id_user]:
                        self.db[seenmovie]["vote"] = vote
                    if seenmovie["id_movie"]==id_movie and seenmovie["vote"] is not None :

                else:
                    return None

def test_get_by_user_and_movie():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    db = seenmovierepo.db_connector.db
    seenmovie: SeenMovie = seenmovierepo.get_by_user_and_movie(3,1)
    assert seenmovie is not None
    assert seenmovie.id_user == 3 and seenmovie.id_movie == 1

def test_insert_into_db():
    seenmovierepo = SeenMovieRepo(MockDBConnector())
    db = seenmovierepo.db_connector.db
    seenmovie: SeenMovie = seenmovierepo.insert_into_db(
        id_user=1, 
        id_movie=4, 
        seen=True, 
        watch_count=1, 
        to_watch_later=False, 
        vote=None, 
        favorite=False
    )
    assert seenmovie is not None
    assert seenmovie.id_user == 1
    assert seenmovie.id_movie == 4
    assert seenmovie.seen is True
    assert seenmovie.vote is None 
    assert seenmovie.to_watch_later is False
    assert seenmovie.watch_count == 1
    assert seenmovie.favorite is False

def test_get_list_seenmovies_by_user():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_list_seenmovies_by_user(4)
    assert movies is not None
    assert movies[0] == Movie(id=3)
    assert movies[1] == Movie(id=2)
    assert movies[2] == Movie(id=1)

def test_get_watchlist_user():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_watchlist_user(1)
    assert movies is not None
    assert movies[0] == Movie(id=5)
    assert movies[1] == Movie(id=6)

def test_get_list_favorite_movie():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_list_favorite_movie(4)
    assert movies is not None
    assert movies[0] == Movie(id=1)

def test_get_list_users_by_movie():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    users : list[User] = seenmovierepo.get_list_users_by_movie(1)
    assert users is not None
    assert users[0].id_user == 3
    assert users[0].username == ""
    assert users[0].pass_word == ""
    assert users[0].salt is None
    assert users[0] == User(id_user=3, username="",pass_word="", salt=None)
    assert users[1] == User(id_user=5, username="",pass_word="", salt=None)
    assert users[2] == User(id_user=4, username="",pass_word="", salt=None)

def test_note_movie():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    vote_movie : int = seenmovierepo.note_movie(id_user=)