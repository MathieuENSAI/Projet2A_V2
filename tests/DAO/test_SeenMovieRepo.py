from typing import TYPE_CHECKING, Literal, Optional, Union
from src.DAO.SeenMovieRepo import SeenMovieRepo
from src.Model.SeenMovie import SeenMovie
from src.Model.Movie import Movie 
from src.Model.APIUser import APIUser

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
            "vote": 8,
            "favorite": True,
            "username": "", 
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
            "vote": 6,
            "favorite": False,
            "username": "",
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
            "vote": None,
            "favorite": False,
            "username": "",
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
            "vote": 7,
            "favorite": True,
            "username": "",
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
            "vote": None,
            "favorite": False,
            "username": "",
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
            "vote": 9,
            "favorite": True,
            "username": "",
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
            "vote": 5,
            "favorite": False,
            "username": "",
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
            "vote": None,
            "favorite": False,
            "username": "",
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
            "vote": 10,
            "favorite": True,
            "username": "",
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
            "vote": None,
            "favorite": False,
            "username": "",
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
            "vote": 6,
            "favorite": False,
            "username": "",
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
            "vote": 8,
            "favorite": True,
            "username": "",
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
            "vote": None,
            "favorite": False,
            "username": "",
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
                
            case """INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, to_watch_later, vote, favorite)
                VALUES (%(id_user)s, %(id_movie)s, %(seen)s, %(to_watch_later)s, %(vote)s, %(favorite)s)
                ON CONFLICT(id_user, id_movie) DO UPDATE
                SET seen = EXCLUDED.seen,
                    to_watch_later = EXCLUDED.to_watch_later,
                    vote = EXCLUDED.vote,
                    favorite = EXCLUDED.favorite
                RETURNING *;""":
                if not data:
                    raise Exception
                self.db.append({"id_user": data['id_user'], "id_movie" : data['id_movie'], 
                                "seen": data['seen'], "to_watch_later": data['to_watch_later']
                                ,"vote": data['vote'], "favorite": data['favorite']})
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
                        movie = dict(id = seenmovie["id_movie"])
                        list_seenmovies.append(movie)
                if list_seenmovies != []: 
                    return list_seenmovies
                return None

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
                        movie = dict(id = seenmovie["id_movie"])
                        list_seenmovies.append(movie)
                if list_seenmovies != []: 
                    return list_seenmovies
                return None
            
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
                        movie = dict(id = seenmovie["id_movie"])
                        list_seenmovies.append(movie)
                if list_seenmovies != []: 
                    return list_seenmovies
                return None
            
            case """UPDATE projet_info.seenmovies
            SET seen = %(seen)s, 
                to_watch_later = %(to_watch_later)s,
                vote = %(vote)s,
                favorite = %(favorite)s
            WHERE id_user = %(id_user)s
            AND id_movie = %(id_movie)s;""":
                if not data:
                    raise Exception
                id_user = data["id_user"]
                id_movie = data["id_movie"]
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["id_movie"] == id_movie:
                        seenmovie["favorite"] = data["favorite"]
                        seenmovie["seen"] = data["seen"]
                        seenmovie["to_watch_later"] = data["to_watch_later"]
                        seenmovie["vote"] = data["vote"]
                        return True
                return False
                
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
                        user = dict(id_user = seenmovie["id_user"],
                                    username = seenmovie["username"])
                        list_users.append(user)
                if list_users != []: 
                    return list_users
                return None
            
            case """UPDATE projet_info.seenmovies
           SET favorite = FALSE
           WHERE id_user = %(id_user)s AND id_movie = %(id_movie)s;""":
                if not data:
                    raise Exception
                id_user = data["id_user"]
                id_movie = data["id_movie"]
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["id_movie"] == id_movie:
                        seenmovie["favorite"] = False
                        return True
                return False
            
            case """UPDATE projet_info.seenmovies
           SET to_watch_later = FALSE
           WHERE id_user = %(id_user)s AND id_movie = %(id_movie)s;""":
                if not data:
                    raise Exception
                id_user = data["id_user"]
                id_movie = data["id_movie"]
                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["id_movie"] == id_movie:
                        seenmovie["to_watch_later"] = False
                        return True
                return False
                    
            case """
            INSERT INTO projet_info.seenmovies (id_user, id_movie, seen, favorite, vote, to_watch_later)
            VALUES (%(id_user)s, %(id_movie)s, TRUE, FALSE, %(vote)s, FALSE)
            ON CONFLICT (id_movie, id_user)
            DO UPDATE SET vote = EXCLUDED.vote, seen=TRUE;
            SELECT AVG(vote) AS vote_avg, COUNT(vote) AS vote_count 
            FROM projet_info.seenmovies
            WHERE id_movie = %(id_movie)s;""" :
                id_user = data["id_user"]
                id_movie = data["id_movie"]
                vote = data["vote"]

                note_sum = 0
                nb_film = 0
                movie_found = False 

                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["id_movie"] == id_movie:
                        seenmovie["vote"] = vote
                        seenmovie["seen"] = True
                        movie_found = True
                    if seenmovie["id_movie"] == id_movie and seenmovie["vote"] is not None:
                        note_sum += seenmovie["vote"]
                        nb_film += 1

                if not movie_found:
                    self.db.append({"id_user": id_user, "id_movie": id_movie, "seen": True, "vote": vote, "favorite": False, "to_watch_later":False})
                    note_sum += vote
                    nb_film += 1

                if nb_film > 0:
                    return dict(vote_avg = note_sum / nb_film, vote_count = nb_film)
                else:
                    return None
                
            case """
        UPDATE projet_info.SeenMovies
        SET vote=NULL
        WHERE id_user=%(id_user)s AND id_movie=%(id_movie)s;
        SELECT AVG(vote) AS vote_avg, COUNT(vote) AS vote_count 
            FROM projet_info.seenmovies
            WHERE id_movie = %(id_movie)s;
        """:
                id_user = data["id_user"]
                id_movie = data["id_movie"]
                note_sum = 0
                nb_film = 0

                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["id_movie"] == id_movie:
                        seenmovie["vote"] = None
                    elif seenmovie["id_movie"] == id_movie and seenmovie["vote"] is not None:
                        note_sum += seenmovie["vote"]
                        nb_film += 1

                if nb_film > 0:
                    return dict(vote_avg = note_sum / nb_film, vote_count = nb_film)
                else:
                    return None
            case """
        SELECT AVG(vote) AS vote_avg FROM projet_info.seenmovies
        WHERE id_user=%(id_user)s;
        """:
                id_user = data["id_user"]
                note_sum = 0
                nb_film = 0

                for seenmovie in self.db:
                    if seenmovie["id_user"] == id_user and seenmovie["vote"] is not None:
                        note_sum += seenmovie["vote"]
                        nb_film += 1

                if nb_film > 0:
                    return dict(vote_avg = note_sum/nb_film)
                else:
                    return None
            case """
        SELECT M.*, COUNT(CASE WHEN SM.favorite=TRUE THEN 1 END) AS total_liked
        FROM projet_info.Movie M
        JOIN projet_info.SeenMovies SM ON M.id=SM.id_movie
        WHERE NOT EXISTS (
            SELECT 1
            FROM projet_info.SeenMovies SM2
            WHERE SM2.id_user = %(id_user)s
            AND SM2.id_movie = M.id
        )
        GROUP BY M.id
        HAVING COUNT(CASE WHEN SM.favorite = TRUE THEN 1 END) > 0
        ORDER BY total_liked DESC, vote_average DESC NULLS LAST LIMIT %(top)s;
        """:
                id_user = data["id_user"]
                top = data["top"]

                grouped_likes = {}
                for seenmovie in self.db:
                    if seenmovie["id_user"] != id_user and seenmovie["favorite"]:
                        movie_id = seenmovie["id_movie"]
                        grouped_likes[movie_id] = grouped_likes.get(movie_id, 0) + 1

                sorted_movies = sorted(grouped_likes.items(), key=lambda x: x[1], reverse=True)

                top_movies = sorted_movies[:top]

                result = []
                for movie_id, likes in top_movies:
                    movie_details = next((movie for movie in self.db if movie["id_movie"] == movie_id), None)
                    if movie_details:
                        result.append({
                            "movie": Movie(id=movie_details["id_movie"], **movie_details),
                            "total_liked": likes
                        })
                return result
                    

def test_get_by_user_and_movie_found():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovie: SeenMovie = seenmovierepo.get_by_user_and_movie(3,1)
    assert seenmovie is not None
    assert seenmovie.id_user == 3 and seenmovie.id_movie == 1
    assert seenmovie.seen is True
    assert seenmovie.vote == 8

def test_get_by_user_and_movie_none():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovie: SeenMovie = seenmovierepo.get_by_user_and_movie(43,1)
    assert seenmovie is None

def test_insert_into_db():
    seenmovierepo = SeenMovieRepo(MockDBConnector())
    seenmovie: SeenMovie = seenmovierepo.insert_into_db(
        id_user=1, 
        id_movie=4, 
        seen=True,  
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
    assert seenmovie.favorite is False

def test_get_movies_seen_by_user_found():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_movies_seen_by_user(4)
    assert movies is not None
    assert movies[0] == Movie(id=3)
    assert movies[1] == Movie(id=2)
    assert movies[2] == Movie(id=1)

def test_get_movies_seen_by_user_None():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_movies_seen_by_user(2)
    assert movies is None
    
def test_get_watchlist_user_found():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_watchlist_movie(1)
    assert movies is not None
    assert movies[0] == Movie(id=5)
    assert movies[1] == Movie(id=6)

def test_get_watchlist_user_None():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_watchlist_movie(3)
    assert movies is None


def test_get_user_favorites_movie_found():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_user_favorites_movie(4)
    assert movies is not None
    assert movies[0] == Movie(id=1)

def test_get_user_favorites_movie_none():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    movies: list[Movie] = seenmovierepo.get_user_favorites_movie(1)
    assert movies is None

def test_get_users_who_watch_movie_found():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    users : list[APIUser] = seenmovierepo.get_users_who_watch_movie(1)
    assert users is not None
    assert users[0] == APIUser(id_user=3, username="")
    assert users[1] == APIUser(id_user=5, username="")
    assert users[2] == APIUser(id_user=4, username="")

def test_get_users_who_watch_movie_none():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    users : list[APIUser] = seenmovierepo.get_users_who_watch_movie(10)
    assert users is None


def test_update_db_sucess():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovie = SeenMovie(id_user=3,
            id_movie= 1,
            seen=True,
            to_watch_later=True,
            vote=6,
            favorite=False)
    update : bool = seenmovierepo.update_db(seenmovie=seenmovie)
    assert update is True
    assert seenmovierepo.get_by_user_and_movie(id_user=3,id_movie=1) == seenmovie

def test_update_db_fail():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    seenmovie = SeenMovie(id_user=3,
            id_movie= 2,
            seen=True,
            to_watch_later=True,
            vote=6,
            favorite=False)
    update : bool = seenmovierepo.update_db(seenmovie=seenmovie)
    assert update is False
    assert seenmovierepo.get_by_user_and_movie(id_user=3,id_movie=2) is None

def test_remove_from_user_favorites_success():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    removed : int = seenmovierepo.remove_from_user_favorites(id_user=5,id_movie=1)
    assert removed is True
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=1).favorite is False

def test_remove_from_user_favorites_fail():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    removed : int = seenmovierepo.remove_from_user_favorites(id_user=5,id_movie=5)
    assert removed is False
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=5) is None

def test_remove_from_user_watchlist_success():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    removed : int = seenmovierepo.remove_from_user_watchlist(id_user=1,id_movie=6)
    assert removed is True
    assert seenmovierepo.get_by_user_and_movie(id_user=1,id_movie=6).to_watch_later is False

def test_remove_from_user_watchlist_fail():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    removed : int = seenmovierepo.remove_from_user_watchlist(id_user=5,id_movie=5)
    assert removed is False
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=5) is None

def test_note_movie_new_note():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    note : dict = seenmovierepo.note_movie(id_user=5,id_movie=5, note=7)
    assert note is not None
    assert note["vote_avg"] == 8
    assert note["vote_count"] == 2
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=5).vote == 7
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=5).seen is True
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=5).favorite is False

def test_note_movie_modified_note():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    note : dict = seenmovierepo.note_movie(id_user=5,id_movie=2, note=5)
    assert note is not None
    assert note["vote_avg"] == 5
    assert note["vote_count"] == 2
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=2).vote == 5
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=2).seen is True

def test_remove_note_movie_still_noted():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    note : dict = seenmovierepo.remove_note_movie(id_user=5,id_movie=1)
    assert note is not None
    assert note["vote_avg"] == 8
    assert note["vote_count"] == 2
    assert seenmovierepo.get_by_user_and_movie(id_user=5,id_movie=1).vote is None

def test_remove_note_movie_no_more_note():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    note : dict = seenmovierepo.remove_note_movie(id_user=4,id_movie=3)
    assert note is None
    assert seenmovierepo.get_by_user_and_movie(id_user=4,id_movie=3).vote is None

def test_mean_note_user_result():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    note : dict = seenmovierepo.mean_note_user(id_user=3)
    assert note == 23/3
    

def test_mean_note_user_None():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    note : dict = seenmovierepo.mean_note_user(id_user=2)
    assert note is None 

def test_movies_liked_by_others_users():
    seenmovierepo=SeenMovieRepo(MockDBConnector())
    liked_movies : dict = seenmovierepo.get_top_movies_liked_by_others_users(15,4)
    assert len(liked_movies) == 3
    assert liked_movies[0]["total_liked"] == 3
    assert liked_movies[0]["movie"] == Movie(id=1)
    assert liked_movies[1]["total_liked"] == 1