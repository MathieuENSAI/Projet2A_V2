from typing import TYPE_CHECKING, Literal, Optional, Union
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.Model.SeenMovie import SeenMovie

if TYPE_CHECKING:
    from src.Model.SeenMovie import SeenMovie

class MockDBConnector:
    def __init__(self):
        self.db = [{"id_user": 1, "id_movie": 1, "seen": True, "vote": 10, "favorite" : True}, 
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
            
            case "SELECT * from projet_info.User;":
                return self.db
            case "UPDATE projet_info.User SET username = %(username)s, salt = %(salt)s, pass_word = %(pass_word)s WHERE username = %(last_username)s RETURNING *;":
                last_username = data["last_username"]
                for index_user, user in enumerate(self.db):
                    if user['username']==last_username:
                        data.pop("last_username")
                        self.db[index_user] = {'id_user': index_user} | data
                        return self.db[index_user]

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
    seenmovie: SeenMovie = seenmovierepo.insert_into_db(1,4,True,None,False)
    assert seenmovie is not None
    assert seenmovie.__dict__ == db[-1]
    assert seenmovie.id_user == 1
    assert seenmovie.id_movie == 4
    assert seenmovie.seen == True
    assert seenmovie.vote == None
    assert seenmovie.favorite == False

def test_delete_from_db_success():
    seenmovierepo=SeenMovieRepo(db_connector)
    seenmovie = SeenMovie(id_user=1, id_movie=3,seen=True, vote=1, favorite=True)
    assert seenmovierepo.delete_from_db(seenmovie) == True

def test_update_db():
    seenmovierepo=SeenMovieRepo(db_connector)
    seenmovie = SeenMovie(id_user=1, id_movie=3,seen=True, vote=2, favorite=True)
    assert seenmovierepo.update_db(seenmovie) == True

def test_get_list_seenmovies_by_user_none():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_seenmovies_by_user(15) is None

def test_get_list_seenmovies_by_user_success():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_seenmovies_by_user(1) == [1,2,3]

def test_get_watchlist_user_none():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_watchlist_user(15) is None

def test_get_watchlist_user_success():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_watchlist_user(2) == [3]

def test_get_list_favorite_movie_none():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_favorite_movie(15) is None

def test_get_list_favorite_movie_success():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_favorite_movie(3) == [2]

def test_get_list_users_by_movie_none():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_users_by_movie(15) is None

def test_get_list_users_by_movie_success():
    seenmovierepo=SeenMovieRepo(db_connector)
    assert seenmovierepo.get_list_users_by_movie(2) == [1,3]