import re

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