from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = 'Movies'
app.version = '0.0.1'


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=15, default='movie')
    overview: str = Field(min_length=15, max_length=50, default="movie's desciption")
    year: int = Field(le=2022, default=1900)
    rating: float = Field(ge=1.0, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            'example':{
                'id': 1,
                'title': 'Movie',
                'overview': "movie's desciption",
                'year': 1900,
                'rating': 1.0,
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


@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie] :
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    movie = list(filter(lambda x: x['id'] == id, movies))
    return JSONResponse(content=movie)


@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    movie_by_category = list(filter(lambda x: x['category'] == category, movies))
    return JSONResponse(content=movie_by_category)

@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={'message': 'a movie has been added'})

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
    return JSONResponse(content={'message': 'a movie has been modified'})


@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
    return JSONResponse(content={'message': 'a movie has been deleted'})