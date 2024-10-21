from src.Model.Movie import Movie
import os


class MovieService:
    movie_db: None
    tmdb_token = os.environ["TMDB_TOKEN"]
    header = {
    "accept": "application/json",
    "Authorization": "Bearer "+tmdb_token
    }

    def __init__(self, movie_db: None):
        self.movie_db = movie_db
        

    def get_by_id(self, movie_id: int, language = None) -> Movie:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        params = {
        'language': language
        }
        print(movie_id)
        response = requests.get(url, params=params,headers=header)
        data = response.json()
        print(data)
        return Movie(movie_id, data.get('original_title', 'Not found'))

    def search_id_movie(self, query: str,
                        language = None, primary_release_year = None, 
                        page = None, region = None, year = None) -> list:
        payload = {'query': query,
                    'language': language,
                    'primary_release_year': primary_release_year,
                    'page': page,
                    'region': region,
                    'year': year}
        response = requests.get('https://api.themoviedb.org/3/search/movie?',
        params=payload, headers=header)
        data = response.json()
        films = data.get('results', [])
        resultats = [(film['id'], film['title']) for film in films]
        return resultats