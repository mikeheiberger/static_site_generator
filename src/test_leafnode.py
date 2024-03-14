import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_props(self):
        node = LeafNode("This is a paragraph of text.", "p")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_with_one_prop(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_with_multiple_props(self):
        node = LeafNode("Click me!", "a", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Click me!</a>")

    def test_with_no_value(self):
        node = LeafNode(None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "LeafNode requires a value")
    
    def test_with_no_tag(self):
        node = LeafNode("This is some raw text", None, {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "This is some raw text")

if __name__ == "__main__":
    unittest.main()
