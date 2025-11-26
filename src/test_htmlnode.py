import unittest
from htmlnode import HTMLNode , LeafNode , ParentNode
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
        expected = "LeafNode(tag=p, value=text, children=None, props={'class': 'test'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_parent_to_html_no_tag_raises_error(self):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(None, [child_node])
            with self.assertRaises(ValueError):
                parent_node.to_html()

    def test_parent_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_empty_children_raises_error(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent_node = ParentNode("div", [child1, child2])
        expected = "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_to_html_mixed_children(self):
        leaf_child = LeafNode("span", "text")
        parent_child = ParentNode("p", [LeafNode("b", "bold")])
        parent_node = ParentNode("div", [leaf_child, parent_child])
        expected = "<div><span>text</span><p><b>bold</b></p></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_value_always_none(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertIsNone(parent_node.value)

    def test_parent_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        expected = f"HTMLNode(tag=div, value=None, children=[{repr(child_node)}], props={{'class': 'container'}})"
        self.assertEqual(repr(parent_node), expected)

    def test_parent_to_html_with_props(self):
        child_node = LeafNode("p", "content")
        parent_node = ParentNode("div", [child_node], {"class": "wrapper", "id": "main"})
        result = parent_node.to_html()
        self.assertEqual(result, "<div><p>content</p></div>")

    def test_parent_deeply_nested(self):
        deep_child = LeafNode("strong", "deep text")
        mid_parent = ParentNode("em", [deep_child])
        inner_parent = ParentNode("p", [mid_parent])
        outer_parent = ParentNode("div", [inner_parent])
        expected = "<div><p><em><strong>deep text</strong></em></p></div>"
        self.assertEqual(outer_parent.to_html(), expected)    

    
if __name__ == "__main__":
    unittest.main()
