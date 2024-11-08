movies = [1]
query = """
        INSERT INTO projet_info.Movie (id, original_language, original_title, release_date, title, overview)
        VALUES %s
        """ 
query += ", %s"*(len(movies)-1) +  "ON CONFLICT (id) DO NOTHING RETURNING id;"
print(query)