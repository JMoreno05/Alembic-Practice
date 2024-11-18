from sqlalchemy import Field, SQLModel, Relationship
from enum import Enum

class GenreURLChoices(Enum):
    METAL = 'metal'
    ROCK = 'rock'
    COUNTRY = 'country'
    POP = 'pop'
    RNB = 'rnb'
    COMEDY = 'comedy'

class AlbumBase(SQLModel):
    title: str
    release_year: int
    band_id: int = Field(foreign_key="band.id")
    
class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band"=Relationship(back_populates="albums")
    
class BandBase(SQLModel):
    # {'id': 6, 'name': 'Bill Engvall', 'genre': 'Comedy'},
    name: str
    genre: str

class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    album: list[Album] = Relationship(back_populates="band")
