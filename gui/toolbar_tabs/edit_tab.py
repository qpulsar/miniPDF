"""
Edit tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from gui.toolbar_tabs.base_tab import BaseTab
from gui.utils import create_icon_button
from gui.utils.messages import INFO_TITLE, PDF_OPEN_REQUIRED
from gui.dialogs.text_extraction_dialog import TextExtractionDialog

class EditTab(BaseTab):
    """Edit tab for the toolbar."""
    
    def __init__(self, parent, app):
        """
        Initialize the edit tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        super().__init__(parent, app)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the edit tab."""
        # Text frame
        text_frame = self.create_frame("text", "Metin")
        
        # Extract text button with icon
        create_icon_button(
            text_frame,
            icon_name="extract_text",
            text="Metin Çıkar",
            command=self._extract_text,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Add text button with icon
        create_icon_button(
            text_frame,
            icon_name="text",  # add_text yerine text kullan
            text="Metin Ekle",
            command=self._add_text,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Note operations frame
        note_frame = self.create_frame("note", "Not İşlemleri")
        
        # Add note button with icon
        create_icon_button(
            note_frame,
            icon_name="note",  # add_note yerine note kullan
            text="Not Ekle",
            command=self._add_note,
            compound=tk.LEFT,
            style="secondary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Highlight button with icon
        create_icon_button(
            note_frame,
            icon_name="highlight",
            text="Vurgula",
            command=self._highlight,
            compound=tk.LEFT,
            style="secondary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Drawing frame
        drawing_frame = self.create_frame("drawing", "Çizim")
        
        # Draw button with icon
        create_icon_button(
            drawing_frame,
            icon_name="draw",
            text="Çiz",
            command=self._draw,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
    
    def _extract_text(self):
        """Extract text from the PDF."""
        if not self.check_pdf_open():
            return
        
        # Create a dialog for text extraction
        dialog = TextExtractionDialog(
            self.app.root,
            self.app,
            self.app.pdf_manager.current_file,
            self.app.pdf_manager.current_page_index,
            self._on_extract_text
        )
    
    def _on_extract_text(self, text, save_path=None):
        """
        Callback for text extraction.
        
        Args:
            text (str): Extracted text
            save_path (str, optional): Path to save the text to
        """
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo(INFO_TITLE, f"Metin başarıyla kaydedildi: {save_path}")
            except Exception as e:
                messagebox.showerror("Hata", f"Metin kaydedilirken hata oluştu: {e}")
    
    def _add_text(self):
        """Add text to the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _highlight(self):
        """Highlight text in the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _add_note(self):
        """Add a note to the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _draw(self):
        """Draw on the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
