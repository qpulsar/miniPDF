"""
View toolbar tab.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QSlider, QLabel, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ..utils.icon_utils import IconProvider

class ViewTab(QWidget):
    """Tab for view controls."""
    
    ZOOM_LEVELS = ["25%", "50%", "75%", "100%", "125%", "150%", "200%", "300%", "400%"]
    
    def __init__(self, parent=None):
        """Initialize the tab."""
        super().__init__(parent)
        self.parent = parent
        
        # Set up the UI
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create zoom controls
        zoom_layout = QHBoxLayout()
        layout.addLayout(zoom_layout)
        
        # Zoom out button
        self.zoom_out_btn = QPushButton("-")
        self.zoom_out_btn.setFixedWidth(30)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(self.zoom_out_btn)
        
        # Zoom slider
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setMinimum(25)  # 25%
        self.zoom_slider.setMaximum(400)  # 400%
        self.zoom_slider.setValue(100)  # 100%
        self.zoom_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.zoom_slider.setTickInterval(25)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        zoom_layout.addWidget(self.zoom_slider)
        
        # Zoom in button
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedWidth(30)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(self.zoom_in_btn)
        
        # Zoom label
        self.zoom_label = QLabel("100%")
        self.zoom_label.setFixedWidth(50)
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        zoom_layout.addWidget(self.zoom_label)
        
        # Create fit controls
        fit_layout = QHBoxLayout()
        layout.addLayout(fit_layout)
        
        # Fit to width button
        self.fit_width_btn = QPushButton("Fit Width")
        self.fit_width_btn.clicked.connect(self.fit_width)
        fit_layout.addWidget(self.fit_width_btn)
        
        # Fit to screen button
        self.fit_screen_btn = QPushButton("Fit Screen")
        self.fit_screen_btn.clicked.connect(self.fit_screen)
        fit_layout.addWidget(self.fit_screen_btn)
        
        # Create zoom combo box
        self.zoom_combo = QComboBox()
        self.zoom_combo.addItems(self.ZOOM_LEVELS)
        self.zoom_combo.setCurrentText("100%")
        self.zoom_combo.currentTextChanged.connect(self.on_zoom_combo_changed)
        fit_layout.addWidget(self.zoom_combo)
        
        # Add stretch to push controls to top
        layout.addStretch()
        
    def zoom_in(self):
        """Handle zoom in."""
        current = self.zoom_slider.value()
        self.zoom_slider.setValue(min(current + 25, 400))
        
    def zoom_out(self):
        """Handle zoom out."""
        current = self.zoom_slider.value()
        self.zoom_slider.setValue(max(current - 25, 25))
        
    def on_zoom_changed(self, value):
        """Handle zoom slider change."""
        self.zoom_label.setText(f"{value}%")
        if self.parent and self.parent.preview:
            self.parent.preview.set_zoom(value / 100.0)
            
    def on_zoom_combo_changed(self, text):
        """Handle zoom combo box change."""
        self.zoom_slider.setValue(int(text.strip("%")))
        
    def fit_width(self):
        """Fit page to window width."""
        if self.parent and self.parent.preview:
            self.parent.preview.fit_width()
            # Update slider to match new zoom level
            zoom = self.parent.preview.current_zoom * 100
            self.zoom_slider.setValue(int(zoom))
            
    def fit_screen(self):
        """Fit page to screen."""
        if self.parent and self.parent.preview:
            self.parent.preview.fit_screen()
            # Update slider to match new zoom level
            zoom = self.parent.preview.current_zoom * 100
            self.zoom_slider.setValue(int(zoom))
            
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
            
    def update_preview(self):
        """Update the preview with current zoom level."""
        preview = self.parent.preview
        if preview:
            current_page = preview.current_page
            if current_page is not None:
                preview.show_page(current_page, self.get_current_zoom())
