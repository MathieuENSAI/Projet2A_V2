from pydantic import BaseModel


class Genre(BaseModel):
    id_genre : int
    name_genre: str

    def info(self):
        info = f"""
        id_genre: {self.id}
        name_genre: {self.name_genre}
        """

        return info
