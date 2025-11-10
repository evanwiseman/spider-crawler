import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import List, Optional


def normalize_url(url: str) -> str:
    result = urlparse(url)
    joined = result.netloc + result.path
    normalized = joined.rstrip("/").lower()
    return normalized


def get_html(url: str) -> str:
    res = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

    if not res.ok:
        raise Exception("request failed")

    contentType = res.headers.get("content-type")
    if not contentType or "text/html" not in contentType.lower():
        raise Exception(f"response content-type invalid: {contentType}")

    return res.text


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
        urls.append(urljoin(base_url, href))

    return urls


def get_images_from_html(html: str, base_url: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    img_list = soup.find_all(name="img")

    urls = []
    for img in img_list:
        src = img.get("src")
        if not src:
            continue
        urls.append(urljoin(base_url, src))

    return urls


def extract_page_data(html: str, page_url: str) -> dict:
    data = {}
    data["url"] = page_url
    data["h1"] = get_h1_from_html(html)
    data["first_paragraph"] = get_first_paragraph_from_html(html)
    data["outgoing_links"] = get_urls_from_html(html, page_url)
    data["image_urls"] = get_images_from_html(html, page_url)
    return data


def is_same_domain(url1: str, url2: str) -> bool:
    parsed1 = urlparse(url1)
    parsed2 = urlparse(url2)
    if parsed1.netloc == parsed2.netloc:
        return True
    return False


def crawl_page(
    base_url: str,
    current_url: Optional[str] = None,
    page_data: Optional[dict] = None,
) -> dict:
    if not current_url:
        current_url = base_url
    if not page_data:
        page_data = {}

    # check base and current domain match (skip)
    if not is_same_domain(base_url, current_url):
        return

    # normalize the current url
    normalized_current = normalize_url(current_url)

    # check if the page has already been crawled (skip)
    if normalized_current in page_data:
        return

    print(f"extracting from {current_url}...")
    try:
        html = get_html(current_url)
        data = extract_page_data(html, current_url)
        page_data[normalized_current] = data
        for url in data["outgoing_links"]:
            crawl_page(current_url, url, page_data)
    except Exception:
        # mark as seen and skip
        page_data[normalized_current] = None
        print(f"failed extracting from {current_url}")
        return page_data

    print(f"finished extracting from {current_url}.")
    return page_data
