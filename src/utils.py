from textnode import TextType , TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes :
        if node.text_type == TextType.PLAIN : 
            count_delimeter = node.text.count(delimiter)
            if count_delimeter %2 != 0 :
                raise ValueError("Invalid markdown syntax")
            else :
                if count_delimeter == 0 :
                    new_nodes.append(TextNode(text = node.text , text_type = TextType.PLAIN))
                else : 
                    left,center,right = node.text.split(delimiter,maxsplit = 2)
                    old_nodes.extend([TextNode(text = left , text_type = TextType.PLAIN),
                    TextNode(text = center , text_type = text_type),TextNode(text = right , text_type = TextType.PLAIN)])
        else :
            new_nodes.append(node)
    
    return new_nodes
