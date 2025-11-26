import unittest
from htmlnode import HTMLNode
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
        self.assertEqual(node.add_to_html(), 'href="https://example.com" ')
    
    def test_repr(self):
        node = HTMLNode("p", "text", ["child"], {"class": "test"})
        expected = "HTMLNode(tag=p, value=text, children=['child'], props={'class': 'test'})"
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
