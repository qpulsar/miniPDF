"""
Security operations for PDF files in the miniPDF application.
"""
import os
from PyPDF2 import PdfReader, PdfWriter
import tempfile

class PDFSecurity:
    """Class for handling PDF security operations like encryption and decryption."""
    
    @staticmethod
    def encrypt_pdf(pdf_file, user_password, owner_password=None):
        """
        Encrypt a PDF file with passwords.
        
        Args:
            pdf_file (str): Path to the PDF file
            user_password (str): Password for opening the PDF
            owner_password (str, optional): Password for full access to the PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()
            
            # Copy all pages to the writer
            for page in reader.pages:
                writer.add_page(page)
            
            # Use the same password for both if owner_password is not provided
            if not owner_password:
                owner_password = user_password
            
            # Encrypt the PDF
            writer.encrypt(user_password, owner_password)
            
            # Save the encrypted PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_path = temp_file.name
            
            with open(temp_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Replace the original file with the encrypted one
            os.replace(temp_path, pdf_file)
            return True
        except Exception as e:
            print(f"Error encrypting PDF: {e}")
            return False
    
    @staticmethod
    def decrypt_pdf(pdf_file, password):
        """
        Decrypt a PDF file using the provided password.
        
        Args:
            pdf_file (str): Path to the PDF file
            password (str): Password to decrypt the PDF
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            reader = PdfReader(pdf_file)
            
            # Check if the PDF is encrypted
            if not reader.is_encrypted:
                print("PDF is not encrypted")
                return False
            
            # Try to decrypt with the provided password
            if not reader.decrypt(password):
                print("Incorrect password")
                return False
            
            writer = PdfWriter()
            
            # Copy all pages to the writer
            for page in reader.pages:
                writer.add_page(page)
            
            # Save the decrypted PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_path = temp_file.name
            
            with open(temp_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Replace the original file with the decrypted one
            os.replace(temp_path, pdf_file)
            return True
        except Exception as e:
            print(f"Error decrypting PDF: {e}")
            return False
