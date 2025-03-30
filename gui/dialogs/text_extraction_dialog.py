"""
Text extraction dialog for the miniPDF application.
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QTextEdit, QPushButton, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt

class TextExtractionDialog(QDialog):
    """Dialog for extracting text from PDF documents."""
    
    def __init__(self, parent, app, doc, selected_page_index, on_extract_callback):
        """
        Initialize the text extraction dialog.
        
        Args:
            parent: Parent widget
            app: Main application instance
            doc: PDF document
            selected_page_index: Index of the selected page
            on_extract_callback: Callback function for extraction
        """
        super().__init__(parent)
        self.app = app
        self.doc = doc
        self.selected_page_index = selected_page_index
        self.on_extract_callback = on_extract_callback
        
        self.setWindowTitle("Metin Çıkart")
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the dialog."""
        layout = QVBoxLayout(self)
        
        # Extraction options
        options_layout = QVBoxLayout()
        options_label = QLabel("Çıkartma Seçenekleri")
        options_layout.addWidget(options_label)
        
        self.scope_var = Qt.CheckState.Unchecked
        
        current_page_radio = QRadioButton(f"Mevcut Sayfa (Sayfa {self.selected_page_index + 1})")
        current_page_radio.setChecked(True)
        current_page_radio.toggled.connect(self.update_scope)
        options_layout.addWidget(current_page_radio)
        
        all_pages_radio = QRadioButton("Tüm Sayfalar")
        all_pages_radio.toggled.connect(self.update_scope)
        options_layout.addWidget(all_pages_radio)
        
        layout.addLayout(options_layout)
        
        # Text display
        text_layout = QVBoxLayout()
        text_label = QLabel("Çıkartılan Metin")
        text_layout.addWidget(text_label)
        
        self.text_area = QTextEdit()
        text_layout.addWidget(self.text_area)
        
        layout.addLayout(text_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        extract_button = QPushButton("Çıkart")
        extract_button.clicked.connect(self.extract_text)
        button_layout.addWidget(extract_button)
        
        copy_button = QPushButton("Kopyala")
        copy_button.clicked.connect(self.copy_text)
        button_layout.addWidget(copy_button)
        
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_text)
        button_layout.addWidget(save_button)
        
        close_button = QPushButton("Kapat")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def update_scope(self):
        """Update the extraction scope."""
        if self.sender().text() == f"Mevcut Sayfa (Sayfa {self.selected_page_index + 1})":
            self.scope_var = "current_page"
        else:
            self.scope_var = "all_pages"
    
    def extract_text(self):
        """Extract text based on selected options."""
        self.on_extract_callback(self, self.scope_var, self.selected_page_index, self.text_area)
    
    def copy_text(self):
        """Copy the extracted text to the clipboard."""
        text = self.text_area.toPlainText()
        
        if not text.strip():
            print("Bilgi: Kopyalanacak metin yok.")
            return
        
        self.clipboard().setText(text)
        self.app.status_var = "Metin panoya kopyalandı"
    
    def save_text(self):
        """Save the extracted text to a file."""
        text = self.text_area.toPlainText()
        
        if not text.strip():
            print("Bilgi: Kaydedilecek metin yok.")
            return
        
        # Ask user where to save the text
        from PyQt6.QtWidgets import QFileDialog
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Çıkartılan Metni Kaydet",
            "",
            "Metin Dosyaları (*.txt);;Tüm Dosyalar (*)"
        )
        
        if not save_path:
            return
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print("Başarılı: Metin başarıyla kaydedildi!")
            self.app.status_var = f"Metin {save_path} konumuna kaydedildi"
        except Exception as e:
            print(f"Hata: Metin kaydedilemedi: {e}")
            self.app.status_var = "Metin kaydedilemedi"
