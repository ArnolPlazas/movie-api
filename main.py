from fastapi import FastAPI, Body, Path, Query, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder


from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()
app.title = 'Movies'
app.version = '0.0.1'

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'arnol@mail.com':
            raise HTTPException(status_code=403, detail='Credentials not correct')

class User(BaseModel):
    email: str
    password: str

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

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'arnol@mail.com' and user.password == '1234':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Don't found"})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
        
        


@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movie_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Don't found"})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    movies.append(movie)
    return JSONResponse(status_code=201, content={'message': 'a movie has been added'})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Don't found"})

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'a movie has been modified'})


@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "Don't found"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'a movie has been deleted'})