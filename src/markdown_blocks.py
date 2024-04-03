import re

def markdown_to_blocks(markdown: str) -> list[str]:
    stripped_blocks = []
    blocks = re.split(r"(?:\r?\n){2,}", markdown)
    for block in blocks:
        stripped = block.strip(" \n")
        if stripped != "":
            stripped_blocks.append(stripped)
    return stripped_blocks