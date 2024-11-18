from fastapi import FastAPI
app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Beatles', 'genre': 'Rock'},
    {'id': 2, 'name': 'Led Zeppelin', 'genre': 'Rock'},
    {'id': 3, 'name': 'The Rolling Stones', 'genre': 'Rock'},
    {'id': 4, 'name': 'The Who', 'genre': 'Rock'},
    {'id': 5, 'name': 'Pink Floyd', 'genre': 'Rock'},
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