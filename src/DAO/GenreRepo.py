from src.DAO.DBConnector import DBConnector
from src.Model.Genre import Genre

class  GenreRepo:
    db_connector : DBConnector

    def __init__(self, db_connector: DBConnector):

        self.db_connector = db_connector

    def insert_into_db(self, genres:list[dict]):
        query = """
        INSERT INTO projet_info.Genre (id_genre, name_genre)
        VALUES %s
        """ 
        query += ", %s"*(len(genres)-1) +  " ON CONFLICT (id_genre) DO NOTHING RETURNING id_genre;"
        # Préparer les valeurs pour l'insertion
        values = [(genre['id_genre'], genre['name_genre']) for genre in genres]
        raw_created = self.db_connector.sql_query(query, values, "none")

        return True if raw_created else False
    
    def get_by_id(self, id_genre:int):

        query = "SELECT * From projet_info.Genre WHERE id_genre=%s;"
        raw_selected = self.db_connector.sql_query(query, [id_genre], "one")

        return Genre(**raw_selected) if raw_selected else None
    
    def get_by_name_genre(self, name_genre:str):
        query = "SELECT * FROM projet_info.Genre WHERE name_genre=%s;"
        raw_selected = self.db_connector.sql_query(query, [name_genre], "one")

        return Genre(**raw_selected) if raw_selected else None
    
        

if __name__ == "__main__" :
    import dotenv
    dotenv.load_dotenv()
    db_connector = DBConnector()
    genre_repo = GenreRepo(db_connector)
    print(genre_repo.get_by_name_genre("romance"))