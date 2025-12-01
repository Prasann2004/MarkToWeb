import unittest 
from utils import *
from textnode import * 
class UtilsTest(unittest.TestCase):
    def test_single_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN)
        ]
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[2].text, " word")

    def test_multiple_delimiters_bold(self):
        node = TextNode("This **bold** and **more bold** text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN)
        ]
        self.assertEqual(len(result), 5)

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)

    def test_no_delimiter_present(self):
        node = TextNode("This is plain text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is plain text")
        self.assertEqual(result[0].text_type, TextType.PLAIN)

    def test_odd_delimiter_count_raises_error(self):
        node = TextNode("This has `unmatched delimiter", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("code", TextType.CODE),
            TextNode("bold", TextType.BOLD),
            TextNode("link", TextType.LINK, "http://example.com")
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, nodes)

    def test_empty_delimiter_content(self):
        node = TextNode("This has `` empty code", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].text_type, TextType.CODE)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`start` middle `end`", TextType.PLAIN)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "")
        self.assertEqual(result[1].text, "start")
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text, "end")
        self.assertEqual(result[4].text, "")

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![first](https://example.com/1.png) and ![second](https://example.com/2.jpg)"
        )
        self.assertListEqual([("first", "https://example.com/1.png"), ("second", "https://example.com/2.jpg")], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("This is just plain text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_mixed_with_links(self):
        matches = extract_markdown_images(
            "Here is a [link](https://example.com) and an ![image](https://example.com/pic.png)"
        )
        self.assertListEqual([("image", "https://example.com/pic.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Here's [first link](https://example.com) and [second link](https://test.com)"
        )
        self.assertListEqual([("first link", "https://example.com"), ("second link", "https://test.com")], matches)

    def test_extract_markdown_links_empty_text(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("This is just plain text with no links")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_mixed_with_images(self):
        matches = extract_markdown_links(
            "Here is an ![image](https://example.com/pic.png) and a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


if __name__ == "__main__":
    unittest.main()