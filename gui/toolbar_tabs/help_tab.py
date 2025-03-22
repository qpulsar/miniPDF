"""
Help tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from gui.toolbar_tabs.base_tab import BaseTab
from gui.utils import create_icon_button
from gui.utils.messages import INFO_TITLE

class HelpTab(BaseTab):
    """Help tab for the toolbar."""
    
    def __init__(self, parent, app):
        """
        Initialize the help tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        super().__init__(parent, app)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the help tab."""
        # Theme selection frame
        theme_frame = self.create_frame("theme", "Tema Seçimi")
        
        # Theme label
        ttk.Label(theme_frame, text="Tema:").pack(side=tk.LEFT, padx=5, pady=5)
        
        # Theme combobox
        self.theme_combobox = ttk.Combobox(
            theme_frame,
            values=ttk.Style().theme_names(),
            state="readonly",
            width=15
        )
        self.theme_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.theme_combobox.set("flatly")
        self.theme_combobox.bind("<<ComboboxSelected>>", self._change_theme)
        
        # Support operations frame
        support_frame = self.create_frame("support", "Destek")
        
        # Contact button with icon
        create_icon_button(
            support_frame,
            icon_name="contact",
            text="İletişim",
            command=self._show_contact,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Report bug button with icon
        create_icon_button(
            support_frame,
            icon_name="bug",
            text="Hata Bildir",
            command=self._report_bug,
            compound=tk.LEFT,
            style="danger",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Documentation frame
        docs_frame = self.create_frame("docs", "Dökümanlar")
        
        # User guide button with icon
        create_icon_button(
            docs_frame,
            icon_name="text",
            text="Kullanım Kılavuzu",
            command=self._show_user_guide,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # FAQ button with icon
        create_icon_button(
            docs_frame,
            icon_name="help",
            text="SSS",
            command=self._show_faq,
            compound=tk.LEFT,
            style="primary",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # About button with icon
        create_icon_button(
            docs_frame,
            icon_name="info",
            text="Hakkında",
            command=self._show_about,
            compound=tk.LEFT,
            style="info",
            padding=(5, 5)
        ).pack(side=tk.LEFT, padx=2, pady=2)
    
    def _change_theme(self, event):
        """Change the application theme."""
        selected_theme = self.theme_combobox.get()
        self.app.root.style.theme_use(selected_theme)
    
    def _show_user_guide(self):
        """Show the user guide."""
        messagebox.showinfo(
            title=INFO_TITLE,
            message="Kullanım kılavuzu henüz hazır değil."
        )
    
    def _show_faq(self):
        """Show the FAQ."""
        messagebox.showinfo(
            title=INFO_TITLE,
            message="SSS henüz hazır değil."
        )
    
    def _show_about(self):
        """Show the about dialog."""
        messagebox.showinfo(
            title=INFO_TITLE,
            message="miniPDF v1.0.0\n\n"
                   "PDF dosyalarını düzenlemek için basit bir araç.\n\n"
                   " 2024 miniPDF"
        )
    
    def _show_contact(self):
        """Show the contact dialog."""
        messagebox.showinfo(
            title=INFO_TITLE,
            message="İletişim bilgileri henüz hazır değil."
        )
    
    def _report_bug(self):
        """Show the bug report dialog."""
        messagebox.showinfo(
            title=INFO_TITLE,
            message="Hata bildirim formu henüz hazır değil."
        )
