"""
PDF Manager module for handling PDF operations like page deletion, addition, and saving.
"""
import fitz  # PyMuPDF

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
            print(f"Error opening PDF: {e}")
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
            new_doc = fitz.open()
            for i in range(len(self.doc)):
                if i != page_index:
                    new_doc.insert_pdf(self.doc, from_page=i, to_page=i)
            
            # Replace the current document with the new one
            self.doc.close()
            self.doc = new_doc
            return True
        except Exception as e:
            print(f"Error deleting page: {e}")
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
            import os
            current_path = os.path.abspath(path)
            
            # Önce geçici bir dosyaya kaydet
            import tempfile
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, "temp_save.pdf")
            
            # Normal kaydet
            self.doc.save(temp_path)
            
            # Dosyayı kapat
            self.doc.close()
            
            # Geçici dosyayı hedef konuma taşı
            import shutil
            shutil.move(temp_path, current_path)
            
            # Dosyayı tekrar aç
            self.doc = fitz.open(current_path)
            
            if save_path:  # Update file path if saving to a new location
                self.file_path = save_path
            return True
        except Exception as e:
            print(f"Error saving PDF: {e}")
            return False
    
    def close(self):
        """Close the current PDF document."""
        if self.doc:
            self.doc.close()
            self.doc = None
            self.file_path = None
            self.current_file = None
