from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlmodel import Session, select
from models import BandBase, BandCreate, Band, GenreURLChoices, Album
from typing import Annotated
from contextlib import asynccontextmanager
from db import init_db, get_session

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

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
    q: Annotated[str | None , Query(max_length=10)] = None,
    session: Session = Depends(get_session)
    
    ) -> list[Band]:
    band_list = session.exec(select(Band)).all()
    
    if genre:
        band_list =  [b for b in band_list if b.genre.value.lower() == genre.value]
        
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()#ab
        ]

    return band_list
    

@app.get('/bands/{band_id}')
async def get_band(
    band_id: Annotated[int, Path(title='The band ID')],
    session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band
"""
@app.get('/bands/genre/{genre}')
async def get_band_by_genre(genre: GenreURLChoices) -> list[Band]:
    bands = [Band(**band) for band in BANDS if band['genre'].value.lower() == genre.value]
    return bands
"""
@app.post('/bands')
async def create_band(
   band_data:BandCreate, 
   session: Session = Depends(get_session)
    ) -> Band:
    band = Band(name=band_data.name,
               genre=band_data.genre)
    session.add(band)

    if band_data.albums:
      for album in band_data.albums:
         album_obj = Album(
            title=album.title,
            release_date=album.release_date,
            band=band) #using relationship instead of id that is not created yet
         session.add(album_obj)

    session.commit()

    session.refresh(band) #refreshes the object with the new data from the db (pk created during commit))

    return band
 