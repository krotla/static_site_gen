import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("p", "Paragraph")
        self.assertEqual(node.props_to_html(), None)

    def test_props_to_html2(self):
        node = HtmlNode("a", "This is link", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html3(self):
        node = HtmlNode("a", "This is link", None, {"href": "https://www.google.com",})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")

if __name__ == "__main__":
    unittest.main()