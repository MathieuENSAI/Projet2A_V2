--INITIALISER LA TABLE Utilisateur --
INSERT INTO projet_info.User(username, pass_word)
VALUES
('admin', 'admin48'),
('projetInfo', '48'),
('ensai', 'ensai48'),
('eleve', 'eleve48');

-- INTIALISER LA TABLE UserFolowers
INSERT INTO projet_info.UserFollowers(id_user, id_follower)
VALUES (1, 2), (1, 3), (1,4), (2, 1), (2, 4), (3, 2), (3, 4);

--INSERER les données dans la table Movie
INSERT INTO projet_info.Movie(id, original_language, original_title, release_date, title)
VALUES
(1, 'en', 'Retour mortel de showley', '2024-05-12', 'Retour mortel de showley'),
(2, 'fr', 'Nindja Blanc', '2023-05-05', 'Nindja Blanc'),
(3, 'en', 'Legend of Tomorow', '2022-11-05', 'Legend of Tomorow');

-- -- INITIALISER LA TABLE SeenMovie
INSERT INTO projet_info.SeenMovies(id_user, id_movie, seen, to_watch_later, watch_count, vote, favorite)
VALUES
(1, 1, TRUE, FALSE, 1, 8, TRUE),
(1, 2, TRUE, FALSE, 1, 3, FALSE),
(2, 3, FALSE, TRUE, 0, NULL, FALSE),
(3, 2, TRUE, FALSE, 1, 9, TRUE);

-- INSERER Les données dans la table Genre
INSERT INTO projet_info.Genre(id_genre, name_genre)
VALUES (1, 'action'), (2, 'romance'), (3, 'guerre'), (4, 'comedi');

-- INSER les données dans la table MovieGenre
INSERT INTO projet_info.MovieGenre(id_movie, id_genre)
VALUES (1, 1), (1, 3), (2, 2), (3, 1), (3, 3);
