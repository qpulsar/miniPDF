"""
Material Design 3 (M3) button styles for the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk

# Material Design 3 color palette
PRIMARY_COLOR = "#6750A4"
ON_PRIMARY_COLOR = "#FFFFFF"
SECONDARY_COLOR = "#625B71"
ON_SECONDARY_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#FFFBFE"
ON_BACKGROUND_COLOR = "#1C1B1F"

# Button styles
BUTTON_STYLE = {
    "background": PRIMARY_COLOR,
    "foreground": ON_PRIMARY_COLOR,
    "font": ("Roboto", 14),
    "borderwidth": 0,
    "relief": tk.FLAT,
    "padding": (16, 8),
    "cursor": "hand2",
}

BUTTON_HOVER_STYLE = {
    "background": "#7965B0",  # Lighter primary color
}

BUTTON_ACTIVE_STYLE = {
    "background": "#5C4A8C",  # Darker primary color
}

# Apply M3 button styles
def apply_m3_button_styles(root):
    """Apply Material Design 3 button styles to the application."""
    style = ttk.Style(root)
    
    # Configure the TButton style
    style.configure(
        "M3.TButton",
        **BUTTON_STYLE
    )
    
    # Map hover and active states
    style.map(
        "M3.TButton",
        background=[
            ("active", BUTTON_ACTIVE_STYLE["background"]),
            ("!active", BUTTON_STYLE["background"]),
        ],
        foreground=[
            ("active", BUTTON_STYLE["foreground"]),
            ("!active", BUTTON_STYLE["foreground"]),
        ],
    )
    
    # Set the default button style
    style.theme_use("default")
    style.configure("TButton", **BUTTON_STYLE)
    style.map(
        "TButton",
        background=[
            ("active", BUTTON_ACTIVE_STYLE["background"]),
            ("!active", BUTTON_STYLE["background"]),
        ],
        foreground=[
            ("active", BUTTON_STYLE["foreground"]),
            ("!active", BUTTON_STYLE["foreground"]),
        ],
    )
