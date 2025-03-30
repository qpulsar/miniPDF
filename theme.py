"""
Theme configuration for the PDF Editor application.
"""
from PyQt6.QtGui import QFont
import logging

# Logging ayarları
logger = logging.getLogger(__name__)

# Font configurations
FONTS = {
    "DEFAULT": QFont("Segoe UI", 9),
    "HEADING": QFont("Segoe UI", 12, QFont.Weight.Bold),
    "SMALL": QFont("Segoe UI", 8),
}

# Padding values (in pixels)
PADDING = {
    "SMALL": 4,
    "MEDIUM": 8,
    "LARGE": 12,
}

# Icon sizes (in pixels)
ICON_SIZES = {
    "SMALL": 16,
    "MEDIUM": 24,
    "LARGE": 32,
}

# Material theme colors
COLORS = {
    "PRIMARY": "#2196F3",
    "PRIMARY_DARK": "#1976D2",
    "PRIMARY_LIGHT": "#BBDEFB",
    "ACCENT": "#FF4081",
    "ACCENT_DARK": "#F50057",
    "ACCENT_LIGHT": "#FF80AB",
    "BACKGROUND": "#FAFAFA",
    "SURFACE": "#FFFFFF",
    "ERROR": "#B00020",
    "ON_PRIMARY": "#FFFFFF",
    "ON_SECONDARY": "#000000",
    "ON_BACKGROUND": "#000000",
    "ON_SURFACE": "#000000",
    "ON_ERROR": "#FFFFFF",
    "DISABLED": "#9E9E9E",
}

def get_theme_colors():
    """Get the current theme colors.
    
    Returns:
        dict: Dictionary containing theme colors
    """
    return COLORS
