import unittest
from generate_page import extract_title


class TestCopyStatic(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# Hello  ")
        self.assertEqual(
            title,
            'Hello')
    def test_extract_title_longer(self):
        md = """Testing

## Header 2

# Title

Text"""
        title = extract_title(md)
        self.assertEqual(
            title,
            'Title')

if __name__ == "__main__":
    unittest.main()