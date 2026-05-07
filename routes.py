from fastapi import APIRouter
from pydantic import BaseModel
from client import search_track

router = APIRouter()

class Track(BaseModel):
    title: str
    artist: str | None

@router.post("/popularity")
async def track_search(track: Track):
    title, artist = search_track(track.title)
    return {"popularity": 80, "artist": artist, "track": title}
