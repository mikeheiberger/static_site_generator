import unittest

from textnode import (
    TextNode,
    split_nodes_delimiter,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code
)

text_type_link = "link"
text_type_image = "image"

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("Test", "bold", "https://www.google.com")
        node2 = TextNode("Test", "underline", "https://www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_different_text(self):
        node = TextNode("Test1", "bold")
        node2 = TextNode("Test2", "bold")
        self.assertNotEqual(node, node2)

    def test_codeblock_delimiter(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text)
            ]
        )

    def test_two_codeblock_delimiter(self):
        node = TextNode("This is `text` with two `code block` words", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_code),
                TextNode(" with two ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" words", text_type_text)
            ]
        )
    
    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text)
            ]
        )

    def test_italic_delimiter(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text)
            ]
        )
    
    def test_multiple_nodes(self):
        node1 = TextNode("This is text with a **bold** word", text_type_text)
        node2 = TextNode("This is more text with a **bold** word", text_type_text)
        new_nodes = split_nodes_delimiter([node1, node2], "**", text_type_bold)
        self.assertListEqual(
            new_nodes, 
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
                TextNode("This is more text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" word", text_type_text),
            ]
        )

if __name__ == "__main__":
    unittest.main()