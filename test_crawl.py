import unittest
from crawl import (
    normalize_url,
    get_h1_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data,
)


class TestNormalizeURL(unittest.TestCase):
    def test_default(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_slash(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_capitals(self):
        input_url = "https://BLOG.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_http(self):
        input_url = "http://BLOG.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)


class TestGetH1FromHTML(unittest.TestCase):
    def test_default(self):
        input_html = """
            <html><body>
                <h1>Heading 1</h1>
            </body></html>
            """
        actual = get_h1_from_html(input_html)
        expected = "Heading 1"
        self.assertEqual(actual, expected)
        self.assertNotIn("<h1>", actual)
        self.assertNotIn("</h1>", actual)

    def test_missing(self):
        input_html = """
            <html><body>
                <p>html missing heading 1</p>
            </body></html>
            """
        actual = get_h1_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)
        self.assertNotIn("<h1>", actual)
        self.assertNotIn("</h1>", actual)

    def test_empty(self):
        input_html = """
            <html><body>
                <h1></h1>
            </body></html>
            """
        actual = get_h1_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_multiple(self):
        input_html = """
            <html><body>
                <h1>Heading 1</h1>
                <h1>Heading 2</h1>
            </body><html>
            """
        actual = get_h1_from_html(input_html)
        expected = "Heading 1"
        self.assertEqual(actual, expected)


class TestGetFirstParagraphFromHTML(unittest.TestCase):
    def test_default(self):
        input_html = """
            <html><body>
                <h1>Heading 1</h1>
                <main>
                    <p>body paragraph</p>
                </main>
            </body></html>
            """
        actual = get_first_paragraph_from_html(input_html)
        expected = "body paragraph"
        self.assertEqual(actual, expected)

    def test_high_priority(self):
        input_body = """
            <html><body>
                <p>low priority</p>
                <main>
                    <p>high priority</p>
                </main>
            </body></html>
            """
        actual = get_first_paragraph_from_html(input_body)
        expected = "high priority"
        self.assertEqual(actual, expected)
        self.assertNotIn("<p>", actual)
        self.assertNotIn("</p>", actual)

    def test_low_priority(self):
        input_body = """
            <html><body>
                <p>low priority</p>
                <main>
                    <h1>missing high priority</h1>
                </main>
            </body></html>
            """
        actual = get_first_paragraph_from_html(input_body)
        expected = "low priority"
        self.assertEqual(actual, expected)
        self.assertNotIn("<p>", actual)
        self.assertNotIn("</p>", actual)

    def test_missing_main(self):
        input_body = """
            <html><body>
                <p>low priority</p>
            </body></html>
            """
        actual = get_first_paragraph_from_html(input_body)
        expected = "low priority"
        self.assertEqual(actual, expected)


class TestGetURLsFromHTML(unittest.TestCase):
    def test_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <a href="https://blog.boot.dev"><span>Boot.dev</span></a>
            </body></html>
            """
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><boddy>
                <a href="/about"><span>About</span></a>
            </body></html>
            """
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/about"]
        self.assertListEqual(actual, expected)

    def test_multiple(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <a href="https://blog.boot.dev"><span>Boot.dev</span></a>
                <a href="/about"><span>About</span></a>
            </body></html>
            """
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev", "https://blog.boot.dev/about"]
        self.assertListEqual(actual, expected)

    def test_missing(self):
        input_url = "https://blog.boot.dev"
        input_body = "<html><body></body></html>"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertListEqual(actual, expected)

    def test_missing_href(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><boddy>
                <a><span>About</span></a>
            </body></html>
            """
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertListEqual(actual, expected)


class TestGetImagesFromHTML(unittest.TestCase):
    def test_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <img src="https://blog.boot.dev/logo.png" alt="Logo">
            </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertListEqual(actual, expected)

    def test_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <img src="/logo.png" alt="Logo">
            </body></html>
            """
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertListEqual(actual, expected)

    def test_multiple(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <img src="https://blog.boot.dev/logo.png" alt="Logo">
                <img src="/logo.png" alt="Logo">
            </body></html>
            """
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png", "https://blog.boot.dev/logo.png"]
        self.assertListEqual(actual, expected)

    def test_missing(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
            </body></html>
            """
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertListEqual(actual, expected)

    def test_missing_src(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <img alt="Logo">
            </body></html>
            """
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertListEqual(actual, expected)


class TestExtractPageData(unittest.TestCase):
    def test_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"],
        }
        self.assertDictEqual(actual, expected)

    def test_missing(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
            </body></html>
            """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertDictEqual(actual, expected)

    def test_multiple_headers(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <h1>Test Title 1</h1>
                <h1>Test Title 2</h1>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title 1",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"],
        }
        self.assertDictEqual(actual, expected)

    def test_multiple_paragraph(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <p>This is the second paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"],
        }
        self.assertDictEqual(actual, expected)

    def test_multiple_links(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <a href="/link2">Link 2</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [
                "https://blog.boot.dev/link1",
                "https://blog.boot.dev/link2",
            ],
            "image_urls": ["https://blog.boot.dev/image1.jpg"],
        }
        self.assertDictEqual(actual, expected)

    def test_multiple_images(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
                <img src="/image2.jpg" alt="Image 2">
            </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": [
                "https://blog.boot.dev/image1.jpg",
                "https://blog.boot.dev/image2.jpg",
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_multiple_all(self):
        input_url = "https://blog.boot.dev"
        input_body = """
            <html><body>
                <h1>Test Title 1</h1>
                <h1>Test Title 2</h1>
                <p>This is the first paragraph.</p>
                <p>This is the second paragraph.</p>
                <a href="/link1">Link 1</a>
                <a href="/link2">Link 2</a>
                <img src="/image1.jpg" alt="Image 1">
                <img src="/image2.jpg" alt="Image 2">
            </body></html>
        """
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title 1",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [
                "https://blog.boot.dev/link1",
                "https://blog.boot.dev/link2",
            ],
            "image_urls": [
                "https://blog.boot.dev/image1.jpg",
                "https://blog.boot.dev/image2.jpg",
            ],
        }
        self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
