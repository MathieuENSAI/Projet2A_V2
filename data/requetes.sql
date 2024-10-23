UPDATE projet_info.seenmovies
            SET seen = TRUE, 
                vote = 10,
                favorite = TRUE
            WHERE id_user = 1
            AND id_movie = 3