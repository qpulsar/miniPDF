"""
Main application GUI for the PDF Editor.
"""
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                           QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox,
                           QStatusBar)
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

from gui.toolbar import Toolbar
from gui.sidebar import Sidebar
from gui.preview import PDFPreview
from core.pdf_manager import PDFManager
import config

class PDFEditorApp(QMainWindow):
    """Main application class for the PDF Editor."""
    
    def __init__(self):
        """Initialize the PDF Editor application."""
        super().__init__()
        
        # Initialize PDF manager
        self.pdf_manager = PDFManager()
        
        # Setup UI
        self.setup_ui()
        
        # Apply material theme
        apply_stylesheet(self, theme='dark_teal.xml')
        
    def setup_ui(self):
        """Setup the main user interface."""
        self.setWindowTitle("miniPDF Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        self.toolbar = Toolbar(self)
        main_layout.addWidget(self.toolbar)
        
        # Create content area with sidebar and preview
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        main_layout.addWidget(content_widget)
        
        # Create sidebar for page list
        self.sidebar = Sidebar(self)
        content_layout.addWidget(self.sidebar)
        
        # Create preview area
        self.preview = PDFPreview(self)
        content_layout.addWidget(self.preview)
        
        # Set content layout stretch factors
        content_layout.setStretch(0, 1)  # Sidebar
        content_layout.setStretch(1, 4)  # Preview
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def open_pdf(self):
        """Open a PDF file."""
        file_path = self.get_open_filename("Open PDF File", [("PDF Files", "*.pdf")])
        if file_path:
            if self.pdf_manager.open_pdf(file_path):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    self.preview.show_page(0)
                self.status_bar.showMessage(f"Opened: {file_path}")
            else:
                self.show_error("Error", "Failed to open the PDF file.")
    
    def save_pdf(self):
        """Save the current PDF file."""
        if not self.pdf_manager.doc:
            self.show_info("Info", "No PDF file is currently open.")
            return
            
        # If we have a current file path, save directly to it
        if self.pdf_manager.file_path:
            if self.pdf_manager.save_pdf():
                self.status_bar.showMessage(f"Saved: {self.pdf_manager.file_path}")
                self.show_info("Success", "PDF file saved successfully.")
            else:
                self.show_error("Error", "Failed to save the PDF file.")
            return
        
        # If no current file path, show save dialog
        self.save_pdf_as()

    def save_pdf_as(self):
        """Save the current PDF file with a new name."""
        if not self.pdf_manager.doc:
            self.show_info("Info", "No PDF file is currently open.")
            return
            
        save_path = self.get_save_filename("Save PDF File", [("PDF Files", "*.pdf")])
        
        if save_path:
            if self.pdf_manager.save_pdf(save_path):
                self.status_bar.showMessage(f"Saved: {save_path}")
                self.show_info("Success", "PDF file saved successfully.")
            else:
                self.show_error("Error", "Failed to save the PDF file.")
    
    def delete_current_page(self):
        """Delete the currently selected page."""
        if not self.pdf_manager.doc:
            self.show_info("Info", "No PDF file is currently open.")
            return
            
        current_page = self.sidebar.get_selected_page_index()
        if current_page is None:
            self.show_info("Info", "No page selected.")
            return
            
        if QMessageBox.Yes == QMessageBox.question(self, "Confirm", "Are you sure you want to delete this page?"):
            if self.pdf_manager.delete_page(current_page):
                self.sidebar.update_page_list()
                
                # Select a new page if available
                page_count = self.pdf_manager.get_page_count()
                if page_count > 0:
                    new_index = min(current_page, page_count - 1)
                    self.sidebar.select_page(new_index)
                    self.preview.show_page(new_index)
                else:
                    self.preview.clear()
                
                self.status_bar.showMessage("Page deleted")
            else:
                self.show_error("Error", "Failed to delete the page.")
    
    def on_closing(self):
        """Handle application closing."""
        if self.pdf_manager.doc:
            if QMessageBox.Yes == QMessageBox.question(self, "Confirm", "Do you want to save changes before exiting?"):
                self.save_pdf()
            self.pdf_manager.close()
        
        self.close()
    
    def reload_pdf(self):
        """Reload the current PDF file to reflect changes."""
        if self.pdf_manager.current_file:
            current_page_index = self.preview.current_page_index
            
            # Reopen the PDF file
            if self.pdf_manager.open_pdf(self.pdf_manager.current_file):
                self.sidebar.update_page_list()
                
                # Try to show the same page that was being viewed
                page_count = self.pdf_manager.get_page_count()
                if page_count > 0:
                    # Make sure the page index is valid
                    if current_page_index is not None and current_page_index < page_count:
                        self.preview.show_page(current_page_index)
                    else:
                        # Show the first page if the previous page is no longer valid
                        self.preview.show_page(0)
                else:
                    self.preview.clear()
                    
                self.status_bar.showMessage(f"Reloaded: {self.pdf_manager.current_file}")
            else:
                self.show_error("Error", "Failed to reload the PDF file.")

    def show_error(self, title, message):
        """Show error message dialog.
        
        Args:
            title (str): Dialog title
            message (str): Error message
        """
        QMessageBox.critical(self, title, message)
        
    def show_info(self, title, message):
        """Show information message dialog.
        
        Args:
            title (str): Dialog title
            message (str): Information message
        """
        QMessageBox.information(self, title, message)
        
    def get_open_filename(self, title, filetypes):
        """Show file open dialog.
        
        Args:
            title (str): Dialog title
            filetypes (list): List of file type tuples (description, extension)
            
        Returns:
            str: Selected filename or empty string if cancelled
        """
        filters = ";;".join([f"{desc} ({ext})" for desc, ext in filetypes])
        filename, _ = QFileDialog.getOpenFileName(self, title, "", filters)
        return filename
        
    def get_save_filename(self, title, filetypes):
        """Show file save dialog.
        
        Args:
            title (str): Dialog title
            filetypes (list): List of file type tuples (description, extension)
            
        Returns:
            str: Selected filename or empty string if cancelled
        """
        filters = ";;".join([f"{desc} ({ext})" for desc, ext in filetypes])
        filename, _ = QFileDialog.getSaveFileName(self, title, "", filters)
        return filename

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = PDFEditorApp()
    window.show()
    sys.exit(app.exec())
