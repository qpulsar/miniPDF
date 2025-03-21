"""
View tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.toolbar_tabs.base_tab import BaseTab

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
        
        # Zoom in button
        self.add_button(
            zoom_frame,
            text="Yakınlaştır",
            command=self._zoom_in
        )
        
        # Zoom out button
        self.add_button(
            zoom_frame,
            text="Uzaklaştır",
            command=self._zoom_out
        )
        
        # Layout frame
        layout_frame = self.create_frame("layout", "Düzen")
        
        # Page layout button
        self.add_button(
            layout_frame,
            text="Sayfa Düzeni",
            command=self._change_page_layout
        )
        
        # Theme frame
        theme_frame = self.create_frame("theme", "Tema")
        
        # Theme button
        self.add_button(
            theme_frame,
            text="Tema Değiştir",
            command=self._change_theme
        )
    
    def _zoom_in(self):
        """Zoom in on the PDF."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        self.app.zoom_in()
    
    def _zoom_out(self):
        """Zoom out on the PDF."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        self.app.zoom_out()
    
    def _change_page_layout(self):
        """Change the page layout."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        # Create a dialog for layout options
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Sayfa Düzeni")
        dialog.geometry("300x250")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Create a frame for layout options
        layout_frame = ttk.LabelFrame(dialog, text="Düzen Seçenekleri")
        layout_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a variable for the layout
        layout_var = tk.StringVar(value="single")
        
        # Create radio buttons for layout options
        layouts = [
            ("single", "Tek Sayfa"),
            ("double", "Çift Sayfa"),
            ("continuous", "Sürekli Kaydırma"),
            ("book", "Kitap Görünümü")
        ]
        
        for value, text in layouts:
            ttk.Radiobutton(
                layout_frame,
                text=text,
                variable=layout_var,
                value=value
            ).pack(anchor=tk.W, padx=20, pady=10)
        
        # Add buttons frame
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add apply button
        ttk.Button(
            buttons_frame,
            text="Uygula",
            command=lambda: self._apply_page_layout(dialog, layout_var.get())
        ).pack(side=tk.RIGHT, padx=5)
        
        # Add cancel button
        ttk.Button(
            buttons_frame,
            text="İptal",
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _apply_page_layout(self, dialog, layout):
        """
        Apply the selected page layout.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            layout (str): Selected layout
        """
        # Apply the layout
        self.app.change_page_layout(layout)
        
        # Close the dialog
        dialog.destroy()
    
    def _change_theme(self):
        """Change the application theme."""
        # Create a dialog for theme options
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Tema Değiştir")
        dialog.geometry("300x300")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Create a frame for theme options
        theme_frame = ttk.LabelFrame(dialog, text="Tema Seçenekleri")
        theme_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a variable for the theme
        theme_var = tk.StringVar(value="light")
        
        # Create radio buttons for theme options
        themes = [
            ("light", "Açık Tema"),
            ("dark", "Koyu Tema"),
            ("blue", "Mavi Tema"),
            ("green", "Yeşil Tema"),
            ("purple", "Mor Tema")
        ]
        
        for value, text in themes:
            ttk.Radiobutton(
                theme_frame,
                text=text,
                variable=theme_var,
                value=value
            ).pack(anchor=tk.W, padx=20, pady=10)
        
        # Add buttons frame
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add apply button
        ttk.Button(
            buttons_frame,
            text="Uygula",
            command=lambda: self._apply_theme(dialog, theme_var.get())
        ).pack(side=tk.RIGHT, padx=5)
        
        # Add cancel button
        ttk.Button(
            buttons_frame,
            text="İptal",
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _apply_theme(self, dialog, theme):
        """
        Apply the selected theme.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            theme (str): Selected theme
        """
        # Apply the theme
        self.app.change_theme(theme)
        
        # Close the dialog
        dialog.destroy()
