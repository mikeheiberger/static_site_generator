import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_eq(self):
        html_props = " href=\"https://www.google.com\" target=\"_blank\""
        node = HTMLNode(props={"href": "https://www.google.com", "target" : "_blank"})
        self.assertEqual(node.props_to_html(), html_props)
        node2 = HTMLNode(props={"href": "https://www.google.com", "target" : "_blank"})
        self.assertEqual(node2.props_to_html(), html_props)
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_props_to_html_not_eq(self):
        html_props_wthout_space = "href=\"https://www.google.com\" target=\"_blank\""
        node = HTMLNode(props={"href": "https://www.google.com", "target" : "_blank"})
        self.assertNotEqual(node.props_to_html(), html_props_wthout_space)

if __name__ == "__main__":
    unittest.main()