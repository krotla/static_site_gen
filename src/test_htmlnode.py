import unittest

from htmlnode import HtmlNode, LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("p", "Paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html2(self):
        node = HtmlNode("a", "This is link", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html3(self):
        node = HtmlNode("a", "This is link", None, {"href": "https://www.google.com",})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is BOLD!")
        self.assertEqual(node.to_html(), "<b>This is BOLD!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")


if __name__ == "__main__":
    unittest.main()