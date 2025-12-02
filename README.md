# Static Site Generator

A custom-built static site generator written in Python that converts Markdown files into a complete HTML website. This project demonstrates core web development concepts including Markdown parsing, HTML generation, and static site architecture.

## Features

- **Markdown to HTML Conversion**: Converts Markdown files to HTML with full support for:
  - Headings (h1-h6)
  - Paragraphs
  - Bold and italic text
  - Code blocks and inline code
  - Blockquotes
  - Ordered and unordered lists
  - Links and images
  
- **Recursive Site Generation**: Automatically processes nested directory structures, maintaining the same hierarchy in the output
- **Template System**: Uses a simple template with `{{ Title }}` and `{{ Content }}` placeholders
- **Static Asset Handling**: Copies CSS, images, and other static files to the public directory
- **Title Extraction**: Automatically extracts page titles from h1 headings in Markdown files

## Project Structure

```
static_site_generator/
├── src/                    # Source code
│   ├── main.py            # Main application logic
│   ├── block.py           # Markdown block parsing
│   ├── textnode.py        # Text node and inline parsing
│   ├── htmlnode.py        # HTML node classes
│   ├── utils.py           # Utility functions
│   └── test_*.py          # Unit tests
├── content/               # Markdown source files
│   ├── index.md
│   └── blog/
├── static/                # Static assets (CSS, images)
│   ├── index.css
│   └── images/
├── public/                # Generated HTML output (auto-generated)
├── template.html          # HTML template
├── main.sh               # Build and serve script
└── test.sh               # Test runner script
```

## Installation

### Prerequisites

- Python 3.12.3

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Prasann2004/static_site_generator.git
cd static_site_generator
```

2. No additional dependencies required - uses only Python standard library!

## Usage

### Generate the Site

To build the static site, run:

```bash
python3 src/main.py
```

This will:
1. Delete any existing `public/` directory
2. Copy all files from `static/` to `public/`
3. Recursively process all `.md` files in `content/`
4. Generate corresponding `.html` files in `public/`

### Build and Serve

To build and immediately start a local server:

```bash
./main.sh
```

This builds the site and starts a Python HTTP server on port 8888. Visit `http://localhost:8888` to view your site.

### Run Tests

To run the unit test suite:

```bash
./test.sh
```

Or manually:

```bash
python3 -m unittest discover -s src
```

## How It Works

### 1. Markdown Parsing

The generator processes Markdown in two stages:

- **Block-level parsing** (`block.py`): Identifies block types (headings, paragraphs, lists, code blocks, quotes)
- **Inline parsing** (`textnode.py`, `utils.py`): Handles inline formatting (bold, italic, code, links, images)

### 2. HTML Generation

- Each Markdown element is converted to an `HTMLNode` object
- The `HTMLNode` hierarchy is rendered to HTML strings
- Content is injected into the template using placeholders

### 3. Template System

The `template.html` file uses two placeholders:
- `{{ Title }}`: Replaced with the h1 heading from the Markdown
- `{{ Content }}`: Replaced with the generated HTML content

### 4. Directory Structure Preservation

The generator maintains the same directory structure from `content/` in the `public/` output:
- `content/blog/post.md` → `public/blog/post.html`
- `content/about/team.md` → `public/about/team.html`

## Core Components

### `main.py`
- `generate_page()`: Converts a single Markdown file to HTML
- `generate_pages_recursive()`: Processes directory trees
- `copy_static_to_public()`: Handles static asset copying

### `block.py`
- `markdown_to_html_node()`: Main conversion function
- `block_to_block_type()`: Identifies Markdown block types
- `BlockType`: Enum for block types (heading, paragraph, list, etc.)

### `textnode.py`
- `TextNode`: Represents inline text with formatting
- `text_node_to_html_node()`: Converts text nodes to HTML
- `TextType`: Enum for text types (bold, italic, code, link, image)

### `htmlnode.py`
- `HTMLNode`: Base HTML node class
- `LeafNode`: HTML node with no children (text, images)
- `ParentNode`: HTML node with children (div, p, ul, etc.)

### `utils.py`
- `extract_title()`: Extracts h1 heading from Markdown
- `text_to_textnodes()`: Parses inline Markdown formatting
- `markdown_to_blocks()`: Splits Markdown into blocks

## Example

Create a Markdown file in `content/`:

```markdown
# My First Post

This is a **bold** statement and this is *italic*.

## Code Example

Here's some code:

\`\`\`
def hello():
    print("Hello, world!")
\`\`\`

Check out [my website](https://example.com)!
```

Run the generator:

```bash
python3 src/main.py
```

The HTML output in `public/` will have:
- A properly formatted HTML structure
- Styled content using your CSS
- All inline formatting preserved
- The h1 heading as the page title

## Testing

The project includes comprehensive unit tests for:
- HTML node generation
- Text node parsing
- Block type detection
- Markdown to HTML conversion
- Utility functions

Run tests with:
```bash
python3 -m unittest discover -s src
```
