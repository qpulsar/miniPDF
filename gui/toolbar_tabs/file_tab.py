"""
File tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
import os
from gui.toolbar_tabs.base_tab import BaseTab
from gui.utils import create_icon_button
from gui.utils.messages import INFO_TITLE

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
        """Export the current PDF page as an image."""
        self.app.export_as_image()
    
    def _export_as_text(self):
        """Export the PDF as text."""
        self.app.export_as_text()
    
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
