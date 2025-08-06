import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode, \
                    text_node_to_html_node, markdown_to_html_node, heading_block_tag
from textnode import TextNode, TextType


class TestHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

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

    def test_heading_block_tag(self):
        md_heading_block = "# H1"
        h_tag = heading_block_tag(md_heading_block)
        self.assertEqual("h1", h_tag)

        md_heading_block = "## H2"
        h_tag = heading_block_tag(md_heading_block)
        self.assertEqual("h2", h_tag)

        md_heading_block = "### H3"
        h_tag = heading_block_tag(md_heading_block)
        self.assertEqual("h3", h_tag)

        md_heading_block = "#### H4"
        h_tag = heading_block_tag(md_heading_block)
        self.assertEqual("h4", h_tag)

        md_heading_block = "##### H5"
        h_tag = heading_block_tag(md_heading_block)
        self.assertEqual("h5", h_tag)

        md_heading_block = "###### H6"
        h_tag = heading_block_tag(md_heading_block)
        self.assertEqual("h6", h_tag)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# This is **bolded** heading 1

## Next heading 2

### This is another heading  3 with _italic_ text and `code` here

#### Next heading 4

##### Next heading 5

###### Next heading 6

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is <b>bolded</b> heading 1</h1><h2>Next heading 2</h2><h3>This is another heading  3 with <i>italic</i> text and <code>code</code> here</h3><h4>Next heading 4</h4><h5>Next heading 5</h5><h6>Next heading 6</h6></div>",
        )

    def test_blockquotes(self):
        md = """
>This is **bolded** paragraph
>text in a p
>tag here

>This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bolded</b> paragraph text in a p tag here</blockquote><blockquote>This is another paragraph with <i>italic</i> text and <code>code</code> here</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First unordered list item
- Second unordered list item
- Third unordered list item

- This is single unordered list item with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First unordered list item</li><li>Second unordered list item</li><li>Third unordered list item</li></ul><ul><li>This is single unordered list item with <i>italic</i> text and <code>code</code> here</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First ordered list item
1. Second ordered list item
1. Third ordered list item

1. This is single ordered **list item** with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First ordered list item</li><li>Second ordered list item</li><li>Third ordered list item</li></ol><ol><li>This is single ordered <b>list item</b> with <i>italic</i> text and <code>code</code> here</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()