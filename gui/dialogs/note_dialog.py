"""
Note dialog for the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk
from gui.dialogs.base_dialog import BaseDialog

class NoteDialog(BaseDialog):
    """Dialog for adding notes to PDF documents."""
    
    def __init__(self, parent, app, page, page_index, on_add_note_callback):
        """
        Initialize the note dialog.
        
        Args:
            parent: Parent widget
            app: Main application instance
            page: PDF page
            page_index: Index of the page
            on_add_note_callback: Callback function for adding the note
        """
        super().__init__(
            parent,
            title="Not Ekle",
            geometry="500x400"
        )
        
        self.app = app
        self.page = page
        self.page_index = page_index
        self.on_add_note_callback = on_add_note_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the dialog."""
        # Create a frame for note properties
        properties_frame = self.create_labeled_frame("Not Özellikleri")
        properties_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Note title
        self.title_var = tk.StringVar(value="Not")
        self.create_form_row(
            properties_frame,
            "Başlık:",
            ttk.Entry,
            variable=self.title_var,
            width=30
        )
        
        # Note icon
        self.icon_var = tk.StringVar(value="note")
        _, icon_combobox = self.create_form_row(
            properties_frame,
            "Simge:",
            ttk.Combobox,
            variable=self.icon_var,
            values=["note", "comment", "help", "insert", "key", "paragraph"],
            width=15,
            state="readonly"
        )
        
        # Note position
        position_frame = ttk.Frame(properties_frame)
        position_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(position_frame, text="Konum (x, y):").pack(side=tk.LEFT, padx=5)
        
        # Default position at 100, 100
        self.x_var = tk.IntVar(value=100)
        x_spinbox = ttk.Spinbox(position_frame, from_=0, to=1000, textvariable=self.x_var, width=5)
        x_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.y_var = tk.IntVar(value=100)
        y_spinbox = ttk.Spinbox(position_frame, from_=0, to=1000, textvariable=self.y_var, width=5)
        y_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Create a frame for note content
        content_frame = self.create_labeled_frame("Not İçeriği")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text area for note content
        self.text_area, _ = self.create_text_area(content_frame, height=10)
        
        # Create a frame for action buttons
        action_frame = self.create_buttons_frame()
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add button
        self.add_button(
            action_frame,
            text="Not Ekle",
            command=self.add_note,
            side=tk.RIGHT
        )
        
        # Cancel button
        self.add_button(
            action_frame,
            text="İptal",
            command=self.dialog.destroy,
            side=tk.RIGHT
        )
        
        # Set focus to the text area
        self.text_area.focus_set()
    
    def add_note(self):
        """Add the note to the PDF page."""
        title = self.title_var.get()
        icon = self.icon_var.get()
        x = self.x_var.get()
        y = self.y_var.get()
        content = self.text_area.get("1.0", tk.END).strip()
        
        if not content:
            tk.messagebox.showwarning("Uyarı", "Not içeriği boş olamaz.")
            return
        
        self.on_add_note_callback(
            self.page,
            self.page_index,
            title,
            content,
            x,
            y,
            icon
        )
        
        self.dialog.destroy()
