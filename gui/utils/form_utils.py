"""
Form utilities for the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk

def create_labeled_frame(parent, text, **kwargs):
    """
    Create a labeled frame.
    
    Args:
        parent: Parent widget
        text (str): Label text for the frame
        **kwargs: Additional keyword arguments for the frame
        
    Returns:
        ttk.LabelFrame: The created frame
    """
    frame = ttk.LabelFrame(parent, text=text, **kwargs)
    return frame

def create_text_area(parent, **kwargs):
    """
    Create a text area with a scrollbar.
    
    Args:
        parent: Parent widget
        **kwargs: Additional keyword arguments for the text area
        
    Returns:
        tuple: (text_area, scrollbar)
    """
    # Eğer wrap parametresi verilmemişse, varsayılan olarak WORD kullan
    if 'wrap' not in kwargs:
        kwargs['wrap'] = tk.WORD
    
    # Create a text area with a scrollbar
    text_area = tk.Text(parent, **kwargs)
    scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    return text_area, scrollbar

def create_buttons_frame(parent, **kwargs):
    """
    Create a frame for action buttons.
    
    Args:
        parent: Parent widget
        **kwargs: Additional keyword arguments for the frame
        
    Returns:
        ttk.Frame: The created frame
    """
    frame = ttk.Frame(parent, **kwargs)
    return frame

def add_button(parent, text, command, side=tk.LEFT, **kwargs):
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
    button = ttk.Button(
        parent,
        text=text,
        command=command,
        **kwargs
    )
    button.pack(side=side, padx=5, pady=5)
    return button

def create_form_row(parent, label_text, widget_class, variable=None, **kwargs):
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
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.X, padx=5, pady=5)
    
    label = ttk.Label(frame, text=label_text)
    label.pack(side=tk.LEFT, padx=5)
    
    if variable is not None:
        widget = widget_class(frame, textvariable=variable, **kwargs)
    else:
        widget = widget_class(frame, **kwargs)
    
    widget.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    return frame, widget
