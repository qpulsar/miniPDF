"""
Main application window for the PDF Editor.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QFileDialog, QMessageBox, QStatusBar, QMenuBar)
from PyQt6.QtCore import Qt
from .toolbar import Toolbar
from .sidebar import Sidebar
from .preview import PDFPreview
from core.pdf_manager import PDFManager
from .menu import MenuBar

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
        
        # Create menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
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
        
    def on_open(self):
        """Handle open file action."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.open_pdf(file_path):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    self.preview.show_page(0)
                self.status_bar.showMessage(f"Opened {file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not open PDF file."
                )
                
    def on_save(self):
        """Handle save action."""
        if not self.pdf_manager.file_path:
            self.on_save_as()
            return
            
        if self.pdf_manager.save_pdf():
            self.status_bar.showMessage("File saved successfully")
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not save PDF file."
            )
            
    def on_save_as(self):
        """Handle save as action."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.save_pdf_as(file_path):
                self.status_bar.showMessage(f"File saved as {file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not save PDF file."
                )
                
    def on_print(self):
        """Handle print action."""
        QMessageBox.information(
            self,
            "Info",
            "Printing will be implemented in a future version."
        )
        
    def on_add_page(self):
        """Handle add page action."""
        QMessageBox.information(
            self,
            "Info",
            "Page addition will be implemented in a future version."
        )
        
    def on_delete_page(self):
        """Handle delete page action."""
        if not self.pdf_manager.doc:
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to delete."
            )
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this page?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.pdf_manager.delete_page(current_page):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    new_page = min(current_page, self.pdf_manager.get_page_count() - 1)
                    self.preview.show_page(new_page)
                    self.sidebar.setCurrentRow(new_page)
                self.status_bar.showMessage("Page deleted")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not delete page."
                )
                
    def on_rotate_page(self, angle):
        """Handle rotate page action."""
        if not self.pdf_manager.doc:
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to rotate."
            )
            return
            
        if self.pdf_manager.rotate_page(current_page, angle):
            self.preview.show_page(current_page)
            self.status_bar.showMessage(f"Page rotated by {angle}°")
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not rotate page."
            )
            
    def on_move_page(self):
        """Handle move page action."""
        QMessageBox.information(
            self,
            "Info",
            "Page moving will be implemented in a future version."
        )
        
    def on_export_page(self):
        """Handle export page action."""
        QMessageBox.information(
            self,
            "Info",
            "Page export will be implemented in a future version."
        )
        
    def on_add_text(self):
        """Handle add text action."""
        QMessageBox.information(
            self,
            "Info",
            "Text addition will be implemented in a future version."
        )
        
    def on_draw(self):
        """Handle draw action."""
        QMessageBox.information(
            self,
            "Info",
            "Drawing will be implemented in a future version."
        )
        
    def on_highlight(self):
        """Handle highlight action."""
        QMessageBox.information(
            self,
            "Info",
            "Highlighting will be implemented in a future version."
        )
        
    def on_delete_annotation(self):
        """Handle delete annotation action."""
        QMessageBox.information(
            self,
            "Info",
            "Annotation deletion will be implemented in a future version."
        )
        
    def on_ocr(self):
        """Handle OCR action."""
        QMessageBox.information(
            self,
            "Info",
            "OCR will be implemented in a future version."
        )
        
    def on_merge(self):
        """Handle merge PDFs action."""
        QMessageBox.information(
            self,
            "Info",
            "PDF merging will be implemented in a future version."
        )
        
    def on_split(self):
        """Handle split PDF action."""
        QMessageBox.information(
            self,
            "Info",
            "PDF splitting will be implemented in a future version."
        )
        
    def on_encrypt(self):
        """Handle encrypt PDF action."""
        QMessageBox.information(
            self,
            "Info",
            "PDF encryption will be implemented in a future version."
        )
        
    def on_decrypt(self):
        """Handle decrypt PDF action."""
        QMessageBox.information(
            self,
            "Info",
            "PDF decryption will be implemented in a future version."
        )
        
    def on_zoom_in(self):
        """Handle zoom in action."""
        self.toolbar.view_tab.zoom_in()
        
    def on_zoom_out(self):
        """Handle zoom out action."""
        self.toolbar.view_tab.zoom_out()
        
    def on_fit_width(self):
        """Handle fit width action."""
        QMessageBox.information(
            self,
            "Info",
            "Fit width will be implemented in a future version."
        )
        
    def on_page_layout(self, layout):
        """Handle page layout change."""
        QMessageBox.information(
            self,
            "Info",
            "Page layout will be implemented in a future version."
        )
        
    def on_theme(self, theme):
        """Handle theme change."""
        QMessageBox.information(
            self,
            "Info",
            "Theme change will be implemented in a future version."
        )
        
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
