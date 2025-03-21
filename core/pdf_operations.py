"""
Core PDF operations for the miniPDF application.
"""
import os
from PyPDF2 import PdfReader, PdfWriter
import tempfile

class PDFOperations:
    """Class for handling PDF operations like rotation, extraction, etc."""
    
    @staticmethod
    def rotate_page(pdf_file, page_index, angle):
        """
        Rotate a specific page in a PDF file.
        
        Args:
            pdf_file (str): Path to the PDF file
            page_index (int): Index of the page to rotate
            angle (int): Rotation angle (90, 180, 270)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            # Copy all pages to the writer
            for i, page in enumerate(reader.pages):
                if i == page_index:
                    # Rotate the specified page
                    page.rotate(angle)
                writer.add_page(page)
            
            # Save the rotated PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_path = temp_file.name
            
            with open(temp_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Replace the original file with the modified one
            os.replace(temp_path, pdf_file)
            return True
        except Exception as e:
            print(f"Error rotating page: {e}")
            return False
    
    @staticmethod
    def extract_page(pdf_file, page_index, output_path):
        """
        Extract a specific page from a PDF file and save it as a new PDF.
        
        Args:
            pdf_file (str): Path to the PDF file
            page_index (int): Index of the page to extract
            output_path (str): Path to save the extracted page
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            # Add the specified page to the writer
            writer.add_page(reader.pages[page_index])
            
            # Save the extracted page to the output file
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Error extracting page: {e}")
            return False
    
    @staticmethod
    def add_blank_page(pdf_file, width=595, height=842):
        """
        Add a blank page to a PDF file.
        
        Args:
            pdf_file (str): Path to the PDF file
            width (int): Width of the blank page (default: A4 width in points)
            height (int): Height of the blank page (default: A4 height in points)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            # Copy all existing pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Add a blank page
            writer.add_blank_page(width, height)
            
            # Save the modified PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_path = temp_file.name
            
            with open(temp_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Replace the original file with the modified one
            os.replace(temp_path, pdf_file)
            return True
        except Exception as e:
            print(f"Error adding blank page: {e}")
            return False
    
    @staticmethod
    def parse_page_range(page_range_str, total_pages):
        """
        Parse a page range string into a list of page indices.
        
        Args:
            page_range_str (str): Page range string (e.g., "1-3,5,7-9")
            total_pages (int): Total number of pages in the PDF
            
        Returns:
            list: List of page indices
        """
        page_indices = []
        
        # Split by comma
        parts = page_range_str.split(',')
        
        for part in parts:
            part = part.strip()
            
            # Check if it's a range (contains '-')
            if '-' in part:
                start, end = part.split('-')
                try:
                    start_idx = int(start.strip()) - 1  # Convert to 0-based index
                    end_idx = int(end.strip()) - 1
                    
                    # Validate range
                    if 0 <= start_idx <= end_idx < total_pages:
                        page_indices.extend(range(start_idx, end_idx + 1))
                except ValueError:
                    # Skip invalid ranges
                    continue
            else:
                # Single page
                try:
                    page_idx = int(part) - 1  # Convert to 0-based index
                    if 0 <= page_idx < total_pages:
                        page_indices.append(page_idx)
                except ValueError:
                    # Skip invalid page numbers
                    continue
        
        return sorted(page_indices)
