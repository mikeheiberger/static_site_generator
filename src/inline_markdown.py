from textnode import (
    TextNode,
    text_type_text
)

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