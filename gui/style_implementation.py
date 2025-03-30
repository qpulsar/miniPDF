"""
Implementation file for applying the custom Material Design style to the miniPDF application.
"""
from PyQt6.QtWidgets import QWidget, QPushButton, QFrame, QLabel, QTabWidget, QTabBar, QToolBar, QToolButton, QSeparator, QTreeWidget, QTreeWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from theme import COLORS, FONTS, PADDING
import logging

# Logging settings
logger = logging.getLogger(__name__)

def apply_style_to_widget(widget):
    """Apply styling to a widget.
    
    Args:
        widget: QWidget instance to style
    """
    try:
        # Set font
        widget.setFont(FONTS["DEFAULT"])
        
        # Set padding
        widget.setContentsMargins(
            PADDING["MEDIUM"],
            PADDING["MEDIUM"],
            PADDING["MEDIUM"],
            PADDING["MEDIUM"]
        )
        
        # Set background color
        widget.setStyleSheet(f"background-color: {COLORS['BACKGROUND']};")
        
        # Set text color
        if isinstance(widget, QLabel):
            widget.setStyleSheet(f"background-color: {COLORS['BACKGROUND']}; color: {COLORS['TEXT']};")
        
        # Set button styles
        if isinstance(widget, QPushButton):
            widget.setStyleSheet(f"background-color: {COLORS['PRIMARY']}; color: {COLORS['ON_PRIMARY']};")
        
        # Set tab widget styles
        if isinstance(widget, QTabWidget):
            widget.setStyleSheet(f"background-color: {COLORS['BACKGROUND']};")
            tab_bar = widget.tabBar()
            tab_bar.setStyleSheet(f"background-color: {COLORS['PRIMARY']}; color: {COLORS['ON_PRIMARY']};")
            tab_bar.setTabTextColor(0, QColor(COLORS['ON_PRIMARY']))
        
        # Set toolbar styles
        if isinstance(widget, QToolBar):
            widget.setStyleSheet(f"background-color: {COLORS['BACKGROUND']};")
        
        # Set tool button styles
        if isinstance(widget, QToolButton):
            widget.setStyleSheet(f"background-color: {COLORS['PRIMARY']}; color: {COLORS['ON_PRIMARY']};")
        
        # Set separator styles
        if isinstance(widget, QSeparator):
            widget.setStyleSheet(f"background-color: {COLORS['BORDER']};")
        
        # Set tree widget styles
        if isinstance(widget, QTreeWidget):
            widget.setStyleSheet(f"background-color: {COLORS['BACKGROUND']}; color: {COLORS['TEXT']};")
            header = widget.header()
            header.setStyleSheet(f"background-color: {COLORS['PRIMARY']}; color: {COLORS['ON_PRIMARY']};")
        
    except Exception as e:
        logger.error(f"Error applying style to widget: {e}")

def style_important_button(button):
    """Apply accent styling to important buttons.
    
    Args:
        button: QPushButton instance to style
    """
    try:
        button.setStyleSheet(f"background-color: {COLORS['ACCENT']}; color: {COLORS['ON_PRIMARY']};")
        
    except Exception as e:
        logger.error(f"Error styling important button: {e}")

def apply_style_to_app(app):
    """Apply the custom style to the entire application.
    
    Args:
        app: Main application instance
    """
    try:
        # Apply style to all widgets
        for widget in app.findChildren(QWidget):
            apply_style_to_widget(widget)
            
    except Exception as e:
        logger.error(f"Error applying style to app: {e}")

def apply_style_to_dialog(dialog):
    """Apply the custom style to a dialog window.
    
    Args:
        dialog: Dialog window instance
    """
    try:
        # Apply style to all widgets in dialog
        for widget in dialog.findChildren(QWidget):
            apply_style_to_widget(widget)
            
    except Exception as e:
        logger.error(f"Error applying style to dialog: {e}")
