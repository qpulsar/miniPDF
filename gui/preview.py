"""
PDF preview implementation for the PDF Editor.
"""
from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QSizePolicy
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
        self.current_page = None
        self.current_zoom = 1.0
        
        # Create widget to hold content
        self.content = QWidget()
        self.setWidget(self.content)
        self.setWidgetResizable(True)
        
        # Create layout
        self.layout = QVBoxLayout(self.content)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.layout.addWidget(self.image_label)
        
        # Set background color
        self.setStyleSheet("background-color: #f0f0f0;")
        
    def show_page(self, page_num, zoom=None):
        """Display a specific page.
        
        Args:
            page_num: Page number to display (0-based)
            zoom: Optional zoom factor (1.0 = 100%)
        """
        if zoom is not None:
            self.current_zoom = zoom
            
        self.current_page = page_num
        if not self.parent.pdf_manager.doc:
            return
            
        page = self.parent.pdf_manager.get_page(page_num)
        if not page:
            return
            
        # Get page pixmap
        mat = fitz.Matrix(2.0 * self.current_zoom, 2.0 * self.current_zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to QImage
        img = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            QImage.Format.Format_RGB888
        )
        
        # Display image
        pixmap = QPixmap.fromImage(img)
        self.image_label.setPixmap(pixmap)
        self.image_label.setMinimumSize(1, 1)
        
        # Update status bar
        self.parent.status_bar.showMessage(
            f"Page {page_num + 1} of {self.parent.pdf_manager.get_page_count()}"
        )

    def clear(self):
        """Clear the preview."""
        self.image_label.clear()
        self.current_page = None
