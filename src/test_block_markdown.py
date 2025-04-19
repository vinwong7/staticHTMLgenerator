import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

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

class Test_markdown_to_HTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_headers(self):
        md = """## Header 2
### Header 3
Text
# Header **Bold** 1
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h2>Header 2</h2><h3>Header 3 Text</h3><h1>Header <b>Bold</b> 1</h1></div>",
    )

    def test_codeblock(self):
        md = """
```This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
            md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

    """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
            )

    def test_quoteblock(self):
        md = """
>quotes
>quoting
>uwu
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quotes quoting uwu</blockquote></div>",
        )

if __name__ == "__main__":
    unittest.main()