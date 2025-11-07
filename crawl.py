from urllib import parse


def normalize_url(url: str) -> str:
    result = parse.urlparse(url)
    joined = result.netloc + result.path
    normalized = joined.rstrip("/").lower()
    return normalized
