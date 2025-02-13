import os
import logging
import dotenv

from unittest import mock

from utils.log_decorator import log
from utils.singleton import Singleton
from dao.db_connection import DBConnection

from service.utilisateur_service import UtilisateurService


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    @log
    def lancer(self, pg_schema: str = "projet_info"):
        """Lancement de la réinitialisation des données"""
  
        mock.patch.dict(os.environ, {"POSTGRES_SCHEMA": pg_schema}).start()

        dotenv.load_dotenv()

        pg_schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = f"DROP SCHEMA IF EXISTS {pg_schema} CASCADE; CREATE SCHEMA {pg_schema};"

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()
        init_db.close()

        init_data = open("data/init_data.sql", encoding="utf-8")
        init_data_as_string = init_data.read()
        init_data.close()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
                    cursor.execute(init_data_as_string)
        except Exception as e:
            logging.info(e)
            raise

        # Appliquer le hashage des mots de passe à chaque utilisateur
        # utilisateur_service = UtilisateurService()
        # for j in utilisateur_service.lister_tous(inclure_mdp=True):
        #     utilisateur_service.modifier(j)

        return True


if __name__ == "__main__":

    ResetDatabase().lancer()
