import re
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def block_to_block_type(block: str) -> str:
    # Heading test
    heading_matched = re.match(r"#{1,6}", block)
    if heading_matched:
        return block_type_heading

    # Code test
    code_matched = re.match(r"```([\s\S]*?)```", block)
    if code_matched:
        return block_type_code

    # Quote test
    lines = block.splitlines()
    all_lines_are_quotes = True
    for line in lines:
        if not line.startswith(">"):
            all_lines_are_quotes = False
            break
    if all_lines_are_quotes:
        return block_type_quote

    # Asterisk unordered list
    all_lines_start_asterisk = True
    for line in lines:
        if not line.startswith("*"):
            all_lines_start_asterisk = False
            break
    if all_lines_start_asterisk:
        return block_type_unordered_list

    # Dash unordered list
    all_lines_start_dash = True
    for line in lines:
        if not line.startswith("-"):
            all_lines_start_dash = False
            break
    if all_lines_start_dash:
        return block_type_unordered_list

    # Ordered list
    if lines[0].startswith("1."):
        is_ordered_list = True
        for i in range (1, len(lines)):
            if not lines[i].startswith(f"{i + 1}."):
                is_ordered_list = False
                break
        if is_ordered_list:
            return block_type_ordered_list
    
    # Otherwise its a paragraph
    return block_type_paragraph

def markdown_to_blocks(markdown: str) -> list[str]:
    stripped_blocks = []
    blocks = re.split(r"(?:\r?\n){2,}", markdown)
    for block in blocks:
        stripped = block.strip(" \n")
        if stripped != "":
            stripped_blocks.append(stripped)
    return stripped_blocks

def paragraph_block_to_htmlnode(block: str) -> HTMLNode:
    return LeafNode(block, "p")

def heading_block_to_htmlnode(block: str) -> HTMLNode:
    heading_matched = re.match(r"^(#+)(.*)", block)
    heading_symbols_count = len(heading_matched.group(1))
    text = heading_matched.group(0).strip(" #")
    return LeafNode(text, f"h{heading_symbols_count}")

def code_block_to_htmlnode(block: str) -> HTMLNode:
    code_node = LeafNode(block, "code")
    return ParentNode([code_node], "pre")

def quote_block_to_htmlnode(block: str) -> HTMLNode:
    lines = block.splitlines()
    trimmed_lines = []
    for line in lines:
        trimmed_lines.append(line.strip(">"))
    quote = "\n".join(trimmed_lines)
    return LeafNode(quote, "blockquote")

def unordered_list_to_htmlnode(block: str) -> HTMLNode:
    list_nodes = []
    lines = block.splitlines()
    for line in lines:
        line = line.strip("-*")
        list_nodes.append(LeafNode(line, "li"))
    return ParentNode(list_nodes, "ul")

def ordered_list_to_htmlnode(block: str) -> HTMLNode:
    list_nodes = []
    lines = block.splitlines()
    for i in range (0, len(lines)):
        line = lines[i]
        line_trimmed = re.sub(f"^{i+1}.", "", line)
        list_nodes.append(LeafNode(line_trimmed, "li"))
    return ParentNode(list_nodes, "ol")

def markdown_to_html_node(markdown: str) -> HTMLNode:
    child_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type is block_type_paragraph:
            child_nodes.append(paragraph_block_to_htmlnode(block))
        elif block_type is block_type_heading:
            child_nodes.append(heading_block_to_htmlnode(block))
        elif block_type is block_type_quote:
            child_nodes.append(quote_block_to_htmlnode(block))
        elif block_type is block_type_code:
            child_nodes.append(code_block_to_htmlnode(block))
        elif block_type is block_type_unordered_list:
            child_nodes.append(unordered_list_to_htmlnode(block))
        elif block_type is block_type_ordered_list:
            child_nodes.append(ordered_list_to_htmlnode(block))
    return ParentNode(child_nodes, "div")