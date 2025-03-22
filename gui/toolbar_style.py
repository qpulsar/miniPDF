"""
Custom styling for the toolbar in the PDF Editor application.
"""
import ttkbootstrap as ttk
from theme import get_theme_colors

def apply_toolbar_style(toolbar, style):
    """
    Apply custom styling to the toolbar
    
    Args:
        toolbar: The toolbar instance
        style: The ttk style object
    """
    # Get colors from the current theme
    colors = get_theme_colors(style)
    
    # Configure the TButton style
    style.configure(
        "TButton",
        background=colors["PRIMARY"],
        foreground=colors["ON_PRIMARY"]
    )
    
    # Configure important buttons style
    style.configure(
        "Accent.TButton",
        background=colors["ACCENT"],
        foreground=colors["ON_PRIMARY"]
    )
    
    # Configure the TFrame style
    style.configure(
        "TFrame",
        background=colors["BACKGROUND"]
    )
    
    # Configure the TLabel style
    style.configure(
        "TLabel",
        background=colors["BACKGROUND"],
        foreground=colors["TEXT"]
    )
    
    # Configure the TNotebook style
    style.configure(
        "TNotebook",
        background=colors["BACKGROUND"]
    )
    
    # Configure the TNotebook.Tab style
    style.configure(
        "TNotebook.Tab",
        background=colors["PRIMARY"],
        foreground=colors["ON_PRIMARY"]
    )
    
    # Configure selected tab
    style.map(
        "TNotebook.Tab",
        background=[("selected", colors["HIGHLIGHT"])],
        foreground=[("selected", colors["TEXT"])]
    )
    
    # Configure the TLabelframe style
    style.configure(
        "TLabelframe",
        background=colors["BACKGROUND"],
        foreground=colors["TEXT"]
    )
    
    # Configure the TLabelframe.Label style
    style.configure(
        "TLabelframe.Label",
        background=colors["BACKGROUND"],
        foreground=colors["TEXT"]
    )
    
    # Apply style to important buttons
    if hasattr(toolbar, 'save_button'):
        toolbar.save_button.configure(style="Accent.TButton")
    
    if hasattr(toolbar, 'delete_page_button'):
        toolbar.delete_page_button.configure(style="Accent.TButton")
