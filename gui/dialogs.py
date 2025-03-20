"""
Dialog windows for the PDF Editor application.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class TextExtractionDialog:
    """Dialog for extracting text from PDF documents."""
    
    def __init__(self, parent, app, doc, selected_page_index, on_extract_callback):
        """Initialize the text extraction dialog.
        
        Args:
            parent: Parent widget
            app: Main application instance
            doc: PyMuPDF Document object
            selected_page_index: Index of the selected page
            on_extract_callback: Callback function for extraction
        """
        self.parent = parent
        self.app = app
        self.doc = doc
        self.selected_page_index = selected_page_index
        self.on_extract_callback = on_extract_callback
        
        # Create the dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Extract Text")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create a frame for extraction options
        options_frame = ttk.LabelFrame(self.dialog, text="Extraction Options")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Radio buttons for extraction scope
        self.scope_var = tk.StringVar(value="current_page")
        
        current_page_radio = ttk.Radiobutton(
            options_frame,
            text=f"Current Page (Page {selected_page_index + 1})",
            variable=self.scope_var,
            value="current_page"
        )
        current_page_radio.pack(anchor=tk.W, padx=10, pady=5)
        
        all_pages_radio = ttk.Radiobutton(
            options_frame,
            text="All Pages",
            variable=self.scope_var,
            value="all_pages"
        )
        all_pages_radio.pack(anchor=tk.W, padx=10, pady=5)
        
        # Create a frame for the text display
        text_frame = ttk.LabelFrame(self.dialog, text="Extracted Text")
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text area for displaying extracted text
        self.text_area = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a frame for action buttons
        action_frame = ttk.Frame(self.dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Extract button
        extract_button = ttk.Button(
            action_frame,
            text="Extract",
            command=self.extract_text
        )
        extract_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        save_button = ttk.Button(
            action_frame,
            text="Save to File",
            command=self.save_text
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_button = ttk.Button(
            action_frame,
            text="Close",
            command=self.dialog.destroy
        )
        close_button.pack(side=tk.RIGHT, padx=5)
    
    def extract_text(self):
        """Extract text based on selected options."""
        scope = self.scope_var.get()
        self.on_extract_callback(self.dialog, scope, self.selected_page_index, self.text_area)
    
    def save_text(self):
        """Save the extracted text to a file."""
        text = self.text_area.get("1.0", tk.END)
        
        if not text.strip():
            messagebox.showinfo("Info", "No text to save.")
            return
        
        # Ask user where to save the text
        save_path = filedialog.asksaveasfilename(
            title="Save Extracted Text",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if not save_path:
            return
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            messagebox.showinfo("Success", "Text saved successfully!")
            self.app.status_var.set(f"Text saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text: {e}")
            self.app.status_var.set("Failed to save text")


class NoteDialog:
    """Dialog for adding notes to PDF documents."""
    
    def __init__(self, parent, app, page, page_index, on_add_note_callback):
        """Initialize the note dialog.
        
        Args:
            parent: Parent widget
            app: Main application instance
            page: PyMuPDF Page object
            page_index: Index of the page
            on_add_note_callback: Callback function for adding the note
        """
        self.parent = parent
        self.app = app
        self.page = page
        self.page_index = page_index
        self.on_add_note_callback = on_add_note_callback
        
        # Create the dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Note")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create a frame for note properties
        properties_frame = ttk.LabelFrame(self.dialog, text="Note Properties")
        properties_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Note title
        title_frame = ttk.Frame(properties_frame)
        title_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(title_frame, text="Title:").pack(side=tk.LEFT, padx=5)
        
        self.title_var = tk.StringVar(value="Note")
        title_entry = ttk.Entry(title_frame, textvariable=self.title_var, width=30)
        title_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Note icon
        icon_frame = ttk.Frame(properties_frame)
        icon_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(icon_frame, text="Icon:").pack(side=tk.LEFT, padx=5)
        
        self.icon_var = tk.StringVar(value="note")
        icon_combobox = ttk.Combobox(
            icon_frame, 
            textvariable=self.icon_var, 
            values=["note", "comment", "help", "insert", "key", "paragraph"],
            width=15,
            state="readonly"
        )
        icon_combobox.pack(side=tk.LEFT, padx=5)
        
        # Note position
        position_frame = ttk.Frame(properties_frame)
        position_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(position_frame, text="Position (x, y):").pack(side=tk.LEFT, padx=5)
        
        # Default position at 100, 100
        self.x_var = tk.IntVar(value=100)
        x_spinbox = ttk.Spinbox(position_frame, from_=0, to=1000, textvariable=self.x_var, width=5)
        x_spinbox.pack(side=tk.LEFT, padx=5)
        
        self.y_var = tk.IntVar(value=100)
        y_spinbox = ttk.Spinbox(position_frame, from_=0, to=1000, textvariable=self.y_var, width=5)
        y_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Create a frame for note content
        content_frame = ttk.LabelFrame(self.dialog, text="Note Content")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text area for note content
        self.text_area = tk.Text(content_frame, wrap=tk.WORD, height=10)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a frame for action buttons
        action_frame = ttk.Frame(self.dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Add button
        add_button = ttk.Button(
            action_frame,
            text="Add Note",
            command=self.add_note
        )
        add_button.pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(
            action_frame,
            text="Cancel",
            command=self.dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # Set focus to the text area
        self.text_area.focus_set()
    
    def add_note(self):
        """Add the note to the PDF page."""
        position = (self.x_var.get(), self.y_var.get())
        text = self.text_area.get("1.0", tk.END)
        title = self.title_var.get()
        icon = self.icon_var.get()
        
        self.on_add_note_callback(
            self.dialog,
            self.page,
            self.page_index,
            position,
            text,
            title,
            icon
        )
