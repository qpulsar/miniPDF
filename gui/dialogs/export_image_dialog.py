"""
Dialog for exporting PDF pages as images.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QComboBox, QSpinBox, QRadioButton, QPushButton,
                           QButtonGroup, QGroupBox)
from PyQt6.QtCore import Qt

class ExportImageDialog(QDialog):
    """Dialog for configuring image export settings."""
    
    def __init__(self, parent, page_count):
        """Initialize the dialog.
        
        Args:
            parent: Parent widget
            page_count (int): Total number of pages in the PDF
        """
        super().__init__(parent)
        self.page_count = page_count
        self.result = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dialog UI."""
        self.setWindowTitle("Görüntü Dışa Aktarma Ayarları")
        layout = QVBoxLayout(self)
        
        # Format selection
        format_group = QGroupBox("Görüntü Formatı")
        format_layout = QHBoxLayout()
        
        format_label = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PNG", "JPEG"])
        
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # Quality settings for JPEG
        quality_group = QGroupBox("JPEG Kalitesi")
        quality_layout = QHBoxLayout()
        
        quality_label = QLabel("Kalite:")
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(85)
        self.quality_spin.setEnabled(False)
        
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_spin)
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Connect format change to quality enable/disable
        self.format_combo.currentTextChanged.connect(
            lambda text: self.quality_spin.setEnabled(text == "JPEG")
        )
        
        # Page selection
        page_group = QGroupBox("Sayfa Seçimi")
        page_layout = QVBoxLayout()
        
        self.page_mode_group = QButtonGroup(self)
        
        self.current_page_radio = QRadioButton("Geçerli Sayfa")
        self.current_page_radio.setChecked(True)
        self.page_mode_group.addButton(self.current_page_radio)
        page_layout.addWidget(self.current_page_radio)
        
        self.all_pages_radio = QRadioButton("Tüm Sayfalar")
        self.page_mode_group.addButton(self.all_pages_radio)
        page_layout.addWidget(self.all_pages_radio)
        
        self.range_pages_radio = QRadioButton("Seçilen Sayfalar")
        self.page_mode_group.addButton(self.range_pages_radio)
        page_layout.addWidget(self.range_pages_radio)
        
        self.range_pages_entry = QLabel("Sayfa numaralarını ve/veya ayrılan sayfaları yazıp tek tek virgül koyun.\nÖrnek: 1,3,5-12")
        page_layout.addWidget(self.range_pages_entry)
        
        self.range_pages_input = QLabel()
        page_layout.addWidget(self.range_pages_input)
        
        page_group.setLayout(page_layout)
        layout.addWidget(page_group)
        
        # Output mode
        output_group = QGroupBox("Çıktı Modu")
        output_layout = QVBoxLayout()
        
        self.output_mode_group = QButtonGroup(self)
        
        self.single_file_radio = QRadioButton("Tek Dosya")
        self.single_file_radio.setChecked(True)
        self.output_mode_group.addButton(self.single_file_radio)
        output_layout.addWidget(self.single_file_radio)
        
        self.multiple_files_radio = QRadioButton("Ayrı Dosyalar")
        self.output_mode_group.addButton(self.multiple_files_radio)
        output_layout.addWidget(self.multiple_files_radio)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
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
        """Sayfa aralığını doğrula ve sayfa listesini döndür."""
        if not range_str:
            return None
            
        try:
            pages = set()
            parts = range_str.split(',')
            
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
                    
            return sorted(list(pages))
            
        except ValueError:
            return None
            
    def accept(self):
        """Handle dialog acceptance."""
        if self.range_pages_radio.isChecked():
            range_str = self.range_pages_input.text()
            pages = self.validate_range(range_str)
            if pages is None:
                return
        elif self.all_pages_radio.isChecked():
            pages = list(range(self.page_count))
        else:
            pages = None
        
        self.result = {
            'format': self.format_combo.currentText().lower(),
            'quality': self.quality_spin.value() if self.format_combo.currentText() == "JPEG" else None,
            'page_mode': 'current' if self.current_page_radio.isChecked() else 'all' if self.all_pages_radio.isChecked() else 'range',
            'pages': pages,
            'output_mode': 'single' if self.single_file_radio.isChecked() else 'multiple'
        }
        super().accept()
        
    def reject(self):
        """Handle dialog rejection."""
        self.result = None
        super().reject()
