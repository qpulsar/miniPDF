"""
Text export dialog for PDF pages.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from .base_dialog import BaseDialog

class TextExportDialog(BaseDialog):
    def __init__(self, parent, text_content):
        super().__init__(
            parent,
            title="Metni Görüntüle",
            geometry="600x400"
        )
        
        self.text_content = text_content
        self.result = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Ana frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Metin alanı
        text_frame = ttk.LabelFrame(main_frame, text="Metin İçeriği", padding="5")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Metin alanı ve kaydırma çubuğu
        self.text_area, scrollbar = self.create_text_area(
            text_frame,
            wrap=tk.WORD,
            width=60,
            height=15
        )
        
        # Metni ekle
        self.text_area.insert("1.0", self.text_content)
        
        # Salt okunur yap
        self.text_area.configure(state="disabled")
        
        # Butonlar
        btn_frame = self.create_buttons_frame()
        
        self.add_button(
            btn_frame,
            text="İptal",
            command=self.cancel,
            style="danger"
        )
        
        self.add_button(
            btn_frame,
            text="Kaydet",
            command=self.ok,
            style="primary"
        )
        
        # Enter tuşunu Kaydet butonuna bağla
        self.dialog.bind("<Return>", lambda e: self.ok())
        # Escape tuşunu İptal butonuna bağla
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
    def ok(self):
        """Kaydet butonuna tıklandığında."""
        self.result = self.text_area.get("1.0", tk.END)
        self.close()
        
    def cancel(self):
        """İptal butonuna tıklandığında."""
        self.result = None
        self.close()
