"""
Custom styling for the PDF Editor application.
"""
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from theme import get_theme_colors

def apply_custom_style(root):
    """Apply custom styling to the application.
    
    Args:
        root: The root Tkinter window
    """
    style = ttk.Style()
    
    # Get colors from the current theme
    COLORS = get_theme_colors(style)
    
    # Configure the TButton style
    style.configure(
        "TButton",
        background=COLORS["PRIMARY"],
        foreground=COLORS["ON_PRIMARY"],
        padding=(10, 5),
        font=("Helvetica", 10)
    )
    
    # Configure the TFrame style
    style.configure(
        "TFrame",
        background=COLORS["BACKGROUND"]
    )
    
    # Configure the TLabel style
    style.configure(
        "TLabel",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"],
        font=("Helvetica", 10)
    )
    
    # Configure the TNotebook style
    style.configure(
        "TNotebook",
        background=COLORS["BACKGROUND"],
        tabmargins=[2, 5, 2, 0]
    )
    
    # Configure the TNotebook.Tab style
    style.configure(
        "TNotebook.Tab",
        background=COLORS["SECONDARY"],
        foreground=COLORS["TEXT"],
        padding=[10, 5],
        font=("Helvetica", 10)
    )
    
    # Configure selected tab
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLORS["HIGHLIGHT"])],
        foreground=[("selected", COLORS["TEXT"])]
    )
    
    # Configure the TLabelframe style
    style.configure(
        "TLabelframe",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"],
        bordercolor=COLORS["BORDER"]
    )
    
    # Configure the TLabelframe.Label style
    style.configure(
        "TLabelframe.Label",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"],
        font=("Helvetica", 10, "bold")
    )
    
    # Configure the Treeview style
    style.configure(
        "Treeview",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"],
        fieldbackground=COLORS["BACKGROUND"]
    )
    
    # Configure the Treeview.Heading style
    style.configure(
        "Treeview.Heading",
        background=COLORS["PRIMARY"],
        foreground=COLORS["ON_PRIMARY"],
        font=("Helvetica", 10, "bold")
    )
    
    # Configure the TScale style
    style.configure(
        "TScale",
        background=COLORS["BACKGROUND"],
        troughcolor=COLORS["SECONDARY"],
        slidercolor=COLORS["PRIMARY"]
    )
    
    # Configure the TScrollbar style
    style.configure(
        "TScrollbar",
        background=COLORS["BACKGROUND"],
        troughcolor=COLORS["SECONDARY"],
        arrowcolor=COLORS["TEXT"]
    )
    
    # Configure the TEntry style
    style.configure(
        "TEntry",
        fieldbackground=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"]
    )
    
    # Configure the TCombobox style
    style.configure(
        "TCombobox",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"],
        fieldbackground=COLORS["BACKGROUND"]
    )
    
    # Configure the TRadiobutton style
    style.configure(
        "TRadiobutton",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"]
    )
    
    # Configure the TCheckbutton style
    style.configure(
        "TCheckbutton",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"]
    )
    
    # Create special styles for important buttons
    style.configure(
        "Accent.TButton",
        background=COLORS["ACCENT"],
        foreground=COLORS["ON_PRIMARY"],
        padding=(10, 5),
        font=("Helvetica", 10)
    )
    
    # Set the background color of the root window
    root.configure(background=COLORS["BACKGROUND"])
    
    # Return the style object for further customization if needed
    return style
