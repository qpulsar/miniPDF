"""
Icon utilities for the PDF Editor.
"""
import os
import logging
from PyQt6.QtGui import QIcon, QPainter, QColor
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QStyle

try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False
    
logger = logging.getLogger(__name__)

class IconProvider:
    """Provides icons for the application."""
    
    ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "icons")
    
    @classmethod
    def get_icon(cls, name):
        """Get an icon by name.
        
        Args:
            name: Icon name without extension
            
        Returns:
            QIcon: Icon instance
        """
        # Try SVG first if cairosvg is available
        if HAS_CAIROSVG:
            svg_path = os.path.join(cls.ICON_PATH, f"{name}.svg")
            if os.path.exists(svg_path):
                try:
                    png_path = os.path.join(cls.ICON_PATH, f"{name}.png")
                    cairosvg.svg2png(url=svg_path, write_to=png_path)
                    return QIcon(png_path)
                except Exception as e:
                    logger.error(f"Error converting SVG to PNG: {e}")
        
        # Fallback to built-in icons
        return cls._get_fallback_icon(name)
    
    @staticmethod
    def _get_fallback_icon(name):
        """Get a fallback icon using simple shapes.
        
        Args:
            name: Icon name
            
        Returns:
            QIcon: Icon instance
        """
        icon = QIcon()
        
        # Create a simple shape based on icon name
        if name in ["open", "save", "save_as"]:
            return QIcon.fromTheme(name)
        elif name == "delete":
            return QIcon.fromTheme("edit-delete")
        elif name == "zoom_in":
            return QIcon.fromTheme("zoom-in")
        elif name == "zoom_out":
            return QIcon.fromTheme("zoom-out")
        elif name == "rotate":
            return QIcon.fromTheme("object-rotate-right")
        
        # Default icon
        return QIcon.fromTheme("application-pdf")
