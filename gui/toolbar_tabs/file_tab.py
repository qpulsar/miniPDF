"""
File tab for the toolbar in the miniPDF application.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QMessageBox, QFileDialog)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from gui.toolbar_tabs.base_tab import BaseTab
from core.text_extraction import TextExtractor
from gui.dialogs.export_image_dialog import ExportImageDialog
from gui.dialogs.text_export_dialog import TextExportDialog

class FileTab(BaseTab):
    """File tab for the toolbar."""
    
    def __init__(self, parent, app):
        """Initialize the file tab.
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent, app)
        self.text_extractor = TextExtractor()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the file tab."""
        # Main layout
        main_layout = QHBoxLayout()
        
        # File operations
        file_layout = QVBoxLayout()
        
        # Open button with icon
        open_btn = QPushButton("PDF Aç")
        open_btn.setIcon(QIcon.fromTheme("document-open"))
        open_btn.clicked.connect(self.app.open_pdf)
        file_layout.addWidget(open_btn)
        
        # Save button with icon
        save_btn = QPushButton("Kaydet")
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        save_btn.clicked.connect(self.app.save_pdf)
        file_layout.addWidget(save_btn)
        
        # Save As button with icon
        save_as_btn = QPushButton("Farklı Kaydet")
        save_as_btn.setIcon(QIcon.fromTheme("document-save-as"))
        save_as_btn.clicked.connect(self.app.save_pdf_as)
        file_layout.addWidget(save_as_btn)
        
        main_layout.addLayout(file_layout)
        
        # Export operations
        export_layout = QVBoxLayout()
        
        # Export as image button
        export_img_btn = QPushButton("Resim Olarak")
        export_img_btn.setIcon(QIcon.fromTheme("image"))
        export_img_btn.clicked.connect(self._export_as_image)
        export_layout.addWidget(export_img_btn)
        
        # Export text button
        export_text_btn = QPushButton("Metin Olarak")
        export_text_btn.setIcon(QIcon.fromTheme("text-plain"))
        export_text_btn.clicked.connect(self._export_as_text)
        export_layout.addWidget(export_text_btn)
        
        main_layout.addLayout(export_layout)
        
        # Print operations
        print_layout = QVBoxLayout()
        
        # Print button with icon
        print_btn = QPushButton("Yazdır")
        print_btn.setIcon(QIcon.fromTheme("print"))
        print_btn.clicked.connect(self._print_pdf)
        print_layout.addWidget(print_btn)
        
        main_layout.addLayout(print_layout)
        
        # Exit operations
        exit_layout = QVBoxLayout()
        
        # Exit button with icon
        exit_btn = QPushButton("Çıkış")
        exit_btn.setIcon(QIcon.fromTheme("exit"))
        exit_btn.clicked.connect(self._close_application)
        exit_layout.addWidget(exit_btn)
        
        main_layout.addLayout(exit_layout)
        
        # Set the main layout
        self.setLayout(main_layout)
    
    def _export_as_image(self):
        """Export PDF pages as images."""
        if not self.check_pdf_open():
            return
            
        dialog = ExportImageDialog(self, self.app.pdf_manager.get_page_count())
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.result:
            settings = dialog.result
            
            # Get pages to export
            if settings['page_mode'] == 'current':
                current_page = self.app.sidebar.get_selected_page_index()
                if current_page is None:
                    QMessageBox.warning(self, "Uyarı", "Lütfen bir sayfa seçin.")
                    return
                pages = [current_page]
            else:
                pages = list(range(self.app.pdf_manager.get_page_count()))
            
            # Get output path(s)
            if settings['output_mode'] == 'single':
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Resmi Kaydet",
                    "",
                    f"Image Files (*.{settings['format']})"
                )
                if not file_path:
                    return
                output_paths = [file_path]
            else:
                output_dir = QFileDialog.getExistingDirectory(
                    self,
                    "Görüntüleri Kaydetmek İçin Klasör Seçin"
                )
                if not output_dir:
                    return
                    
                # Create output paths for each page
                output_paths = []
                for i in pages:
                    filename = f"page_{i+1}.{settings['format']}"
                    output_paths.append(os.path.join(output_dir, filename))
            
            # Export images
            success_count = 0
            error_messages = []
            
            for i, (page_num, output_path) in enumerate(zip(pages, output_paths)):
                try:
                    page = self.app.pdf_manager.get_page(page_num)
                    if page:
                        img = self.app.pdf_manager.get_page_as_image(page_num, settings['zoom'])
                        if img:
                            if settings['format'] == 'jpeg':
                                img.save(output_path, quality=settings['quality'])
                            else:
                                img.save(output_path)
                            success_count += 1
                        else:
                            error_messages.append(f"Sayfa {page_num + 1}: Görüntü oluşturulamadı")
                    else:
                        error_messages.append(f"Sayfa {page_num + 1}: Sayfa bulunamadı")
                except Exception as e:
                    error_messages.append(f"Sayfa {page_num + 1}: {str(e)}")
            
            # Show result
            if success_count == len(pages):
                QMessageBox.information(
                    self,
                    "Başarılı",
                    f"Tüm sayfalar başarıyla kaydedildi ({success_count} sayfa)"
                )
            elif success_count > 0:
                QMessageBox.warning(
                    self,
                    "Kısmi Başarı",
                    f"{len(pages)} sayfadan {success_count} tanesi kaydedildi.\n"
                    f"Hatalar:\n" + "\n".join(error_messages)
                )
            else:
                QMessageBox.critical(
                    self,
                    "Hata",
                    f"Hiçbir sayfa kaydedilemedi.\nHatalar:\n" + "\n".join(error_messages)
                )
    
    def _export_as_text(self):
        """Export PDF page as text."""
        if not self.check_pdf_open():
            return
            
        current_page = self.app.sidebar.get_selected_page_index()
        if current_page is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir sayfa seçin.")
            return
            
        try:
            # Extract text
            text = self.text_extractor.extract_text(
                self.app.pdf_manager.doc,
                current_page
            )
            
            # Show text export dialog
            dialog = TextExportDialog(self, text)
            if dialog.exec() == QDialog.DialogCode.Accepted and dialog.result:
                # Get save path
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Metni Kaydet",
                    "",
                    "Text Files (*.txt);;All Files (*.*)"
                )
                
                if not file_path:  # Cancelled
                    return
                    
                # Save text to file
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(dialog.result)
                        
                    QMessageBox.information(
                        self,
                        "Başarılı",
                        "Metin başarıyla kaydedildi."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Hata",
                        f"Metin kaydedilirken hata oluştu:\n{str(e)}"
                    )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Metin çıkartılırken hata oluştu:\n{str(e)}"
            )
    
    def _print_pdf(self):
        """Print the current PDF."""
        if not self.check_pdf_open():
            return
            
        QMessageBox.information(
            self,
            "Bilgi",
            "Yazdırma özelliği henüz eklenmedi."
        )
    
    def _close_application(self):
        """Close the application."""
        self.app.close()
