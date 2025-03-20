"""
Tests for the GUI components.
"""
import unittest
import tkinter as tk
import os
import tempfile
import fitz  # PyMuPDF

from gui.app import PDFEditorApp
from gui.sidebar import Sidebar
from gui.preview import PDFPreview

class GUITests(unittest.TestCase):
    """Test cases for GUI components."""
    
    def setUp(self):
        """Set up test fixtures."""
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
        
        # Create a root window for testing
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.root.destroy()
        self.temp_dir.cleanup()
    
    def test_app_initialization(self):
        """Test that the app initializes correctly."""
        app = PDFEditorApp(self.root)
        
        # Check that components are created
        self.assertIsNotNone(app.toolbar)
        self.assertIsNotNone(app.sidebar)
        self.assertIsNotNone(app.preview)
        self.assertIsNotNone(app.pdf_manager)
    
    def test_sidebar_initialization(self):
        """Test that the sidebar initializes correctly."""
        app = PDFEditorApp(self.root)
        sidebar = app.sidebar
        
        # Check that the page tree is created
        self.assertIsNotNone(sidebar.page_tree)
        
        # Initially, there should be no pages
        self.assertEqual(len(sidebar.page_tree.get_children()), 0)
    
    def test_sidebar_update_page_list(self):
        """Test updating the page list in the sidebar."""
        app = PDFEditorApp(self.root)
        
        # Open the test PDF
        app.pdf_manager.open_pdf(self.test_pdf_path)
        app.sidebar.update_page_list()
        
        # Check that the page list is updated
        self.assertEqual(len(app.sidebar.page_tree.get_children()), 3)
    
    def test_preview_initialization(self):
        """Test that the preview initializes correctly."""
        app = PDFEditorApp(self.root)
        preview = app.preview
        
        # Check that the canvas is created
        self.assertIsNotNone(preview.canvas)
        
        # Initially, there should be no image
        self.assertIsNone(preview.current_image)
        self.assertIsNone(preview.current_page_index)
    
    # Note: More comprehensive GUI tests would typically use a testing framework
    # like pytest-tk or would mock the tkinter components. These tests are
    # simplified examples.


if __name__ == "__main__":
    unittest.main()
