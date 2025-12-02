from enum import Enum
from utils import markdown_to_blocks
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from utils import text_to_textnodes

class BlockType(Enum) :
    PARA = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UN_LIST = "unordered_list"
    LIST = "ordered_list"

def block_to_block_type(markdown_block) : 
    lines = [line.strip() for line in markdown_block.split('\n')]
    
    if lines[0].startswith("#") :
        return BlockType.HEAD
    if markdown_block[:3] == "```" and markdown_block[::-1][:3] == "```"  :
        return BlockType.CODE
    
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.UN_LIST
    
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    
    if is_ordered_list:
        return BlockType.LIST
    
    return BlockType.PARA

def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARA:
            text = ' '.join(block.split())
            children = text_to_children(text)
            block_node = ParentNode("p", children)
        
        elif block_type == BlockType.HEAD:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            text = block[level:].strip()
            children = text_to_children(text)
            block_node = ParentNode(f"h{level}", children)
        
        elif block_type == BlockType.CODE:
            code_text = block[3:-3]
            if code_text.startswith('\n'):
                code_text = code_text[1:]
            if code_text.endswith('\n'):
                code_text = code_text[:-1]
            lines = code_text.split('\n')
            if lines:
                min_indent = float('inf')
                for line in lines:
                    if line.strip():
                        indent = len(line) - len(line.lstrip())
                        min_indent = min(min_indent, indent)
                if min_indent != float('inf'):
                    lines = [line[min_indent:] if len(line) >= min_indent else line for line in lines]
                code_text = '\n'.join(lines)
            text_node = TextNode(code_text, TextType.PLAIN)
            code_html_node = text_node_to_html_node(text_node)
            block_node = ParentNode("pre", [ParentNode("code", [code_html_node])])
        
        elif block_type == BlockType.QUOTE:
            lines = [line.strip() for line in block.split('\n')]
            quote_text = '\n'.join(line[1:].strip() for line in lines if line)
            children = text_to_children(quote_text)
            block_node = ParentNode("blockquote", children)
        
        elif block_type == BlockType.UN_LIST:
            lines = [line.strip() for line in block.split('\n')]
            list_items = []
            for line in lines:
                if line:
                    item_text = line[2:].strip()
                    item_children = text_to_children(item_text)
                    list_items.append(ParentNode("li", item_children))
            block_node = ParentNode("ul", list_items)
        
        elif block_type == BlockType.LIST:
            lines = [line.strip() for line in block.split('\n')]
            list_items = []
            for line in lines:
                if line:
                    item_text = line[line.index('. ') + 2:].strip()
                    item_children = text_to_children(item_text)
                    list_items.append(ParentNode("li", item_children))
            block_node = ParentNode("ol", list_items)
        
        block_nodes.append(block_node)
    
    return ParentNode("div", block_nodes)
def text_to_children(text):
    
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        if node.text_type == TextType.PLAIN and not node.text:
            continue
        children.append(text_node_to_html_node(node))
    return children