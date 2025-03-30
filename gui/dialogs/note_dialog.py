"""
Dialog for adding and editing PDF annotations.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QTextEdit, QPushButton, QComboBox)
from PyQt6.QtCore import Qt

class NoteDialog(QDialog):
    """Dialog for adding and editing PDF annotations."""
    
    def __init__(self, parent, title="Not Ekle", initial_text=""):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            title (str): Dialog title
            initial_text (str): Initial text for the note
        """
        super().__init__(parent)
        self.initial_text = initial_text
        self.result = None
        
        self.setWindowTitle(title)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout(self)
        
        # Note type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Not Tipi:")
        type_layout.addWidget(type_label)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Text", "Highlight", "Underline", "StrikeOut"])
        type_layout.addWidget(self.type_combo)
        
        layout.addLayout(type_layout)
        
        # Note content
        content_label = QLabel("Not İçeriği:")
        layout.addWidget(content_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.initial_text)
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
        self.result = {
            'type': self.type_combo.currentText().lower(),
            'text': self.text_edit.toPlainText()
        }
        super().accept()
        
    def reject(self):
        """Handle dialog rejection."""
        self.result = None
        super().reject()
