from sqlmodel import SQLModel, Relationship, Field
from pydantic import BaseModel, field_validator, validator

        
from enum import Enum
from datetime import date

class GenreURLChoices(Enum):
    METAL = 'metal'
    ROCK = 'rock'
    COUNTRY = 'country'
    POP = 'pop'
    RNB = 'rnb'
    COMEDY = 'comedy'

class GenreChoices(Enum):
    METAL = 'Metal'
    ROCK = 'Rock'
    COUNTRY = 'Country'
    POP = 'Pop'
    RNB = 'RnB'
    COMEDY = 'Comedy'

class AlbumBase(SQLModel):
    title: str
    release_date: date
    
    
class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band"=Relationship(back_populates="albums")
    band_id: int | None = Field(foreign_key="band.id")
    #instance of the band object, reference the band using a string b/c band is defined below this

    
class BandBase(SQLModel):
    # contains common fields but will never be used in the app. 
    # will be referenced in other subclasses
    # {'id': 6, 'name': 'Bill Engvall', 'genre': 'Comedy'},
    name: str
    genre: GenreChoices


    
class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None
    @validator('genre', pre=True)
    def title_case_genre(cls,value):
        if value == 'rnb' :
            return "RnB"
        return value.title() # rock -> Rock 
    
class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")
