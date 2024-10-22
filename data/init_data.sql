-- INITIALISER LA TABLE Utilisateur --
INSERT INTO projet_info.User(username, pass_word)
VALUES
('admin', 'admin48'),
('projetInfo', '48'),
('ensai', 'ensai48'),
('eleve', 'eleve48');

-- INTIALISER LA TABLE UserFolowers
INSERT INTO projet_info.UserFollowers(id_user, id_follower)
VALUES (1, 2), (1, 3), (1,4), (2, 1), (2, 4), (3, 2), (3, 4);

-- INITIALISER LA TABLE SeenMovie
INSERT INTO projet_info.SeenMovie(id_user, id_movie, seen, vote, favorite)
VALUES
(1, 1, TRUE, 8, TRUE),
(1, 2, TRUE, 3, FALSE),
(2, 3, FALSE, NONE, FALSE),
(3, 2, TRUE, 9, TRUE);