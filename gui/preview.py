"""
PDF preview widget.
"""
from PyQt6.QtWidgets import QScrollArea, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, QPointF
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor
import pymupdf

class PDFPreview(QScrollArea):
    """Widget for displaying PDF pages."""
    
    def __init__(self, parent=None):
        """Initialize the widget."""
        super().__init__(parent)
        self.app = parent
        
        # Set up the UI
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create content widget
        content = QWidget()
        self.setWidget(content)
        
        # Create layout
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create label for displaying the page
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.page_label)
        
        # Initialize variables
        self.current_page = None
        self.current_zoom = 1.0
        self.scale_factor = 2.0  # Higher quality rendering
        
        # Drawing state
        self.drawing = False
        self.drawing_points = []
        self.current_stroke = []
        
        # Annotation state
        self.annotation_mode = None
        self.annotation_color = None
        self.annotation_width = None
        self.annotation_text = None
        self.start_pos = None
        
        # Connect events
        self.page_label.mousePressEvent = self.on_mouse_press
        self.page_label.mouseMoveEvent = self.on_mouse_move
        self.page_label.mouseReleaseEvent = self.on_mouse_release
        
    def show_page(self, page_num):
        """Display a page from the PDF.
        
        Args:
            page_num: Page number to display (0-based)
        """
        if not self.app.pdf_manager.doc:
            return
            
        page = self.app.pdf_manager.get_page(page_num)
        if not page:
            return
            
        self.current_page = page_num
        
        # Get page pixmap
        mat = pymupdf.Matrix(self.scale_factor * self.current_zoom,
                         self.scale_factor * self.current_zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to QImage
        img = QImage(pix.samples, pix.width, pix.height,
                    pix.stride, QImage.Format.Format_RGB888)
        
        # Create pixmap and display
        pixmap = QPixmap.fromImage(img)
        self.page_label.setPixmap(pixmap)
        
        # Update size
        self.update_size()
        
    def update_size(self):
        """Update widget size based on page and zoom."""
        if not self.page_label.pixmap():
            return
            
        # Get available space
        viewport = self.viewport().size()
        pixmap = self.page_label.pixmap()
        
        # Calculate scaled size
        scaled_size = pixmap.size()
        if scaled_size.width() > viewport.width():
            scaled_size.setHeight(int(scaled_size.height() *
                                   viewport.width() / scaled_size.width()))
            scaled_size.setWidth(viewport.width())
            
        # Update label size
        self.page_label.setMinimumSize(scaled_size)
        self.page_label.setMaximumSize(scaled_size)
        
    def set_zoom(self, zoom):
        """Set zoom level.
        
        Args:
            zoom: Zoom factor (1.0 = 100%)
        """
        self.current_zoom = zoom
        if self.current_page is not None:
            self.show_page(self.current_page)
            
    def start_text_annotation(self, color, text):
        """Start text annotation mode.
        
        Args:
            color: Annotation color
            text: Text content
        """
        self.annotation_mode = "text"
        self.annotation_color = color
        self.annotation_text = text
        self.start_pos = None
        
    def start_highlight_annotation(self, color):
        """Start highlight annotation mode.
        
        Args:
            color: Highlight color
        """
        self.annotation_mode = "highlight"
        self.annotation_color = color
        self.start_pos = None
        
    def start_ink_annotation(self, color, width):
        """Start ink annotation mode.
        
        Args:
            color: Ink color
            width: Line width
        """
        self.annotation_mode = "ink"
        self.annotation_color = color
        self.annotation_width = width
        self.drawing = False
        self.drawing_points = []
        self.current_stroke = []
        
    def stop_annotation(self):
        """Stop annotation mode."""
        self.annotation_mode = None
        self.annotation_color = None
        self.annotation_width = None
        self.annotation_text = None
        self.start_pos = None
        self.drawing = False
        self.drawing_points = []
        self.current_stroke = []
        
    def on_mouse_press(self, event):
        """Handle mouse press event."""
        if not self.annotation_mode or self.current_page is None:
            return
            
        pos = self.get_page_coordinates(event.pos())
        
        if self.annotation_mode == "ink":
            self.drawing = True
            self.current_stroke = [pos]
        else:
            self.start_pos = pos
            
    def on_mouse_move(self, event):
        """Handle mouse move event."""
        if not self.annotation_mode or self.current_page is None:
            return
            
        if self.annotation_mode == "ink" and self.drawing:
            pos = self.get_page_coordinates(event.pos())
            self.current_stroke.append(pos)
            self.update_preview()
            
    def on_mouse_release(self, event):
        """Handle mouse release event."""
        if not self.annotation_mode or self.current_page is None:
            return
            
        pos = self.get_page_coordinates(event.pos())
        
        if self.annotation_mode == "ink":
            if self.drawing:
                self.drawing = False
                self.current_stroke.append(pos)
                self.drawing_points.append(self.current_stroke)
                self.current_stroke = []
                
                # Add ink annotation
                if self.drawing_points:
                    color = (self.annotation_color.redF(),
                            self.annotation_color.greenF(),
                            self.annotation_color.blueF())
                    self.app.pdf_manager.add_ink_annotation(
                        self.current_page,
                        self.drawing_points,
                        color=color,
                        width=self.annotation_width
                    )
                    self.drawing_points = []
                    self.show_page(self.current_page)
        else:
            if self.start_pos:
                # Create rectangle
                x0 = min(self.start_pos.x(), pos.x())
                y0 = min(self.start_pos.y(), pos.y())
                x1 = max(self.start_pos.x(), pos.x())
                y1 = max(self.start_pos.y(), pos.y())
                rect = (x0, y0, x1, y1)
                
                # Add annotation
                color = (self.annotation_color.redF(),
                        self.annotation_color.greenF(),
                        self.annotation_color.blueF())
                if self.annotation_mode == "text":
                    self.app.pdf_manager.add_text_annotation(
                        self.current_page,
                        rect,
                        self.annotation_text,
                        color=color
                    )
                else:  # highlight
                    self.app.pdf_manager.add_highlight_annotation(
                        self.current_page,
                        rect,
                        color=color
                    )
                    
                self.start_pos = None
                self.show_page(self.current_page)
                
    def get_page_coordinates(self, pos):
        """Convert widget coordinates to page coordinates.
        
        Args:
            pos: Position in widget coordinates
            
        Returns:
            QPointF: Position in page coordinates
        """
        if not self.page_label.pixmap():
            return QPointF()
            
        # Get page size
        page = self.app.pdf_manager.get_page(self.current_page)
        if not page:
            return QPointF()
            
        # Calculate scale factors
        pixmap = self.page_label.pixmap()
        scale_x = page.rect.width / pixmap.width()
        scale_y = page.rect.height / pixmap.height()
        
        # Convert coordinates
        x = pos.x() * scale_x
        y = pos.y() * scale_y
        
        return QPointF(x, y)
        
    def update_preview(self):
        """Update preview with current drawing."""
        if not self.page_label.pixmap():
            return
            
        # Create working copy of the page
        pixmap = self.page_label.pixmap().copy()
        painter = QPainter(pixmap)
        
        # Set up pen
        if self.annotation_color:
            pen = QPen(self.annotation_color)
            if self.annotation_mode == "ink":
                pen.setWidthF(self.annotation_width * self.scale_factor)
            painter.setPen(pen)
            
        # Draw current stroke
        if self.current_stroke:
            path = [self.get_widget_coordinates(p) for p in self.current_stroke]
            for i in range(len(path) - 1):
                painter.drawLine(path[i], path[i + 1])
                
        painter.end()
        self.page_label.setPixmap(pixmap)
        
    def get_widget_coordinates(self, pos):
        """Convert page coordinates to widget coordinates.
        
        Args:
            pos: Position in page coordinates
            
        Returns:
            QPointF: Position in widget coordinates
        """
        if not self.page_label.pixmap():
            return QPointF()
            
        # Get page size
        page = self.app.pdf_manager.get_page(self.current_page)
        if not page:
            return QPointF()
            
        # Calculate scale factors
        pixmap = self.page_label.pixmap()
        scale_x = pixmap.width() / page.rect.width
        scale_y = pixmap.height() / page.rect.height
        
        # Convert coordinates
        x = pos.x() * scale_x
        y = pos.y() * scale_y
        
        return QPointF(x, y)
