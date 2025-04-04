"""
Text extraction and OCR operations for PDF files.
"""
import fitz  # PyMuPDF
import os
from PIL import Image
from tkinter import messagebox
import logging

# Logging ayarları
logger = logging.getLogger(__name__)


class TextExtractor:
    """Class for extracting text and images from PDF files."""

    def __init__(self):
        """Initialize the text extractor."""
        pass

    def extract_text_from_page(self, page):
        """Extract text from a PDF page.

        Args:
            page: PyMuPDF Page object

        Returns:
            str: Extracted text
        """
        if page:
            return page.get_text()
        return ""

    def extract_text_from_document(self, doc):
        """Extract text from an entire PDF document.

        Args:
            doc: PyMuPDF Document object

        Returns:
            list: List of strings, one per page
        """
        if not doc:
            return []

        text_by_page = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_by_page.append(page.get_text())

        return text_by_page

    def extract_text(self, doc, scope="all_pages", page_index=None):
        """Extract text based on scope.

        Args:
            doc: PyMuPDF Document object
            scope (str): 'current_page' or 'all_pages'
            page_index (int, optional): Index of the current page if scope is 'current_page'

        Returns:
            str: Extracted text
        """
        if not doc:
            return ""

        try:
            if scope == "current_page" and page_index is not None:
                # Extract text from the selected page
                page = doc[page_index]
                return self.extract_text_from_page(page)
            else:
                # Extract text from all pages
                text_by_page = self.extract_text_from_document(doc)

                # Format the text with page numbers
                formatted_text = ""
                for i, page_text in enumerate(text_by_page):
                    formatted_text += f"--- Page {i + 1} ---\n\n"
                    formatted_text += page_text
                    formatted_text += "\n\n"

                return formatted_text
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return f"Error extracting text: {e}"

    def save_text_to_file(self, text, file_path):
        """Save extracted text to a file.

        Args:
            text (str): Text to save
            file_path (str): Path to save the text file

        Returns:
            bool: True if successful, False otherwise
        """
        if not text or not file_path:
            return False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            logger.error(f"Error saving text to file: {e}")
            return False

    def search_text(self, doc, search_string):
        """Search for text in a PDF document.

        Args:
            doc: PyMuPDF Document object
            search_string (str): Text to search for

        Returns:
            list: List of tuples (page_num, instances) where instances is a list of matches
        """
        if not doc or not search_string:
            return []

        results = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            instances = page.search_for(search_string)
            if instances:
                results.append((page_num, instances))

        return results

    def extract_page_as_image(self, page, zoom=1.0):
        """Extract a PDF page as an image.

        Args:
            page: PyMuPDF Page object
            zoom (float): Zoom factor for the image (default: 1.0)

        Returns:
            PIL.Image: Extracted image or None if failed
        """
        try:
            if not page:
                return None

            # Get the page's matrix for the specified zoom
            mat = fitz.Matrix(zoom, zoom)

            # Get the pixmap
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            return img

        except Exception as e:
            logger.error(f"Error extracting page as image: {e}")
            return None

    def save_page_as_image(self, page, file_path, zoom=1.0):
        """Save a PDF page as an image file.

        Args:
            page: PyMuPDF Page object
            file_path (str): Path to save the image
            zoom (float): Zoom factor for the image (default: 1.0)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Extract the image
            img = self.extract_page_as_image(page, zoom)
            if img is None:
                return False

            # Save the image
            img.save(file_path)
            return True

        except Exception as e:
            logger.error(f"Error saving page as image: {e}")
            return False

    def save_pages_as_images(self, doc, output_dir, start_page=None, end_page=None, zoom=1.0):
        """Save multiple PDF pages as image files.

        Args:
            doc: PyMuPDF Document object
            output_dir (str): Directory to save the images
            start_page (int, optional): Start page index (0-based)
            end_page (int, optional): End page index (exclusive)
            zoom (float): Zoom factor for the images (default: 1.0)

        Returns:
            tuple: (success_count, total_count, error_messages)
        """
        if not doc or not output_dir:
            return 0, 0, ["Invalid document or output directory"]

        # Sayfa aralığını ayarla
        if start_page is None:
            start_page = 0
        if end_page is None:
            end_page = len(doc)

        success_count = 0
        error_messages = []
        total_count = end_page - start_page

        try:
            # Çıktı klasörünü oluştur (yoksa)
            os.makedirs(output_dir, exist_ok=True)

            # Her sayfayı dışa aktar
            for page_num in range(start_page, end_page):
                try:
                    page = doc[page_num]
                    output_path = os.path.join(output_dir, f"sayfa_{page_num + 1}.png")

                    if self.save_page_as_image(page, output_path, zoom):
                        success_count += 1
                    else:
                        error_messages.append(f"Sayfa {page_num + 1} kaydedilemedi")

                except Exception as e:
                    error_messages.append(f"Sayfa {page_num + 1}: {str(e)}")

            return success_count, total_count, error_messages

        except Exception as e:
            logger.error(f"Error in batch image export: {e}")
            return success_count, total_count, [str(e)]

    # Note: For actual OCR functionality, you would need to integrate
    # with a library like pytesseract or a cloud OCR service.
    def perform_ocr(self, page):
        """Placeholder for OCR functionality.

        This would require integration with an OCR library like pytesseract.

        Args:
            page: PyMuPDF Page object

        Returns:
            str: OCR extracted text (placeholder)
        """
        # This is a placeholder. In a real implementation, you would:
        # 1. Convert the page to an image
        # 2. Use an OCR library to extract text
        # 3. Return the extracted text
        return "OCR functionality requires integration with an OCR library"