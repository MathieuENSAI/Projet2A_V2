DROP SCHEMA IF EXISTS projet_info CASCADE;
CREATE SCHEMA projet_info;

--------------------------------------------------------------
-- Utilisateurs
--------------------------------------------------------------

DROP TABLE IF EXISTS projet_info.utilisateur CASCADE ;
CREATE TABLE projet_info.User (
    id_user serial PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    password VARCHAR(250)
);

DROP TABLE IF EXISTS projet_info.Movie CASCADE;
CREATE TABLE projet_info.Movie(
    id INT PRIMARY KEY,
    original_language CHAR(16),
    original_title CHAR(128),
    release_date DATE,
    titre CHAR(128),
    vote_average FLOAT,
    vote_count INT
);

DROP TABLE IF EXISTS projet_info.SeenMovies CASCADE ; 
CREATE TABLE projet_info.seenmovies (
    id_seenmovie SERIAL PRIMARY KEY,
    id_user INT,
    id_movie INT,
    seen BOOLEAN,
    vote INT,
    favorite BOOLEAN,
    FOREIGN KEY (id_user) REFERENCES User(id),
    FOREIGN KEY (id_movie) REFERENCES Movie(id)
)