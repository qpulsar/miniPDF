"""
PDF preview implementation for the PDF Editor.
"""
from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage
import fitz

class PDFPreview(QScrollArea):
    """Widget for displaying PDF pages."""
    
    def __init__(self, parent=None):
        """Initialize preview widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        
        # Create widget to hold content
        self.content = QWidget()
        self.setWidget(self.content)
        self.setWidgetResizable(True)
        
        # Create layout
        self.layout = QVBoxLayout(self.content)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create label for displaying page
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.page_label)
        
        # Set background color
        self.setStyleSheet("background-color: #f0f0f0;")
        
    def show_page(self, page_num):
        """Display a specific page.
        
        Args:
            page_num: Page number to display (0-based)
        """
        if not self.parent.pdf_manager.doc:
            return
            
        page = self.parent.pdf_manager.get_page(page_num)
        if not page:
            return
            
        # Get page pixmap
        mat = fitz.Matrix(2, 2)  # 2x zoom
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to QImage
        img = QImage(pix.samples, pix.width, pix.height,
                    pix.stride, QImage.Format.Format_RGB888)
                    
        # Create pixmap and set to label
        pixmap = QPixmap.fromImage(img)
        self.page_label.setPixmap(pixmap)
        
        # Update status bar
        self.parent.status_bar.showMessage(
            f"Page {page_num + 1} of {self.parent.pdf_manager.get_page_count()}"
        )
