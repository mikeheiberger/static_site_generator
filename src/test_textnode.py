import unittest
from textnode import TextNode

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

if __name__ == "__main__":
    unittest.main()