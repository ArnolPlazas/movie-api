from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result

    def get_movie(self, id: int):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result

    def get_movies_by_category(self, category: str):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result

    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict()) # Enviar los parametros para que sean leidas como parametros
        self.db.add(new_movie)
        self.db.commit()
        return

    def update_movie(self, id: int, movie: Movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        self.db.commit()
        return
    
    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return

