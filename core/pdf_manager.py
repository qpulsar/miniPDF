"""
Core PDF management functionality.
"""
import pymupdf
import logging
import os

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
            
    def split_pdf(self, output_dir, split_ranges=None):
        """Split PDF into multiple files.
        
        Args:
            output_dir: Directory to save split PDFs
            split_ranges: List of tuples (start, end) for page ranges.
                        If None, each page becomes a separate PDF.
                        Page numbers are 0-based.
                        
        Returns:
            list: List of created PDF file paths, empty if failed
        """
        if not self.doc:
            return []
            
        try:
            output_files = []
            page_count = len(self.doc)
            
            # If no ranges specified, create one PDF per page
            if not split_ranges:
                split_ranges = [(i, i) for i in range(page_count)]
                
            # Create output PDFs
            for i, (start, end) in enumerate(split_ranges):
                if start < 0 or end >= page_count or start > end:
                    logger.error(f"Invalid page range: {start}-{end}")
                    continue
                    
                try:
                    # Create new PDF
                    new_doc = pymupdf.open()
                    
                    # Copy pages
                    new_doc.insert_pdf(self.doc, from_page=start, to_page=end)
                    
                    # Save PDF
                    output_file = os.path.join(output_dir, f"split_{i + 1}.pdf")
                    new_doc.save(output_file)
                    new_doc.close()
                    
                    output_files.append(output_file)
                except Exception as e:
                    logger.error(f"Error creating split PDF {i + 1}: {e}")
                    continue
                    
            return output_files
        except Exception as e:
            logger.error(f"Error splitting PDF: {e}")
            return []
            
    def add_text_annotation(self, page_num, rect, text, color=(1, 1, 0)):
        """Add a text annotation to a page.
        
        Args:
            page_num: Page number (0-based)
            rect: Rectangle coordinates (x0, y0, x1, y1)
            text: Text content
            color: Annotation color in RGB format (default: yellow)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return False
            
        try:
            page = self.doc[page_num]
            annot = page.add_text_annot(rect, text)
            annot.set_colors(stroke=color)
            annot.update()
            self._has_changes = True
            return True
        except Exception as e:
            logger.error(f"Error adding text annotation: {e}")
            return False
            
    def add_highlight_annotation(self, page_num, rect, color=(1, 1, 0)):
        """Add a highlight annotation to a page.
        
        Args:
            page_num: Page number (0-based)
            rect: Rectangle coordinates (x0, y0, x1, y1)
            color: Highlight color in RGB format (default: yellow)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return False
            
        try:
            page = self.doc[page_num]
            annot = page.add_highlight_annot(rect)
            annot.set_colors(stroke=color)
            annot.update()
            self._has_changes = True
            return True
        except Exception as e:
            logger.error(f"Error adding highlight annotation: {e}")
            return False
            
    def add_ink_annotation(self, page_num, points, color=(0, 0, 1), width=2):
        """Add an ink (drawing) annotation to a page.
        
        Args:
            page_num: Page number (0-based)
            points: List of point lists, each sublist is a stroke
            color: Ink color in RGB format (default: blue)
            width: Line width (default: 2)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return False
            
        try:
            page = self.doc[page_num]
            annot = page.add_ink_annot(points)
            annot.set_colors(stroke=color)
            annot.set_border(width=width)
            annot.update()
            self._has_changes = True
            return True
        except Exception as e:
            logger.error(f"Error adding ink annotation: {e}")
            return False
            
    def get_annotations(self, page_num):
        """Get all annotations on a page.
        
        Args:
            page_num: Page number (0-based)
            
        Returns:
            list: List of annotations, empty if failed
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return []
            
        try:
            page = self.doc[page_num]
            return page.annots()
        except Exception as e:
            logger.error(f"Error getting annotations: {e}")
            return []
            
    def delete_annotation(self, page_num, annot_index):
        """Delete an annotation from a page.
        
        Args:
            page_num: Page number (0-based)
            annot_index: Index of annotation to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or page_num < 0 or page_num >= len(self.doc):
            return False
            
        try:
            page = self.doc[page_num]
            annots = page.annots()
            if annot_index < 0 or annot_index >= len(annots):
                return False
                
            page.delete_annot(annots[annot_index])
            self._has_changes = True
            return True
        except Exception as e:
            logger.error(f"Error deleting annotation: {e}")
            return False
