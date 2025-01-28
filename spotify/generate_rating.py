import base64
import json

from django.conf import settings
from requests import get, post

import logging
logger = logging.getLogger(__name__)
client_id = settings.SOCIAL_AUTH_SPOTIFY_ID
client_secret = settings.SOCIAL_AUTH_SPOTIFY_SECRET

logger.error(f"Spotify ID exists: {client_id is not None}")
logger.error(f"Spotify Secret exists: {client_secret is not None}")

class SpotifyAPIError(Exception):
    """Custom exception for Spotify API related errors"""
    pass

def get_token():
    """Get Spotify token to access artist and track info

    Returns:
        json result with access token
    Raises:
        SpotifyAPIError: If there's any issue getting the spotify access token
    """

    if not client_id or not client_secret:
        raise SpotifyAPIError("Missing client credentials")

    auth_string = f"{client_id.strip()}:{client_secret.strip()}"
    auth_bytes = auth_string.encode("utf-8")
    # auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "dumps-or-fire/1.1"
    }

    data = {"grant_type": "client_credentials"}
    try:
        result = post(url, headers=headers, data=data)
        if result.status_code != 200:
            print(f"Error response content: {result.content}")
        result.raise_for_status()
        json_result = json.loads(result.content)

        if "access_token" not in json_result:
            raise SpotifyAPIError("No access token in response")

        return json_result["access_token"]

    except json.JSONDecodeError as e:
        raise SpotifyAPIError(f"Failed to decode token response: {str(e)}")

    except Exception as e:
        raise SpotifyAPIError(f"Failed to get access token: {str(e)}")


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_popularity(content_type="track", content_name="", input_id=""):
    """Get popularity rating for Spotify content.

    Args:
        content_type (str): Type of content ('track', 'artist', or 'playlist')
        content_name (str): Name of the content to search for
        input_id (str): Spotify ID of the content

    Returns:
        tuple: (popularity rating, content name, image URL)

    Raises:
        SpotifyAPIError: If there's any error accessing the Spotify API
        ValueError: If invalid args are provided
    """
    if content_name == "" and input_id == "":
        raise ValueError("Either content_name or input_id must be provided")

    if content_type not in ["track", "album", "artist", "playlist"]:
        raise ValueError(f"Invalid content_type: {content_type}")

    try:
        token = get_token()

        # Here we either use provided id or get one from the search
        if content_name != "" and input_id == "":
            result = user_search(token, content_name, search_type=content_type)
            if result is None:
                return None
            id = result["id"]
        else:
            id = input_id

        # Search for content and return items associated with content
        url = f"https://api.spotify.com/v1/{content_type}s/{id}"
        headers = get_auth_header(token)

        result = get(url, headers=headers)
        result.raise_for_status()

        json_result = json.loads(result.content)

        if "name" not in json_result:
            raise SpotifyAPIError("Missing name in API response")

        # Get popularity of content (using avg function if playlist)
        if content_type == "playlist":
            popularity = get_avg_popularity(result, json_result)
        else:
            if "popularity" not in json_result:
                raise SpotifyAPIError("Missing popularity in API response")
            popularity = json_result["popularity"]

        # Get name of content
        name = json_result["name"]
        if content_type != "playlist":
            if "artists" not in json_result or not json_result["artists"]:
                raise SpotifyAPIError("Missing artist information in API response")
            name = f"{name} - {json_result['artists'][0]['name']}"

        # Get image of content
        if content_type == "track":
            if "album" not in json_result or "images" not in json_result["album"] \
                or not json_result["album"]["images"]:
                raise SpotifyAPIError("Missing album image in API response")
            image = json_result["album"]["images"][0]["url"]
        else:
            if "images" not in json_result or not json_result["images"]:
                raise SpotifyAPIError("Missing image in API response")
            image = json_result["images"][0]["url"]

        return popularity, name, image

    except json.JSONDecodeError as e:
        raise SpotifyAPIError(f"Failed to decode API response: {str(e)}")
    except Exception as e:
        if isinstance(e, SpotifyAPIError):
            raise
        raise SpotifyAPIError(f"Error getting content popularity: {str(e)}")


def get_avg_popularity(result, json_result):
    """Calculate average popularity of tracks in a playlist

    Raises:
        SpotifyAPIError: if playlist has no valid tracks
    """
    sum = 0
    num_tracks = 0

    for track in json_result["tracks"]["items"]:
        result = track["track"]
        sum += result["popularity"]
        num_tracks += 1

    if num_tracks == 0:
        raise SpotifyAPIError("No valid tracks found in playlist")

    return sum // num_tracks


def user_search(token, track_name, search_type="track"):
    """Search for a track and return items associated with track using spotify API

    Raises:
        json.JSONDecodeError:
        SpotifyAPIError:
    """
    try:
        url = f"https://api.spotify.com/v1/search?q={track_name}&type={search_type}&limit=1"
        headers = get_auth_header(token)

        result = get(url, headers=headers)
        result.raise_for_status()

        json_result = json.loads(result.content)

        if f"{search_type}s" not in json_result:
            raise SpotifyAPIError(f"Missing {search_type}s in search response")

        items = json_result[f"{search_type}s"]["items"]

        if not items:
            return None

        return items[0]

    except json.JSONDecodeError as e:
        raise SpotifyAPIError(f"Failed to decode search response: {str(e)}")
    except Exception as e:
        if isinstance(e, SpotifyAPIError):
            raise
        raise SpotifyAPIError(f"Error searching for content: {str(e)}")
