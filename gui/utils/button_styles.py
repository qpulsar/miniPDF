"""
Material Design 3 (M3) button styles for the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from theme import get_theme_colors

# Apply M3 button styles
def apply_m3_button_styles(root):
    """Apply Material Design 3 button styles to the application."""
    # Get the existing style from the root window
    style = ttk.Style()
    
    # Get theme colors
    colors = style.colors
    
    # Get our custom theme colors mapping
    theme_colors = get_theme_colors(style)
    
    # Button styles
    button_style = {
        "background": theme_colors["PRIMARY"],
        "foreground": theme_colors["ON_PRIMARY"],
        "font": ("Roboto", 14),
        "borderwidth": 0,
        "relief": tk.FLAT,
        "padding": (16, 8),
        "cursor": "hand2",
    }
    
    button_hover_style = {
        "background": colors.light,  # Lighter primary color
    }
    
    button_active_style = {
        "background": colors.dark,  # Darker primary color
    }
    
    # Configure the TButton style
    style.configure(
        "M3.TButton",
        background=theme_colors["PRIMARY"],
        foreground=theme_colors["ON_PRIMARY"],
        font=("Roboto", 14),
        borderwidth=0,
        relief=tk.FLAT,
        padding=(16, 8),
        cursor="hand2",
    )
    
    # Map hover and active states
    style.map(
        "M3.TButton",
        background=[
            ("active", colors.dark),
            ("!active", theme_colors["PRIMARY"]),
        ],
        foreground=[
            ("active", theme_colors["ON_PRIMARY"]),
            ("!active", theme_colors["ON_PRIMARY"]),
        ],
    )
    
    # Configure other styles
    style.configure(
        "TLabel",
        background=theme_colors["BACKGROUND"],
        foreground=theme_colors["TEXT"],
        font=("Roboto", 12),
    )
    
    style.configure(
        "TFrame",
        background=theme_colors["BACKGROUND"],
    )
    
    style.configure(
        "TCombobox",
        fieldbackground=theme_colors["BACKGROUND"],
        foreground=theme_colors["TEXT"],
        background=theme_colors["BACKGROUND"],
    )
    
    style.configure(
        "TEntry",
        fieldbackground=theme_colors["BACKGROUND"],
        foreground=theme_colors["TEXT"],
        background=theme_colors["BACKGROUND"],
    )
