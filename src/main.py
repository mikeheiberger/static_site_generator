from textnode import TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    if text_node.text_type == "text_type_text":
        return LeafNode(text_node.text)
    elif text_node.text_type == "text_type_bold":
        return LeafNode(text_node.text, "b")
    elif text_node.text_type == "text_type_italic":
        return LeafNode(text_node.text, "i")
    elif text_node.text_type == "text_type_code":
        return LeafNode(text_node.text, "code")
    elif text_node.text_type == "text_type_link":
        return LeafNode(text_node.text, "a", { "href": text_node.url })
    elif text_node.text_type == "text_type_image":
        return LeafNode("", "img", { "src": text_node.url, "alt": text_node.text })
    else:
        raise Exception(f"Could not handle text node of type {text_node.text_type}")

def main():
    text_node = TextNode("This is a text node", "text_type_bold", "https://www.boot.dev")
    print(text_node)
    htmlNode = text_node_to_html_node(text_node)
    print(htmlNode.to_html())


main()