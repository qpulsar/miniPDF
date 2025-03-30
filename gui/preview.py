"""
PDF page preview module.
"""
import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QSlider, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage

class PDFPreview(QScrollArea):
    """Widget for displaying PDF page previews."""
    
    def __init__(self, parent):
        """Initialize the PDF preview widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.app = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Setup preview UI."""
        # Create widget to hold the preview
        self.preview_widget = QWidget()
        self.setWidget(self.preview_widget)
        self.setWidgetResizable(True)
        
        # Create layout
        layout = QVBoxLayout(self.preview_widget)
        
        # Create preview label
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.preview_label)
        
        # Create zoom controls
        zoom_layout = QHBoxLayout()
        self.zoom_label = QLabel("Zoom:")
        zoom_layout.addWidget(self.zoom_label)
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(50)
        self.zoom_slider.setMaximum(200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self._on_zoom_change)
        zoom_layout.addWidget(self.zoom_slider)
        
        self.zoom_value_label = QLabel("100%")
        zoom_layout.addWidget(self.zoom_value_label)
        
        layout.addLayout(zoom_layout)
        
        self.preview_widget.setLayout(layout)
        
        # Store the current image
        self.current_image = None
        self.current_page_index = None
        
    def _on_zoom_change(self):
        """Handle zoom level changes."""
        if self.current_page_index is not None:
            self.show_page(self.current_page_index, self.zoom_slider.value() / 100.0)
        self.zoom_value_label.setText(f"{self.zoom_slider.value()}%")
    
    def show_page(self, page_index, zoom=1.0):
        """Display a PDF page on the preview.
        
        Args:
            page_index (int): Index of the page to display
            zoom (float): Zoom factor for the page
        """
        self.current_page_index = page_index
        page = self.app.pdf_manager.get_page(page_index)
        
        if page:
            # Get page pixmap
            matrix = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert to QImage
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            
            # Convert to QPixmap and display
            pixmap = QPixmap.fromImage(img)
            self.preview_label.setPixmap(pixmap)
            
            # Store the original image
            self.current_image = img
            
    def clear(self):
        """Clear the preview."""
        self.preview_label.clear()
        self.current_image = None
        self.current_page_index = None
