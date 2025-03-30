"""
Tests for the GUI components.
"""
import unittest
import sys
import os
import tempfile
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

from gui.app import PDFEditorApp
from gui.toolbar_tabs.edit_tab import EditTab
from gui.toolbar_tabs.view_tab import ViewTab
from gui.preview import PDFPreview

class GUITests(unittest.TestCase):
    """Test cases for GUI components."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for all tests."""
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        """Set up test fixtures."""
        self.editor = PDFEditorApp()
        
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
        self.editor.close()
        self.temp_dir.cleanup()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures for all tests."""
        cls.app.quit()
    
    def test_edit_tab(self):
        """Test edit tab functionality."""
        edit_tab = EditTab(self.editor.toolbar)
        
        # Test initial state
        self.assertIsNotNone(edit_tab)
        
        # Load test PDF
        self.editor.pdf_manager.open_pdf(self.test_pdf_path)
        self.editor.sidebar.update_page_list()
        self.editor.sidebar.setCurrentRow(1)  # Select second page
        
        # Test rotate left
        QTest.mouseClick(edit_tab.findChild(QPushButton, "Rotate Left"), Qt.MouseButton.LeftButton)
        page = self.editor.pdf_manager.get_page(1)
        self.assertEqual(page.rotation, 270)
        
        # Test rotate right
        QTest.mouseClick(edit_tab.findChild(QPushButton, "Rotate Right"), Qt.MouseButton.LeftButton)
        page = self.editor.pdf_manager.get_page(1)
        self.assertEqual(page.rotation, 0)
        
        # Test delete page
        initial_count = self.editor.pdf_manager.get_page_count()
        QTest.mouseClick(edit_tab.findChild(QPushButton, "Delete Page"), Qt.MouseButton.LeftButton)
        self.assertEqual(self.editor.pdf_manager.get_page_count(), initial_count - 1)
    
    def test_view_tab(self):
        """Test view tab functionality."""
        view_tab = ViewTab(self.editor.toolbar)
        
        # Test initial state
        self.assertIsNotNone(view_tab)
        self.assertEqual(view_tab.zoom_combo.currentText(), "100%")
        
        # Load test PDF
        self.editor.pdf_manager.open_pdf(self.test_pdf_path)
        self.editor.sidebar.update_page_list()
        self.editor.sidebar.setCurrentRow(0)  # Select first page
        
        # Test zoom in
        initial_zoom = view_tab.get_current_zoom()
        QTest.mouseClick(view_tab.findChild(QPushButton, "Zoom In"), Qt.MouseButton.LeftButton)
        self.assertGreater(view_tab.get_current_zoom(), initial_zoom)
        
        # Test zoom out
        QTest.mouseClick(view_tab.findChild(QPushButton, "Zoom Out"), Qt.MouseButton.LeftButton)
        self.assertEqual(view_tab.get_current_zoom(), initial_zoom)
        
        # Test zoom combo box
        view_tab.zoom_combo.setCurrentText("200%")
        self.assertEqual(view_tab.get_current_zoom(), 2.0)
    
    def test_preview(self):
        """Test preview functionality."""
        preview = PDFPreview(self.editor)
        
        # Test initial state
        self.assertIsNotNone(preview)
        self.assertIsNone(preview.current_page)
        self.assertEqual(preview.current_zoom, 1.0)
        
        # Load test PDF
        self.editor.pdf_manager.open_pdf(self.test_pdf_path)
        
        # Test showing page
        preview.show_page(1)
        self.assertEqual(preview.current_page, 1)
        
        # Test showing page with zoom
        preview.show_page(1, zoom=2.0)
        self.assertEqual(preview.current_zoom, 2.0)
        
        # Test clear
        preview.clear()
        self.assertIsNone(preview.current_page)


if __name__ == "__main__":
    unittest.main()
