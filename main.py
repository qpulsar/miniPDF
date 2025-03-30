"""
Main entry point for the PDF Editor application.
"""
import sys
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from gui.app import PDFEditorApp
import config

def main():
    """Start the PDF Editor application."""
    try:
        # Create QApplication instance
        app = QApplication(sys.argv)
        
        # Create main window
        window = PDFEditorApp()
        window.setWindowTitle(config.APP_NAME)
        window.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # Apply material theme
        apply_stylesheet(app, theme='dark_teal.xml')
        
        # Show window and start event loop
        window.show()
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
