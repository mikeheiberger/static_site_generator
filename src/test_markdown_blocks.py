import unittest
from markdown_blocks import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks,
    block_to_block_type
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items

        """
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ]
        )
    
    def test_markdown_blocks_with_extra_whitespace(self):
        markdown = """
This is **bolded** paragraph


This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line




* This is a list
* with items

        """
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ]
        )

    def test_block_to_block_type_heading(self):
        heading = "### This is a heading"
        block_type = block_to_block_type(heading)
        self.assertEqual(block_type, block_type_heading)
    
    def test_block_to_block_type_code(self):
        code = """```Here is some code.
        It spans multiple lines.
        Three lines, actually.```"""
        block_type = block_to_block_type(code)
        self.assertEqual(block_type, block_type_code)

    def test_block_to_block_type_quote(self):
        quote = """>Here is a quote block.
>It spans multiple lines.
>Three lines, actually."""
        block_type = block_to_block_type(quote)
        self.assertEqual(block_type, block_type_quote)

    def test_block_to_block_type_asterisk_unordered_list(self):
        unordered_list = """*Here is an unordered list
*It spans multiple lines
*Three lines, actually
*Now it is four"""
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, block_type_unordered_list)

    def test_block_to_block_type_dash_unordered_list(self):
        unordered_list = """-Here is an unordered list
-It spans multiple lines
-Three lines, actually
-Now it is four"""
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, block_type_unordered_list)

    def test_block_to_block_type_mixed_unordered_list(self):
        unordered_list = """-Here is an unordered list
*It spans multiple lines
-Three lines, actually
-Now it is four"""
        block_type = block_to_block_type(unordered_list)
        self.assertEqual(block_type, block_type_paragraph)
    
    def test_block_to_block_type_ordered_list(self):
        ordered_list = """1. First thing
2. Second thing
3. Third thing
4. Fourth thing"""
        block_type = block_to_block_type(ordered_list)
        self.assertEqual(block_type, block_type_ordered_list)

    def test_block_to_block_type_ordered_list_broken(self):
        ordered_list = """1. First thing
2. Second thing
2. Third thing
4. Fourth thing"""
        block_type = block_to_block_type(ordered_list)
        self.assertEqual(block_type, block_type_paragraph)

if __name__ == "__main__":
    unittest.main()
