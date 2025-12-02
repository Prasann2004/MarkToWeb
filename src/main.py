import os
import shutil
import logging
from block import markdown_to_html_node
from utils import extract_title

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    title = extract_title(markdown_content)
    
    full_html = template_content.replace('{{ Title }}', title)
    full_html = full_html.replace('{{ Content }}', html_content)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

def copy_static_to_public(source_dir="static", dest_dir="public"):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        logging.info(f"Deleted existing directory: {dest_dir}")
    
    os.makedirs(dest_dir)
    logging.info(f"Created directory: {dest_dir}")
    
    _copy_directory_contents(source_dir, dest_dir)

def _copy_directory_contents(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        logging.warning(f"Source directory does not exist: {source_dir}")
        return
    
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)
            logging.info(f"Copied file: {source_path} -> {dest_path}")
        elif os.path.isdir(source_path):
            os.makedirs(dest_path)
            logging.info(f"Created directory: {dest_path}")
            _copy_directory_contents(source_path, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    if not os.path.exists(dir_path_content):
        logging.warning(f"Content directory does not exist: {dir_path_content}")
        return
    
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(source_path):
            if source_path.endswith('.md'):
                dest_filename = item.replace('.md', '.html')
                dest_path = os.path.join(dest_dir_path, dest_filename)
                
                generate_page(source_path, template_path, dest_path)
        
        elif os.path.isdir(source_path):
            dest_subdir = os.path.join(dest_dir_path, item)
            os.makedirs(dest_subdir, exist_ok=True)
            
            generate_pages_recursive(source_path, template_path, dest_subdir)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    public_dir = os.path.join(project_root, "public")
    static_dir = os.path.join(project_root, "static")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        logging.info(f"Deleted existing directory: {public_dir}")
    
    copy_static_to_public(static_dir, public_dir)
    
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == "__main__":
    main()
