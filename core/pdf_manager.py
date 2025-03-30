"""
Core PDF management functionality.
"""
import os
import fitz
import logging

logger = logging.getLogger(__name__)

class PDFManager:
    """Manages PDF document operations."""
    
    def __init__(self):
        """Initialize PDF manager."""
        self.doc = None
        self.file_path = None
        self._has_changes = False
        
    def open_pdf(self, file_path):
        """Open a PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.doc = fitz.open(file_path)
            self.file_path = file_path
            self._has_changes = False
            return True
            
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            return False
            
    def save_pdf(self):
        """Save the current PDF file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or not self.file_path:
            return False
            
        try:
            self.doc.save(self.file_path)
            self._has_changes = False
            return True
            
        except Exception as e:
            logger.error(f"Error saving PDF: {e}")
            return False
            
    def save_pdf_as(self, file_path):
        """Save the current PDF file with a new name.
        
        Args:
            file_path: New file path
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc:
            return False
            
        try:
            self.doc.save(file_path)
            self.file_path = file_path
            self._has_changes = False
            return True
            
        except Exception as e:
            logger.error(f"Error saving PDF: {e}")
            return False
            
    def get_page_count(self):
        """Get the number of pages in the PDF.
        
        Returns:
            int: Number of pages, 0 if no document is open
        """
        return len(self.doc) if self.doc else 0
        
    def get_page(self, page_num):
        """Get a specific page from the PDF.
        
        Args:
            page_num: Page number (0-based)
            
        Returns:
            Page: PDF page object, None if invalid
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return None
            
        return self.doc[page_num]
        
    def has_changes(self):
        """Check if there are unsaved changes.
        
        Returns:
            bool: True if there are unsaved changes
        """
        return self._has_changes
        
    def mark_changed(self):
        """Mark the document as having unsaved changes."""
        self._has_changes = True
        
    def close(self):
        """Close the current PDF document."""
        if self.doc:
            self.doc.close()
            self.doc = None
            self.file_path = None
            self._has_changes = False
