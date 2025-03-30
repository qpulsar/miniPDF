"""
File tab for the toolbar in the miniPDF application.
"""
from PyQt6.QtWidgets import QPushButton, QMessageBox, QFileDialog, QVBoxLayout, QHBoxLayout
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
        # File operations frame
        file_frame = self.create_frame("file", "Dosya İşlemleri")
        file_layout = QVBoxLayout()
        file_frame.setLayout(file_layout)
        
        file_operations_layout = QHBoxLayout()
        file_layout.addLayout(file_operations_layout)
        
        # Open button with icon
        open_btn = QPushButton("PDF Aç", file_frame)
        open_btn.setIcon(QIcon.fromTheme("document-open"))
        open_btn.clicked.connect(self.app.open_pdf)
        file_operations_layout.addWidget(open_btn)
        
        # Save button with icon
        save_btn = QPushButton("Kaydet", file_frame)
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        save_btn.clicked.connect(self.app.save_pdf)
        file_operations_layout.addWidget(save_btn)
        
        # Save As button with icon
        save_as_btn = QPushButton("Farklı Kaydet", file_frame)
        save_as_btn.setIcon(QIcon.fromTheme("document-save-as"))
        save_as_btn.clicked.connect(self.app.save_pdf_as)
        file_operations_layout.addWidget(save_as_btn)
        
        # Export frame
        export_frame = self.create_frame("export", "Dışa Aktar")
        export_layout = QVBoxLayout()
        export_frame.setLayout(export_layout)
        
        export_operations_layout = QHBoxLayout()
        export_layout.addLayout(export_operations_layout)
        
        # Export as image button
        export_img_btn = QPushButton("Resim Olarak", export_frame)
        export_img_btn.setIcon(QIcon.fromTheme("image"))
        export_img_btn.clicked.connect(self._export_as_image)
        export_operations_layout.addWidget(export_img_btn)
        
        # Export text button
        export_text_btn = QPushButton("Metin Olarak", export_frame)
        export_text_btn.setIcon(QIcon.fromTheme("text-plain"))
        export_text_btn.clicked.connect(self._export_as_text)
        export_operations_layout.addWidget(export_text_btn)
        
        # Print operations frame
        print_frame = self.create_frame("print", "Yazdır")
        print_layout = QVBoxLayout()
        print_frame.setLayout(print_layout)
        
        print_operations_layout = QHBoxLayout()
        print_layout.addLayout(print_operations_layout)
        
        # Print button with icon
        print_btn = QPushButton("Yazdır", print_frame)
        print_btn.setIcon(QIcon.fromTheme("print"))
        print_btn.clicked.connect(self._print_pdf)
        print_operations_layout.addWidget(print_btn)
        
        # Exit frame
        exit_frame = self.create_frame("exit", "Çıkış")
        exit_layout = QVBoxLayout()
        exit_frame.setLayout(exit_layout)
        
        exit_operations_layout = QHBoxLayout()
        exit_layout.addLayout(exit_operations_layout)
        
        # Exit button with icon
        exit_btn = QPushButton("Çıkış", exit_frame)
        exit_btn.setIcon(QIcon.fromTheme("exit"))
        exit_btn.clicked.connect(self._close_application)
        exit_operations_layout.addWidget(exit_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(file_frame)
        main_layout.addWidget(export_frame)
        main_layout.addWidget(print_frame)
        main_layout.addWidget(exit_frame)
        self.setLayout(main_layout)
    
    def _export_as_image(self):
        """Export PDF pages as images."""
        if not self.check_pdf_open():
            return
            
        # Dışa aktarma ayarları dialogunu göster
        dialog = ExportImageDialog(self, len(self.app.pdf_manager.doc))
        dialog.exec()
        
        if dialog.result is None:  # İptal edildi
            return
            
        pages, settings = dialog.result
        
        # Tek sayfa için geçerli sayfayı kullan
        if pages is None:
            pages = [self.app.preview.current_page_index]
        
        # Kaydetme yeri seç
        if settings['output_mode'] == 'single':
            file_path = QFileDialog.getSaveFileName(
                self,
                "Resmi Kaydet",
                "",
                "PNG Files (*.png);;JPEG Files (*.jpg;*.jpeg);;All Files (*.*)"
            )
            if not file_path[0]:
                return
            output_paths = [file_path[0]]
            
        else:  # multiple
            output_dir = QFileDialog.getExistingDirectory(
                self,
                "Görüntüleri Kaydetmek İçin Klasör Seçin"
            )
            if not output_dir:
                return
                
            # Her sayfa için dosya yolu oluştur
            output_paths = [
                os.path.join(output_dir, f"sayfa_{page + 1}.{settings['format']}")
                for page in pages
            ]
        
        try:
            success_count = 0
            error_messages = []
            
            # Her sayfayı dışa aktar
            for i, page_num in enumerate(pages):
                try:
                    page = self.app.pdf_manager.doc[page_num]
                    success = self.text_extractor.save_page_as_image(
                        page,
                        output_paths[i],
                        zoom=settings['zoom']
                    )
                    
                    if success:
                        success_count += 1
                    else:
                        error_messages.append(f"Sayfa {page_num + 1} kaydedilemedi")
                        
                except Exception as e:
                    error_messages.append(f"Sayfa {page_num + 1}: {str(e)}")
            
            # Sonucu göster
            total_count = len(pages)
            if success_count == total_count:
                QMessageBox.information(
                    self,
                    "Başarılı",
                    f"Tüm sayfalar başarıyla kaydedildi ({success_count} sayfa)"
                )
            elif success_count > 0:
                QMessageBox.warning(
                    self,
                    "Kısmi Başarı",
                    f"{total_count} sayfadan {success_count} tanesi kaydedildi.\n"
                    f"Hatalar:\n" + "\n".join(error_messages)
                )
            else:
                QMessageBox.critical(
                    self,
                    "Hata",
                    f"Hiçbir sayfa kaydedilemedi.\nHatalar:\n" + "\n".join(error_messages)
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Görüntü kaydedilirken hata oluştu:\n{str(e)}"
            )

    def _export_as_text(self):
        """Export PDF page as text."""
        if not self.check_pdf_open():
            return
            
        try:
            # Geçerli sayfanın metnini al
            text = self.text_extractor.extract_text(
                self.app.pdf_manager.doc,
                self.app.preview.current_page_index
            )
            
            # Text export dialogunu göster
            dialog = TextExportDialog(self, text)
            dialog.exec()
            
            if dialog.result is None:  # İptal edildi
                return
                
            # Kaydetme yeri seç
            file_path = QFileDialog.getSaveFileName(
                self,
                "Metni Kaydet",
                "",
                "Text Files (*.txt);;All Files (*.*)"
            )
            
            if not file_path[0]:  # İptal edildi
                return
                
            # Metni dosyaya kaydet
            try:
                with open(file_path[0], 'w', encoding='utf-8') as f:
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
        
        # On macOS, use the default PDF viewer to print
        if os.name == "posix":
            self.app.open_with_default_app()
        else:
            self.show_not_implemented()
    
    def _close_application(self):
        """Close the application."""
        self.app.root.quit()

    def check_pdf_open(self):
        """Check if a PDF is currently open."""
        if not self.app.pdf_manager.doc:
            QMessageBox.information(self, "Bilgi", "Önce bir PDF dosyası açmalısınız.")
            return False
        return True
