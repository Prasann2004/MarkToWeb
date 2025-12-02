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
                    new_nodes.append(node)
                else : 
                    parts = node.text.split(delimiter)
                    for i, part in enumerate(parts):
                        if i % 2 == 0:  # Even indices are plain text
                            new_nodes.append(TextNode(text=part, text_type=TextType.PLAIN))
                        else:  # Odd indices are formatted text
                            new_nodes.append(TextNode(text=part, text_type=text_type))
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

def text_to_textnodes(text) : 
    result = [TextNode(text = text,text_type = TextType.PLAIN)]
    result = split_nodes_image(result)
    result = split_nodes_link(result)
    result = split_nodes_delimiter(result, "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "*", TextType.ITALIC)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    return result

def markdown_to_blocks(markdown) : 
    delimeter = "\n\n"
    initial_blocks = markdown.split(delimeter)
    
    result = []
    for block in initial_blocks:
        block = block.strip()
        if not block:
            continue
            
        lines = block.split('\n')
        current_block_lines = []
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('#') and current_block_lines:
                result.append('\n'.join(current_block_lines).strip())
                current_block_lines = [line]
            else:
                current_block_lines.append(line)
        
        if current_block_lines:
            result.append('\n'.join(current_block_lines).strip())
    
    return [b for b in result if b]