import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        # Test with multiple attributes
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "https://www.google.com", "target": "_blank"}
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_none(self):
        # Test with no props (should return empty string)
        node = HTMLNode("p", "Hello world")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        # Test that repr looks correct for debugging
        node = HTMLNode("h1", "Title", None, {"class": "header"})
        expected = "HTMLNode(h1, Title, children: None, {'class': 'header'})"
        self.assertEqual(repr(node), expected)

    def test_values(self):
        # Test that the constructor correctly assigns values
        node = HTMLNode("div", "content")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

if __name__ == "__main__":
    unittest.main()