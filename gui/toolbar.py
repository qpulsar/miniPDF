"""
Toolbar module for the PDF Editor application.
This is the main toolbar class that uses the modular tab implementations.
"""
import tkinter as tk
from tkinter import ttk

from gui.toolbar_style import apply_toolbar_style
from gui.toolbar_tabs import FileTab, PageTab, EditTab, ToolsTab, ViewTab, HelpTab

class Toolbar(ttk.Frame):
    """Toolbar widget with MS Office-style ribbon interface for PDF operations."""
    
    def __init__(self, parent, app):
        """Initialize the toolbar.
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent)
        # Apply custom styling
        self.style = ttk.Style()
        apply_toolbar_style(self, self.style)
        self.app = app
        
        # Create the main notebook for the ribbon
        self.ribbon = ttk.Notebook(self)
        self.ribbon.pack(fill=tk.X, expand=False, padx=2, pady=2)
        
        # Create tabs for each category
        self.file_tab = ttk.Frame(self.ribbon)
        self.page_tab = ttk.Frame(self.ribbon)
        self.edit_tab = ttk.Frame(self.ribbon)
        self.tools_tab = ttk.Frame(self.ribbon)
        self.view_tab = ttk.Frame(self.ribbon)
        self.help_tab = ttk.Frame(self.ribbon)
        
        # Add tabs to the notebook
        self.ribbon.add(self.file_tab, text="Dosya")
        self.ribbon.add(self.page_tab, text="Sayfa")
        self.ribbon.add(self.edit_tab, text="Düzenleme")
        self.ribbon.add(self.tools_tab, text="Araçlar")
        self.ribbon.add(self.view_tab, text="Görüntüleme")
        self.ribbon.add(self.help_tab, text="Yardım")
        
        # Initialize all ribbon tabs with their respective classes
        self.file_tab_controller = FileTab(self.file_tab, app)
        self.page_tab_controller = PageTab(self.page_tab, app)
        self.edit_tab_controller = EditTab(self.edit_tab, app)
        self.tools_tab_controller = ToolsTab(self.tools_tab, app)
        self.view_tab_controller = ViewTab(self.view_tab, app)
        self.help_tab_controller = HelpTab(self.help_tab, app)
