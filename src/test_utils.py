import unittest 
from utils import split_nodes_delimiter
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


if __name__ == "__main__":
    unittest.main()