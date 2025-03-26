"""
File tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
import os
import tempfile
import shutil
from datetime import datetime
from core.text_extraction import TextExtractor
from gui.dialogs.export_image_dialog import ExportImageDialog
from gui.dialogs.text_export_dialog import TextExportDialog
from gui.dialogs.print_dialog import PrintDialog
from gui.utils.messages import *
from gui.toolbar_tabs.base_tab import BaseTab
from gui.utils import create_icon_button

class FileTab(BaseTab):
    """File tab for the toolbar."""
    
    def __init__(self, parent, app):
        """
        Initialize the file tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        super().__init__(parent, app)
        self.text_extractor = TextExtractor()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the file tab."""
        # File operations frame
        file_frame = self.create_frame("file", "Dosya İşlemleri")
        
        # Open button with icon
        create_icon_button(
            file_frame,
            icon_name="open",
            text="PDF Aç",
            command=self.app.open_pdf,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Save button with icon
        create_icon_button(
            file_frame,
            icon_name="save",
            text="Kaydet",
            command=self.app.save_pdf,
            compound=tk.LEFT,
            style="success",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Save as button with icon
        create_icon_button(
            file_frame,
            icon_name="save_as",
            text="Farklı Kaydet",
            command=self.app.save_pdf_as,
            compound=tk.LEFT,
            style="success",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Export operations frame
        export_frame = self.create_frame("export", "Dışa Aktar")
        
        # Export as image with icon
        create_icon_button(
            export_frame,
            icon_name="image",
            text="Görüntü Olarak",
            command=self._export_as_image,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Export as text with icon
        create_icon_button(
            export_frame,
            icon_name="text",
            text="Metin Olarak",
            command=self._export_as_text,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Print operations frame
        print_frame = self.create_frame("print", "Yazdır")
        
        # Print button with icon
        create_icon_button(
            print_frame,
            icon_name="print",
            text="Yazdır",
            command=self._print_pdf,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Exit frame
        exit_frame = self.create_frame("exit", "Çıkış")
        
        # Exit button with icon
        create_icon_button(
            exit_frame,
            icon_name="exit",
            text="Çıkış",
            command=self._close_application,
            compound=tk.LEFT,
            style="danger",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
    
    def _export_as_image(self):
        """Export PDF pages as images."""
        if not self.check_pdf_open():
            return
            
        # Dışa aktarma ayarları dialogunu göster
        dialog = ExportImageDialog(self.app.root, len(self.app.pdf_manager.doc))
        dialog.show()
        
        if dialog.result is None:  # İptal edildi
            return
            
        pages, settings = dialog.result
        
        # Tek sayfa için geçerli sayfayı kullan
        if pages is None:
            pages = [self.app.preview.current_page_index]
        
        # Kaydetme yeri seç
        if settings['output_mode'] == 'single':
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{settings['format']}",
                filetypes=[
                    ("PNG Files", "*.png"),
                    ("JPEG Files", "*.jpg;*.jpeg"),
                    ("All Files", "*.*")
                ]
            )
            if not file_path:
                return
            output_paths = [file_path]
            
        else:  # multiple
            output_dir = filedialog.askdirectory(
                title="Görüntüleri Kaydetmek İçin Klasör Seçin"
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
                messagebox.showinfo(
                    "Başarılı",
                    f"Tüm sayfalar başarıyla kaydedildi ({success_count} sayfa)"
                )
            elif success_count > 0:
                messagebox.showwarning(
                    "Kısmi Başarı",
                    f"{total_count} sayfadan {success_count} tanesi kaydedildi.\n"
                    f"Hatalar:\n" + "\n".join(error_messages)
                )
            else:
                messagebox.showerror(
                    "Hata",
                    f"Hiçbir sayfa kaydedilemedi.\nHatalar:\n" + "\n".join(error_messages)
                )
                
        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü kaydedilirken hata oluştu:\n{str(e)}")

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
            dialog = TextExportDialog(self.app.root, text)
            dialog.show()
            
            if dialog.result is None:  # İptal edildi
                return
                
            # Kaydetme yeri seç
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Text Files", "*.txt"),
                    ("Markdown Files", "*.md"),
                    ("All Files", "*.*")
                ]
            )
            
            if not file_path:  # İptal edildi
                return
                
            # Metni dosyaya kaydet
            try:
                # Markdown formatı için basit düzenleme
                if file_path.lower().endswith('.md'):
                    # PDF'ten çıkarılan metni Markdown formatına dönüştür
                    lines = dialog.result.split('\n')
                    md_text = ""
                    
                    # Başlık ekle
                    md_text += "# PDF'ten Çıkarılan Metin\n\n"
                    
                    # İçeriği ekle
                    for line in lines:
                        if line.strip():
                            # Boş olmayan satırlar için paragraf formatı
                            md_text += line.strip() + "\n\n"
                    
                    # Altbilgi ekle
                    md_text += "---\n"
                    md_text += f"*Bu metin {self.app.pdf_manager.file_path} dosyasından {datetime.now().strftime('%Y-%m-%d %H:%M')} tarihinde çıkarılmıştır.*"
                    
                    content = md_text
                else:
                    content = dialog.result
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                messagebox.showinfo(
                    "Başarılı",
                    "Metin başarıyla kaydedildi!"
                )
                
            except Exception as e:
                messagebox.showerror(
                    "Hata",
                    f"Metin kaydedilirken hata oluştu:\n{str(e)}"
                )
                
        except Exception as e:
            messagebox.showerror(
                "Hata",
                f"Metin çıkartılırken hata oluştu:\n{str(e)}"
            )
    
    def _print_pdf(self):
        """Print the current PDF."""
        if not self.check_pdf_open():
            return
        
        try:
            # Yazdırma dialogunu göster
            dialog = PrintDialog(
                self.app.root, 
                self.app.pdf_manager,
                self.app.preview.current_page_index
            )
            dialog.show()
            
            # Sonucu kontrol et
            if dialog.result:
                self.app.status_var.set("Yazdırma işlemi başlatıldı")
            
        except Exception as e:
            messagebox.showerror(
                "Hata",
                f"Yazdırma işlemi sırasında hata oluştu: {str(e)}"
            )
    
    def _close_application(self):
        """Close the application."""
        self.app.root.quit()

    def check_pdf_open(self):
        """Check if a PDF is currently open."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Bilgi", "Önce bir PDF dosyası açmalısınız.")
            return False
        return True
