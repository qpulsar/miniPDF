"""
Implementation file for applying the custom pastel minimalist style to the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk
import sys

# Color scheme - Pastel minimalist theme
COLORS = {
    # Primary UI elements (headers, buttons)
    "PRIMARY": "#A8E6CF",
    
    # Important action buttons (delete, save)
    "ACCENT": "#FFAAA5",
    
    # Selected tabs and highlights
    "HIGHLIGHT": "#D4E7FF",
    
    # Background color
    "BACKGROUND": "#F7F7F7",
    
    # Text and icons
    "TEXT": "#4A4A4A",
    
    # Secondary elements
    "SECONDARY": "#E8E8E8",
    
    # Borders and separators
    "BORDER": "#DDDDDD",
}

def apply_style_to_widget(widget):
    """
    Recursively apply styling to a widget and all its children
    
    Args:
        widget: The tkinter widget to style
    """
    widget_class = widget.winfo_class()
    
    if widget_class in ('TFrame', 'Frame'):
        widget.configure(background=COLORS["BACKGROUND"])
    
    elif widget_class in ('TLabel', 'Label'):
        widget.configure(background=COLORS["BACKGROUND"], foreground=COLORS["TEXT"])
    
    elif widget_class in ('TButton', 'Button'):
        widget.configure(background=COLORS["PRIMARY"], foreground=COLORS["TEXT"])
    
    elif widget_class == 'TNotebook':
        style = ttk.Style()
        style.configure('TNotebook', background=COLORS["BACKGROUND"])
        style.configure('TNotebook.Tab', background=COLORS["PRIMARY"], foreground=COLORS["TEXT"])
        style.map('TNotebook.Tab', 
                 background=[('selected', COLORS["HIGHLIGHT"])],
                 foreground=[('selected', COLORS["TEXT"])])
    
    elif widget_class in ('TLabelframe', 'Labelframe'):
        widget.configure(background=COLORS["BACKGROUND"])
        
    elif widget_class == 'Toplevel':
        widget.configure(background=COLORS["BACKGROUND"])
    
    elif widget_class == 'Canvas':
        widget.configure(background=COLORS["BACKGROUND"])
    
    # Apply style to all children
    for child in widget.winfo_children():
        apply_style_to_widget(child)

def style_important_button(button):
    """
    Apply accent styling to important buttons like delete or save
    
    Args:
        button: The button widget to style
    """
    button.configure(background=COLORS["ACCENT"])

def apply_style_to_app(app):
    """
    Apply the custom style to the entire application
    
    Args:
        app: The main application instance
    """
    root = app.root
    
    # Configure ttk style
    style = ttk.Style()
    style.configure('TFrame', background=COLORS["BACKGROUND"])
    style.configure('TLabel', background=COLORS["BACKGROUND"], foreground=COLORS["TEXT"])
    style.configure('TButton', background=COLORS["PRIMARY"], foreground=COLORS["TEXT"])
    style.configure('Accent.TButton', background=COLORS["ACCENT"], foreground=COLORS["TEXT"])
    style.configure('TNotebook', background=COLORS["BACKGROUND"])
    style.configure('TNotebook.Tab', background=COLORS["PRIMARY"], foreground=COLORS["TEXT"])
    style.map('TNotebook.Tab', 
             background=[('selected', COLORS["HIGHLIGHT"])],
             foreground=[('selected', COLORS["TEXT"])])
    style.configure('TLabelframe', background=COLORS["BACKGROUND"], foreground=COLORS["TEXT"])
    style.configure('TLabelframe.Label', background=COLORS["BACKGROUND"], foreground=COLORS["TEXT"])
    style.configure('Treeview', background=COLORS["BACKGROUND"], fieldbackground=COLORS["BACKGROUND"], foreground=COLORS["TEXT"])
    style.configure('Treeview.Heading', background=COLORS["PRIMARY"], foreground=COLORS["TEXT"])
    style.configure('TSeparator', background=COLORS["BORDER"])
    
    # Apply style to all widgets
    apply_style_to_widget(root)
    
    # Style important buttons
    if hasattr(app, 'toolbar'):
        if hasattr(app.toolbar, 'save_button'):
            style_important_button(app.toolbar.save_button)
        if hasattr(app.toolbar, 'delete_page_button'):
            style_important_button(app.toolbar.delete_page_button)
    
    # Configure root window
    root.configure(background=COLORS["BACKGROUND"])

def apply_style_to_dialog(dialog):
    """
    Apply the custom style to a dialog window
    
    Args:
        dialog: The dialog window instance
    """
    dialog.configure(background=COLORS["BACKGROUND"])
    apply_style_to_widget(dialog)
