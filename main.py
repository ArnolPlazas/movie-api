from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = 'Movies'
app.version = '0.0.1'


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=15, default='movie')
    overview: str = Field(min_length=15, max_length=50, default="movie's desciption")
    year: int = Field(le=2022, default=1900)
    rating: float
    category: str

    class Config:
        schema_extra = {
            'example':{
                'id': 1,
                'title': 'Movie',
                'overview': "movie's desciption",
                'year': 1900,
                'rating': 0.0,
                'category': 'Comedy'
            }
        }

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": 2009,
		"rating": 7.8,
		"category": "Acción"
	},
        {
		"id": 2,
		"title": "Avatar 2",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": 2022,
		"rating": 7.1,
		"category": "Acción"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1> Hello world</h1>')


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    movie = list(filter(lambda x: x['id'] == id, movies))
    return movie


@app.get('/movies/', tags=['movies'])
def get_movie_by_category(category: str, year: int):
    movie = list(filter(lambda x: x['category'] == category and x['year'] == year, movies))
    return movie

@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)

    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return movies


@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    return movies