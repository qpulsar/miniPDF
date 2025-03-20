"""
PDF page preview module.
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io

class PDFPreview(ttk.Frame):
    """Widget for displaying PDF page previews."""
    
    def __init__(self, parent, app):
        """Initialize the PDF preview widget.
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent, relief=tk.SUNKEN, borderwidth=1)
        self.app = app
        
        # Create a frame for the preview controls
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X, side=tk.TOP, pady=5)
        
        # Add zoom controls
        self.zoom_label = ttk.Label(self.control_frame, text="Zoom:")
        self.zoom_label.pack(side=tk.LEFT, padx=5)
        
        self.zoom_var = tk.IntVar(value=100)
        self.zoom_scale = ttk.Scale(
            self.control_frame,
            from_=50,
            to=200,
            orient=tk.HORIZONTAL,
            variable=self.zoom_var,
            length=150,
            command=self._on_zoom_change
        )
        self.zoom_scale.pack(side=tk.LEFT, padx=5)
        
        self.zoom_value_label = ttk.Label(self.control_frame, text="100%", width=5)
        self.zoom_value_label.pack(side=tk.LEFT, padx=5)
        
        # Create a canvas for displaying the PDF page
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        
        # Add scrollbars
        self.h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.v_scrollbar = ttk.Scrollbar(self.canvas_frame)
        self.v_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        
        # Create the canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set,
            bg="light gray"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Configure scrollbars
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        
        # Create an image item on the canvas
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW)
        
        # Store the current image
        self.current_image = None
        self.current_page_index = None
        self.tk_image = None
        
        # Bind events
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.zoom_var.trace_add("write", self._update_zoom_label)
    
    def _update_zoom_label(self, *args):
        """Update the zoom percentage label."""
        self.zoom_value_label.config(text=f"{self.zoom_var.get()}%")
    
    def _on_zoom_change(self, *args):
        """Handle zoom level changes."""
        if self.current_page_index is not None:
            self.show_page(self.current_page_index)
    
    def _on_canvas_resize(self, event):
        """Handle canvas resize events."""
        if self.current_page_index is not None:
            self.show_page(self.current_page_index)
    
    def show_page(self, page_index):
        """Display a PDF page on the canvas.
        
        Args:
            page_index (int): Index of the page to display
        """
        self.current_page_index = page_index
        page = self.app.pdf_manager.get_page(page_index)
        
        if page:
            # Get the zoom factor
            zoom_factor = self.zoom_var.get() / 100.0
            
            # Render the page to a pixmap
            matrix = fitz.Matrix(zoom_factor, zoom_factor)
            pix = page.get_pixmap(matrix=matrix)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Store the original image
            self.current_image = img
            
            # Convert to PhotoImage for display
            self.tk_image = ImageTk.PhotoImage(image=img)
            
            # Update the canvas
            self.canvas.itemconfig(self.image_id, image=self.tk_image)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    
    def clear(self):
        """Clear the preview."""
        self.canvas.itemconfig(self.image_id, image="")
        self.current_image = None
        self.current_page_index = None
        self.tk_image = None

# Import here to avoid circular import issues
import fitz  # PyMuPDF
