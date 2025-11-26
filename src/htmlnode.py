class HTMLNode :
    def __init__(self,tag = None,value = None,children = None,props = None) : 
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props 
    
    def to_html(self) :
        raise NotImplementedError
    
    def add_to_html(self) :
        if not self.props : 
            return ""
        else : 
            result = ""
            for key , value in self.props.items() :
                result +=key+"="+f"\"{value}\" "
            return result

    def __repr__(self) : 
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"