import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestBlock_Breakdown(unittest.TestCase):
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

    def test_markdown_to_blocks_multiple_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        ],
    )       

class TestBlock_Identify(unittest.TestCase):
    def test_headers(self):
        md = "### Heading 3 test"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_ordered_list(self):
        md = """1. Item 1
2. Item 2
3. Item 3 """
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.OLIST, block_type)
    
    def test_unordered_list(self):
        md = """- Item 1
- Item 2
- Item 3 """
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.ULIST, block_type)

    def test_code_block(self):
        md = "```Item 1```"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, block_type)

    def test_paragraph(self):
        md = "paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.PARAGRAPH, block_type)

    def test_quote(self):
        md = """>quotes
>quoting
>quotes"""
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, block_type)



        
if __name__ == "__main__":
    unittest.main()