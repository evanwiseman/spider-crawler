from bs4 import BeautifulSoup
from urllib import parse
from typing import List


def normalize_url(url: str) -> str:
    result = parse.urlparse(url)
    joined = result.netloc + result.path
    normalized = joined.rstrip("/").lower()
    return normalized


def get_h1_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find(name="h1")
    if h1 is None:
        return ""
    return h1.get_text()


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find(name="main")

    # high priority main and paragraph
    if main and main.p:
        return main.p.get_text()

    # low priority outside of main
    p = soup.find(name="p")
    return p.get_text() if p else ""


def get_urls_from_html(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    a_list = soup.find_all(name="a")

    urls = []
    for a in a_list:
        href = a.get("href")
        if not href:
            continue
        urls.append(parse.urljoin(base_url, href))

    return urls


def get_images_from_html(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    img_list = soup.find_all(name="img")

    urls = []
    for img in img_list:
        src = img.get("src")
        if not src:
            continue
        urls.append(parse.urljoin(base_url, src))

    return urls
