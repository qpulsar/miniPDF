"""
File tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk
import sys
from gui.toolbar_tabs.base_tab import BaseTab

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
        
        # Open button
        self.add_button(
            file_frame,
            text="PDF Aç",
            command=self.app.open_pdf
        )
        
        # Save button
        self.add_button(
            file_frame,
            text="PDF Kaydet",
            command=self.app.save_pdf,
            style="Accent.TButton"
        )
        
        # Save As button
        self.add_button(
            file_frame,
            text="Farklı Kaydet",
            command=self.app.save_pdf
        )
        
        # Export operations frame
        export_frame = self.create_frame("export", "Dışa Aktar")
        
        # Export as image
        self.add_button(
            export_frame,
            text="Görüntü Olarak",
            command=self._export_as_image
        )
        
        # Export as text
        self.add_button(
            export_frame,
            text="Metin Olarak",
            command=self._export_as_text
        )
        
        # Print operations frame
        print_frame = self.create_frame("print", "Yazdır")
        
        # Print button
        self.add_button(
            print_frame,
            text="Yazdır",
            command=self._print_pdf
        )
        
        # Exit frame
        exit_frame = self.create_frame("exit", "Çıkış")
        
        # Exit button
        self.add_button(
            exit_frame,
            text="Çıkış",
            command=self._close_application
        )
    
    def _export_as_image(self):
        """Export the current PDF page as an image."""
        self.app.export_as_image()
    
    def _export_as_text(self):
        """Export the PDF as text."""
        self.app.export_as_text()
    
    def _print_pdf(self):
        """Print the current PDF."""
        if not self.app.pdf_manager.current_file:
            return
        
        # On macOS, use the default PDF viewer to print
        if sys.platform == "darwin":
            import subprocess
            subprocess.run(["open", "-a", "Preview", self.app.pdf_manager.current_file])
        # On Windows, use the default PDF viewer
        elif sys.platform == "win32":
            import os
            os.startfile(self.app.pdf_manager.current_file, "print")
        # On Linux, use xdg-open
        else:
            import subprocess
            subprocess.run(["xdg-open", self.app.pdf_manager.current_file])
    
    def _close_application(self):
        """Close the application."""
        self.app.root.quit()
