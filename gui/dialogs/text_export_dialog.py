"""
Dialog for exporting PDF text content.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QTextEdit, QPushButton)
from PyQt6.QtCore import Qt

class TextExportDialog(QDialog):
    """Dialog for viewing and exporting PDF text content."""
    
    def __init__(self, parent, text):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            text (str): Text content to display
        """
        super().__init__(parent)
        self.text = text
        self.result = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI."""
        self.setWindowTitle("Metin Dışa Aktarma")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Text preview
        preview_label = QLabel("Önizleme:")
        layout.addWidget(preview_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.text)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        ok_button = QPushButton("Tamam")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        cancel_button = QPushButton("İptal")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def accept(self):
        """Handle dialog acceptance."""
        self.result = self.text_edit.toPlainText()
        super().accept()
        
    def reject(self):
        """Handle dialog rejection."""
        self.result = None
        super().reject()
