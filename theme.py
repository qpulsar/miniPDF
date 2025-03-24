"""
Custom theme configuration for the PDF Editor application.
Uses ttkbootstrap theme colors for consistent styling.
"""
import ttkbootstrap as ttk
import logging
from functools import lru_cache

# Logging ayarları
logger = logging.getLogger(__name__)

# Tema renklerini önbelleğe alarak performansı artırma
@lru_cache(maxsize=8)
def get_theme_colors(style=None):
    """
    Get the colors from the current ttkbootstrap theme.
    
    Args:
        style: ttk.Style instance, if None a new one will be created
        
    Returns:
        Dictionary with color definitions
    """
    if style is None:
        style = ttk.Style()
    
    # Define default colors in case we can't get them from the style
    default_colors = {
        "primary": "#007bff",
        "secondary": "#6c757d",
        "success": "#28a745",
        "info": "#17a2b8",
        "warning": "#ffc107",
        "danger": "#dc3545",
        "light": "#f8f9fa",
        "dark": "#343a40",
        "bg": "#ffffff",
        "fg": "#212529",
        "border": "#dee2e6",
    }
    
    # Try to get colors from the ttkbootstrap theme
    theme_colors = {}
    try:
        if hasattr(style, 'colors'):
            # The colors attribute might be an object with attributes, not a dictionary
            colors_obj = style.colors
            
            # Safely get attributes from the colors object
            theme_colors = {
                "primary": getattr(colors_obj, "primary", default_colors["primary"]),
                "secondary": getattr(colors_obj, "secondary", default_colors["secondary"]),
                "success": getattr(colors_obj, "success", default_colors["success"]),
                "info": getattr(colors_obj, "info", default_colors["info"]),
                "warning": getattr(colors_obj, "warning", default_colors["warning"]),
                "danger": getattr(colors_obj, "danger", default_colors["danger"]),
                "light": getattr(colors_obj, "light", default_colors["light"]),
                "dark": getattr(colors_obj, "dark", default_colors["dark"]),
                "bg": getattr(colors_obj, "bg", default_colors["bg"]),
                "fg": getattr(colors_obj, "fg", default_colors["fg"]),
                "border": getattr(colors_obj, "border", default_colors["border"]),
            }
        else:
            # Get colors from the current theme
            theme_name = style.theme_use()
            
            # Extract some colors from the current theme
            bg_color = style.lookup('TFrame', 'background') or default_colors["bg"]
            fg_color = style.lookup('TLabel', 'foreground') or default_colors["fg"]
            primary_color = style.lookup('TButton', 'background') or default_colors["primary"]
            
            # Create a colors dictionary
            theme_colors = {
                "primary": primary_color,
                "secondary": default_colors["secondary"],
                "success": default_colors["success"],
                "info": default_colors["info"],
                "warning": default_colors["warning"],
                "danger": default_colors["danger"],
                "light": default_colors["light"],
                "dark": default_colors["dark"],
                "bg": bg_color,
                "fg": fg_color,
                "border": default_colors["border"],
            }
    except Exception as e:
        # If anything goes wrong, use default colors
        logger.warning(f"Could not get theme colors: {e}")
        theme_colors = default_colors
    
    # Determine contrasting text colors for primary, secondary, etc.
    def get_contrasting_color(bg_color):
        """Calculate a contrasting text color (black or white) based on background color brightness."""
        if not bg_color or not bg_color.startswith('#'):
            return "#FFFFFF"  # Default to white text
            
        try:
            # Convert hex to RGB
            r = int(bg_color[1:3], 16)
            g = int(bg_color[3:5], 16)
            b = int(bg_color[5:7], 16)
            
            # Calculate brightness (simplified formula)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            
            # Return white for dark colors, black for light colors
            return "#FFFFFF" if brightness < 128 else "#000000"
        except Exception as e:
            logger.warning(f"Error calculating contrasting color: {e}")
            return "#FFFFFF"  # Default to white text
    
    # Get contrasting text colors
    primary_color = theme_colors.get("primary", default_colors["primary"])
    secondary_color = theme_colors.get("secondary", default_colors["secondary"])
    
    on_primary = get_contrasting_color(primary_color)
    on_secondary = get_contrasting_color(secondary_color)
    
    # Create the final color dictionary
    colors = {
        # Primary UI elements (headers, buttons)
        "PRIMARY": theme_colors.get("primary", default_colors["primary"]),
        
        # Important action buttons (delete, save)
        "ACCENT": theme_colors.get("danger", default_colors["danger"]),
        
        # Selected tabs and highlights
        "HIGHLIGHT": theme_colors.get("info", default_colors["info"]),
        
        # Background color
        "BACKGROUND": theme_colors.get("bg", default_colors["bg"]),
        
        # Text and icons
        "TEXT": theme_colors.get("fg", default_colors["fg"]),
        
        # Secondary elements
        "SECONDARY": theme_colors.get("secondary", default_colors["secondary"]),
        
        # Borders and separators
        "BORDER": theme_colors.get("border", default_colors["border"]),
        
        # Success messages and indicators
        "SUCCESS": theme_colors.get("success", default_colors["success"]),
        
        # Warning messages and indicators
        "WARNING": theme_colors.get("warning", default_colors["warning"]),
        
        # Error messages and indicators
        "ERROR": theme_colors.get("danger", default_colors["danger"]),
        
        # On primary (text on primary color)
        "ON_PRIMARY": on_primary,
        
        # On secondary (text on secondary color)
        "ON_SECONDARY": on_secondary,
        
        # On background (text on background color)
        "ON_BACKGROUND": theme_colors.get("fg", default_colors["fg"]),
    }
    
    return colors

# Padding ve spacing sabitleri
PADDING = {
    "SMALL": 5,
    "MEDIUM": 10,
    "LARGE": 15,
}

# Font yapılandırmaları
FONTS = {
    "DEFAULT": ("Helvetica", 10),
    "HEADER": ("Helvetica", 12, "bold"),
    "SMALL": ("Helvetica", 9),
}
