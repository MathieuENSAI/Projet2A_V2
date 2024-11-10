from typing import TYPE_CHECKING, Literal, Optional, Union
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.Model.SeenMovie import SeenMovie

if TYPE_CHECKING:
    from src.Model.SeenMovie import SeenMovie

class MockDBConnector:
    def __init__(self):
        self.db = [{"id_user": 1, "id_movie": 1, "seen": True, "vote": 10, "favorite" : True},
                   {"id_user": 2, "id_movie": 2, "seen": True, "vote": 5, "favorite" : True}, 
                   {"id_user": 2, "id_movie": 1, "seen": True, "vote": 0, "favorite" : False},
                   {"id_user": 3, "id_movie": 2, "seen": True, "vote": 10, "favorite" : False},
                   {"id_user": 1, "id_movie": 2, "seen": False, "vote": None, "favorite" : False},
                   {"id_user": 1, "id_movie": 3, "seen": False, "vote": None, "favorite" : False},
                   {"id_user": 1, "id_movie": 4, "seen": False, "vote": None, "favorite" : False}]

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
                
            case """INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, vote, favorite)
                VALUES (%(id_user)s, %(id_movie)s, %(seen)s, %(vote)s, %(favorite)s)
                RETURNING *;""":
                if not data:
                    raise Exception
                self.db.append({"id_user": data['id_user'], "id_movie" : data['id_movie'], 
                                "seen": data['seen'], "vote": data['vote'], "favorite": data['favorite']})
                return(self.db[-1])
            
            case  """SELECT id_movie 
            FROM projet_info.seenmovies 
            WHERE %(id_user)s = id_user
            AND seen = TRUE""":
                if not data:
                    raise Exception
                id_user = data["id_user"]
                list_seenmovies = []
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["seen"] == True:
                        movie = seenmovie["id_movie"]
                        list_seenmovies.append(movie)
                return list_seenmovies

            case """SELECT id_movie 
            FROM projet_info.seenmovies 
            WHERE %(id_user)s = id_user
            AND seen = FALSE""":
                if not data:
                    raise Exception
                id_user = data["id_user"]
                list_seenmovies = []
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["seen"] == False:
                        movie = seenmovie["id_movie"]
                        list_seenmovies.append(movie)
                return list_seenmovies
            
            case """SELECT id_movie 
            FROM projet_info.seenmovies 
            WHERE %(id_user)s = id_user
            AND favorite = TRUE""":
                if not data:
                    raise Exception
                id_user = data["id_user"]
                list_seenmovies = []
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["favorite"] == True:
                        movie = seenmovie["id_movie"]
                        list_seenmovies.append(movie)
                return list_seenmovies
            
            case """SELECT id_user 
            FROM projet_info.seenmovies 
            WHERE %(id_movie)s = id_movie
            AND seen = TRUE""":
                if not data:
                    raise Exception
                id_movie = data["id_movie"]
                list_users = []
                for seenmovie in self.db:
                    if seenmovie["id_movie"] == id_movie and seenmovie["seen"] == True:
                        user = seenmovie["id_user"]
                        list_users.append(user)
                return list_users

def test_get_by_user_and_movie():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    db = seenmovierepo.db_connector.db
    seenmovie: SeenMovie = seenmovierepo.get_by_user_and_movie(1,1)
    assert seenmovie is not None
    assert seenmovie.id_user == 1 and seenmovie.id_movie == 1
    assert seenmovie.__dict__ == db[0]

def test_insert_into_db():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    db = seenmovierepo.db_connector.db
    seenmovie: SeenMovie = seenmovierepo.insert_into_db(1,4,True,0,False)
    assert seenmovie is not None
    assert seenmovie.__dict__ == db[-1]
    assert seenmovie.id_user == 1
    assert seenmovie.id_movie == 4
    assert seenmovie.seen == True
    assert seenmovie.vote == 0
    assert seenmovie.favorite == False

def test_get_list_seenmovies_by_user():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[int] = seenmovierepo.get_list_seenmovies_by_user(2)
    assert movies is not None
    assert movies == [2,1]

def test_get_watchlist_user():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[int] = seenmovierepo.get_watchlist_user(1)
    assert movies is not None
    assert movies == [2,3,4]

def test_get_list_favorite_movie():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[int] = seenmovierepo.get_list_favorite_movie(2)
    assert movies is not None
    assert movies == [2]

def test_get_list_users_by_movie():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    users : list[int] = seenmovierepo.get_list_users_by_movie(2)
    assert users is not None
    assert users == [2,3]