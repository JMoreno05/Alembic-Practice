from sqlmodel import SQLModel, Relationship, Field
from pydantic import BaseModel

        
from enum import Enum
from datetime import date

class GenreURLChoices(Enum):
    METAL = 'metal'
    ROCK = 'rock'
    COUNTRY = 'country'
    POP = 'pop'
    RNB = 'rnb'
    COMEDY = 'comedy'

class Album(SQLModel):
    title: str
    release_date: date
    #band_id: int #= Field(foreign_key="band.id")
    
#class Album(AlbumBase, table=True):
    #id: int = Field(default=None, primary_key=True)
    #band: "Band"=Relationship(back_populates="albums")
    
class Band(BaseModel):
    # {'id': 6, 'name': 'Bill Engvall', 'genre': 'Comedy'},
    name: str
    genre: str
    albums: list[Album] = []
    
#class Band(BandBase):
    #id: int = Field(default=None, primary_key=True)
    #album: list[Album] = Relationship(back_populates="band")
