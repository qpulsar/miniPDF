"""
Main entry point for the PDF Editor application.
"""
import sys
import os
import locale

# Set default locale to handle unsupported locale settings
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, 'C')

# Monkey patch locale.setlocale to prevent errors
original_setlocale = locale.setlocale

def patched_setlocale(category, loc=None):
    try:
        return original_setlocale(category, loc)
    except locale.Error:
        if loc is None or loc == '':
            return 'C'
        return loc

# Apply the patch
locale.setlocale = patched_setlocale

# Now import ttkbootstrap
import ttkbootstrap as ttk

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.app import PDFEditorApp
from gui.utils.button_styles import apply_m3_button_styles
import config

def main():
    """Start the PDF Editor application."""
    # Use ttkbootstrap Window instead of ThemedTk
    root = ttk.Window(themename=config.THEME)
    root.title(config.APP_NAME)
    root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    
    # Apply M3 button styles
    apply_m3_button_styles(root)
    
    app = PDFEditorApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
