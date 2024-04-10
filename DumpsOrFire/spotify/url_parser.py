from urllib.parse import urlparse

def get_url_id(url: str) -> str:
    '''uses urllib.parse.urlparse to extract the playlist id from a spotify playlist url'''
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")
    return path_parts[2]

def get_url_type(url: str) -> str:
    '''uses urllib.parse.urlparse to extract the playlist type from a spotify playlist url'''
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")
    return path_parts[1]
