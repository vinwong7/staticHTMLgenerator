import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Boot.dev", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Boot.dev</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>")
        
    def test_parent_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("b", "text")
        child_node3 = LeafNode("i", "emphasis")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>text</b><i>emphasis</i></div>")
    
    def test_parent_to_html_with_multiple_children_nested(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("p","testing", {"class":"test"})
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("a", "link", {"href": "https://boot.dev"})
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(parent_node.to_html(), '<div><span><b>grandchild</b><p class="test">testing</p></span><b>child2</b><a href="https://boot.dev">link</a></div>')

if __name__ == "__main__":
    unittest.main()
