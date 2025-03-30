"""
View operations tab for the toolbar.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ..utils.icon_utils import IconProvider

class ViewTab(QWidget):
    """Tab for view operations."""
    
    ZOOM_LEVELS = ["25%", "50%", "75%", "100%", "125%", "150%", "200%", "300%", "400%"]
    
    def __init__(self, parent=None):
        """Initialize view tab.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        
        # Create layout
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)
        
        # Create zoom combo box
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(self.ZOOM_LEVELS)
        self.zoom_combo.setCurrentText("100%")
        self.zoom_combo.currentTextChanged.connect(self.on_zoom_changed)
        layout.addWidget(self.zoom_combo)
        
        # Create buttons
        zoom_in_btn = QPushButton("Zoom In")
        zoom_in_btn.setIcon(IconProvider.get_icon("zoom_in"))
        zoom_in_btn.clicked.connect(self.zoom_in)
        layout.addWidget(zoom_in_btn)
        
        zoom_out_btn = QPushButton("Zoom Out")
        zoom_out_btn.setIcon(IconProvider.get_icon("zoom_out"))
        zoom_out_btn.clicked.connect(self.zoom_out)
        layout.addWidget(zoom_out_btn)
        
        fit_width_btn = QPushButton("Fit Width")
        fit_width_btn.clicked.connect(self.fit_width)
        layout.addWidget(fit_width_btn)
        
    def get_current_zoom(self):
        """Get current zoom level as float."""
        return float(self.zoom_combo.currentText().strip("%")) / 100.0
        
    def set_zoom(self, zoom):
        """Set zoom level.
        
        Args:
            zoom: Zoom level as float (1.0 = 100%)
        """
        zoom_str = f"{int(zoom * 100)}%"
        if zoom_str in self.ZOOM_LEVELS:
            self.zoom_combo.setCurrentText(zoom_str)
            self.update_preview()
            
    def on_zoom_changed(self, text):
        """Handle zoom combo box changes.
        
        Args:
            text: Selected zoom level text
        """
        self.update_preview()
        
    def zoom_in(self):
        """Zoom in one level."""
        current_idx = self.zoom_combo.currentIndex()
        if current_idx < len(self.ZOOM_LEVELS) - 1:
            self.zoom_combo.setCurrentIndex(current_idx + 1)
            
    def zoom_out(self):
        """Zoom out one level."""
        current_idx = self.zoom_combo.currentIndex()
        if current_idx > 0:
            self.zoom_combo.setCurrentIndex(current_idx - 1)
            
    def fit_width(self):
        """Fit page to window width."""
        # TODO: Implement this feature
        pass
        
    def update_preview(self):
        """Update the preview with current zoom level."""
        preview = self.parent.parent().preview
        if preview:
            current_page = preview.current_page
            if current_page is not None:
                preview.show_page(current_page, self.get_current_zoom())
