import base64
from requests import post, get
import json

from django.conf import settings

client_id = settings.SOCIAL_AUTH_SPOTIFY_ID
client_secret = settings.SOCIAL_AUTH_SPOTIFY_SECRET


def get_token():
    """ Get Spotify token to access artist and track info """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_track_popularity(track_name: str):
    if track_name == "":
        return None
    token = get_token()
    track_result = user_search(token, track_name, "track")
    if not track_result:
        return None
    return track_result["popularity"]

def get_track_image(track_name: str):
    token = get_token()
    track_result = user_search(token , track_name, "track")
    if not track_result:
        return None
    return track_result["album"]["images"][0]["url"]

def get_album_popularity(album_name: str):
    if album_name == "":
        return None
    token = get_token()
    album_result = user_search(token, album_name, "album")
    if not album_result:
        return None
    return album_result["popularity"]

def get_playlist_popularity(playlist_name: str):
    token = get_token()
    playlist_result = user_search(token, playlist_name, "playlist")
    ...


def get_songs_by_artist(token, artist_id):
    """ Return top tracks from given artist """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def user_search(token, track_name, search_type = "track"):
    """ Search for a track and return items associated with track """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type={search_type}&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)[f"{search_type}s"]["items"]
    
    if len(json_result) == 0:
        print(f"No {search_type} with this name exists...")
        return None
    
    return json_result[0]




token = get_token()
