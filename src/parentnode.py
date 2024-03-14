from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")

        if self.children == None:
            raise ValueError("ParentNode must have children")
        
        props = self.props_to_html()
        html = f"<{self.tag}{props}>"
        
        for child in self.children:
            html += child.to_html()
        
        html += f"</{self.tag}>"
        return html
