import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_no_children(self):
        node = ParentNode(None, "p")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")
    
    def test_no_tag(self):
        node = ParentNode([LeafNode("Some text")], None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_no_parentnode_children(self):
        node = ParentNode(
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text"),
                LeafNode("italic text", "i"),
                LeafNode("Normal text"),
            ],
            "p",
        )
        html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), html)

    def test_parentnode_as_last_child(self):
        node = ParentNode(
            [
                LeafNode("Some bold text", "b"),
                ParentNode(
                    [
                        LeafNode("Some more bold text", "b"),
                        LeafNode("Some italic text", "i"),
                        LeafNode("Some normal text")
                    ],
                    "p",
                    { "href": "https://www.google.com" }
                )
            ],
            "p"
        )
        html = "<p><b>Some bold text</b><p href=\"https://www.google.com\"><b>Some more bold text</b><i>Some italic text</i>Some normal text</p></p>"
        self.assertEqual(node.to_html(), html)
    
    def test_parentnode_inbetween_other_nodes(self):
        node = ParentNode(
            [
                LeafNode("Some bold text", "b"),
                ParentNode(
                    [
                        LeafNode("Some more bold text", "b"),
                        LeafNode("Some italic text", "i"),
                        LeafNode("Some normal text")
                    ],
                    "p",
                    { "href": "https://www.google.com" }
                ),
                LeafNode("Italic text", "i", props={ "href": "https://www.google.com"})
            ],
            "p"
        )
        html = "<p><b>Some bold text</b><p href=\"https://www.google.com\"><b>Some more bold text</b><i>Some italic text</i>Some normal text</p><i href=\"https://www.google.com\">Italic text</i></p>"
        self.assertEqual(node.to_html(), html)

    def test_parentnode_two_levels(self):
        node = ParentNode(
            [
                ParentNode(
                    [
                        ParentNode(
                            [
                                LeafNode("Italic text", "i")
                            ],
                            "p"
                        ),
                        LeafNode("Bold text", "b")
                    ],
                    "p"
                )
            ],
            "p"
        )
        html = "<p><p><p><i>Italic text</i></p><b>Bold text</b></p></p>"
        self.assertEqual(node.to_html(), html)

if __name__ == "__main__":
    unittest.main()