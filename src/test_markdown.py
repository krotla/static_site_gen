import unittest
     
from markdown import BlockType, markdown_to_blocks, block_to_block_type                     
from textnode import _extract_markdown_images, _extract_markdown_links


class TestMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = _extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = _extract_markdown_links(
            "This is text with an [The boot site](https://www.w3schools.com/python/default.asp)"
        )
        self.assertListEqual([("The boot site", "https://www.w3schools.com/python/default.asp")], matches)

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