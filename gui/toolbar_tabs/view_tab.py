"""
View tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.toolbar_tabs.base_tab import BaseTab
from gui.utils import create_icon_button

class ViewTab(BaseTab):
    """View tab for the toolbar."""
    
    def __init__(self, parent, app):
        """
        Initialize the view tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        super().__init__(parent, app)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the view tab."""
        # Zoom frame
        zoom_frame = self.create_frame("zoom", "Yakınlaştırma")
        
        # Zoom in button with icon
        create_icon_button(
            zoom_frame,
            icon_name="zoom_in",
            text="Yakınlaştır",
            command=self._zoom_in,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Zoom out button with icon
        create_icon_button(
            zoom_frame,
            icon_name="zoom_out",
            text="Uzaklaştır",
            command=self._zoom_out,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Fit to width button with icon
        create_icon_button(
            zoom_frame,
            icon_name="fullscreen",
            text="Genişliğe Sığdır",
            command=self._fit_to_width,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Fit to page button with icon
        create_icon_button(
            zoom_frame,
            icon_name="fullscreen_exit",
            text="Sayfaya Sığdır",
            command=self._fit_to_page,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Display frame
        display_frame = self.create_frame("display", "Görünüm")
        
        # Toggle thumbnails button with icon
        create_icon_button(
            display_frame,
            icon_name="image",
            text="Küçük Resimler",
            command=self._toggle_thumbnails,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Toggle outline button with icon
        create_icon_button(
            display_frame,
            icon_name="text",
            text="İçindekiler",
            command=self._toggle_outline,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
    
    def _zoom_in(self):
        """Zoom in the PDF view."""
        if not self.check_pdf_open():
            return
        
        self.app.preview.zoom_in()
    
    def _zoom_out(self):
        """Zoom out the PDF view."""
        if not self.check_pdf_open():
            return
        
        self.app.preview.zoom_out()
    
    def _fit_to_width(self):
        """Fit the PDF to the width of the view."""
        if not self.check_pdf_open():
            return
        
        self.app.preview.fit_to_width()
    
    def _fit_to_page(self):
        """Fit the PDF to the page of the view."""
        if not self.check_pdf_open():
            return
        
        self.app.preview.fit_to_page()
    
    def _toggle_thumbnails(self):
        """Toggle the thumbnails panel."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _toggle_outline(self):
        """Toggle the outline panel."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
