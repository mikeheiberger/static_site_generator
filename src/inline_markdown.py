import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        words = old_node.text.split(delimiter)
        if len(words) % 2 == 0:
            raise Exception("Invalid Markdown. Delimiters must be closed")
        for i in range(0, len(words)):
            text = words[i]
            if text == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text, text_type_text))
            else:
                new_nodes.append(TextNode(text, text_type))
        
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_link(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        extracted_links = extract_markdown_images(old_node.text)
        if not extracted_links:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        for extracted in extracted_links:
            split = current_text.split(f"![{extracted[0]}]({extracted[1]})", 1)
            if len(split) != 2:
                raise ValueError("Invalid markdown, image not closed")
            if split[0] != "":
                new_nodes.append(TextNode(split[0], text_type_text))
            new_nodes.append(TextNode(extracted[0], text_type_image, extracted[1]))
            current_text = split[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, text_type_text))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        extracted_links = extract_markdown_link(old_node.text)
        if not extracted_links:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        for extracted in extracted_links:
            split = current_text.split(f"[{extracted[0]}]({extracted[1]})", 1)
            if len(split) != 2:
                raise ValueError("Invalid markdown, link not closed")
            if split[0] != "":
                new_nodes.append(TextNode(split[0], text_type_text))
            new_nodes.append(TextNode(extracted[0], text_type_link, extracted[1]))
            current_text = split[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, text_type_text))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
