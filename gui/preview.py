"""
PDF preview widget for miniPDF.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QScrollArea, QToolButton, QFrame)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QRectF, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QImage
from .utils.icon_utils import IconProvider
from .utils.settings_utils import (
    apply_theme_to_widget, apply_button_styles, 
    save_zoom_level, load_zoom_level
)
from .settings import Settings

class PDFPreview(QWidget):
    """Widget for displaying PDF pages."""
    
    # Signals for annotation events
    annotation_added = pyqtSignal(int, object)  # page_num, annotation
    
    def __init__(self, parent=None):
        """Initialize preview widget."""
        super().__init__(parent)
        self.app = parent
        self.settings = Settings()
        
        # Set up layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create navigation buttons at the top
        self.create_navigation_buttons()
        
        # Create scroll area for page display
        self.create_scroll_area()
        
        # Create page movement buttons at the bottom
        self.create_page_movement_buttons()
        
        # Initialize variables
        self.current_page = None
        self.current_zoom = load_zoom_level() / 100.0  # Kaydedilen zoom oranını yükle (settings_utils kullanarak)
        self.current_pixmap = None
        self.drawing = False
        self.last_point = None
        self.annotation_mode = None
        self.annotation_color = None
        self.annotation_text = None
        self.annotation_width = None
        
        # Tema değişikliklerini dinle
        if parent:
            parent.theme_changed.connect(self.apply_theme)
            
    def apply_theme(self):
        """Tema değişikliklerini uygula."""
        try:
            # Temayı widget'a uygula (settings_utils kullanarak)
            apply_theme_to_widget(self)
            
            # Butonlara stil uygula
            apply_button_styles(self)
            
            # Scroll area ve page container için tema renklerini ayarla
            from .utils.settings_utils import is_dark_theme, get_setting
            
            current_theme = get_setting('theme')
            is_dark = is_dark_theme(current_theme)
            
            if is_dark:
                bg_color = "#1e1e1e"
                text_color = "#ffffff"
            else:
                bg_color = "#e0e0e0"
                text_color = "#000000"
            
            # Update scroll area background
            self.scroll_area.setStyleSheet(f"""
                QScrollArea {{
                    background-color: {bg_color};
                    border: none;
                }}
            """)
            
            # Update page container background
            self.page_container.setStyleSheet(f"background-color: {bg_color};")
            
            # Update page indicator text color
            self.page_indicator.setStyleSheet(f"color: {text_color};")
            
            # Tüm alt bileşenlere tema değişikliklerini uygula
            for child in self.findChildren(QWidget):
                if hasattr(child, 'apply_theme') and callable(child.apply_theme):
                    child.apply_theme()
                    
        except Exception as e:
            print(f"Preview tema güncelleme hatası: {e}")
            import traceback
            print(traceback.format_exc())
        
    def create_navigation_buttons(self):
        """Create navigation buttons at the top of the preview."""
        # Create container for navigation buttons
        nav_container = QWidget()
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(5)
        
        # Add page indicator label
        self.page_indicator = QLabel("Page 0 of 0")
        self.page_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_indicator.setMinimumWidth(100)
        
        # Add buttons to layout
        nav_layout.addWidget(self.page_indicator)

        # Add spacer to push buttons to the center
        nav_layout.addStretch()
        
        # Add container to main layout
        self.layout.addWidget(nav_container)
        
        # Add separator
        self.layout.addWidget(self.create_separator())
        
    def create_scroll_area(self):
        """Create scroll area for page display."""
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #e0e0e0;
                border: none;
            }
        """)
        
        # Create container widget for page display
        self.page_container = QWidget()
        self.page_container.setStyleSheet("background-color: #e0e0e0;")
        self.scroll_area.setWidget(self.page_container)
        
        # Create layout for page container
        self.page_layout = QVBoxLayout(self.page_container)
        self.page_layout.setContentsMargins(20, 20, 20, 20)
        self.page_layout.setSpacing(0)
        self.page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create label for displaying page
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_label.setMinimumSize(QSize(400, 400))
        self.page_layout.addWidget(self.page_label)
        
        # Add scroll area to main layout
        self.layout.addWidget(self.scroll_area, 1)  # Give it stretch factor
        
    def create_page_movement_buttons(self):
        """Create page movement buttons at the bottom of the preview."""
        # Add separator
        self.layout.addWidget(self.create_separator())
        
        # Create container for movement buttons
        move_container = QWidget()
        move_layout = QHBoxLayout(move_container)
        move_layout.setContentsMargins(5, 5, 5, 5)
        move_layout.setSpacing(5)

        # Add spacer to push buttons to the center
        move_layout.addStretch()
        
        # Add container to main layout
        self.layout.addWidget(move_container)
        
    def create_tool_button(self, tooltip, icon_name, slot):
        """Create a tool button.
        
        Args:
            tooltip: Button tooltip
            icon_name: Icon name
            slot: Function to call when clicked
            
        Returns:
            QToolButton: Created button
        """
        button = QToolButton()
        button.setIcon(IconProvider.get_icon(icon_name))
        button.setIconSize(QSize(24, 24))
        button.setToolTip(tooltip)
        button.setFixedSize(QSize(32, 32))
        button.clicked.connect(slot)
        # QToolButton için stil tanımlaması
        button.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 4px;
            }
            QToolButton:hover {
                background-color: palette(highlight);
                border-color: palette(highlight);
            }
            QToolButton:pressed {
                background-color: palette(dark);
            }
        """)
        return button
        
    def create_separator(self):
        """Create a horizontal separator line.
        
        Returns:
            QFrame: Separator line
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("separator")
        return separator
        
    def set_zoom(self, zoom):
        """Set zoom level.
        
        Args:
            zoom: Zoom level (1.0 = 100%)
        """
        self.current_zoom = zoom
        # Zoom oranını ayarlara kaydet (settings_utils kullanarak)
        zoom_percent = int(zoom * 100)
        save_zoom_level(zoom_percent)
        if self.current_pixmap:
            self.update_display()
            
    def zoom_in(self):
        """Zoom in on the current page."""
        self.set_zoom(self.current_zoom * 1.2)
        self.app.status_bar.showMessage(f"Zoom: {int(self.current_zoom * 100)}%")
            
    def zoom_out(self):
        """Zoom out on the current page."""
        self.set_zoom(self.current_zoom / 1.2)
        self.app.status_bar.showMessage(f"Zoom: {int(self.current_zoom * 100)}%")
            
    def fit_width(self):
        """Fit page to window width."""
        if self.current_pixmap:
            available_width = self.scroll_area.width() - 40  # Account for margins
            zoom = available_width / self.current_pixmap.width()
            self.set_zoom(zoom)
            self.app.status_bar.showMessage("Fit to width")
            
    def fit_page(self):
        """Fit page to screen."""
        if self.current_pixmap:
            available_width = self.scroll_area.width() - 40  # Account for margins
            available_height = self.scroll_area.height() - 40  # Account for margins
            zoom_width = available_width / self.current_pixmap.width()
            zoom_height = available_height / self.current_pixmap.height()
            self.set_zoom(min(zoom_width, zoom_height))
            self.app.status_bar.showMessage("Fit to page")
            
    def update_display(self):
        """Update the display with current zoom level."""
        if self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(
                int(self.current_pixmap.width() * self.current_zoom),
                int(self.current_pixmap.height() * self.current_zoom),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.page_label.setPixmap(scaled_pixmap)
            
            # Update page indicator
            if self.app.pdf_manager.doc:
                page_count = self.app.pdf_manager.get_page_count()
                if page_count > 0 and self.current_page is not None:
                    self.page_indicator.setText(f"Page {self.current_page + 1} of {page_count}")
            
    def show_page(self, page_num):
        """Show the specified page.
        
        Args:
            page_num: Page number to display
        """
        if not self.app.pdf_manager.doc:
            return
            
        # Check if page number is valid
        if page_num < 0 or page_num >= self.app.pdf_manager.get_page_count():
            return
            
        # Get page pixmap
        self.current_page = page_num
        pixmap = self.app.pdf_manager.get_page_pixmap(page_num)
        if pixmap:
            self.current_pixmap = pixmap
            self.update_display()
            
            # Update status bar
            self.app.status_bar.showMessage(f"Showing page {page_num + 1} of {self.app.pdf_manager.get_page_count()}")
            
    def prev_page(self):
        """Show the previous page."""
        if self.current_page is not None and self.current_page > 0:
            self.show_page(self.current_page - 1)
            
    def next_page(self):
        """Show the next page."""
        if (self.current_page is not None and 
            self.current_page < self.app.pdf_manager.get_page_count() - 1):
            self.show_page(self.current_page + 1)
            
    def go_to_last_page(self):
        """Go to the last page."""
        if self.app.pdf_manager.doc:
            self.show_page(self.app.pdf_manager.get_page_count() - 1)
            
    def move_page_up(self):
        """Move the current page up in the document."""
        if not self.app.pdf_manager.doc or self.current_page is None:
            return
            
        if self.current_page > 0:
            # Implementation will be added later
            # For now, just show a message in the status bar
            self.app.status_bar.showMessage("Move page up functionality not implemented yet")
            
    def move_page_down(self):
        """Move the current page down in the document."""
        if not self.app.pdf_manager.doc or self.current_page is None:
            return
            
        if self.current_page < self.app.pdf_manager.get_page_count() - 1:
            # Implementation will be added later
            # For now, just show a message in the status bar
            self.app.status_bar.showMessage("Move page down functionality not implemented yet")
            
    def clear(self):
        """Clear the current display."""
        self.current_page = None
        self.current_pixmap = None
        self.page_label.clear()
        self.page_indicator.setText("Page 0 of 0")
            
    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)
        # Update display to maintain zoom level
        self.update_display()
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton and self.annotation_mode:
            self.drawing = True
            self.last_point = self.get_page_coordinates(event.pos())
            
    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if self.drawing and self.last_point and self.annotation_mode:
            current_point = self.get_page_coordinates(event.pos())
            
            if self.annotation_mode == "ink":
                # Draw line on pixmap
                painter = QPainter(self.current_pixmap)
                painter.setPen(QPen(self.annotation_color, self.annotation_width))
                painter.drawLine(self.last_point, current_point)
                painter.end()
                
                # Update display
                self.update_display()
                
            self.last_point = current_point
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            
            if not self.annotation_mode:
                return
                
            current_point = self.get_page_coordinates(event.pos())
            
            if self.annotation_mode == "text":
                # Add text annotation
                rect = QRectF(
                    self.last_point.x(),
                    self.last_point.y(),
                    100,  # Default width
                    50    # Default height
                )
                # Implementation will be added later
                self.app.status_bar.showMessage("Text annotation functionality not implemented yet")
                
            elif self.annotation_mode == "highlight":
                # Add highlight annotation
                rect = QRectF(
                    self.last_point.x(),
                    self.last_point.y(),
                    current_point.x() - self.last_point.x(),
                    current_point.y() - self.last_point.y()
                )
                # Implementation will be added later
                self.app.status_bar.showMessage("Highlight functionality not implemented yet")
                
            elif self.annotation_mode == "line":
                # Add line annotation
                # Implementation will be added later
                self.app.status_bar.showMessage("Line drawing functionality not implemented yet")
                
            elif self.annotation_mode == "circle":
                # Add circle annotation
                # Implementation will be added later
                self.app.status_bar.showMessage("Circle drawing functionality not implemented yet")
                
            # Reset annotation mode
            self.annotation_mode = None
            self.last_point = None
            
    def get_page_coordinates(self, widget_pos):
        """Convert widget coordinates to page coordinates.
        
        Args:
            widget_pos: Position in widget coordinates
            
        Returns:
            QPoint: Position in page coordinates
        """
        # Get position relative to page_label
        label_pos = self.page_label.mapFrom(self, widget_pos)
        
        # Convert to page coordinates (accounting for zoom)
        page_x = label_pos.x() / self.current_zoom
        page_y = label_pos.y() / self.current_zoom
        
        return QPoint(int(page_x), int(page_y))
        
    def start_text_annotation(self, color, text):
        """Start text annotation mode.
        
        Args:
            color: Annotation color
            text: Text to add
        """
        self.annotation_mode = "text"
        self.annotation_color = color
        self.annotation_text = text
        self.app.status_bar.showMessage("Click on the page to add text annotation")
        
    def start_highlight_annotation(self, color):
        """Start highlight annotation mode.
        
        Args:
            color: Highlight color
        """
        self.annotation_mode = "highlight"
        self.annotation_color = color
        self.app.status_bar.showMessage("Click and drag to highlight text")
        
    def start_line_annotation(self, color, width):
        """Start line annotation mode.
        
        Args:
            color: Line color
            width: Line width
        """
        self.annotation_mode = "line"
        self.annotation_color = color
        self.annotation_width = width
        self.app.status_bar.showMessage("Click and drag to draw a line")
        
    def start_circle_annotation(self, color, width):
        """Start circle annotation mode.
        
        Args:
            color: Circle color
            width: Line width
        """
        self.annotation_mode = "circle"
        self.annotation_color = color
        self.annotation_width = width
        self.app.status_bar.showMessage("Click and drag to draw a circle")
        
    def set_theme(self, theme):
        """Set theme colors for preview area.
        
        Args:
            theme: Theme name ("light" or "dark")
        """
        if theme == "dark":
            bg_color = "#1e1e1e"
            text_color = "#ffffff"
        else:
            bg_color = "#ffffff"
            text_color = "#000000"
        
        # Update scroll area background
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {bg_color};
                border: none;
            }}
        """)
        
        # Update page container background
        self.page_container.setStyleSheet(f"background-color: {bg_color};")
        
        # Update page indicator text color
        self.page_indicator.setStyleSheet(f"color: {text_color};")
