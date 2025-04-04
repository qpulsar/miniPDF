"""
Tests for text extraction functionality.
"""
import unittest
import os
import tempfile
import pymupdf

from core.text_extraction import TextExtractor

class TextExtractionTests(unittest.TestCase):
    """Test cases for TextExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.text_extractor = TextExtractor()
        
        # Create a temporary PDF file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_pdf_path = os.path.join(self.temp_dir.name, "test.pdf")
        
        # Create a simple PDF with text content
        doc = fitz.open()
        page1 = doc.new_page(width=595, height=842)  # A4 size
        page1.insert_text((50, 50), "This is test page 1")
        page1.insert_text((50, 100), "With multiple lines")
        
        page2 = doc.new_page(width=595, height=842)
        page2.insert_text((50, 50), "This is test page 2")
        page2.insert_text((50, 100), "With searchable content")
        
        doc.save(self.test_pdf_path)
        self.doc = doc  # Keep the document open for tests
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.doc:
            self.doc.close()
        self.temp_dir.cleanup()
    
    def test_extract_text_from_page(self):
        """Test extracting text from a single page."""
        page = self.doc[0]
        text = self.text_extractor.extract_text_from_page(page)
        
        self.assertIn("This is test page 1", text)
        self.assertIn("With multiple lines", text)
    
    def test_extract_text_from_document(self):
        """Test extracting text from the entire document."""
        text_by_page = self.text_extractor.extract_text_from_document(self.doc)
        
        self.assertEqual(len(text_by_page), 2)
        self.assertIn("This is test page 1", text_by_page[0])
        self.assertIn("This is test page 2", text_by_page[1])
    
    def test_search_text(self):
        """Test searching for text in the document."""
        # Search for text on page 1
        results = self.text_extractor.search_text(self.doc, "test page 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 0)  # First page
        
        # Search for text on page 2
        results = self.text_extractor.search_text(self.doc, "searchable")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 1)  # Second page
        
        # Search for text that appears on both pages
        results = self.text_extractor.search_text(self.doc, "test page")
        self.assertEqual(len(results), 2)
        
        # Search for non-existent text
        results = self.text_extractor.search_text(self.doc, "nonexistent text")
        self.assertEqual(len(results), 0)
    
    def test_perform_ocr(self):
        """Test the OCR placeholder function."""
        page = self.doc[0]
        result = self.text_extractor.perform_ocr(page)
        
        # This is just checking the placeholder message
        self.assertIn("OCR functionality requires integration", result)


if __name__ == "__main__":
    unittest.main()
