"""
Tests for the PDF Manager module.
"""
import unittest
import os
import tempfile
import fitz  # PyMuPDF

from core.pdf_manager import PDFManager

class PDFManagerTests(unittest.TestCase):
    """Test cases for PDFManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pdf_manager = PDFManager()
        
        # Create a temporary PDF file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_pdf_path = os.path.join(self.temp_dir.name, "test.pdf")
        
        # Create a simple PDF with 3 pages
        doc = fitz.open()
        for i in range(3):
            page = doc.new_page(width=595, height=842)  # A4 size
            page.insert_text((50, 50), f"Test Page {i + 1}")
        doc.save(self.test_pdf_path)
        doc.close()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.pdf_manager.close()
        self.temp_dir.cleanup()
    
    def test_open_pdf(self):
        """Test opening a PDF file."""
        result = self.pdf_manager.open_pdf(self.test_pdf_path)
        self.assertTrue(result)
        self.assertEqual(self.pdf_manager.file_path, self.test_pdf_path)
        self.assertIsNotNone(self.pdf_manager.doc)
        self.assertFalse(self.pdf_manager.has_changes())
    
    def test_get_page_count(self):
        """Test getting the page count."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        self.assertEqual(self.pdf_manager.get_page_count(), 3)
    
    def test_get_page(self):
        """Test getting a specific page."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        page = self.pdf_manager.get_page(1)  # Second page
        self.assertIsNotNone(page)
        
        # Test invalid page index
        page = self.pdf_manager.get_page(10)
        self.assertIsNone(page)
    
    def test_rotate_page(self):
        """Test rotating a page."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        
        # Test valid rotation
        result = self.pdf_manager.rotate_page(1, 90)
        self.assertTrue(result)
        self.assertTrue(self.pdf_manager.has_changes())
        
        # Verify rotation
        page = self.pdf_manager.get_page(1)
        self.assertEqual(page.rotation, 90)
        
        # Test invalid page
        result = self.pdf_manager.rotate_page(10, 90)
        self.assertFalse(result)
        
        # Test invalid angle
        result = self.pdf_manager.rotate_page(1, 45)
        self.assertFalse(result)
    
    def test_delete_page(self):
        """Test deleting a page."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        initial_count = self.pdf_manager.get_page_count()
        
        # Delete the second page
        result = self.pdf_manager.delete_page(1)
        self.assertTrue(result)
        self.assertTrue(self.pdf_manager.has_changes())
        
        # Check page count decreased
        self.assertEqual(self.pdf_manager.get_page_count(), initial_count - 1)
        
        # Test deleting invalid page
        result = self.pdf_manager.delete_page(10)
        self.assertFalse(result)
    
    def test_extract_text(self):
        """Test extracting text from a page."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        
        # Test valid page
        text = self.pdf_manager.extract_text(1)
        self.assertIn("Test Page 2", text)
        
        # Test invalid page
        text = self.pdf_manager.extract_text(10)
        self.assertEqual(text, "")
    
    def test_extract_image(self):
        """Test extracting page as image."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        
        # Test valid page with default zoom
        image_data = self.pdf_manager.extract_image(1)
        self.assertIsNotNone(image_data)
        
        # Test valid page with custom zoom
        image_data = self.pdf_manager.extract_image(1, zoom=1.5)
        self.assertIsNotNone(image_data)
        
        # Test invalid page
        image_data = self.pdf_manager.extract_image(10)
        self.assertIsNone(image_data)
    
    def test_save_pdf(self):
        """Test saving a PDF."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        
        # Make some changes
        self.pdf_manager.rotate_page(1, 90)
        self.assertTrue(self.pdf_manager.has_changes())
        
        # Save to a new path
        new_path = os.path.join(self.temp_dir.name, "saved.pdf")
        result = self.pdf_manager.save_pdf_as(new_path)
        self.assertTrue(result)
        self.assertFalse(self.pdf_manager.has_changes())
        self.assertTrue(os.path.exists(new_path))
        
        # Verify the saved file is a valid PDF
        doc = fitz.open(new_path)
        self.assertEqual(len(doc), 3)
        self.assertEqual(doc[1].rotation, 90)  # Verify rotation was saved
        doc.close()
    
    def test_close(self):
        """Test closing a PDF."""
        self.pdf_manager.open_pdf(self.test_pdf_path)
        self.assertIsNotNone(self.pdf_manager.doc)
        
        # Make some changes
        self.pdf_manager.rotate_page(1, 90)
        self.assertTrue(self.pdf_manager.has_changes())
        
        self.pdf_manager.close()
        self.assertIsNone(self.pdf_manager.doc)
        self.assertIsNone(self.pdf_manager.file_path)
        self.assertFalse(self.pdf_manager.has_changes())


if __name__ == "__main__":
    unittest.main()
