from src.Model.Movie import Movie
from src.Model.Genre import Genre
import requests
import os


class MovieFromTMDService:
    movie_db: None
    tmdb_token = os.environ["TMDB_TOKEN"]
    header = {
    "accept": "application/json",
    "Authorization": "Bearer "+tmdb_token
    }

    def __init__(self, movie_db: None):
        self.movie_db = movie_db
        

    def get_by_id(self, movie_id: int) -> Movie:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        print(movie_id)
        response = requests.get(url,headers=header)
        data = response.json()
        print(data)
        return Movie(id = movie_id, original_language = data.get('original_language', 'Not found'),
                      original_title = data.get('original_title', 'Not found'),
                      release_date = data.get('original_title', 'Not found'),
                      title = data.get('title', 'Not found'),
                      overview = data.get('overview', 'Not found'),
                      vote_average = None, vote_count = None)

    def get_by_title(self, title: str):
        payload = {'query': title}
        response = requests.get('https://api.themoviedb.org/3/search/movie?',
        params=payload, headers=header)
        data = response.json()
        films = data.get('results', [])
        resultats = []
        for film in films:
            movie = Movie(
                id=film['id'],
                original_language=film.get('original_language','Not found'),
                original_title=film.get('original_title','Not found'),
                release_date=film.get('release_date','Not found'),
                title=film.get('title','Not found'),
                overview=film.get('overview','Not found'),
                vote_average=None,
                vote_count=None,
            )
            resultats.append(movie)
        return resultats
    
    def get_by_release_date(self, release_date: str):
        payload = {'release_date.gte': release_date} 
        response = requests.get('https://api.themoviedb.org/3/discover/movie?', 
                                params=payload, headers=header)
        data = response.json()
        films = data.get('results', [])
        resultats = []
        for film in films:
            movie = Movie(
                id=film['id'],
                original_language=film.get('original_language', 'Not found'),
                original_title=film.get('original_title', 'Not found'),
                release_date=film.get('release_date', 'Not found'),
                title=film.get('title', 'Not found'),
                overview=film.get('overview', 'Not found'),
                vote_average=None, 
                vote_count=None,
            )
            resultats.append(movie)
        return resultats

    def search_movie(self, query: str,
                        language = None, primary_release_year = None, 
                        page = None, region = None, year = None) -> list:
        payload = {'query': query,
                    'language': language,
                    'primary_release_year': primary_release_year,
                    'region': region,
                    'year': year}
        response = requests.get('https://api.themoviedb.org/3/search/movie?',
        params=payload, headers=header)
        data = response.json()
        films = data.get('results', [])
        resultats = []
        for film in films:
            movie = Movie(
                id=film['id'],
                original_language=film.get('original_language','Not found'),
                original_title=film.get('original_title','Not found'),
                release_date=film.get('release_date','Not found'),
                title=film.get('title','Not found'),
                overview=film.get('overview','Not found'),
                vote_average=None,
                vote_count=None,
            )
            resultats.append(movie)
        return resultats
    
    def get_id_name_genre(self)-> list[Genre]:
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

        response = requests.get(url, headers=headers).json()['genres']

    

        print(response.json()['genres'][0]['id'])

