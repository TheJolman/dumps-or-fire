import httpx
import json

client = httpx.Client(
    base_url="https://musicbrainz.org/ws/2",
    headers={
        "User-Agent": "dumps-or-fire/2.0 (git@jolman.me)",
        "Accept": "application/json",
    },
)

def search_track(query: str) -> tuple[str, str]:
    r = client.get("/recording", params={"query": query, "limit": 1})
    print(r.url)
    print(r.status_code)
    result = json.loads(r.content)
    recording = result["recordings"][0]
    title = recording["title"]
    artist = recording["artist-credit"][0]["name"]

    return title, artist
