"""
PDF Manager module for handling PDF operations like page deletion, addition, and saving.
"""
import fitz  # PyMuPDF
import os
import tempfile
import shutil
import logging
from contextlib import contextmanager

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFManager:
    """Class for managing PDF documents."""
    
    def __init__(self):
        """Initialize the PDF manager."""
        self.doc = None
        self.file_path = None
        self.current_file = None
    
    def open_pdf(self, file_path):
        """Open a PDF file.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.doc:
                self.close()
            self.doc = fitz.open(file_path)
            self.file_path = file_path
            self.current_file = file_path
            return True
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            return False
    
    def get_page_count(self):
        """Get the number of pages in the PDF.
        
        Returns:
            int: Number of pages or 0 if no document is open
        """
        if self.doc:
            return len(self.doc)
        return 0
    
    def get_page(self, page_index):
        """Get a specific page from the PDF.
        
        Args:
            page_index (int): Index of the page to get
            
        Returns:
            Page: PyMuPDF Page object or None if invalid
        """
        if self.doc and 0 <= page_index < len(self.doc):
            return self.doc[page_index]
        return None
    
    @contextmanager
    def _create_temp_doc(self):
        """Context manager to create a temporary document and handle cleanup.
        
        Yields:
            fitz.Document: A new temporary PDF document
        """
        temp_doc = fitz.open()
        try:
            yield temp_doc
        finally:
            if temp_doc:
                temp_doc.close()
    
    def delete_page(self, page_index):
        """Delete a page from the PDF.
        
        Args:
            page_index (int): Index of the page to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or not (0 <= page_index < len(self.doc)):
            return False
        
        try:
            # Create a new document without the specified page
            with self._create_temp_doc() as new_doc:
                for i in range(len(self.doc)):
                    if i != page_index:
                        new_doc.insert_pdf(self.doc, from_page=i, to_page=i)
                
                # Save to a temporary file
                temp_fd, temp_path = tempfile.mkstemp(suffix=".pdf")
                os.close(temp_fd)
                new_doc.save(temp_path)
            
            # Close the current document
            self.doc.close()
            
            # Open the new document
            self.doc = fitz.open(temp_path)
            
            # Clean up the temporary file
            os.unlink(temp_path)
            
            return True
        except Exception as e:
            logger.error(f"Error deleting page: {e}")
            return False
    
    def save_pdf(self, save_path=None):
        """Save the PDF to a file.
        
        Args:
            save_path (str, optional): Path to save the PDF. If None, uses the original path.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc:
            return False
        
        try:
            path = save_path if save_path else self.file_path
            current_path = os.path.abspath(path)
            
            # Create a temporary file
            fd, temp_path = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)
            
            # Save to the temporary file
            self.doc.save(temp_path)
            
            # Create a backup of the original file if it exists
            backup_path = None
            if os.path.exists(current_path):
                backup_fd, backup_path = tempfile.mkstemp(suffix=".pdf.bak")
                os.close(backup_fd)
                shutil.copy2(current_path, backup_path)
            
            try:
                # Close the document
                self.doc.close()
                
                # Move the temporary file to the destination
                shutil.move(temp_path, current_path)
                
                # Reopen the document
                self.doc = fitz.open(current_path)
                
                # Remove the backup if everything went well
                if backup_path and os.path.exists(backup_path):
                    os.unlink(backup_path)
                
                if save_path:  # Update file path if saving to a new location
                    self.file_path = save_path
                
                return True
            except Exception as e:
                # If something went wrong and we have a backup, restore it
                if backup_path and os.path.exists(backup_path):
                    if os.path.exists(current_path):
                        os.unlink(current_path)
                    shutil.move(backup_path, current_path)
                    
                # Reopen the original document
                if self.file_path:
                    self.doc = fitz.open(self.file_path)
                
                raise e
                
        except Exception as e:
            logger.error(f"Error saving PDF: {e}")
            return False
    
    def close(self):
        """Close the current PDF document."""
        if self.doc:
            self.doc.close()
            self.doc = None
            self.file_path = None
            self.current_file = None
