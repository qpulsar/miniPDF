"""
Image export dialog for PDF pages.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import os
from .base_dialog import BaseDialog

class ExportImageDialog(BaseDialog):
    def __init__(self, parent, total_pages):
        super().__init__(
            parent,
            title="Resim olarak kaydet",
            geometry="500x600"
        )
        
        self.total_pages = total_pages
        self.result = None
        
        # Değişkenler
        self.page_selection = tk.StringVar(value="current")
        self.page_range = tk.StringVar(value="")
        self.image_format = tk.StringVar(value="PNG")
        self.dpi = tk.StringVar(value="300")
        self.zoom = tk.DoubleVar(value=100.0)
        self.output_mode = tk.StringVar(value="single")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Ana frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sayfa Seçimi Bölümü
        page_frame = ttk.LabelFrame(main_frame, text="Sayfa Aralığı", padding="5")
        page_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(
            page_frame,
            text="Tümü",
            variable=self.page_selection,
            value="all"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            page_frame,
            text="Geçerli Sayfa",
            variable=self.page_selection,
            value="current"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            page_frame,
            text="Seçilen Sayfalar",
            variable=self.page_selection,
            value="range"
        ).pack(anchor=tk.W)
        
        range_frame = ttk.Frame(page_frame)
        range_frame.pack(fill=tk.X, pady=5)
        ttk.Label(
            range_frame,
            text="Sayfa numaralarını ve/veya ayrılan sayfaları yazıp tek tek virgül koyun.\nÖrnek: 1,3,5-12"
        ).pack(side=tk.LEFT)
        
        self.range_entry = ttk.Entry(page_frame, textvariable=self.page_range)
        self.range_entry.pack(fill=tk.X, pady=5)
        
        # Görüntü Ayarları Bölümü
        settings_frame = ttk.LabelFrame(main_frame, text="Görüntü Ayarları", padding="5")
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Format seçimi
        format_frame = ttk.Frame(settings_frame)
        format_frame.pack(fill=tk.X, pady=5)
        ttk.Label(format_frame, text="Görüntü Tipi:").pack(side=tk.LEFT)
        format_combo = ttk.Combobox(
            format_frame,
            textvariable=self.image_format,
            values=["PNG - Portable Network Graphic", "JPEG - Joint Photographic Experts Group"],
            state="readonly",
            width=40
        )
        format_combo.pack(side=tk.LEFT, padx=5)
        
        # DPI ayarı
        dpi_frame = ttk.Frame(settings_frame)
        dpi_frame.pack(fill=tk.X, pady=5)
        ttk.Label(dpi_frame, text="Çözünürlük:").pack(side=tk.LEFT)
        dpi_combo = ttk.Combobox(
            dpi_frame,
            textvariable=self.dpi,
            values=["72 dpi", "150 dpi", "300 dpi", "600 dpi"],
            state="readonly",
            width=10
        )
        dpi_combo.pack(side=tk.LEFT, padx=5)
        
        # Zoom ayarı
        zoom_frame = ttk.Frame(settings_frame)
        zoom_frame.pack(fill=tk.X, pady=5)
        ttk.Label(zoom_frame, text="Sayfaya Yakınlaştırma:").pack(side=tk.LEFT)
        zoom_spin = ttk.Spinbox(
            zoom_frame,
            from_=10,
            to=200,
            increment=10,
            textvariable=self.zoom,
            width=10
        )
        zoom_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(zoom_frame, text="%").pack(side=tk.LEFT)
        
        # Çıktı Modu
        output_frame = ttk.LabelFrame(main_frame, text="Resim formatı", padding="5")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(
            output_frame,
            text="Tek dosya olarak kaydet",
            variable=self.output_mode,
            value="single"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            output_frame,
            text="Her sayfayı ayrı dosya olarak kaydet",
            variable=self.output_mode,
            value="multiple"
        ).pack(anchor=tk.W)
        
        # Butonlar
        btn_frame = self.create_buttons_frame(parent=main_frame)
        
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
        
        # Enter tuşunu Tamam butonuna bağla
        self.dialog.bind("<Return>", lambda e: self.ok())
        # Escape tuşunu İptal butonuna bağla
        self.dialog.bind("<Escape>", lambda e: self.cancel())
        
        # Giriş alanına fokusla
        self.range_entry.focus_set()
        
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
                    if start < 1 or end > self.total_pages or start > end:
                        return None
                    pages.update(range(start - 1, end))
                else:
                    page = int(part)
                    if page < 1 or page > self.total_pages:
                        return None
                    pages.add(page - 1)
                    
            return sorted(list(pages))
            
        except ValueError:
            return None
            
    def get_export_settings(self):
        """Dışa aktarma ayarlarını al."""
        # DPI değerini sayıya çevir
        dpi = int(self.dpi.get().split()[0])
        
        # Zoom değerini 0-1 aralığına çevir
        zoom = self.zoom.get() / 100.0
        
        # Görüntü formatını al
        image_format = self.image_format.get().split()[0].lower()
        
        return {
            'dpi': dpi,
            'zoom': zoom,
            'format': image_format,
            'output_mode': self.output_mode.get()
        }
            
    def ok(self):
        """Tamam butonuna tıklandığında."""
        selection = self.page_selection.get()
        pages = None
        
        if selection == "all":
            pages = list(range(self.total_pages))
        elif selection == "current":
            pages = None  # None özel durum olarak geçerli sayfayı belirtir
        else:  # range
            range_str = self.page_range.get().strip()
            pages = self.validate_range(range_str)
            
            if pages is None:
                messagebox.showerror(
                    "Hata",
                    f"Geçersiz sayfa aralığı. 1 ile {self.total_pages} arasında sayfa numaraları girin."
                )
                return
        
        settings = self.get_export_settings()
        self.result = (pages, settings)
        self.close()
        
    def cancel(self):
        """İptal butonuna tıklandığında."""
        self.result = None
        self.close()
