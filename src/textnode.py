class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(left, right):
        return (left.text == right.text and
                left.text_type == right.text_type and
                left.url == right.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
