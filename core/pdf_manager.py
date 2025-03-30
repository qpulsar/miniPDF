"""
Core PDF management functionality.
"""
import pymupdf
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
            self.doc = pymupdf.open(file_path)
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
            
    def merge_pdfs(self, pdf_files):
        """Merge multiple PDFs into one.
        
        Args:
            pdf_files: List of PDF file paths to merge
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not pdf_files:
            return False
            
        try:
            # Create new PDF document
            self.doc = pymupdf.open()
            self.file_path = None
            self._has_changes = True
            
            # Add pages from each PDF
            for pdf_file in pdf_files:
                try:
                    src_doc = pymupdf.open(pdf_file)
                    self.doc.insert_pdf(src_doc)
                    src_doc.close()
                except Exception as e:
                    logger.error(f"Error merging PDF {pdf_file}: {e}")
                    continue
                    
            return True
        except Exception as e:
            logger.error(f"Error creating merged PDF: {e}")
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
        
    def rotate_page(self, page_num, angle):
        """Rotate a page by the specified angle.
        
        Args:
            page_num: Page number (0-based)
            angle: Rotation angle in degrees (90, 180, 270)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return False
            
        try:
            page = self.doc[page_num]
            current_rotation = page.rotation
            new_rotation = (current_rotation + angle) % 360
            page.set_rotation(new_rotation)
            self._has_changes = True
            return True
            
        except Exception as e:
            logger.error(f"Error rotating page: {e}")
            return False
            
    def delete_page(self, page_num):
        """Delete a page from the PDF.
        
        Args:
            page_num: Page number (0-based)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return False
            
        try:
            self.doc.delete_page(page_num)
            self._has_changes = True
            return True
            
        except Exception as e:
            logger.error(f"Error deleting page: {e}")
            return False
            
    def extract_text(self, page_num):
        """Extract text from a page.
        
        Args:
            page_num: Page number (0-based)
            
        Returns:
            str: Extracted text, empty string if failed
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return ""
            
        try:
            page = self.doc[page_num]
            return page.get_text()
            
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""
            
    def extract_image(self, page_num, zoom=2.0):
        """Extract page as image.
        
        Args:
            page_num: Page number (0-based)
            zoom: Zoom factor for the image
            
        Returns:
            bytes: PNG image data, None if failed
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return None
            
        try:
            page = self.doc[page_num]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            return pix.tobytes()
            
        except Exception as e:
            logger.error(f"Error extracting image: {e}")
            return None
            
    def add_page(self, page):
        """Add a page to the PDF.
        
        Args:
            page: Page object to add
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc:
            return False
            
        try:
            self.doc.insert_page(-1, page)
            self._has_changes = True
            return True
            
        except Exception as e:
            logger.error(f"Error adding page: {e}")
            return False
            
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
