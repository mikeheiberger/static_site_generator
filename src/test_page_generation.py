import unittest
from page_generation import extract_title

class TestPageGeneration(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
# Here is the header

## Here is an h2 header

Some other text.
And **more** text.
"""
        title = extract_title(markdown)
        self.assertEqual(
            title,
            "Here is the header"
        )
    
    def test_extract_title_two_h1(self):
        markdown = """
# Here is the first header

# And a second header. Oh no!
Some other text.
And **more** text.
"""
        with self.assertRaises(ValueError) as context:
            title = extract_title(markdown)
        self.assertEqual(str(context.exception), "Invalid markdown. Only one h1 header allowed")

    def test_extract_title_no_h1(self):
        markdown = """
Here is the header. Oops!

Some other text.
And **more** text.
"""
        with self.assertRaises(ValueError) as context:
            title = extract_title(markdown)
        self.assertEqual(str(context.exception), "Invalid markdown. Must have an h1 header")