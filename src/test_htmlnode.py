import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_double(self):
        node = HTMLNode(props={"prop": "yes", "bobo": "gaga"})
        self.assertEqual(node.props_to_html(), 'prop="yes" bobo="gaga"')

    def test_repr(self):
        node = HTMLNode(tag="boh", value="bohboh", children=[], props={})
        node2 = HTMLNode(tag="boh", value="bohboh", children=[], props={})
        self.assertEqual(node.__repr__(), node2.__repr__())


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_requires_value(self):
        node = LeafNode("p", "text")
        node.value = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_without_tag_returns_value(self):
        node = LeafNode("p", "text")
        node.tag = None
        self.assertEqual(node.to_html(), "text")


class TestParentNode(unittest.TestCase):
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

    def test_parent_requires_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node.tag = None
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_requires_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        parent_node.children = None
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_props_applied(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "wrapper"})
        self.assertEqual(
            parent_node.to_html(), '<div class="wrapper"><span>child</span></div>'
        )


if __name__ == "__main__":
    unittest.main()
