import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_link
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code
)

class TextInlineMarkdown(unittest.TestCase):
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
    
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        extracted = extract_markdown_images(text)
        self.assertListEqual(
            extracted,
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png")
            ]
        )

    def test_extract_markdown_links(self):
        text = "This is text with an [link](https://www.example.com) and [another](https://www.example.com/another)"
        extracted = extract_markdown_link(text)
        self.assertListEqual(
            extracted,
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another")
            ]
        )

    def test_extract_markdown_links_single(self):
        text = "This is text with an [link](https://www.example.com)"
        extracted = extract_markdown_link(text)
        self.assertListEqual(
            extracted,
            [("link", "https://www.example.com")]
        )

if __name__ == "__main__":
    unittest.main()