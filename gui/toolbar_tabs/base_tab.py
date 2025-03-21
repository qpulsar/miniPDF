"""
Base tab class for toolbar tabs in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from gui.utils import add_button
from gui.utils import (
    PDF_OPEN_REQUIRED, FEATURE_NOT_IMPLEMENTED,
    INFO_TITLE, SUCCESS_TITLE
)

class BaseTab:
    """Base class for toolbar tabs."""
    
    def __init__(self, parent, app):
        """
        Initialize the base tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        self.parent = parent
        self.app = app
        self.frames = {}
        
    def create_frame(self, name, text):
        """
        Create a labeled frame in the tab.
        
        Args:
            name (str): Name of the frame
            text (str): Label text for the frame
            
        Returns:
            ttk.LabelFrame: The created frame
        """
        frame = ttk.LabelFrame(self.parent, text=text)
        frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        self.frames[name] = frame
        return frame
    
    def add_button(self, frame, text, command, side=tk.LEFT, **kwargs):
        """
        Add a button to a frame.
        
        Args:
            frame (ttk.Frame): Frame to add the button to
            text (str): Button text
            command: Button command
            side: Pack side (default: tk.LEFT)
            **kwargs: Additional keyword arguments for the button
            
        Returns:
            ttk.Button: The created button
        """
        return add_button(frame, text, command, side, **kwargs)
    
    def check_pdf_open(self):
        """
        Check if a PDF file is open.
        
        Returns:
            bool: True if a PDF is open, False otherwise
        """
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo(INFO_TITLE, PDF_OPEN_REQUIRED)
            return False
        return True
    
    def show_not_implemented(self):
        """Show a message for features that are not yet implemented."""
        messagebox.showinfo(INFO_TITLE, FEATURE_NOT_IMPLEMENTED)
    
    def show_success_message(self, message):
        """
        Show a success message.
        
        Args:
            message (str): Success message to show
        """
        messagebox.showinfo(SUCCESS_TITLE, message)
