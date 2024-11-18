from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class GenreURLChoices(Enum):
    METAL = 'metal'
    ROCK = 'rock'
    COUNTRY = 'country'
    POP = 'pop'
    RNB = 'rnb'
    COMEDY = 'comedy'

BANDS = [
    {'id': 1, 'name': 'Black Sabbath', 'genre': 'Metal'},
    {'id': 2, 'name': 'Led Zeppelin', 'genre': 'Rock'},
    {'id': 3, 'name': 'Dixie Chicks', 'genre': 'Country'},
    {'id': 4, 'name': 'Pink', 'genre': 'Pop'},
    {'id': 5, 'name': 'The Supremes', 'genre': 'R&B'},
    {'id': 6, 'name': 'Bill Engvall', 'genre': 'Comedy'},
]

@app.get('/')
async def index() -> dict[str,str]:
    return {'hello':'world  '}

@app.get('about')
async def about() -> str:
    return 'About'
 
@app.get('/bands')
async def get_bands() -> list[dict]:
    return BANDS

@app.get('/bands/{band_id}')
async def get_band(band_id: int) -> dict:
    band = next((band for band in BANDS if band['id'] == band_id), None)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def get_band_by_genre(genre: GenreURLChoices) -> list[dict]:
    bands = [band for band in BANDS if band['genre'].lower() == genre.value]
    return bands