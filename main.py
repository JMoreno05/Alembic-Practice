from fastapi import FastAPI, HTTPException, Path, Query
from models import BandBase, BandCreate, BandWithID, GenreURLChoices
from typing import Annotated

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
        {'title': 'Black Sabbath', 'release_date': '1970-02-13'},
        {'title': 'Paranoid', 'release_date': '1970-09-18'},]},
    {'id': 2, 'name': 'Led Zeppelin', 'genre': 'Rock', 'albums': [
        {'title': 'Led Zeppelin', 'release_date': '1969-01-12'},
        {'title': 'Led Zeppelin II', 'release_date': '1969-10-22'},]},
    {'id': 3, 'name': 'Dixie Chicks', 'genre': 'Country', 'albums': [
        {'title': 'Wide Open Spaces', 'release_date': '1998-01-27'},
        {'title': 'Fly', 'release_date': '1999-08-31'},]},
    {'id': 4, 'name': 'Pink', 'genre': 'Pop', 'albums': [
        {'title': 'Can\'t Take Me Home', 'release_date': '2000-04-04'},
        {'title': 'Missundaztood', 'release_date': '2001-11-20'},]},
    {'id': 5, 'name': 'The Supremes', 'genre': 'RnB', 'albums': [
        {'title': 'Meet The Supremes', 'release_date': '1962-12-12'},
        {'title': 'Where Did Our Love Go', 'release_date': '1964-08-31'},]},
    {'id': 6, 'name': 'Bill Engvall', 'genre': 'Comedy', 'albums': [
        {'title': 'Here\'s Your Sign', 'release_date': '1996-06-04'},
        {'title': 'Dorkfish', 'release_date': '1998-10-06'},]},
]

@app.get('/bands')
async def get_bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None , Query(max_length=10)] = None
    #has_albums: bool = False
    ) -> list[BandWithID]:
    #if using query parameters, allow for no parameters by allowing None
    # not in url or empty in url
    band_list = [BandWithID(**kwargs) for kwargs in BANDS]
    
    if genre:
        band_list =  [b for b in band_list if b.genre.value.lower() == genre.value]
    """ if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0] """
    
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()#ab
        ]

    return band_list
    

@app.get('/bands/{band_id}')
async def get_band(band_id: Annotated[int, Path(title='The band ID')]) -> BandWithID:
    band = next((BandWithID(**band) for band in BANDS if band['id'] == band_id), None)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def get_band_by_genre(genre: GenreURLChoices) -> list[BandWithID]:
    bands = [BandWithID(**band) for band in BANDS if band['genre'].value.lower() == genre.value]
    return bands

@app.post('/bands')
async def create_band(band_data:BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] +1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band
