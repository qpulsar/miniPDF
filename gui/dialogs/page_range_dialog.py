"""
Dialog for selecting page ranges in PDF documents.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class PageRangeDialog(QDialog):
    """Dialog for selecting page ranges."""
    
    def __init__(self, parent, page_count):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            page_count (int): Total number of pages in the PDF
        """
        super().__init__(parent)
        self.page_count = page_count
        self.result = None
        
        self.setWindowTitle("Sayfa Aralığı Seçimi")
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI."""
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Sayfa numaralarını ve/veya ayrılan sayfaları yazıp tek tek virgül koyun.\n"
            "Örnek: 1,3,5-12"
        )
        layout.addWidget(instructions)
        
        # Range input
        range_layout = QHBoxLayout()
        range_label = QLabel("Sayfa Aralığı:")
        range_layout.addWidget(range_label)
        
        self.range_edit = QLineEdit()
        range_layout.addWidget(self.range_edit)
        
        layout.addLayout(range_layout)
        
        # Page count info
        page_info = QLabel(f"Toplam Sayfa Sayısı: {self.page_count}")
        layout.addWidget(page_info)
        
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
        
    def validate_range(self, range_str):
        """Validate the page range string.
        
        Args:
            range_str (str): Page range string to validate
            
        Returns:
            set: Set of page numbers, or None if invalid
        """
        pages = set()
        try:
            parts = [p.strip() for p in range_str.split(',')]
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if start < 1 or end > self.page_count or start > end:
                        return None
                    pages.update(range(start - 1, end))
                else:
                    page = int(part)
                    if page < 1 or page > self.page_count:
                        return None
                    pages.add(page - 1)
                    
            return pages if pages else None
            
        except ValueError:
            return None
            
    def accept(self):
        """Handle dialog acceptance."""
        range_str = self.range_edit.text().strip()
        pages = self.validate_range(range_str)
        
        if pages is None:
            QMessageBox.warning(
                self,
                "Uyarı",
                f"Geçersiz sayfa aralığı. 1 ile {self.page_count} arasında sayfa numaraları girin."
            )
            return
            
        self.result = pages
        super().accept()
        
    def reject(self):
        """Handle dialog rejection."""
        self.result = None
        super().reject()
