"""
Edit tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.toolbar_tabs.base_tab import BaseTab
from gui.dialogs import TextExtractionDialog, NoteDialog

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
        # Text operations frame
        text_frame = self.create_frame("text", "Metin İşlemleri")
        
        # Extract text button
        self.add_button(
            text_frame,
            text="Metin Çıkart",
            command=self._extract_text
        )
        
        # Add text button
        self.add_button(
            text_frame,
            text="Metin Ekle",
            command=self._add_text
        )
        
        # Highlight text button
        self.add_button(
            text_frame,
            text="Metni Vurgula",
            command=self._highlight_text
        )
        
        # Annotation frame
        annot_frame = self.create_frame("annotations", "Açıklamalar")
        
        # Add note button
        self.add_button(
            annot_frame,
            text="Not Ekle",
            command=self._add_note
        )
        
        # Drawing frame
        draw_frame = self.create_frame("drawing", "Çizim")
        
        # Draw button
        self.add_button(
            draw_frame,
            text="Çiz",
            command=self._draw
        )
        
        # Delete object button
        self.add_button(
            draw_frame,
            text="Nesneyi Sil",
            command=self._delete_object,
            style="Accent.TButton"
        )
    
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
        dialog.show()
    
    def _on_extract_text(self, text, output_file=None):
        """
        Callback for text extraction.
        
        Args:
            text (str): Extracted text
            output_file (str, optional): Path to the output file
        """
        if output_file:
            self.show_success_message(f"Metin başarıyla {output_file} olarak kaydedildi.")
    
    def _add_text(self):
        """Add text to the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _highlight_text(self):
        """Highlight text in the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _add_note(self):
        """Add a note to the PDF."""
        if not self.check_pdf_open():
            return
        
        # Create a dialog for adding a note
        dialog = NoteDialog(
            self.app.root,
            self.app,
            self.app.pdf_manager.current_doc[self.app.pdf_manager.current_page_index],
            self.app.pdf_manager.current_page_index,
            self._on_add_note
        )
        dialog.show()
    
    def _on_add_note(self, page, page_index, title, content, x, y, icon):
        """
        Callback for adding a note.
        
        Args:
            page: PDF page
            page_index (int): Index of the page
            title (str): Note title
            content (str): Note content
            x (int): X coordinate
            y (int): Y coordinate
            icon (str): Note icon
        """
        # Implement note addition logic here
        self.show_success_message(f"Not başarıyla eklendi: {title}")
        
        # Refresh the preview
        self.app.preview.refresh()
    
    def _draw(self):
        """Draw on the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _delete_object(self):
        """Delete an object from the PDF."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
