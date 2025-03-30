"""
PDF preview widget.
"""
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen

class PDFPreview(QScrollArea):
    """Widget for displaying PDF pages."""
    
    # Signals for annotation events
    annotation_added = pyqtSignal(int, object)  # page_num, annotation
    
    def __init__(self, parent=None):
        """Initialize preview widget."""
        super().__init__(parent)
        
        # Set up scrolling
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create container widget
        self.container = QWidget()
        self.setWidget(self.container)
        
        # Create layout
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create label for displaying page
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.page_label)
        
        # Initialize variables
        self.current_page = None
        self.current_zoom = 1.0
        self.current_pixmap = None
        self.drawing = False
        self.last_point = None
        self.annotation_mode = None
        self.annotation_color = None
        self.annotation_text = None
        self.annotation_width = None
        
    def set_zoom(self, zoom):
        """Set zoom level."""
        self.current_zoom = zoom
        if self.current_pixmap:
            self.update_display()
            
    def fit_width(self):
        """Fit page to window width."""
        if self.current_pixmap:
            available_width = self.width() - self.verticalScrollBar().width() - 20
            zoom = available_width / self.current_pixmap.width()
            self.set_zoom(zoom)
            
    def fit_screen(self):
        """Fit page to screen."""
        if self.current_pixmap:
            available_width = self.width() - self.verticalScrollBar().width() - 20
            available_height = self.height() - self.horizontalScrollBar().height() - 20
            zoom_width = available_width / self.current_pixmap.width()
            zoom_height = available_height / self.current_pixmap.height()
            self.set_zoom(min(zoom_width, zoom_height))
            
    def update_display(self):
        """Update the display with current zoom level."""
        if self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                self.current_pixmap.width() * self.current_zoom,
                self.current_pixmap.height() * self.current_zoom,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.page_label.setPixmap(scaled_pixmap)
            
    def show_page(self, page_num):
        """Show the specified page.
        
        Args:
            page_num: Page number to display
        """
        if not self.parent().pdf_manager.doc:
            return
            
        # Get page pixmap
        self.current_page = page_num
        self.current_pixmap = self.parent().pdf_manager.get_page_pixmap(page_num)
        
        if self.current_pixmap:
            self.update_display()
            
    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        # Update display to maintain zoom level
        self.update_display()
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            
    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if self.drawing and self.last_point:
            if self.annotation_mode == "ink":
                # Draw line on pixmap
                painter = QPainter(self.current_pixmap)
                painter.setPen(QPen(self.annotation_color, self.annotation_width))
                painter.drawLine(
                    self.last_point / self.current_zoom,
                    event.pos() / self.current_zoom
                )
                painter.end()
                
                # Update display
                self.update_display()
                
            self.last_point = event.pos()
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            
            if self.annotation_mode == "text":
                # Add text annotation
                rect = QRectF(
                    self.last_point.x() / self.current_zoom,
                    self.last_point.y() / self.current_zoom,
                    100,  # Default width
                    50   # Default height
                )
                self.parent().pdf_manager.add_text_annotation(
                    self.current_page,
                    rect,
                    self.annotation_text,
                    self.annotation_color
                )
                
            elif self.annotation_mode == "highlight":
                # Add highlight annotation
                rect = QRectF(
                    self.last_point.x() / self.current_zoom,
                    self.last_point.y() / self.current_zoom,
                    event.pos().x() / self.current_zoom - self.last_point.x() / self.current_zoom,
                    event.pos().y() / self.current_zoom - self.last_point.y() / self.current_zoom
                )
                self.parent().pdf_manager.add_highlight_annotation(
                    self.current_page,
                    rect,
                    self.annotation_color
                )
                
            elif self.annotation_mode == "ink":
                # Add ink annotation
                self.parent().pdf_manager.add_ink_annotation(
                    self.current_page,
                    self.current_pixmap,
                    self.annotation_color,
                    self.annotation_width
                )
                
            # Reset annotation mode
            self.annotation_mode = None
            self.last_point = None
            
            # Refresh display
            self.show_page(self.current_page)
            
    def start_text_annotation(self, color, text):
        """Start text annotation mode."""
        self.annotation_mode = "text"
        self.annotation_color = color
        self.annotation_text = text
        
    def start_highlight_annotation(self, color):
        """Start highlight annotation mode."""
        self.annotation_mode = "highlight"
        self.annotation_color = color
        
    def start_ink_annotation(self, color, width):
        """Start ink annotation mode."""
        self.annotation_mode = "ink"
        self.annotation_color = color
        self.annotation_width = width
