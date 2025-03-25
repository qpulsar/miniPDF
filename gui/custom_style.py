"""
Custom styling for the PDF Editor application.
"""
import ttkbootstrap as ttk
from theme import get_theme_colors, FONTS, PADDING
import logging

# Logging ayarları
logger = logging.getLogger(__name__)

def apply_custom_style(root):
    """Apply custom styling to the application.
    
    Args:
        root: The root Tkinter window
        
    Returns:
        ttk.Style: The style object for further customization if needed
    """
    style = ttk.Style()
    
    # Get colors from the current theme
    COLORS = get_theme_colors(style)
    
    # Stil konfigürasyonlarını bir sözlük olarak tanımlayalım
    style_configs = {
        "TButton": {
            "configure": {
                "background": COLORS["PRIMARY"],
                "foreground": COLORS["ON_PRIMARY"],
                "padding": (PADDING["MEDIUM"], PADDING["SMALL"]),
                "font": FONTS["DEFAULT"],
            }
        },
        "TFrame": {
            "configure": {
                "background": COLORS["BACKGROUND"]
            }
        },
        "TLabel": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"],
                "font": FONTS["DEFAULT"]
            }
        },
        "TNotebook": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "tabmargins": [2, 5, 2, 0]
            }
        },
        "TNotebook.Tab": {
            "configure": {
                "background": COLORS["SECONDARY"],
                "foreground": COLORS["TEXT"],
                "padding": [PADDING["MEDIUM"], PADDING["SMALL"]],
                "font": FONTS["DEFAULT"]
            },
            "map": {
                "background": [("selected", COLORS["HIGHLIGHT"])],
                "foreground": [("selected", COLORS["TEXT"])]
            }
        },
        "TLabelframe": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"],
                "bordercolor": COLORS["BORDER"]
            }
        },
        "TLabelframe.Label": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"],
                "font": FONTS["HEADER"]
            }
        },
        "Treeview": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"],
                "fieldbackground": COLORS["BACKGROUND"]
            }
        },
        "Treeview.Heading": {
            "configure": {
                "background": COLORS["PRIMARY"],
                "foreground": COLORS["ON_PRIMARY"],
                "font": FONTS["HEADER"]
            }
        },
        "TScale": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "troughcolor": COLORS["SECONDARY"],
                "slidercolor": COLORS["PRIMARY"]
            }
        },
        "TScrollbar": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "troughcolor": COLORS["SECONDARY"],
                "arrowcolor": COLORS["TEXT"]
            }
        },
        "TEntry": {
            "configure": {
                "fieldbackground": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"]
            }
        },
        "TCombobox": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"],
                "fieldbackground": COLORS["BACKGROUND"]
            }
        },
        "TRadiobutton": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"]
            }
        },
        "TCheckbutton": {
            "configure": {
                "background": COLORS["BACKGROUND"],
                "foreground": COLORS["TEXT"]
            }
        },
        "Accent.TButton": {
            "configure": {
                "background": COLORS["ACCENT"],
                "foreground": COLORS["ON_PRIMARY"],
                "padding": (PADDING["MEDIUM"], PADDING["SMALL"]),
                "font": FONTS["DEFAULT"]
            }
        }
    }
    
    # Stil konfigürasyonlarını uygula
    try:
        for widget_style, config in style_configs.items():
            # Configure ayarları
            if "configure" in config:
                style.configure(widget_style, **config["configure"])
            
            # Map ayarları
            if "map" in config:
                style.map(widget_style, **config["map"])
    except Exception as e:
        logger.error(f"Error applying style configuration: {e}")
    
    # Set the background color of the root window
    root.configure(background=COLORS["BACKGROUND"])
    
    # Return the style object for further customization if needed
    return style
