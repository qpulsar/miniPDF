"""
Main application window for the PDF Editor.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QFileDialog, QMessageBox, QStatusBar)
from PyQt6.QtCore import Qt
from .toolbar import Toolbar
from .sidebar import Sidebar
from .preview import PDFPreview
from core.pdf_manager import PDFManager

class PDFEditorApp(QMainWindow):
    """Main window class for the PDF Editor application."""
    
    def __init__(self):
        """Initialize the application window."""
        super().__init__()
        
        # Initialize PDF manager
        self.pdf_manager = PDFManager()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
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
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "PDF Dosyası Aç",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.open_pdf(file_path):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    self.preview.show_page(0)
                self.status_bar.showMessage(f"Opened: {file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not open PDF file."
                )
                
    def save_pdf(self):
        """Save the current PDF file."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "No PDF file is open."
            )
            return False
            
        if self.pdf_manager.file_path:
            if self.pdf_manager.save_pdf():
                self.status_bar.showMessage(f"Saved: {self.pdf_manager.file_path}")
                return True
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not save PDF file."
                )
                return False
                
        return self.save_pdf_as()
        
    def save_pdf_as(self):
        """Save the current PDF file with a new name."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "No PDF file is open."
            )
            return False
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF File As",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.save_pdf_as(file_path):
                self.status_bar.showMessage(f"Saved: {file_path}")
                return True
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not save PDF file."
                )
        return False
        
    def closeEvent(self, event):
        """Handle window close event."""
        if self.pdf_manager.doc and self.pdf_manager.has_changes():
            reply = QMessageBox.question(
                self,
                "Save Changes?",
                "The PDF file has unsaved changes. Do you want to save them?",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            elif reply == QMessageBox.StandardButton.Yes:
                if not self.save_pdf():
                    event.ignore()
                    return
                    
        event.accept()
