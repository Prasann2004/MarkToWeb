import unittest
from htmlnode import HTMLNode , LeafNode
class TestHTMLNode(unittest.TestCase):
    
    def test_init_with_all_params(self):
        node = HTMLNode("div", "Hello", ["child1"], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, ["child1"])
        self.assertEqual(node.props, {"class": "container"})
    
    def test_init_with_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_to_html_raises_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_add_to_html_no_props(self):
        node = HTMLNode("div", "test")
        self.assertEqual(node.add_to_html(), "")
    
    def test_add_to_html_with_props(self):
        node = HTMLNode("div", "test", None, {"class": "container", "id": "main"})
        result = node.add_to_html()
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
    
    def test_add_to_html_single_prop(self):
        node = HTMLNode("a", "link", None, {"href": "https://example.com"})
        self.assertEqual(node.add_to_html(), 'href="https://example.com"')
    
    def test_repr(self):
        node = HTMLNode("p", "text", ["child"], {"class": "test"})
        expected = "HTMLNode(tag=p, value=text, children=['child'], props={'class': 'test'})"
        self.assertEqual(repr(node), expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_empty_value_raises_error(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_none_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("button", "Submit", {"type": "submit", "class": "btn"})
        result = node.to_html()
        self.assertIn('<button', result)
        self.assertIn('type="submit"', result)
        self.assertIn('class="btn"', result)
        self.assertIn('>Submit</button>', result)

    def test_leaf_children_always_none(self):
        node = LeafNode("span", "test")
        self.assertIsNone(node.children)

    def test_leaf_to_html_img_self_closing_style(self):
        node = LeafNode("img", "", {"src": "image.jpg", "alt": "test"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode("p", "text", {"class": "test"})
        expected = "HTMLNode(tag=p, value=text, children=None, props={'class': 'test'})"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
