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
            return None
        return reduce(lambda str, atr: str + f" {atr[0]}=\"{atr[1]}\"", 
                      self.props.items(), "")
   
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"