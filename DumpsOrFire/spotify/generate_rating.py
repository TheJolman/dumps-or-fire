import base64
from requests import post, get
import json
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

from django.conf import settings

from . import url_parser as up # use up.get_url_id(url) to get playlist/song/album id
                               # use up.get_url_type(url) to get playlist/song/album type (returns str) 

client_id = settings.SOCIAL_AUTH_SPOTIFY_ID
client_secret = settings.SOCIAL_AUTH_SPOTIFY_SECRET
# client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


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


"""==================Get Track Data===================="""
def get_track_popularity(track_name: str, id = ""):
    if track_name == "" and id == "":
        return None
    token = get_token()
    track_result = user_search(token, track_name, "track")
    if not track_result:
        return None

    if id != "":
        track_id = id
    else: 
        track_id = track_result["id"]

    """ Search for an track and return items associated with track """
    url = "https://api.spotify.com/v1/tracks"
    headers = get_auth_header(token)
    query = f"/{track_id}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result['popularity']


def get_track_name(track_name: str):
    token = get_token()
    track_result = user_search(token , track_name, "track")
    name = track_result['name'] + ' - ' + track_result['artists'][0]['name']
    if not track_result:
        return None
    return name

def get_track_image(track_name: str):
    token = get_token()
    track_result = user_search(token , track_name, "track")
    if not track_result:
        return None
    return track_result["album"]["images"][0]["url"]


"""==================Get Album Data===================="""
def get_album_popularity(album_name: str, id = ""):
    if album_name == "":
        return None
    token = get_token()
    album_result = user_search(token, album_name, "album")
    if not album_result:
        return None
    
    if id != "":
        album_id = id
    else:
        album_id = album_result["id"]
    
    """ Search for an album and return items associated with album """
    url = "https://api.spotify.com/v1/albums"
    headers = get_auth_header(token)
    query = f"/{album_id}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    return json_result['popularity']


def get_album_image(album_name: str):
    token = get_token()
    album_result = user_search(token, album_name, "album")
    if not album_result:
        return None
    return album_result["images"][0]["url"]


def get_album_name(album_name: str):
    token = get_token()
    album_result = user_search(token, album_name, "album")
    if not album_result:
        return None
    return album_result["name"]


"""==================Get Playlist Data================="""
def get_playlist_popularity(playlist_name: str, id = ""):
    if playlist_name == "":
        return None
    token = get_token()
    playlist_result = user_search(token, playlist_name, "playlist")
    if not playlist_result:
        return None
    
    if id != "":
        playlist_id = id
    else:
        playlist_id = playlist_result["id"]

    """ Search for a playlist and return items associated with playlist """
    url = "https://api.spotify.com/v1/playlists"
    headers = get_auth_header(token)
    query = f"/{playlist_id}"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    sum = 0
    num_tracks = 0
    for track in json_result["tracks"]["items"]:
        result = track["track"]
        sum += result["popularity"]
        num_tracks += 1

    return sum // num_tracks


def get_playlist_image(playlist_name: str):
    token = get_token()
    playlist_result = user_search(token, playlist_name, "playlist")
    if not playlist_result:
        return None
    return playlist_result["images"][0]["url"]
    

def get_playlist_name(playlist_name: str):
    token = get_token()
    playlist_result = user_search(token, playlist_name, "playlist")
    if not playlist_result:
        return None
    return playlist_result["name"]


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


# print(get_playlist_popularity("Top 50 - USA"))
# print(get_playlist_popularity("VAPORWAVE CLASSICS"))
