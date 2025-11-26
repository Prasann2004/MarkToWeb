class HTMLNode :
    def __init__(self,tag = None,value = None,children = None,props = None) : 
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 
    
    def to_html(self) :
        raise NotImplementedError("To_HTML not implemented for HTML_NODE")
    
    def add_to_html(self) :
        if not self.props : 
            return ""
        else : 
            result = ""
            for key , value in self.props.items() :
                result +=key+"="+f"\"{value}\" "
            result = result.rstrip()
            return result

    def __repr__(self) : 
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) :
        if not self.value :
            raise ValueError("No value Passed .")
        if not self.tag : 
            return self.value
        else : 
            result = ""
            result +=f"<{self.tag}"
            if self.props : 
                result +=" "+self.add_to_html()
            result+=">"
            result+=self.value
            result+="</"
            result+=self.tag
            result+=">"
            return result
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class ParentNode(HTMLNode) :
    def __init__(self, tag, children,props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) : 
        if not self.tag : 
            raise ValueError("No tag given")
        if not self.children :
            raise ValueError("Missing Children")
        result = f"<{self.tag}>"
        for child in self.children : 
            result+=child.to_html()
        result += f"</{self.tag}>"
        return result