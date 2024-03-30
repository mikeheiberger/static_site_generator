import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_link,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode("second image", text_type_image, "https://i.imgur.com/3elNhQu.png"),
            ]
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://www.google.com")
            ]
        )

    def test_split_link_with_extra_no_link_node(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com)",
            text_type_text,
        )
        node2 = TextNode("This is just some text", text_type_text)
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://www.google.com"),
                TextNode("This is just some text", text_type_text)
            ]
        )

    def test_split_image_with_text_after(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com). Cool!",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://www.google.com"),
                TextNode(". Cool!", text_type_text)
            ]
        )

    def test_split_link_nothing_before(self):
        node = TextNode(
            "[link](https://www.google.com). That's a link.",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", text_type_link, "https://www.google.com"),
                TextNode(". That's a link.", text_type_text)
            ]
        )
    
    def test_split_image_alone(self):
        node = TextNode("[link](https://www.google.com)", text_type_text)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [TextNode("link", text_type_link, "https://www.google.com")]
        )
    
    def test_text_to_textnodes_everything(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ]
        )

    def test_text_to_textnodes_multiple_bold(self):
        text = "**This** is **text** with an *italic* word and a `code block`" 
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This", text_type_bold),
                TextNode(" is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
            ]
        )

if __name__ == "__main__":
    unittest.main()