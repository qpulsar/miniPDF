"""
Main entry point for the PDF Editor application.
"""
import sys
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet
from gui.app import App

def main():
    """Start the PDF Editor application."""
    try:
        # Create QApplication instance
        app = QApplication(sys.argv)
        
        # Create main window
        print("Creating App instance...")
        window = App()
        print("App instance created")
        print(f"PDF Manager: {window.pdf_manager}")
        print(f"Has open_pdf: {hasattr(window.pdf_manager, 'open_pdf')}")
        if window.pdf_manager:
            print(f"Methods: {dir(window.pdf_manager)}")
        
        window.setWindowTitle("miniPDF Editor")
        window.resize(1200, 800)
        
        # Apply material theme
        apply_stylesheet(app, theme='dark_teal.xml')
        
        # Show window
        window.show()
        
        # Start event loop
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
