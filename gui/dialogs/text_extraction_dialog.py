"""
Text extraction dialog for the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from gui.dialogs.base_dialog import BaseDialog
from datetime import datetime

class TextExtractionDialog(BaseDialog):
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
        super().__init__(
            parent,
            title="Metin Çıkart",
            geometry="600x500"
        )
        
        self.app = app
        self.doc = doc
        self.selected_page_index = selected_page_index
        self.on_extract_callback = on_extract_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the dialog."""
        # Create a frame for extraction options
        options_frame = self.create_labeled_frame("Çıkartma Seçenekleri")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Radio buttons for extraction scope
        self.scope_var = tk.StringVar(value="current_page")
        
        current_page_radio = ttk.Radiobutton(
            options_frame,
            text=f"Mevcut Sayfa (Sayfa {self.selected_page_index + 1})",
            variable=self.scope_var,
            value="current_page"
        )
        current_page_radio.pack(anchor=tk.W, padx=10, pady=5)
        
        all_pages_radio = ttk.Radiobutton(
            options_frame,
            text="Tüm Sayfalar",
            variable=self.scope_var,
            value="all_pages"
        )
        all_pages_radio.pack(anchor=tk.W, padx=10, pady=5)
        
        # Create a frame for the text display
        text_frame = self.create_labeled_frame("Çıkartılan Metin")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text area for displaying extracted text
        self.text_area, _ = self.create_text_area(text_frame)
        
        # Create a frame for action buttons
        action_frame = self.create_buttons_frame(parent=self.dialog)
        
        # Extract button
        self.add_button(
            action_frame,
            text="Çıkart",
            command=self.extract_text
        )
        
        # Copy button
        self.add_button(
            action_frame,
            text="Kopyala",
            command=self.copy_text
        )
        
        # Save button
        self.add_button(
            action_frame,
            text="Kaydet",
            command=self.save_text
        )
        
        # Close button
        self.add_button(
            action_frame,
            text="Kapat",
            command=self.dialog.destroy,
            side=tk.RIGHT
        )
    
    def extract_text(self):
        """Extract text based on selected options."""
        scope = self.scope_var.get()
        self.on_extract_callback(self.dialog, scope, self.selected_page_index, self.text_area)
    
    def copy_text(self):
        """Copy the extracted text to the clipboard."""
        text = self.text_area.get("1.0", tk.END)
        
        if not text.strip():
            messagebox.showinfo("Bilgi", "Kopyalanacak metin yok.")
            return
        
        self.dialog.clipboard_clear()
        self.dialog.clipboard_append(text)
        self.app.status_var.set("Metin panoya kopyalandı")
    
    def save_text(self):
        """Save the extracted text to a file."""
        text = self.text_area.get("1.0", tk.END)
        
        if not text.strip():
            messagebox.showinfo("Bilgi", "Kaydedilecek metin yok.")
            return
        
        # Ask user where to save the text
        save_path = filedialog.asksaveasfilename(
            title="Çıkartılan Metni Kaydet",
            defaultextension=".txt",
            filetypes=[
                ("Metin Dosyaları", "*.txt"), 
                ("Markdown Dosyaları", "*.md"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if not save_path:
            return
        
        try:
            # Markdown formatı için basit düzenleme
            if save_path.lower().endswith('.md'):
                # PDF'ten çıkarılan metni Markdown formatına dönüştür
                lines = text.split('\n')
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
                
                text = md_text
            
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            messagebox.showinfo("Başarılı", "Metin başarıyla kaydedildi!")
            self.app.status_var.set(f"Metin {save_path} konumuna kaydedildi")
        except Exception as e:
            messagebox.showerror("Hata", f"Metin kaydedilemedi: {e}")
            self.app.status_var.set("Metin kaydedilemedi")
