"""
Main entry point for the PDF Editor application.
"""
import tkinter as tk
import sys
import os
from ttkthemes import ThemedTk

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.app import PDFEditorApp
import config     

def main():
    """Start the PDF Editor application."""
    # Use ThemedTk instead of regular Tk
    root = ThemedTk(theme=config.THEME)
    root.title(config.APP_NAME)
    root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    
    app = PDFEditorApp(root)
    app.run()

if __name__ == "__main__":
    main()
