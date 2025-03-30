"""
Annotation toolbar tab.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                           QColorDialog, QInputDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

class AnnotationTab(QWidget):
    """Tab for annotation tools."""
    
    # Signals
    text_annotation_requested = pyqtSignal(QColor, str)
    highlight_annotation_requested = pyqtSignal(QColor)
    ink_annotation_requested = pyqtSignal(QColor, float)
    delete_annotation_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the tab."""
        super().__init__(parent)
        
        # Set up the UI
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add text annotation button
        self.text_btn = QPushButton("Add Text")
        self.text_btn.clicked.connect(self.on_text_clicked)
        layout.addWidget(self.text_btn)
        
        # Add highlight button
        self.highlight_btn = QPushButton("Highlight")
        self.highlight_btn.clicked.connect(self.on_highlight_clicked)
        layout.addWidget(self.highlight_btn)
        
        # Add drawing button
        self.draw_btn = QPushButton("Draw")
        self.draw_btn.clicked.connect(self.on_draw_clicked)
        layout.addWidget(self.draw_btn)
        
        # Add delete button
        self.delete_btn = QPushButton("Delete Annotation")
        self.delete_btn.clicked.connect(self.delete_annotation_requested)
        layout.addWidget(self.delete_btn)
        
        # Add stretch to push buttons to top
        layout.addStretch()
        
        # Initialize colors
        self.text_color = QColor(255, 255, 0)  # Yellow
        self.highlight_color = QColor(255, 255, 0)  # Yellow
        self.ink_color = QColor(0, 0, 255)  # Blue
        self.ink_width = 2.0
        
    def on_text_clicked(self):
        """Handle text annotation button click."""
        # Get text content
        text, ok = QInputDialog.getText(
            self,
            "Add Text Annotation",
            "Enter text:"
        )
        
        if not ok or not text:
            return
            
        # Get color
        color = QColorDialog.getColor(
            self.text_color,
            self,
            "Select Text Color"
        )
        
        if color.isValid():
            self.text_color = color
            self.text_annotation_requested.emit(color, text)
            
    def on_highlight_clicked(self):
        """Handle highlight button click."""
        color = QColorDialog.getColor(
            self.highlight_color,
            self,
            "Select Highlight Color"
        )
        
        if color.isValid():
            self.highlight_color = color
            self.highlight_annotation_requested.emit(color)
            
    def on_draw_clicked(self):
        """Handle draw button click."""
        # Get line width
        width, ok = QInputDialog.getDouble(
            self,
            "Drawing Settings",
            "Line width:",
            value=self.ink_width,
            min=0.1,
            max=10.0,
            decimals=1
        )
        
        if not ok:
            return
            
        # Get color
        color = QColorDialog.getColor(
            self.ink_color,
            self,
            "Select Drawing Color"
        )
        
        if color.isValid():
            self.ink_color = color
            self.ink_width = width
            self.ink_annotation_requested.emit(color, width)
