DROP SCHEMA IF EXISTS projet_info CASCADE;
CREATE SCHEMA projet_info;

--------------------------------------------------------------
-- Utilisateurs
--------------------------------------------------------------

DROP TABLE IF EXISTS projet_info.User CASCADE ;
CREATE TABLE projet_info.User (
    id_user serial PRIMARY KEY,
    username VARCHAR(32) NOT NULL UNIQUE,
    pass_word VARCHAR(256) NOT NULL
);

DROP TABLE IF EXISTS projet_info.Movie CASCADE;
CREATE TABLE projet_info.Movie(
    id INT PRIMARY KEY,
    original_language CHAR(16),
    original_title CHAR(128),
    release_date DATE,
    title CHAR(128),
    vote_average FLOAT,
    vote_count INT, 
    overview CHAR(256)
);

DROP TABLE IF EXISTS projet_info.SeenMovies CASCADE ; 
CREATE TABLE projet_info.SeenMovies (
    id_seenmovie SERIAL PRIMARY KEY,
    id_user INT NOT NULL,
    id_movie INT NOT NULL,
    seen BOOLEAN,
    vote INT,
    favorite BOOLEAN,
    FOREIGN KEY(id_user) REFERENCES projet_info.User(id_user) ON DELETE SET NULL,
    FOREIGN KEY(id_movie) REFERENCES projet_info.Movie(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS projet_info.UserFollowers CASCADE ;
CREATE TABLE projet_info.UserFollowers (
    id_user INT NOT NULL,
    id_follower INT NOT NULL,
    PRIMARY KEY(id_user, id_follower),
    FOREIGN KEY (id_user) REFERENCES projet_info.User(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_follower) REFERENCES projet_info.User(id_user) ON DELETE CASCADE
);

DROP TABLE IF EXISTS projet_info.Genre CASCADE;
CREATE TABLE projet_info.Genre(
    id_genre INT PRIMARY KEY,
    name_genre CHAR(32)
);

DROP TABLE IF EXISTS projet_info.MovieGenre CASCADE;
CREATE TABLE projet_info.MovieGenre(
    id_movie INT,
    id_genre INT,
    FOREIGN KEY (id_movie) REFERENCES projet_info.Movie(id) ON DELETE SET NULL,
    FOREIGN KEY (id_genre) REFERENCES projet_info.Genre(id_genre) ON DELETE CASCADE
);