"""
Ribbon widgets for the toolbar.
"""
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class RibbonSection(QFrame):
    """A section in the ribbon containing a group of related controls."""
    
    def __init__(self, title, parent=None):
        """Initialize ribbon section.
        
        Args:
            title: Section title
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Set appearance
        self.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                margin: 2px;
            }
            QLabel {
                color: #00e676;
                padding: 2px;
                font-size: 10px;
            }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        # Add title
        title_label = QLabel(title.upper())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Create content widget
        self.content = QWidget()
        self.content_layout = QHBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(2)
        layout.addWidget(self.content)
        
    def addWidget(self, widget):
        """Add widget to section content."""
        self.content_layout.addWidget(widget)
