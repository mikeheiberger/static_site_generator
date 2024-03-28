from leafnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

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

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode(text_node.text, "b")
    elif text_node.text_type == text_type_italic:
        return LeafNode(text_node.text, "i")
    elif text_node.text_type == text_type_code:
        return LeafNode(text_node.text, "code")
    elif text_node.text_type == text_type_link:
        return LeafNode(text_node.text, "a", { "href": text_node.url })
    elif text_node.text_type == text_type_image:
        return LeafNode("", "img", { "src": text_node.url, "alt": text_node.text })
    else:
        raise Exception(f"Could not handle text node of type {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        words = old_node.text.split(delimiter)
        # This means we only split once, and we require delimiters to have an open and a close
        if len(words) < 3:
            raise Exception("Delimiters must be closed")
        # Since we have split, the pattern should be:
        # 0. Text
        # 1. Delimited text
        # 2. Text
        # 3. Delimited text
        # ...
        for i in range(0, len(words)):
            text = words[i]
            if i % 2 == 0:
                new_nodes.append(TextNode(text, text_type_text))
            else:
                new_nodes.append(TextNode(text, text_type))
        
    return new_nodes

