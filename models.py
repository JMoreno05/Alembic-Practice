from sqlmodel import SQLModel, Relationship, Field
from pydantic import BaseModel, field_validator

        
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

class Album(SQLModel):
    title: str
    release_date: date
    #band_id: int #= Field(foreign_key="band.id")
    
#class Album(AlbumBase, table=True):
    #id: int = Field(default=None, primary_key=True)
    #band: "Band"=Relationship(back_populates="albums")
    
class BandBase(BaseModel):
    # contains common fields but will never be used in the app. 
    # will be referenced in other subclasses
    # {'id': 6, 'name': 'Bill Engvall', 'genre': 'Comedy'},
    name: str
    genre: GenreChoices
    albums: list[Album] = []

class BandCreate(BandBase):
    @field_validator('genre', pre=True)
    def title_case_genre(cls,value):
        if value == 'rnb' :
            return "RnB"
        return value.title() # rock -> Rock o

class BandWithID(BandBase):
    id:int
    
#class Band(BandBase):
    #id: int = Field(default=None, primary_key=True)
    #album: list[Album] = Relationship(back_populates="band")
