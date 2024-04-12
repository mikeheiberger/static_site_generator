import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    lines = markdown.splitlines()
    title = None
    for line in lines:
        if line.startswith("# "):
            if title is not None:
                raise ValueError("Invalid markdown. Only one h1 header allowed")
            title = line.lstrip("# ").strip()
    if title is None:
        raise ValueError("Invalid markdown. Must have an h1 header")
    return title


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path)
    markdown = from_file.read()
    from_file.close()

    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace(r"{{ Title }}", title)
    page = page.replace(r"{{ Content }}", html)

    dest_dir  = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
        
    with open(dest_path, "w") as dest_file:
        dest_file.write(page)
    
def generate_page_recursive(dir_path_content: str, template_path, dest_dir_path: str):
    content_dir = Path(dir_path_content)
    for child in content_dir.iterdir():
        if child.is_dir():
            generate_page_recursive(
                child, 
                template_path, 
                os.path.join(dest_dir_path, child.name)
            )
        elif child.suffix == ".md":
            generate_page(
                child, 
                template_path, 
                os.path.join(dest_dir_path, f"{child.stem}.html")
            )
