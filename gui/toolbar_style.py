"""
Custom styling for the toolbar in the PDF Editor application.
"""

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

def apply_toolbar_style(toolbar, style):
    """
    Apply custom styling to the toolbar
    
    Args:
        toolbar: The toolbar instance
        style: The ttk style object
    """
    # Configure the TButton style
    style.configure(
        "TButton",
        background=COLORS["PRIMARY"],
        foreground=COLORS["TEXT"]
    )
    
    # Configure important buttons style
    style.configure(
        "Accent.TButton",
        background=COLORS["ACCENT"],
        foreground=COLORS["TEXT"]
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
        foreground=COLORS["TEXT"]
    )
    
    # Configure the TNotebook style
    style.configure(
        "TNotebook",
        background=COLORS["BACKGROUND"]
    )
    
    # Configure the TNotebook.Tab style
    style.configure(
        "TNotebook.Tab",
        background=COLORS["PRIMARY"],
        foreground=COLORS["TEXT"]
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
        foreground=COLORS["TEXT"]
    )
    
    # Configure the TLabelframe.Label style
    style.configure(
        "TLabelframe.Label",
        background=COLORS["BACKGROUND"],
        foreground=COLORS["TEXT"]
    )
    
    # Apply style to important buttons
    if hasattr(toolbar, 'save_button'):
        toolbar.save_button.configure(style="Accent.TButton")
    
    if hasattr(toolbar, 'delete_page_button'):
        toolbar.delete_page_button.configure(style="Accent.TButton")
