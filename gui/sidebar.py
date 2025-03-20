"""
Sidebar module for displaying PDF page list.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Sidebar(ttk.Frame):
    """Sidebar widget for displaying and managing PDF pages."""
    
    def __init__(self, parent, app):
        """Initialize the sidebar.
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent, width=200)
        self.app = app
        
        # Create a label frame for the page list
        self.pages_frame = ttk.LabelFrame(self, text="Pages")
        self.pages_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a treeview for the page list
        self.page_tree = ttk.Treeview(self.pages_frame, columns=("page_num",), show="headings")
        self.page_tree.heading("page_num", text="Page")
        self.page_tree.column("page_num", width=150)
        
        # Add a scrollbar
        self.page_scrollbar = ttk.Scrollbar(
            self.pages_frame,
            orient=tk.VERTICAL,
            command=self.page_tree.yview
        )
        self.page_tree.configure(yscrollcommand=self.page_scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.page_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.page_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.page_tree.bind("<<TreeviewSelect>>", self._on_page_select)
        
        # Add buttons for page manipulation
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.move_up_button = ttk.Button(
            self.button_frame,
            text="Move Up",
            command=self._move_page_up
        )
        self.move_up_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.move_down_button = ttk.Button(
            self.button_frame,
            text="Move Down",
            command=self._move_page_down
        )
        self.move_down_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    
    def update_page_list(self):
        """Update the page list based on the current PDF document."""
        # Clear the current list
        self.page_tree.delete(*self.page_tree.get_children())
        
        # If no document is open, return
        if not self.app.pdf_manager.doc:
            return
        
        # Add pages to the list
        page_count = self.app.pdf_manager.get_page_count()
        for i in range(page_count):
            self.page_tree.insert("", tk.END, values=(f"Page {i + 1}",), iid=str(i))
    
    def get_selected_page_index(self):
        """Get the index of the currently selected page.
        
        Returns:
            int: Selected page index or None if no selection
        """
        selection = self.page_tree.selection()
        if selection:
            return int(selection[0])
        return None
    
    def select_page(self, page_index):
        """Select a page in the treeview.
        
        Args:
            page_index (int): Index of the page to select
        """
        if 0 <= page_index < self.app.pdf_manager.get_page_count():
            self.page_tree.selection_set(str(page_index))
            self.page_tree.see(str(page_index))
    
    def _on_page_select(self, event):
        """Handle page selection events."""
        selected_index = self.get_selected_page_index()
        if selected_index is not None:
            self.app.preview.show_page(selected_index)
    
    def _move_page_up(self):
        """Move the selected page up in the document order."""
        # This will be implemented later
        messagebox.showinfo("Info", "Move Page Up functionality will be implemented soon.")
    
    def _move_page_down(self):
        """Move the selected page down in the document order."""
        # This will be implemented later
        messagebox.showinfo("Info", "Move Page Down functionality will be implemented soon.")
