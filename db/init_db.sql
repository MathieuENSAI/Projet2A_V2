DROP SCHEMA IF EXISTS projet_info CASCADE;
CREATE SCHEMA projet_info;

--------------------------------------------------------------
-- Utilisateurs
--------------------------------------------------------------

CREATE TABLE projet_info.User (
    id_user serial PRIMARY KEY,
    username VARCHAR(32) NOT NULL UNIQUE,
    pass_word VARCHAR(256) NOT NULL,
    salt VARCHAR(256),
    connected BOOLEAN DEFAULT FALSE
);

CREATE TABLE projet_info.Movie(
    id INT PRIMARY KEY,
    original_language CHAR(16),
    original_title CHAR(256),
    release_date DATE,
    title CHAR(256),
    vote_average FLOAT,
    vote_count INT DEFAULT 0, 
    overview CHAR(1024)
);


CREATE TABLE projet_info.SeenMovies (
    id_user INT NOT NULL,
    id_movie INT NOT NULL,
    seen BOOLEAN DEFAULT TRUE,
    to_watch_later BOOLEAN DEFAULT FALSE,
    vote INT,
    favorite BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id_user,id_movie),
    FOREIGN KEY(id_user) REFERENCES projet_info.User(id_user) ON DELETE CASCADE,
    FOREIGN KEY(id_movie) REFERENCES projet_info.Movie(id) ON DELETE CASCADE
);


CREATE TABLE projet_info.UserFollowing (
    id_user INT NOT NULL,
    id_following INT NOT NULL,
    PRIMARY KEY(id_user, id_following),
    FOREIGN KEY (id_user) REFERENCES projet_info.User(id_user) ON DELETE CASCADE,
    FOREIGN KEY (id_following) REFERENCES projet_info.User(id_user) ON DELETE CASCADE
);


CREATE TABLE projet_info.Genre(
    id_genre INT PRIMARY KEY,
    name_genre CHAR(32)
);


CREATE TABLE projet_info.MovieGenre(
    id_movie INT,
    id_genre INT,
    PRIMARY KEY(id_movie, id_genre),
    FOREIGN KEY (id_movie) REFERENCES projet_info.Movie(id) ON DELETE SET NULL,
    FOREIGN KEY (id_genre) REFERENCES projet_info.Genre(id_genre) ON DELETE CASCADE
);
