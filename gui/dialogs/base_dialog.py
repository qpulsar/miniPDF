"""
Base dialog class for the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk
from gui.utils import (
    create_labeled_frame,
    create_text_area,
    create_buttons_frame,
    add_button,
    create_form_row
)

class BaseDialog:
    """Base class for all dialogs in the application."""
    
    def __init__(self, parent, title, geometry="500x400", transient=True, grab=True):
        """
        Initialize the base dialog.
        
        Args:
            parent: Parent widget
            title (str): Dialog title
            geometry (str): Dialog geometry (default: "500x400")
            transient (bool): Whether the dialog is transient (default: True)
            grab (bool): Whether the dialog should grab focus (default: True)
        """
        self.parent = parent
        
        # Create the dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(geometry)
        
        if transient:
            self.dialog.transient(parent)
        
        if grab:
            self.dialog.grab_set()
    
    def create_labeled_frame(self, text, **kwargs):
        """
        Create a labeled frame in the dialog.
        
        Args:
            text (str): Label text for the frame
            **kwargs: Additional keyword arguments for the frame
            
        Returns:
            ttk.LabelFrame: The created frame
        """
        return create_labeled_frame(self.dialog, text, **kwargs)
    
    def create_text_area(self, parent, **kwargs):
        """
        Create a text area with a scrollbar.
        
        Args:
            parent: Parent widget
            **kwargs: Additional keyword arguments for the text area
            
        Returns:
            tuple: (text_area, scrollbar)
        """
        return create_text_area(parent, **kwargs)
    
    def create_buttons_frame(self, **kwargs):
        """
        Create a frame for action buttons.
        
        Args:
            **kwargs: Additional keyword arguments for the frame
            
        Returns:
            ttk.Frame: The created frame
        """
        return create_buttons_frame(self.dialog, **kwargs)
    
    def add_button(self, parent, text, command, side=tk.LEFT, **kwargs):
        """
        Add a button to a frame.
        
        Args:
            parent: Parent widget
            text (str): Button text
            command: Button command
            side: Pack side (default: tk.LEFT)
            **kwargs: Additional keyword arguments for the button
            
        Returns:
            ttk.Button: The created button
        """
        return add_button(parent, text, command, side, **kwargs)
    
    def create_form_row(self, parent, label_text, widget_class, variable=None, **kwargs):
        """
        Create a form row with a label and a widget.
        
        Args:
            parent: Parent widget
            label_text (str): Label text
            widget_class: Widget class (e.g., ttk.Entry, ttk.Combobox)
            variable: Variable to bind to the widget (default: None)
            **kwargs: Additional keyword arguments for the widget
            
        Returns:
            tuple: (frame, widget)
        """
        return create_form_row(parent, label_text, widget_class, variable, **kwargs)
    
    def show(self):
        """Show the dialog and wait for it to be closed."""
        self.dialog.wait_window()
    
    def close(self):
        """Close the dialog."""
        self.dialog.destroy()
