"""
Print dialog for PDF documents.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import os
import tempfile
import subprocess
import platform
from .base_dialog import BaseDialog

class PrintDialog(BaseDialog):
    def __init__(self, parent, pdf_manager, current_page):
        super().__init__(
            parent,
            title="Yazdır",
            geometry="700x600"
        )
        
        self.pdf_manager = pdf_manager
        self.current_page = current_page
        self.total_pages = len(pdf_manager.doc) if pdf_manager.doc else 0
        self.result = None
        
        # Değişkenler
        self.printer_name = tk.StringVar(value="")
        self.page_selection = tk.StringVar(value="all")
        self.page_range = tk.StringVar(value="")
        self.copies = tk.IntVar(value=1)
        self.duplex = tk.StringVar(value="none")
        self.collate = tk.BooleanVar(value=False)
        self.scale = tk.DoubleVar(value=100.0)
        
        # Sistem yazıcılarını al
        self.available_printers = self.get_available_printers()
        if self.available_printers:
            self.printer_name.set(self.available_printers[0])
        
        self.create_widgets()
        
    def create_widgets(self):
        # Ana frame
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Yazıcı seçimi
        printer_frame = ttk.LabelFrame(main_frame, text="Yazıcı", padding="10")
        printer_frame.pack(fill=tk.X, pady=(0, 10))
        
        printer_row = ttk.Frame(printer_frame)
        printer_row.pack(fill=tk.X)
        
        ttk.Label(printer_row, text="İsim:").pack(side=tk.LEFT, padx=(0, 5))
        
        printer_combo = ttk.Combobox(
            printer_row, 
            textvariable=self.printer_name,
            values=self.available_printers,
            width=40
        )
        printer_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            printer_row,
            text="Özellikler...",
            command=self.show_printer_properties
        ).pack(side=tk.LEFT)
        
        status_row = ttk.Frame(printer_frame)
        status_row.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(status_row, text="Durum: Hazır").pack(side=tk.LEFT)
        
        ttk.Checkbutton(
            printer_frame,
            text="Dosyaya Bas",
            variable=tk.BooleanVar(value=False)
        ).pack(anchor=tk.W, pady=(10, 0))
        
        # Kopya sayısı ve harmanlama
        copies_frame = ttk.Frame(printer_frame)
        copies_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(copies_frame, text="Kopyalar:").pack(side=tk.LEFT)
        
        copies_spin = ttk.Spinbox(
            copies_frame,
            from_=1,
            to=99,
            width=5,
            textvariable=self.copies
        )
        copies_spin.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Checkbutton(
            copies_frame,
            text="Karşılaştır",
            variable=self.collate
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(copies_frame, text="Duplex:").pack(side=tk.LEFT)
        
        duplex_combo = ttk.Combobox(
            copies_frame,
            textvariable=self.duplex,
            values=["Hiçbiri", "Uzun Kenar", "Kısa Kenar"],
            width=15
        )
        duplex_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Sayfa aralığı
        page_frame = ttk.LabelFrame(main_frame, text="Sayfa Aralığı", padding="10")
        page_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(
            page_frame,
            text="Tümü",
            variable=self.page_selection,
            value="all"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            page_frame,
            text=f"Geçerli Sayfa ({self.current_page + 1})",
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
        range_frame.pack(fill=tk.X, padx=(20, 0), pady=(5, 0))
        
        ttk.Entry(
            range_frame,
            textvariable=self.page_range,
            width=30
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            range_frame,
            text=f"(toplam {self.total_pages} sayfa)"
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Label(
            page_frame,
            text="Sayfa numarasını ve/veya ayrılan sayfaların başlangıç numarasını yazın. Örneğin, 1, 3, 5-12 gibi."
        ).pack(anchor=tk.W, padx=(20, 0), pady=(5, 0))
        
        # Önizleme
        preview_frame = ttk.LabelFrame(main_frame, text="Önizleme", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Burada PDF'in ilk sayfasının önizlemesi gösterilebilir
        # Basit bir mesaj ekleyelim
        preview_label = ttk.Label(
            preview_frame,
            text="PDF önizlemesi burada gösterilecek"
        )
        preview_label.pack(expand=True)
        
        # Butonlar
        btn_frame = self.create_buttons_frame()
        
        self.add_button(
            btn_frame,
            text="Yazdır",
            command=self.ok,
            style="primary"
        )
        
        self.add_button(
            btn_frame,
            text="İptal",
            command=self.cancel,
            style="danger"
        )
        
    def get_available_printers(self):
        """Sistem yazıcılarını al."""
        printers = []
        
        try:
            if platform.system() == "Windows":
                # Windows için yazıcı listesini al
                import win32print
                for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
                    printers.append(printer[2])
            elif platform.system() == "Darwin":  # macOS
                # macOS için yazıcı listesini al
                import subprocess
                output = subprocess.check_output(["lpstat", "-p"], universal_newlines=True)
                for line in output.split('\n'):
                    if line.startswith("printer "):
                        printers.append(line.split(" ")[1])
            else:  # Linux ve diğer sistemler
                # CUPS yazıcılarını al
                import subprocess
                output = subprocess.check_output(["lpstat", "-p"], universal_newlines=True)
                for line in output.split('\n'):
                    if line.startswith("printer "):
                        printers.append(line.split(" ")[1])
        except Exception as e:
            print(f"Yazıcı listesi alınırken hata oluştu: {e}")
            # Hata durumunda varsayılan yazıcı adı ekle
            printers = ["HP LaserJet 1020"]
            
        return printers
    
    def show_printer_properties(self):
        """Yazıcı özelliklerini göster."""
        messagebox.showinfo(
            "Yazıcı Özellikleri",
            "Bu özellik henüz uygulanmadı."
        )
    
    def get_selected_pages(self):
        """Seçilen sayfaları al."""
        if self.page_selection.get() == "all":
            return list(range(self.total_pages))
        elif self.page_selection.get() == "current":
            return [self.current_page]
        elif self.page_selection.get() == "range":
            pages = []
            try:
                # Sayfa aralığını ayrıştır
                range_str = self.page_range.get().strip()
                if not range_str:
                    return list(range(self.total_pages))
                
                parts = range_str.split(',')
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-')
                        start = int(start.strip()) - 1  # 0-indexed
                        end = int(end.strip())
                        pages.extend(range(start, end))
                    else:
                        pages.append(int(part.strip()) - 1)  # 0-indexed
            except Exception as e:
                messagebox.showerror(
                    "Hata",
                    f"Sayfa aralığı ayrıştırılırken hata oluştu: {e}"
                )
                return []
            
            return pages
        
        return []
    
    def print_pdf(self):
        """PDF'i yazdır."""
        selected_pages = self.get_selected_pages()
        if not selected_pages:
            messagebox.showerror(
                "Hata",
                "Yazdırılacak sayfa seçilmedi."
            )
            return False
        
        try:
            # Geçici bir dosya oluştur
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Seçilen sayfaları içeren yeni bir PDF oluştur
            new_doc = self.pdf_manager.doc.new_doc()
            for page_num in selected_pages:
                if 0 <= page_num < self.total_pages:
                    new_doc.insert_pdf(self.pdf_manager.doc, from_page=page_num, to_page=page_num)
            
            # Geçici dosyaya kaydet
            new_doc.save(temp_path)
            
            # Sistem yazıcısına gönder
            if platform.system() == "Windows":
                # Windows'ta yazdırma
                try:
                    import win32print
                    import win32api
                    
                    printer_name = self.printer_name.get()
                    if not printer_name:
                        printer_name = win32print.GetDefaultPrinter()
                    
                    # Yazdırma işlemi
                    win32api.ShellExecute(
                        0, 
                        "print", 
                        temp_path,
                        f'/d:"{printer_name}"', 
                        ".", 
                        0
                    )
                    return True
                except ImportError:
                    # win32print ve win32api yoksa, varsayılan uygulamayla aç
                    os.startfile(temp_path, "print")
                    return True
            elif platform.system() == "Darwin":  # macOS
                # macOS'ta yazdırma
                subprocess.call(["lpr", "-P", self.printer_name.get(), temp_path])
                return True
            else:  # Linux ve diğer sistemler
                # CUPS ile yazdırma
                subprocess.call(["lpr", "-P", self.printer_name.get(), temp_path])
                return True
                
        except Exception as e:
            messagebox.showerror(
                "Hata",
                f"Yazdırma işlemi sırasında hata oluştu: {e}"
            )
            return False
    
    def ok(self):
        """Yazdır butonuna tıklandığında."""
        if self.print_pdf():
            self.result = True
            self.close()
        
    def cancel(self):
        """İptal butonuna tıklandığında."""
        self.result = None
        self.close()
