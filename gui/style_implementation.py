"""
Implementation file for applying the custom pastel minimalist style to the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk
import sys
import ttkbootstrap as ttk
from theme import get_theme_colors

def apply_style_to_widget(widget, colors=None):
    """
    Recursively apply styling to a widget and all its children
    
    Args:
        widget: The tkinter widget to style
        colors: Dictionary with color definitions, if None will be fetched from theme
    """
    if colors is None:
        style = ttk.Style()
        colors = get_theme_colors(style)
    
    widget_class = widget.winfo_class()
    
    if widget_class in ('TFrame', 'Frame'):
        widget.configure(background=colors["BACKGROUND"])
    
    elif widget_class in ('TLabel', 'Label'):
        widget.configure(background=colors["BACKGROUND"], foreground=colors["TEXT"])
    
    elif widget_class in ('TButton', 'Button'):
        widget.configure(background=colors["PRIMARY"], foreground=colors["ON_PRIMARY"])
    
    elif widget_class == 'TNotebook':
        style = ttk.Style()
        style.configure('TNotebook', background=colors["BACKGROUND"])
        style.configure('TNotebook.Tab', background=colors["PRIMARY"], foreground=colors["ON_PRIMARY"])
        style.map('TNotebook.Tab', 
                 background=[('selected', colors["HIGHLIGHT"])],
                 foreground=[('selected', colors["TEXT"])])
    
    elif widget_class in ('TLabelframe', 'Labelframe'):
        widget.configure(background=colors["BACKGROUND"])
        
    elif widget_class == 'Toplevel':
        widget.configure(background=colors["BACKGROUND"])
    
    elif widget_class == 'Canvas':
        widget.configure(background=colors["BACKGROUND"])
    
    # Apply style to all children
    for child in widget.winfo_children():
        apply_style_to_widget(child, colors)

def style_important_button(button, colors=None):
    """
    Apply accent styling to important buttons like delete or save
    
    Args:
        button: The button widget to style
        colors: Dictionary with color definitions, if None will be fetched from theme
    """
    if colors is None:
        style = ttk.Style()
        colors = get_theme_colors(style)
    
    button.configure(background=colors["ACCENT"])

def apply_style_to_app(app):
    """
    Apply the custom style to the entire application
    
    Args:
        app: The main application instance
    """
    root = app.root
    
    # Configure ttk style
    style = ttk.Style()
    
    # Get colors from the current theme
    colors = get_theme_colors(style)
    
    style.configure('TFrame', background=colors["BACKGROUND"])
    style.configure('TLabel', background=colors["BACKGROUND"], foreground=colors["TEXT"])
    style.configure('TButton', background=colors["PRIMARY"], foreground=colors["ON_PRIMARY"])
    style.configure('Accent.TButton', background=colors["ACCENT"], foreground=colors["ON_PRIMARY"])
    style.configure('TNotebook', background=colors["BACKGROUND"])
    style.configure('TNotebook.Tab', background=colors["PRIMARY"], foreground=colors["ON_PRIMARY"])
    style.map('TNotebook.Tab', 
             background=[('selected', colors["HIGHLIGHT"])],
             foreground=[('selected', colors["TEXT"])])
    style.configure('TLabelframe', background=colors["BACKGROUND"], foreground=colors["TEXT"])
    style.configure('TLabelframe.Label', background=colors["BACKGROUND"], foreground=colors["TEXT"])
    style.configure('Treeview', background=colors["BACKGROUND"], fieldbackground=colors["BACKGROUND"], foreground=colors["TEXT"])
    style.configure('Treeview.Heading', background=colors["PRIMARY"], foreground=colors["ON_PRIMARY"])
    style.configure('TSeparator', background=colors["BORDER"])
    
    # Apply style to all widgets
    apply_style_to_widget(root, colors)
    
    # Style important buttons
    if hasattr(app, 'toolbar'):
        if hasattr(app.toolbar, 'save_button'):
            style_important_button(app.toolbar.save_button, colors)
        if hasattr(app.toolbar, 'delete_page_button'):
            style_important_button(app.toolbar.delete_page_button, colors)
    
    # Configure root window
    root.configure(background=colors["BACKGROUND"])

def apply_style_to_dialog(dialog):
    """
    Apply the custom style to a dialog window
    
    Args:
        dialog: The dialog window instance
    """
    style = ttk.Style()
    colors = get_theme_colors(style)
    
    dialog.configure(background=colors["BACKGROUND"])
    apply_style_to_widget(dialog, colors)
