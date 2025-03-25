"""
Page range selection dialog for PDF operations.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from .base_dialog import BaseDialog

class PageRangeDialog(BaseDialog):
    def __init__(self, parent, total_pages):
        super().__init__(
            parent,
            title="Sayfa Aralığı Seçin",
            geometry="300x150"
        )
        
        self.total_pages = total_pages
        self.result = None
        
        # Değişkenler
        self.range_var = tk.StringVar(value=f"1-{self.total_pages}")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Ana frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bilgi etiketi
        info_text = f"Toplam sayfa sayısı: {self.total_pages}\nSayfa aralığını belirtin (örn: 1-5):"
        ttk.Label(main_frame, text=info_text).pack(pady=(0, 10))
        
        # Giriş alanı
        self.range_entry = ttk.Entry(main_frame, textvariable=self.range_var)
        self.range_entry.pack(fill=tk.X, pady=(0, 10))
        
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
            text="Tamam",
            command=self.ok,
            style="primary"
        )
        
        # Enter tuşunu Tamam butonuna bağla
        self.dialog.bind("<Return>", lambda e: self.ok())
        # Escape tuşunu İptal butonuna bağla
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
        # Giriş alanına fokusla
        self.range_entry.focus_set()
        
    def validate_range(self, range_str):
        """Sayfa aralığını doğrula ve başlangıç-bitiş sayfa numaralarını döndür."""
        try:
            # Aralığı parçala
            start, end = map(int, range_str.split('-'))
            
            # Geçerlilik kontrolü
            if start < 1 or end > self.total_pages or start > end:
                return None
                
            return start - 1, end  # PyMuPDF 0-tabanlı indeks kullanıyor
            
        except ValueError:
            return None
            
    def ok(self):
        """Tamam butonuna tıklandığında."""
        range_str = self.range_var.get().strip()
        result = self.validate_range(range_str)
        
        if result is None:
            messagebox.showerror(
                "Hata",
                f"Geçersiz sayfa aralığı. 1 ile {self.total_pages} arasında bir aralık girin (örn: 1-5)."
            )
            return
            
        self.result = result
        self.close()
        
    def cancel(self):
        """İptal butonuna tıklandığında."""
        self.result = None
        self.close()
