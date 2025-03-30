"""
File operations tab for the toolbar.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class FileTab(QWidget):
    """Tab for file operations."""
    
    def __init__(self, parent=None):
        """Initialize file tab.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        
        # Create layout
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)
        
        # Create buttons
        open_btn = QPushButton("Open")
        open_btn.clicked.connect(self.parent.parent().open_pdf)
        layout.addWidget(open_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.parent.parent().save_pdf)
        layout.addWidget(save_btn)
        
        save_as_btn = QPushButton("Save As")
        save_as_btn.clicked.connect(self.parent.parent().save_pdf_as)
        layout.addWidget(save_as_btn)
