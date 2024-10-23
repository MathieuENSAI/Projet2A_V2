import logging
from utils.log_decorator import log
from business_objet.utilisateur import Utilisateur
from dao.db_connection import DBConnection

class UtilisateurDao:
    """Classe contenant les méthodes pour accéder CRUD pour la table Utilisateur de la base de données"""
     
    @log
    def creer(self, utilisateur:Utilisateur):
        """Creation d'un utilisateur dans la base de données


        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        " INSERT INTO Utilisateur (pseudo, mdp) "
                        " VALUES (%(pseudo)s, %(mdp)s)          "
                        " RETURNING id_utilisateur ;            ",
                        {"pseudo": utilisateur.pseudo,
                            "mdp": utilisateur.mdp},         
                        )
                    res = cursor.fetchone()
        except Exception as error:
            logging.error(error)
            
        created = False
        if res :
            utilisateur.id_utilisateur = res["id_utilisateur"]
            created = True
        return created
    
    @log
    def se_connecter(self, utilisateur:Utilisateur):
        """Connexion d'un utilisateur


        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        connected : bool
            True si la connexion est un succès
            False sinon
        """
        res = None
        try:
            with DBConnection().connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                    "SELECT * FROM Utilisateur                           "
                    "WHERE pseudo = %(pseudo)s AND mdp = %(mdp)s;        ",
                    {"pseudo": utilisateur.pseudo, "mdp": utilisateur.mdp}
                    )
                    res = cursor.fetchone()
        except Exception as error:
            logging(error)
        connected = False
        if res :
            utilisateur.id_utilisateur = res["id_utilisateur"]
            connected = True
        return connected

    @log
    def trouver_par_pseudo(self, pseudo:str):
        res = None
        try :
            with DBConnection().connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                    "SELECT * FROM Utilisateur       "
                    "WHERE Pseudo = %(pseudo)s;      ",
                    {"pseudo":pseudo}
                    )
                    res = cursor.fetchone()
        except Exception as error:
            logging(error)
        if res:
            utilisateur = Utilisateur(res["pseudo"], res["mdp"])
            utilisateur.id_utilisateur = res["id_utilisateur"]
            return utilisateur
        else :
            return None
    
    @log
    def lister_tous(self):  
        res = None
        try :
            with DBConnection().connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                    "SELECT * FROM Utilisateur;"
                    )
                    res = cursor.fetchall()
        except Exception as error :
            logging(error)
        tous_utilisateurs = []
        if res:
            for user in res:
                utilisateur = Utilisateur(user["pseudo"], user["mdp"])
                utilisateur.id_utilisateur = user["id_utilisateur"]
                tous_utilisateurs.append(utilisateur)
        return tous_utilisateurs
        

        

# if __name__ == "__main__":

#     user = Utilisateur(pseudo="test", mdp="test")

#     UtilisateurDao().creer(user)
