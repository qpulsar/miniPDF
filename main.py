"""
Main entry point for the PDF Editor application.
"""
import sys
import os
import locale
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Locale ayarlarını daha güvenli şekilde yapılandırma ve monkey patch
def configure_locale():
    """Configure locale settings safely and apply monkey patch."""
    try:
        # Try to set the locale to the user's default
        locale.setlocale(locale.LC_ALL, '')
        logger.info(f"Locale set to: {locale.getlocale()}")
    except locale.Error as e:
        # If that fails, try English
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            logger.info("Locale set to en_US.UTF-8")
        except locale.Error:
            # If that also fails, use C locale as fallback
            locale.setlocale(locale.LC_ALL, 'C')
            logger.info("Locale set to C (fallback)")
    
    # Monkey patch locale.setlocale to prevent errors in ttkbootstrap
    original_setlocale = locale.setlocale
    
    def patched_setlocale(category, loc=None):
        try:
            return original_setlocale(category, loc)
        except locale.Error:
            logger.warning(f"Locale error suppressed for: {loc}")
            if loc is None or loc == '':
                return 'C'
            return loc
    
    # Apply the patch
    locale.setlocale = patched_setlocale
    logger.info("Applied locale monkey patch for ttkbootstrap compatibility")

# Configure locale before importing other modules
configure_locale()

# Now import ttkbootstrap
import ttkbootstrap as ttk

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.app import PDFEditorApp
from gui.utils.button_styles import apply_m3_button_styles
import config

def main():
    """Start the PDF Editor application."""
    try:
        # Use ttkbootstrap Window instead of ThemedTk
        root = ttk.Window(themename=config.THEME)
        root.title(config.APP_NAME)
        root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
        # Apply M3 button styles
        apply_m3_button_styles(root)
        
        app = PDFEditorApp(root)
        
        root.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
