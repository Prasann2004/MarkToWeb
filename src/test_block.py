import unittest 
from block import *

class BlockTest(unittest.TestCase) : 
    def test_paragraph_block(self):
        block = "This is a regular paragraph with some text."
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEAD)

    def test_code_block(self):
        block = "```\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> with multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UN_LIST)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.LIST)

    def test_single_line_quote(self):
        block = "> Single line quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_multiline_paragraph(self):
        block = "This is a paragraph\nwith multiple lines\nthat should be treated as paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    def test_incomplete_ordered_list(self):
        block = "1. First item\n3. Third item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)

    def test_mixed_list_formatting(self):
        block = "- Unordered item\n1. Ordered item"
        self.assertEqual(block_to_block_type(block), BlockType.PARA)
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_headings(self):
        md = """
    # Heading 1
    ## Heading 2 with **bold**
    ### Heading 3 with _italic_
    #### Heading 4
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading 3 with <i>italic</i></h3><h4>Heading 4</h4></div>",
        )
    def test_blockquote(self):
        md = """
    > This is a blockquote
    > with multiple lines
    > and **formatting**
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote\nwith multiple lines\nand <b>formatting</b></blockquote></div>",
        )
    def test_unordered_list(self):
        md = """
    - First item with **bold**
    - Second item with _italic_
    - Third item with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>",
        )
    def test_ordered_list(self):
        md = """
    1. First item
    2. Second item with **formatting**
    3. Third item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <b>formatting</b></li><li>Third item</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()