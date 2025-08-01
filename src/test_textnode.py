import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter, \
                extract_markdown_images, extract_markdown_links, \
                split_nodes_image, split_nodes_link, text_to_textnodes, \
                markdown_to_blocks
from markdown import BlockType, block_to_block_type


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node2", TextType.ITALIC, None)
        node2 = TextNode("This is a text node2", TextType.ITALIC, None)
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is a text node2", TextType.ITALIC, None)
        node2 = TextNode("This is a text node2", TextType.TEXT, None)
        self.assertNotEqual(node, node2)

    def test_neq3(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "www.boot.dev.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_nodes_delimiter(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        correct_nodes = [
            TextNode("This is a text node", TextType.BOLD),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, correct_nodes)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [The boot site](https://www.w3schools.com/python/default.asp)"
        )
        self.assertListEqual([("The boot site", "https://www.w3schools.com/python/default.asp")], matches)

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with an [Cool link](https://www.w3schools.com/python/default.asp) and also ![image](https://i.imgur.com/3elNhQu.png). There is also a [GO link](https://www.w3schools.com/go/index.php) here.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("Cool link", TextType.LINK, "https://www.w3schools.com/python/default.asp"),
                TextNode(" and also ![image](https://i.imgur.com/3elNhQu.png). There is also a ", TextType.TEXT),
                TextNode("GO link", TextType.LINK, "https://www.w3schools.com/go/index.php"),
                TextNode(" here.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = "This is **bolded** paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

        md = """
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

        md = \
"""- This is a list
- with items"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

        md = \
"""1. This is a list
2. with items"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

        md = "# This is **bolded** paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)

        md = "### This is **bolded** paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        
        md = \
"""```
if success:
        print('Hurra!')
```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)

        md = \
""">Być albo nie być,
>oto jest pytanie"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)

if __name__ == "__main__":
    unittest.main()