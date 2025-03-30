"""
Toolbar styling for the PDF Editor application.
"""
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtCore import Qt
import logging

# Logging settings
logger = logging.getLogger(__name__)

def apply_toolbar_style(toolbar):
    """Apply custom styling to the toolbar.
    
    Args:
        toolbar: QToolBar instance
    """
    try:
        # Set toolbar properties
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setAllowedAreas(Qt.ToolBarArea.TopToolBarArea)
        
        # Set minimum height for the ribbon
        toolbar.setMinimumHeight(110)
        
    except Exception as e:
        logger.error(f"Error applying toolbar style: {e}")
        # If styling fails, ensure basic functionality
        toolbar.setMovable(False)
