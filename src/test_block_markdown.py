import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        # Testing that multiple consecutive newlines are ignored and don't create empty blocks
        md = """
This is a single paragraph.




This is a second paragraph after way too many newlines.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a single paragraph.",
                "This is a second paragraph after way too many newlines.",
            ],
        )

    def test_markdown_to_blocks_whitespace_surround(self):
        # Testing that excessive spaces surrounding blocks are stripped cleanly
        md = "   This block has leading and trailing spaces.   \n\n   Next block here.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This block has leading and trailing spaces.",
                "Next block here.",
            ],
        )
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        # Counter-test: 7 hashes or no space should fall back to paragraph
        self.assertEqual(block_to_block_type("####### Too Many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        code_block = "```\ndef main():\n    print('hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        quote_block = "> This is a quote\n> split over two lines"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
        # Counter-test: missing a '>' on a line makes it a paragraph
        bad_quote = "> First line\n Second line missing bracket"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        ul_block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(ul_block), BlockType.UNORDERED_LIST)
        # Counter-test: missing space after a dash
        bad_ul = "- Item 1\n-Item 2 without space"
        self.assertEqual(block_to_block_type(bad_ul), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        ol_block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST)
        # Counter-test: broken list sequence
        bad_ol = "1. First\n3. Out of order sequence"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        paragraph = "This is a completely normal paragraph block of markdown text."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()