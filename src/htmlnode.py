from functools import reduce

class HtmlNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        return reduce(lambda str, atr: str + f" {atr[0]}=\"{atr[1]}\"", 
                      self.props.items(), "")
   
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HtmlNode):

    def __init__(self, tag, value, props=None):

        super(LeafNode,self).__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node must have value!")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        