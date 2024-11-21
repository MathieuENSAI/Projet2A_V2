from src.Model.Movie import Movie
from src.Model.Genre import Genre
import requests
import os
import dotenv

class MovieFromTMDService:
    dotenv.load_dotenv()
    tmdb_token = os.environ['TMDB_TOKEN']
    header = {
    "accept": "application/json",
    "Authorization": "Bearer "+tmdb_token
    }

    def build_movie(self, data:dict) -> Movie:
        return {'movie': Movie(id = data['id'], original_language = data.get('original_language', None),
                     original_title = data.get('original_title', None),
                     release_date = data.get('release_date', None),
                     title = data.get('title', None),
                     overview = data.get('overview', None)),
                'movie_genre' : {'id_movie': data['id'], 'genres':data.get('genre_ids', data.get('genres', []))}
        }

    def get_by_params(self, payload:dict, url='https://api.themoviedb.org/3/discover/movie?'):
        response = requests.get(url,
        params=payload, headers=self.header)
        data = response.json()
        films = data.get('results', [])
        return [self.build_movie(film) for film in films] if len(films)>0 else []

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
        films = response.json()['results']
        return [self.build_movie(film) for film in films] if len(films)>0 else []

    def get_by_id(self, movie_id: int) -> Movie:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        film = requests.get(url,headers=self.header).json()
        return self.build_movie(film) if film.get('id', None) else None

    def get_by_release_period(self, start_release_date: str, end_release_date: str):
        payload = {'primary_release_date.gte': start_release_date,
                  'primary_release_date.lte': end_release_date} 
        return self.get_by_params(payload)

    def get_lastest_released(self, number:int)-> list[Movie]:
        payload = {"sort_by" : "primary_release_date.desc"}
        return self.get_by_params(payload)[:number]
        
    def get_id_name_genre(self)-> list[Genre]:
        url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
        response = requests.get(url, headers=self.header).json()['genres']
        return [Genre(id_genre = genre['id'], name_genre=genre['name']) for genre in response] if response else []


if __name__ == "__main__" :
   
    movie_TMDB = MovieFromTMDService()

    
       