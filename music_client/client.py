import httpx
import json

client = httpx.Client(
    base_url="https://musicbrainz.org/ws/2",
    headers={
        "User-Agent": "dumps-or-fire/2.0 (git@jolman.me)",
        "Accept": "application/json",
    },
)

r = client.get("/artist", params={"query": "Tame Impala", "limit": 1})
print(r.url)
print(r.status_code)
json_r = json.loads(r.content)
print(json.dumps(json_r, indent=4))
