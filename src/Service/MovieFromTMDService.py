from src.Model.Movie import Movie
from src.Model.Genre import Genre
import requests
import os
import dotenv

class MovieFromTMDService:
    dotenv.load_dotenv()
    movie_db: None
    tmdb_token = os.environ['TMDB_TOKEN']
    header = {
    "accept": "application/json",
    "Authorization": "Bearer "+tmdb_token
    }

    def __init__(self, movie_db: None = None):
        self.movie_db = movie_db
        

    def get_by_id(self, movie_id: int) -> Movie:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        response = requests.get(url,headers=self.header)
        data = response.json()
        return Movie(id = movie_id, original_language = data.get('original_language', None),
                     original_title = data.get('original_title', None),
                     release_date = data.get('release_date', None),
                     title = data.get('title', None),
                     overview = data.get('overview', None))


    def get_by_title(self, title: str):
        payload = {'query': title}
        response = requests.get('https://api.themoviedb.org/3/search/movie?',
        params=payload, headers=self.header)
        data = response.json()
        films = data.get('results', [])
        resultats = []
        for film in films:
            movie = Movie(
                id=film['id'],
                original_language=film.get('original_language',None),
                original_title=film.get('original_title',None),
                release_date=film.get('release_date',None),
                title=film.get('title',None),
                overview=film.get('overview',None)
            )
            resultats.append(movie)
        return resultats
    
    def get_by_release_period(self, start_release_date: str, end_release_date: str):
        payload = {'primary_release_date.gte': start_release_date,
                  'primary_release_date.lte': end_release_date} 
        response = requests.get('https://api.themoviedb.org/3/discover/movie?', 
                                params=payload, headers=self.header)
        data = response.json()
        films = data.get('results', [])
        resultats = []
        for film in films:
            movie = Movie(
                id=film['id'],
                original_language=film.get('original_language', None),
                original_title=film.get('original_title', None),
                release_date=film.get('release_date', None),
                title=film.get('title', None),
                overview=film.get('overview', None)
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
        params=payload, headers=self.header)
        data = response.json()
        films = data.get('results', [])
        resultats = []
        for film in films:
            movie = Movie(
                id=film['id'],
                original_language=film.get('original_language', None),
                original_title=film.get('original_title', None),
                release_date=film.get('release_date', None),
                title=film.get('title', None),
                overview=film.get('overview', None)
            )
            resultats.append(movie)
        return resultats if len(resultats)>0 else None

    def get_id_name_genre(self)-> list[Genre]:
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

        response = requests.get(url, headers=self.headers).json()['genres']

        return [Genre(genre['id'], genre['name']) for genre in response]


