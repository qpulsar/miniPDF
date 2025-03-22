"""
Main application GUI for the PDF Editor.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk

from gui.toolbar import Toolbar
from gui.sidebar import Sidebar
from gui.preview import PDFPreview
from core.pdf_manager import PDFManager
from theme import get_theme_colors
import config

class PDFEditorApp:
    """Main application class for the PDF Editor."""
    
    def __init__(self, root):
        """Initialize the PDF Editor application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        
        # Apply ttk style
        self.style = ttk.Style()
        
        # Get theme colors
        self.theme_colors = get_theme_colors(self.style)
        
        # Initialize PDF manager
        self.pdf_manager = PDFManager()
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create toolbar
        self.toolbar = Toolbar(self.main_frame, self)
        self.toolbar.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))
        
        # Create content area with sidebar and preview
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar for page list
        self.sidebar = Sidebar(self.content_frame, self)
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT, padx=(0, 10))
        
        # Create preview area
        self.preview = PDFPreview(self.content_frame, self)
        self.preview.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        # Set up status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_pdf(self):
        """Open a PDF file."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            if self.pdf_manager.open_pdf(file_path):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    self.preview.show_page(0)
                self.status_var.set(f"Opened: {file_path}")
            else:
                messagebox.showerror("Error", "Failed to open the PDF file.")
    
    def save_pdf(self):
        """Save the current PDF file."""
        if not self.pdf_manager.doc:
            messagebox.showinfo("Info", "No PDF file is currently open.")
            return
            
        # If we have a current file path, save directly to it
        if self.pdf_manager.file_path:
            if self.pdf_manager.save_pdf():
                self.status_var.set(f"Saved: {self.pdf_manager.file_path}")
                messagebox.showinfo("Success", "PDF file saved successfully.")
            else:
                messagebox.showerror("Error", "Failed to save the PDF file.")
            return
        
        # If no current file path, show save dialog
        self.save_pdf_as()

    def save_pdf_as(self):
        """Save the current PDF file with a new name."""
        if not self.pdf_manager.doc:
            messagebox.showinfo("Info", "No PDF file is currently open.")
            return
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if save_path:
            if self.pdf_manager.save_pdf(save_path):
                self.status_var.set(f"Saved: {save_path}")
                messagebox.showinfo("Success", "PDF file saved successfully.")
            else:
                messagebox.showerror("Error", "Failed to save the PDF file.")
    
    def delete_current_page(self):
        """Delete the currently selected page."""
        if not self.pdf_manager.doc:
            messagebox.showinfo("Info", "No PDF file is currently open.")
            return
            
        current_page = self.sidebar.get_selected_page_index()
        if current_page is None:
            messagebox.showinfo("Info", "No page selected.")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this page?"):
            if self.pdf_manager.delete_page(current_page):
                self.sidebar.update_page_list()
                
                # Select a new page if available
                page_count = self.pdf_manager.get_page_count()
                if page_count > 0:
                    new_index = min(current_page, page_count - 1)
                    self.sidebar.select_page(new_index)
                    self.preview.show_page(new_index)
                else:
                    self.preview.clear()
                
                self.status_var.set("Page deleted")
            else:
                messagebox.showerror("Error", "Failed to delete the page.")
    
    def on_closing(self):
        """Handle application closing."""
        if self.pdf_manager.doc:
            if messagebox.askyesno("Confirm", "Do you want to save changes before exiting?"):
                self.save_pdf()
            self.pdf_manager.close()
        
        self.root.destroy()
    
    def run(self):
        """Run the application."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def reload_pdf(self):
        """Reload the current PDF file to reflect changes."""
        if self.pdf_manager.current_file:
            current_page_index = self.preview.current_page_index
            
            # Reopen the PDF file
            if self.pdf_manager.open_pdf(self.pdf_manager.current_file):
                self.sidebar.update_page_list()
                
                # Try to show the same page that was being viewed
                page_count = self.pdf_manager.get_page_count()
                if page_count > 0:
                    # Make sure the page index is valid
                    if current_page_index is not None and current_page_index < page_count:
                        self.preview.show_page(current_page_index)
                    else:
                        # Show the first page if the previous page is no longer valid
                        self.preview.show_page(0)
                else:
                    self.preview.clear()
                    
                self.status_var.set(f"Reloaded: {self.pdf_manager.current_file}")
            else:
                messagebox.showerror("Hata", "PDF dosyası yeniden yüklenirken bir hata oluştu.")
