import re 
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

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes :
        text_images = extract_markdown_images(node.text)
        if not text_images :
            new_nodes.append(node)
        else :
            current_text = node.text
            for alt_text, url in text_images:
                image_markdown = f"![{alt_text}]({url})"
                parts = current_text.split(image_markdown, 1)
                
                if parts[0]:
                    new_nodes.append(TextNode(text=parts[0], text_type=TextType.PLAIN))
                
                new_nodes.append(TextNode(text=alt_text, text_type=TextType.IMAGE, url=url))
                
                current_text = parts[1]
            
            if current_text:
                new_nodes.append(TextNode(text=current_text, text_type=TextType.PLAIN))
    
    return new_nodes 

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text_links = extract_markdown_links(node.text)
        if not text_links:
            new_nodes.append(node)
        else:
            current_text = node.text
            for link_text, url in text_links:
                link_markdown = f"[{link_text}]({url})"
                parts = current_text.split(link_markdown, 1)
                
                if parts[0]:
                    new_nodes.append(TextNode(text=parts[0], text_type=TextType.PLAIN))
                
                new_nodes.append(TextNode(text=link_text, text_type=TextType.LINK, url=url))
                
                current_text = parts[1]
            
            if current_text:
                new_nodes.append(TextNode(text=current_text, text_type=TextType.PLAIN))
    
    return new_nodes