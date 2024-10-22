DROP SCHEMA IF EXISTS projet_info CASCADE;
CREATE SCHEMA projet_info;

--------------------------------------------------------------
-- Utilisateurs
--------------------------------------------------------------

DROP TABLE IF EXISTS projet_info.utilisateur CASCADE ;
CREATE TABLE projet_info.user (
    id_user serial PRIMARY KEY,
    username VARCHAR(30) UNIQUE,
    password VARCHAR(250)
);

DROP TABLE IF EXISTS projet_info.seenmovies CASCADE ; 
CREATE TABLE projet_info.seenmovies (
    id_seenmovie serial PRIMARY KEY,
    id_user INT,
    id_movie INT,
    seen BOOLEAN,
    note INT,
    favorite BOOLEAN
)

DROP TABLE IF EXISTS projet_info.Movie CASCADE;
CREATE TABLE projet_info.Movie(
    movie_id SERIAL PRIMARY KEY,
    original_title CHAR(128),
    date_sortie DATETIME,
    realisateur CHAR(64),
    langue_vo CHAR(32),
    genre CHAR(32),
    resume CHAR(256)
);
