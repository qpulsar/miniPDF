"""
Module for merging and splitting PDF files.
"""
import fitz  # PyMuPDF
import os

class PDFMergeSplit:
    """Class for merging and splitting PDF files."""
    
    def __init__(self):
        """Initialize the merge/split manager."""
        pass
    
    def merge_pdfs(self, pdf_paths, output_path):
        """Merge multiple PDF files into one.
        
        Args:
            pdf_paths (list): List of paths to PDF files to merge
            output_path (str): Path to save the merged PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not pdf_paths or not output_path:
            return False
        
        try:
            merged_doc = fitz.open()
            
            for pdf_path in pdf_paths:
                if os.path.exists(pdf_path):
                    doc = fitz.open(pdf_path)
                    merged_doc.insert_pdf(doc)
                    doc.close()
            
            merged_doc.save(output_path)
            merged_doc.close()
            return True
        except Exception as e:
            print(f"Error merging PDFs: {e}")
            return False
    
    def split_pdf(self, pdf_path, output_dir, pages_per_file=1):
        """Split a PDF into multiple files.
        
        Args:
            pdf_path (str): Path to the PDF file to split
            output_dir (str): Directory to save the split PDFs
            pages_per_file (int, optional): Number of pages per output file. Defaults to 1.
            
        Returns:
            list: List of paths to the created PDF files or empty list if failed
        """
        if not pdf_path or not output_dir or not os.path.exists(pdf_path):
            return []
        
        try:
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Open the source PDF
            doc = fitz.open(pdf_path)
            total_pages = len(doc)
            
            output_files = []
            file_count = 0
            
            # Calculate how many files we'll create
            file_count_total = (total_pages + pages_per_file - 1) // pages_per_file
            
            for start_page in range(0, total_pages, pages_per_file):
                # Create a new PDF for this chunk
                new_doc = fitz.open()
                
                # Calculate end page for this chunk
                end_page = min(start_page + pages_per_file - 1, total_pages - 1)
                
                # Add pages to the new document
                new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
                
                # Generate output filename
                file_count += 1
                output_filename = os.path.join(
                    output_dir, 
                    f"split_{os.path.basename(pdf_path)}_{file_count:03d}_of_{file_count_total:03d}.pdf"
                )
                
                # Save the new document
                new_doc.save(output_filename)
                new_doc.close()
                
                output_files.append(output_filename)
            
            doc.close()
            return output_files
        except Exception as e:
            print(f"Error splitting PDF: {e}")
            return []
    
    def extract_pages(self, pdf_path, output_path, page_indices):
        """Extract specific pages from a PDF and save as a new PDF.
        
        Args:
            pdf_path (str): Path to the source PDF
            output_path (str): Path to save the new PDF
            page_indices (list): List of page indices to extract
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not pdf_path or not output_path or not page_indices:
            return False
        
        try:
            doc = fitz.open(pdf_path)
            new_doc = fitz.open()
            
            for page_idx in sorted(page_indices):
                if 0 <= page_idx < len(doc):
                    new_doc.insert_pdf(doc, from_page=page_idx, to_page=page_idx)
            
            new_doc.save(output_path)
            new_doc.close()
            doc.close()
            return True
        except Exception as e:
            print(f"Error extracting pages: {e}")
            return False
