
def get_url_id(url: str) -> str:
    '''uses urllib.parse.urlparse to extract the playlist id from a spotify playlist url'''
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")
    return path_parts[2]
