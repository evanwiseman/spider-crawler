import unittest
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html


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


if __name__ == "__main__":
    unittest.main()
