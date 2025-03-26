"""
Text export dialog for PDF pages.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import html
import re
from tkhtmlview import HTMLScrolledText
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
        
        # HTML metin alanı
        self.text_area = HTMLScrolledText(text_frame, width=60, height=15)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Düz metni HTML'e dönüştür
        html_content = self.text_to_html(self.text_content)
        
        # HTML içeriğini ekle
        self.text_area.set_html(html_content)
        
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
    
    def strip_tags(self, html_text):
        """HTML etiketlerini kaldır."""
        return re.sub(r'<[^>]*>', '', html_text)
    
    def text_to_html(self, text):
        """Düz metni HTML'e dönüştür."""
        if not text:
            return "<html><body></body></html>"
        
        # Özel karakterleri escape et
        text = html.escape(text)
        
        # Satır sonlarını <br> etiketlerine dönüştür
        text = text.replace('\n', '<br>')
        
        # Basit HTML yapısı oluştur
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 10px; }}
                p {{ margin-bottom: 10px; }}
            </style>
        </head>
        <body>
            {text}
        </body>
        </html>
        """
        return html_content
    
    def html_to_text(self, html_content):
        """HTML'i düz metne dönüştür."""
        # HTML etiketlerini kaldır
        text = self.strip_tags(html_content)
        # HTML karakter referanslarını çöz
        text = html.unescape(text)
        return text
        
    def ok(self):
        """Kaydet butonuna tıklandığında."""
        # HTML içeriğini al ve düz metne dönüştür
        html_content = self.text_area.html
        self.result = self.html_to_text(html_content)
        self.close()
        
    def cancel(self):
        """İptal butonuna tıklandığında."""
        self.result = None
        self.close()
