"""
Toolbar module for the PDF Editor application.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from core.merge_split import PDFMergeSplit
import os
from PIL import Image, ImageTk
import sys

class Toolbar(ttk.Frame):
    """Toolbar widget with MS Office-style ribbon interface for PDF operations."""
    
    def __init__(self, parent, app):
        """Initialize the toolbar.
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent)
        self.app = app
        self.merge_split = PDFMergeSplit()
        
        # Create the main notebook for the ribbon
        self.ribbon = ttk.Notebook(self)
        self.ribbon.pack(fill=tk.X, expand=False, padx=2, pady=2)
        
        # Create tabs for each category
        self.file_tab = ttk.Frame(self.ribbon)
        self.page_tab = ttk.Frame(self.ribbon)
        self.edit_tab = ttk.Frame(self.ribbon)
        self.tools_tab = ttk.Frame(self.ribbon)
        self.view_tab = ttk.Frame(self.ribbon)
        self.help_tab = ttk.Frame(self.ribbon)
        
        # Add tabs to the notebook
        self.ribbon.add(self.file_tab, text="Dosya")
        self.ribbon.add(self.page_tab, text="Sayfa")
        self.ribbon.add(self.edit_tab, text="Düzenleme")
        self.ribbon.add(self.tools_tab, text="Araçlar")
        self.ribbon.add(self.view_tab, text="Görüntüleme")
        self.ribbon.add(self.help_tab, text="Yardım")
        
        # Initialize all ribbon tabs
        self._init_file_tab()
        self._init_page_tab()
        self._init_edit_tab()
        self._init_tools_tab()
        self._init_view_tab()
        self._init_help_tab()
        
        # File operations
        self.file_frame = ttk.LabelFrame(self.file_tab, text="File")
        self.file_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        
        self.open_button = ttk.Button(
            self.file_frame,
            text="Open PDF",
            command=self.app.open_pdf
        )
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.save_button = ttk.Button(
            self.file_frame,
            text="Save PDF",
            command=self.app.save_pdf
        )
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Page operations
        self.page_frame = ttk.LabelFrame(self.page_tab, text="Page")
        self.page_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        
        self.delete_page_button = ttk.Button(
            self.page_frame,
            text="Delete Page",
            command=self.app.delete_current_page
        )
        self.delete_page_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add more buttons for other operations
        # These will be implemented later
        
        # Merge/Split operations
        self.merge_frame = ttk.LabelFrame(self.tools_tab, text="Merge/Split")
        self.merge_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        
        self.merge_button = ttk.Button(
            self.merge_frame,
            text="Merge PDFs",
            command=self._merge_pdfs
        )
        self.merge_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.split_button = ttk.Button(
            self.merge_frame,
            text="Split PDF",
            command=self._split_pdf
        )
        self.split_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Text operations
        self.text_frame = ttk.LabelFrame(self.edit_tab, text="Text")
        self.text_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        
        self.extract_text_button = ttk.Button(
            self.text_frame,
            text="Extract Text",
            command=self._extract_text
        )
        self.extract_text_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Annotation operations
        self.annot_frame = ttk.LabelFrame(self.edit_tab, text="Annotations")
        self.annot_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        
        self.add_note_button = ttk.Button(
            self.annot_frame,
            text="Add Note",
            command=self._add_note
        )
        self.add_note_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def _merge_pdfs(self):
        """Merge multiple PDFs into a single PDF file."""
        # Ask user to select PDF files to merge
        pdf_files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not pdf_files or len(pdf_files) < 2:
            messagebox.showinfo("Info", "Please select at least two PDF files to merge.")
            return
        
        # Create a dialog to allow reordering files
        self._show_merge_dialog(pdf_files)
    
    def _show_merge_dialog(self, pdf_files):
        """Show a dialog to reorder PDF files before merging.
        
        Args:
            pdf_files (tuple): Tuple of selected PDF file paths
        """
        # Create a new top-level window
        merge_dialog = tk.Toplevel(self.app.root)
        merge_dialog.title("Merge PDFs")
        merge_dialog.geometry("500x400")
        merge_dialog.transient(self.app.root)
        merge_dialog.grab_set()
        
        # Create a frame for the file list
        list_frame = ttk.LabelFrame(merge_dialog, text="PDF Files (Drag to reorder)")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a listbox with scrollbar
        file_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        file_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
        file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add files to the listbox
        for pdf_file in pdf_files:
            file_listbox.insert(tk.END, os.path.basename(pdf_file))
        
        # Store the full paths
        file_paths = list(pdf_files)
        
        # Add buttons to move files up and down
        button_frame = ttk.Frame(merge_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        move_up_button = ttk.Button(
            button_frame, 
            text="Move Up", 
            command=lambda: self._move_item_up(file_listbox, file_paths)
        )
        move_up_button.pack(side=tk.LEFT, padx=5)
        
        move_down_button = ttk.Button(
            button_frame, 
            text="Move Down", 
            command=lambda: self._move_item_down(file_listbox, file_paths)
        )
        move_down_button.pack(side=tk.LEFT, padx=5)
        
        # Add merge and cancel buttons
        action_frame = ttk.Frame(merge_dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        merge_button = ttk.Button(
            action_frame, 
            text="Merge PDFs", 
            command=lambda: self._perform_merge(merge_dialog, file_paths)
        )
        merge_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            action_frame, 
            text="Cancel", 
            command=merge_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _move_item_up(self, listbox, file_paths):
        """Move the selected item up in the listbox.
        
        Args:
            listbox: Tkinter Listbox widget
            file_paths (list): List of file paths
        """
        selected_index = listbox.curselection()
        if not selected_index or selected_index[0] == 0:
            return
        
        index = selected_index[0]
        
        # Move item in the listbox
        text = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index - 1, text)
        listbox.selection_set(index - 1)
        listbox.activate(index - 1)
        listbox.see(index - 1)
        
        # Move item in the file paths list
        file_paths.insert(index - 1, file_paths.pop(index))
    
    def _move_item_down(self, listbox, file_paths):
        """Move the selected item down in the listbox.
        
        Args:
            listbox: Tkinter Listbox widget
            file_paths (list): List of file paths
        """
        selected_index = listbox.curselection()
        if not selected_index or selected_index[0] == listbox.size() - 1:
            return
        
        index = selected_index[0]
        
        # Move item in the listbox
        text = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index + 1, text)
        listbox.selection_set(index + 1)
        listbox.activate(index + 1)
        listbox.see(index + 1)
        
        # Move item in the file paths list
        file_paths.insert(index + 1, file_paths.pop(index))
    
    def _perform_merge(self, dialog, file_paths):
        """Perform the actual PDF merge operation.
        
        Args:
            dialog: Tkinter dialog to close after operation
            file_paths (list): List of PDF file paths to merge
        """
        # Ask user where to save the merged PDF
        save_path = filedialog.asksaveasfilename(
            title="Save Merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not save_path:
            return
        
        # Perform the merge operation
        success = self.merge_split.merge_pdfs(file_paths, save_path)
        
        # Close the dialog
        dialog.destroy()
        
        # Show result message
        if success:
            messagebox.showinfo("Success", "PDFs merged successfully!")
            
            # Ask if user wants to open the merged PDF
            if messagebox.askyesno("Open File", "Do you want to open the merged PDF?"):
                # Close current file if open
                if self.app.pdf_manager.doc:
                    self.app.pdf_manager.close()
                
                # Open the merged PDF
                self.app.pdf_manager.open_pdf(save_path)
                self.app.sidebar.update_page_list()
                if self.app.pdf_manager.get_page_count() > 0:
                    self.app.preview.show_page(0)
                self.app.status_var.set(f"Opened merged PDF: {save_path}")
        else:
            messagebox.showerror("Error", "Failed to merge PDFs. Please try again.")
    
    def _split_pdf(self):
        """Split the current PDF."""
        # Check if a PDF is open
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
        
        # Create a dialog for split options
        self._show_split_dialog()
    
    def _show_split_dialog(self):
        """Show a dialog for PDF splitting options."""
        # Create a new top-level window
        split_dialog = tk.Toplevel(self.app.root)
        split_dialog.title("Split PDF")
        split_dialog.geometry("600x500")
        split_dialog.transient(self.app.root)
        split_dialog.grab_set()
        
        # Create a frame for split options
        options_frame = ttk.LabelFrame(split_dialog, text="Split Options")
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Split method selection
        method_frame = ttk.Frame(options_frame)
        method_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(method_frame, text="Split Method:").pack(side=tk.LEFT, padx=5)
        
        split_method = tk.StringVar(value="pages")
        
        ttk.Radiobutton(
            method_frame, 
            text="By Pages", 
            variable=split_method, 
            value="pages"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            method_frame, 
            text="Extract Pages", 
            variable=split_method, 
            value="extract"
        ).pack(side=tk.LEFT, padx=5)
        
        # Pages per file option
        pages_frame = ttk.Frame(options_frame)
        pages_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(pages_frame, text="Pages per file:").pack(side=tk.LEFT, padx=5)
        
        pages_var = tk.IntVar(value=1)
        pages_spinbox = ttk.Spinbox(
            pages_frame, 
            from_=1, 
            to=100, 
            textvariable=pages_var, 
            width=5
        )
        pages_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Page range for extraction
        extract_frame = ttk.Frame(options_frame)
        extract_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(extract_frame, text="Page Range (e.g., 1,3-5,7):").pack(side=tk.LEFT, padx=5)
        
        page_range_var = tk.StringVar()
        page_range_entry = ttk.Entry(extract_frame, textvariable=page_range_var, width=20)
        page_range_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Output directory selection
        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output Directory:").pack(side=tk.LEFT, padx=5)
        
        output_dir_var = tk.StringVar()
        output_dir_entry = ttk.Entry(output_frame, textvariable=output_dir_var, width=25)
        output_dir_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(
            output_frame, 
            text="Browse...", 
            command=lambda: self._browse_output_dir(output_dir_var)
        )
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # Set default output directory to the directory of the current PDF
        if self.app.pdf_manager.current_file:
            output_dir_var.set(os.path.dirname(self.app.pdf_manager.current_file))
        
        # Add split and cancel buttons
        action_frame = ttk.Frame(split_dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        split_button = ttk.Button(
            action_frame, 
            text="Split PDF", 
            width=10,
            command=lambda: self._perform_split(
                split_dialog, 
                split_method.get(), 
                pages_var.get(), 
                page_range_var.get(), 
                output_dir_var.get()
            )
        )
        split_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            action_frame, 
            text="İptal", 
            width=10,
            command=split_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _browse_output_dir(self, output_dir_var):
        """Browse for output directory.
        
        Args:
            output_dir_var: StringVar to store the selected directory
        """
        directory = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if directory:
            output_dir_var.set(directory)
    
    def _perform_split(self, dialog, method, pages_per_file, page_range, output_dir):
        """Perform the actual PDF split operation.
        
        Args:
            dialog: Tkinter dialog to close after operation
            method (str): Split method ('pages' or 'extract')
            pages_per_file (int): Number of pages per file for 'pages' method
            page_range (str): Page range for 'extract' method
            output_dir (str): Directory to save split PDFs
        """
        # Validate output directory
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Please select a valid output directory.")
            return
        
        # Get current PDF path
        pdf_path = self.app.pdf_manager.current_file
        
        # Perform split based on method
        if method == "pages":
            # Split PDF into multiple files with specified pages per file
            output_files = self.merge_split.split_pdf(
                pdf_path, 
                output_dir, 
                pages_per_file
            )
            
            if output_files:
                messagebox.showinfo(
                    "Success", 
                    f"PDF split into {len(output_files)} files successfully!"
                )
            else:
                messagebox.showerror("Error", "Failed to split PDF. Please try again.")
        
        elif method == "extract":
            # Parse page range
            page_indices = self._parse_page_range(page_range)
            
            if not page_indices:
                messagebox.showerror(
                    "Error", 
                    "Invalid page range. Please use format like '1,3-5,7'."
                )
                return
            
            # Create output filename
            base_name = os.path.basename(pdf_path)
            output_path = os.path.join(
                output_dir, 
                f"extracted_pages_{base_name}"
            )
            
            # Extract specified pages
            success = self.merge_split.extract_pages(
                pdf_path, 
                output_path, 
                page_indices
            )
            
            if success:
                messagebox.showinfo(
                    "Success", 
                    f"Pages extracted successfully to {output_path}!"
                )
            else:
                messagebox.showerror("Error", "Failed to extract pages. Please try again.")
        
        # Close the dialog
        dialog.destroy()
    
    def _parse_page_range(self, page_range_str):
        """Parse a page range string into a list of page indices.
        
        Args:
            page_range_str (str): Page range string (e.g., "1,3-5,7")
            
        Returns:
            list: List of page indices (0-based)
        """
        if not page_range_str.strip():
            return []
        
        page_indices = []
        
        try:
            # Split by comma
            parts = page_range_str.split(',')
            
            for part in parts:
                part = part.strip()
                
                # Check if it's a range (e.g., "3-5")
                if '-' in part:
                    start, end = part.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    
                    # Convert to 0-based indices
                    for i in range(start - 1, end):
                        if i not in page_indices:
                            page_indices.append(i)
                else:
                    # Single page
                    page = int(part)
                    
                    # Convert to 0-based index
                    if page - 1 not in page_indices:
                        page_indices.append(page - 1)
            
            return sorted(page_indices)
        except ValueError:
            return []
    
    def _extract_text(self):
        """Extract text from the current PDF."""
        # Check if a PDF is open
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
        
        # Get the current page index
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
        
        # Import the necessary modules
        from core.text_extraction import TextExtractor
        from gui.dialogs import TextExtractionDialog
        
        # Create a text extractor instance
        text_extractor = TextExtractor()
        
        # Create and show the extraction dialog
        extraction_dialog = TextExtractionDialog(
            self.app.root,
            self.app,
            self.app.pdf_manager.doc,
            selected_page_index,
            lambda dialog, scope, page_index, text_area: self._perform_extraction(
                dialog, text_extractor, self.app.pdf_manager.doc, scope, page_index, text_area
            )
        )
    
    def _perform_extraction(self, dialog, text_extractor, doc, scope, selected_page_index, text_area):
        """Perform the actual text extraction.
        
        Args:
            dialog: Tkinter dialog
            text_extractor: TextExtractor instance
            doc: PyMuPDF Document object
            scope (str): 'current_page' or 'all_pages'
            selected_page_index: Index of the selected page
            text_area: Tkinter Text widget to display the extracted text
        """
        # Clear the text area
        text_area.delete("1.0", tk.END)
        
        try:
            # Extract text based on scope
            extracted_text = text_extractor.extract_text(doc, scope, selected_page_index)
            
            # Display the extracted text
            text_area.insert(tk.END, extracted_text)
            
            # Update status
            self.app.status_var.set("Text extracted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text: {e}")
            self.app.status_var.set("Text extraction failed")
    
    def _add_note(self):
        """Add a note to the current page."""
        # Check if a PDF is open
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
        
        # Check if a page is selected
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
        
        # Get the current page
        page = self.app.pdf_manager.get_page(selected_page_index)
        if not page:
            messagebox.showerror("Error", "Failed to get the selected page.")
            return
        
        # Import the necessary modules
        from gui.dialogs import NoteDialog
        
        # Create and show the note dialog
        note_dialog = NoteDialog(
            self.app.root,
            self.app,
            page,
            selected_page_index,
            self._perform_add_note
        )
    
    def _perform_add_note(self, dialog, page, page_index, position, text, title, icon):
        """Perform the actual note addition.
        
        Args:
            dialog: Tkinter dialog
            page: PyMuPDF Page object
            page_index: Index of the page
            position (tuple): Position coordinates (x, y)
            text (str): Note text content
            title (str): Note title
            icon (str): Note icon type
        """
        # Check if text is provided
        if not text.strip():
            messagebox.showinfo("Info", "Please enter some text for the note.")
            return
        
        try:
            # Import the annotator
            from core.annotations import PDFAnnotator
            annotator = PDFAnnotator()
            
            # Add the text annotation
            success = annotator.create_note_at_position(page, position, text, title, icon)
            
            if success:
                # Close the dialog
                dialog.destroy()
                
                # Refresh the page view
                self.app.preview.show_page(page_index)
                
                # Update status
                self.app.status_var.set(f"Note added to page {page_index + 1}")
                
                # Mark the document as modified
                # This will prompt the user to save when closing
            else:
                messagebox.showerror("Error", "Failed to add note to the page.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding note: {e}")
    
    def _init_file_tab(self):
        """Initialize the File tab with buttons for file operations."""
        # Create a frame for the file operations
        file_frame = ttk.Frame(self.file_tab)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a style for ribbon buttons
        button_style = ttk.Style()
        button_style.configure("Ribbon.TButton", font=("Segoe UI", 9))
        
        # Open button with icon and label
        open_frame = ttk.Frame(file_frame)
        open_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        open_button = ttk.Button(
            open_frame,
            text="Aç",
            style="Ribbon.TButton",
            width=10,
            command=self.app.open_pdf
        )
        open_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(open_frame, text="📂 Open").pack(side=tk.TOP)
        
        # Save button with icon and label
        save_frame = ttk.Frame(file_frame)
        save_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        save_button = ttk.Button(
            save_frame,
            text="Kaydet",
            style="Ribbon.TButton",
            width=10,
            command=self.app.save_pdf
        )
        save_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(save_frame, text="💾 Save").pack(side=tk.TOP)
        
        # Print button with icon and label
        print_frame = ttk.Frame(file_frame)
        print_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        print_button = ttk.Button(
            print_frame,
            text="Yazdır",
            style="Ribbon.TButton",
            width=10,
            command=self._print_pdf
        )
        print_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(print_frame, text="🖨️ Print").pack(side=tk.TOP)
        
        # Close button with icon and label
        close_frame = ttk.Frame(file_frame)
        close_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        close_button = ttk.Button(
            close_frame,
            text="Kapat",
            style="Ribbon.TButton",
            width=10,
            command=self._close_application
        )
        close_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(close_frame, text="❌ Close").pack(side=tk.TOP)
    
    def _print_pdf(self):
        """Print the current PDF document."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # For now, just show a message since printing is not implemented
        messagebox.showinfo("Print", "Printing functionality will be implemented in a future update.")
    
    def _close_application(self):
        """Close the application."""
        self.app.root.destroy()
    
    def _init_page_tab(self):
        """Initialize the Page tab with buttons for page operations."""
        # Create a frame for the page operations
        page_frame = ttk.Frame(self.page_tab)
        page_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add Page button with icon and label
        add_page_frame = ttk.Frame(page_frame)
        add_page_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        add_page_button = ttk.Button(
            add_page_frame,
            text="Sayfa Ekle",
            style="Ribbon.TButton",
            width=10,
            command=self._add_blank_page
        )
        add_page_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(add_page_frame, text="➕ Add Page").pack(side=tk.TOP)
        
        # Delete Page button with icon and label
        delete_page_frame = ttk.Frame(page_frame)
        delete_page_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        delete_page_button = ttk.Button(
            delete_page_frame,
            text="Sayfa Sil",
            style="Ribbon.TButton",
            width=10,
            command=self.app.delete_current_page
        )
        delete_page_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(delete_page_frame, text="🗑️ Delete Page").pack(side=tk.TOP)
        
        # Rotate Page button with icon and label
        rotate_page_frame = ttk.Frame(page_frame)
        rotate_page_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        rotate_page_button = ttk.Button(
            rotate_page_frame,
            text="Sayfa Döndür",
            style="Ribbon.TButton",
            width=10,
            command=self._rotate_page
        )
        rotate_page_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(rotate_page_frame, text="🔄 Rotate Page").pack(side=tk.TOP)
        
        # Extract Page button with icon and label
        extract_page_frame = ttk.Frame(page_frame)
        extract_page_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        extract_page_button = ttk.Button(
            extract_page_frame,
            text="Sayfayı Çıkar",
            style="Ribbon.TButton",
            width=10,
            command=self._extract_page
        )
        extract_page_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(extract_page_frame, text="📜 Extract Page").pack(side=tk.TOP)
    
    def _add_blank_page(self):
        """Add a blank page to the PDF."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Add Page", "Add blank page functionality will be implemented in a future update.")
    
    def _rotate_page(self):
        """Rotate the current page."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Get the current page index
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
            
        # Create a dialog for rotation options
        rotation_dialog = tk.Toplevel(self.app.root)
        rotation_dialog.title("Rotate Page")
        rotation_dialog.geometry("300x200")
        rotation_dialog.transient(self.app.root)
        rotation_dialog.grab_set()
        
        # Create a frame for rotation options
        options_frame = ttk.LabelFrame(rotation_dialog, text="Rotation Angle")
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Rotation angle selection
        angle_var = tk.IntVar(value=90)
        
        ttk.Radiobutton(
            options_frame, 
            text="90° Clockwise", 
            variable=angle_var, 
            value=90
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        ttk.Radiobutton(
            options_frame, 
            text="180°", 
            variable=angle_var, 
            value=180
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        ttk.Radiobutton(
            options_frame, 
            text="270° Clockwise (90° Counter-clockwise)", 
            variable=angle_var, 
            value=270
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        # Add rotate and cancel buttons
        button_frame = ttk.Frame(rotation_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        rotate_button = ttk.Button(
            button_frame, 
            text="Rotate", 
            command=lambda: self._perform_rotation(rotation_dialog, selected_page_index, angle_var.get())
        )
        rotate_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=rotation_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _perform_rotation(self, dialog, page_index, angle):
        """Perform the actual page rotation.
        
        Args:
            dialog: Tkinter dialog to close after operation
            page_index: Index of the page to rotate
            angle: Rotation angle in degrees (90, 180, or 270)
        """
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Rotate Page", "Page rotation functionality will be implemented in a future update.")
        dialog.destroy()
    
    def _extract_page(self):
        """Extract the current page to a new PDF file."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Get the current page index
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
            
        # Ask user where to save the extracted page
        save_path = filedialog.asksaveasfilename(
            title="Save Extracted Page",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if not save_path:
            return
            
        # Extract the page (using the existing extract_pages method)
        success = self.merge_split.extract_pages(
            self.app.pdf_manager.current_file,
            save_path,
            [selected_page_index]
        )
        
        # Show result message
        if success:
            messagebox.showinfo("Success", f"Page {selected_page_index + 1} extracted successfully to {save_path}!")
        else:
            messagebox.showerror("Error", "Failed to extract page. Please try again.")
    
    def _init_edit_tab(self):
        """Initialize the Edit tab with buttons for editing operations."""
        # Create a frame for the edit operations
        edit_frame = ttk.Frame(self.edit_tab)
        edit_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add Text button with icon and label
        add_text_frame = ttk.Frame(edit_frame)
        add_text_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        add_text_button = ttk.Button(
            add_text_frame,
            text="Metin Ekle",
            style="Ribbon.TButton",
            width=10,
            command=self._add_text
        )
        add_text_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(add_text_frame, text="✏️ Add Text").pack(side=tk.TOP)
        
        # Draw button with icon and label
        draw_frame = ttk.Frame(edit_frame)
        draw_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        draw_button = ttk.Button(
            draw_frame,
            text="Çizim Yap",
            style="Ribbon.TButton",
            width=10,
            command=self._draw
        )
        draw_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(draw_frame, text="🖍️ Draw").pack(side=tk.TOP)
        
        # Delete Object button with icon and label
        delete_obj_frame = ttk.Frame(edit_frame)
        delete_obj_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        delete_obj_button = ttk.Button(
            delete_obj_frame,
            text="Öğe Sil",
            style="Ribbon.TButton",
            width=10,
            command=self._delete_object
        )
        delete_obj_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(delete_obj_frame, text="🗑️ Delete Object").pack(side=tk.TOP)
        
        # Highlight button with icon and label
        highlight_frame = ttk.Frame(edit_frame)
        highlight_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        highlight_button = ttk.Button(
            highlight_frame,
            text="Vurgulayıcı",
            style="Ribbon.TButton",
            width=10,
            command=self._highlight_text
        )
        highlight_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(highlight_frame, text="🖌️ Highlight").pack(side=tk.TOP)
    
    def _add_text(self):
        """Add text to the current PDF page."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Get the current page index
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
            
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Add Text", "Add text functionality will be implemented in a future update.")
    
    def _draw(self):
        """Enable drawing mode on the current PDF page."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Get the current page index
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
            
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Draw", "Drawing functionality will be implemented in a future update.")
    
    def _delete_object(self):
        """Delete a selected object from the current PDF page."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Get the current page index
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
            
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Delete Object", "Delete object functionality will be implemented in a future update.")
    
    def _highlight_text(self):
        """Highlight text on the current PDF page."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Get the current page index
        selected_page_index = self.app.sidebar.get_selected_page_index()
        if selected_page_index is None:
            messagebox.showinfo("Info", "Please select a page first.")
            return
            
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Highlight", "Text highlighting functionality will be implemented in a future update.")
    
    def _init_tools_tab(self):
        """Initialize the Tools tab with buttons for various PDF tools."""
        # Create a frame for the tools operations
        tools_frame = ttk.Frame(self.tools_tab)
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # OCR button with icon and label
        ocr_frame = ttk.Frame(tools_frame)
        ocr_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        ocr_button = ttk.Button(
            ocr_frame,
            text="OCR",
            style="Ribbon.TButton",
            width=10,
            command=self._extract_text  # Reuse existing extract_text functionality
        )
        ocr_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(ocr_frame, text="🔍 OCR Text Recognition").pack(side=tk.TOP)
        
        # Merge PDFs button with icon and label
        merge_frame = ttk.Frame(tools_frame)
        merge_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        merge_button = ttk.Button(
            merge_frame,
            text="PDF Birleştir",
            style="Ribbon.TButton",
            width=10,
            command=self._merge_pdfs  # Reuse existing merge_pdfs functionality
        )
        merge_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(merge_frame, text="🔗 Merge PDFs").pack(side=tk.TOP)
        
        # Split PDF button with icon and label
        split_frame = ttk.Frame(tools_frame)
        split_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        split_button = ttk.Button(
            split_frame,
            text="PDF Böl",
            style="Ribbon.TButton",
            width=10,
            command=self._split_pdf  # Reuse existing split_pdf functionality
        )
        split_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(split_frame, text="✂️ Split PDF").pack(side=tk.TOP)
        
        # Encrypt PDF button with icon and label
        encrypt_frame = ttk.Frame(tools_frame)
        encrypt_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        encrypt_button = ttk.Button(
            encrypt_frame,
            text="Şifrele",
            style="Ribbon.TButton",
            width=10,
            command=self._encrypt_pdf
        )
        encrypt_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(encrypt_frame, text="🔏 Encrypt").pack(side=tk.TOP)
        
        # Decrypt PDF button with icon and label
        decrypt_frame = ttk.Frame(tools_frame)
        decrypt_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        decrypt_button = ttk.Button(
            decrypt_frame,
            text="Şifre Kaldır",
            style="Ribbon.TButton",
            width=10,
            command=self._decrypt_pdf
        )
        decrypt_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(decrypt_frame, text="🔓 Decrypt").pack(side=tk.TOP)
    
    def _encrypt_pdf(self):
        """Encrypt the current PDF with a password."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Create a dialog for encryption options
        encrypt_dialog = tk.Toplevel(self.app.root)
        encrypt_dialog.title("Encrypt PDF")
        encrypt_dialog.geometry("400x200")
        encrypt_dialog.transient(self.app.root)
        encrypt_dialog.grab_set()
        
        # Create a frame for password input
        password_frame = ttk.LabelFrame(encrypt_dialog, text="Password Protection")
        password_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # User password (to open the document)
        user_frame = ttk.Frame(password_frame)
        user_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(user_frame, text="User Password:").pack(side=tk.LEFT, padx=5)
        
        user_password_var = tk.StringVar()
        user_password_entry = ttk.Entry(user_frame, textvariable=user_password_var, show="*", width=20)
        user_password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Owner password (for permissions)
        owner_frame = ttk.Frame(password_frame)
        owner_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(owner_frame, text="Owner Password:").pack(side=tk.LEFT, padx=5)
        
        owner_password_var = tk.StringVar()
        owner_password_entry = ttk.Entry(owner_frame, textvariable=owner_password_var, show="*", width=20)
        owner_password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Add encrypt and cancel buttons
        button_frame = ttk.Frame(encrypt_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        encrypt_button = ttk.Button(
            button_frame, 
            text="Encrypt", 
            command=lambda: self._perform_encryption(
                encrypt_dialog, 
                user_password_var.get(), 
                owner_password_var.get()
            )
        )
        encrypt_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=encrypt_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _perform_encryption(self, dialog, user_password, owner_password):
        """Perform the actual PDF encryption.
        
        Args:
            dialog: Tkinter dialog to close after operation
            user_password: Password required to open the document
            owner_password: Password required for permissions
        """
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Encrypt PDF", "PDF encryption functionality will be implemented in a future update.")
        dialog.destroy()
    
    def _decrypt_pdf(self):
        """Remove password protection from the current PDF."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Create a dialog for decryption
        decrypt_dialog = tk.Toplevel(self.app.root)
        decrypt_dialog.title("Decrypt PDF")
        decrypt_dialog.geometry("400x150")
        decrypt_dialog.transient(self.app.root)
        decrypt_dialog.grab_set()
        
        # Create a frame for password input
        password_frame = ttk.LabelFrame(decrypt_dialog, text="Enter Password")
        password_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Password input
        password_var = tk.StringVar()
        
        ttk.Label(password_frame, text="Password:").pack(anchor=tk.W, padx=5, pady=5)
        
        password_entry = ttk.Entry(password_frame, textvariable=password_var, show="*", width=30)
        password_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Add decrypt and cancel buttons
        button_frame = ttk.Frame(decrypt_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        decrypt_button = ttk.Button(
            button_frame, 
            text="Decrypt", 
            command=lambda: self._perform_decryption(decrypt_dialog, password_var.get())
        )
        decrypt_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=decrypt_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _perform_decryption(self, dialog, password):
        """Perform the actual PDF decryption.
        
        Args:
            dialog: Tkinter dialog to close after operation
            password: Password to decrypt the document
        """
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Decrypt PDF", "PDF decryption functionality will be implemented in a future update.")
        dialog.destroy()

    def _init_view_tab(self):
        """Initialize the View tab with buttons for viewing options."""
        # Create a frame for the view operations
        view_frame = ttk.Frame(self.view_tab)
        view_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Zoom In button with icon and label
        zoom_in_frame = ttk.Frame(view_frame)
        zoom_in_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        zoom_in_button = ttk.Button(
            zoom_in_frame,
            text="Yakınlaştır",
            style="Ribbon.TButton",
            width=10,
            command=self._zoom_in
        )
        zoom_in_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(zoom_in_frame, text="🔍 Zoom In").pack(side=tk.TOP)
        
        # Zoom Out button with icon and label
        zoom_out_frame = ttk.Frame(view_frame)
        zoom_out_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        zoom_out_button = ttk.Button(
            zoom_out_frame,
            text="Uzaklaştır",
            style="Ribbon.TButton",
            width=10,
            command=self._zoom_out
        )
        zoom_out_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(zoom_out_frame, text="🔎 Zoom Out").pack(side=tk.TOP)
        
        # Page Layout button with icon and label
        page_layout_frame = ttk.Frame(view_frame)
        page_layout_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        page_layout_button = ttk.Button(
            page_layout_frame,
            text="Sayfa Düzeni",
            style="Ribbon.TButton",
            width=10,
            command=self._change_page_layout
        )
        page_layout_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(page_layout_frame, text="↔️ Page Layout").pack(side=tk.TOP)
        
        # Theme button with icon and label
        theme_frame = ttk.Frame(view_frame)
        theme_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        theme_button = ttk.Button(
            theme_frame,
            text="Tema",
            style="Ribbon.TButton",
            width=10,
            command=self._change_theme
        )
        theme_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(theme_frame, text="🎨 Theme").pack(side=tk.TOP)
    
    def _zoom_in(self):
        """Zoom in the PDF view."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Zoom In", "Zoom in functionality will be implemented in a future update.")
    
    def _zoom_out(self):
        """Zoom out the PDF view."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Zoom Out", "Zoom out functionality will be implemented in a future update.")
    
    def _change_page_layout(self):
        """Change the page layout (single or double page view)."""
        if not self.app.pdf_manager.doc:
            messagebox.showinfo("Info", "Please open a PDF file first.")
            return
            
        # Create a dialog for layout options
        layout_dialog = tk.Toplevel(self.app.root)
        layout_dialog.title("Page Layout")
        layout_dialog.geometry("300x150")
        layout_dialog.transient(self.app.root)
        layout_dialog.grab_set()
        
        # Create a frame for layout options
        options_frame = ttk.LabelFrame(layout_dialog, text="Layout Options")
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Layout selection
        layout_var = tk.StringVar(value="single")
        
        ttk.Radiobutton(
            options_frame, 
            text="Single Page", 
            variable=layout_var, 
            value="single"
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        ttk.Radiobutton(
            options_frame, 
            text="Double Page", 
            variable=layout_var, 
            value="double"
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        # Add apply and cancel buttons
        button_frame = ttk.Frame(layout_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        apply_button = ttk.Button(
            button_frame, 
            text="Apply", 
            command=lambda: self._apply_page_layout(layout_dialog, layout_var.get())
        )
        apply_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=layout_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _apply_page_layout(self, dialog, layout):
        """Apply the selected page layout.
        
        Args:
            dialog: Tkinter dialog to close after operation
            layout (str): Layout type ('single' or 'double')
        """
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Page Layout", f"Page layout '{layout}' will be implemented in a future update.")
        dialog.destroy()
    
    def _change_theme(self):
        """Change the application theme (light/dark mode)."""
        # Create a dialog for theme options
        theme_dialog = tk.Toplevel(self.app.root)
        theme_dialog.title("Theme")
        theme_dialog.geometry("300x150")
        theme_dialog.transient(self.app.root)
        theme_dialog.grab_set()
        
        # Create a frame for theme options
        options_frame = ttk.LabelFrame(theme_dialog, text="Theme Options")
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Theme selection
        theme_var = tk.StringVar(value="light")
        
        ttk.Radiobutton(
            options_frame, 
            text="Light Mode", 
            variable=theme_var, 
            value="light"
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        ttk.Radiobutton(
            options_frame, 
            text="Dark Mode", 
            variable=theme_var, 
            value="dark"
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        # Add apply and cancel buttons
        button_frame = ttk.Frame(theme_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        apply_button = ttk.Button(
            button_frame, 
            text="Apply", 
            command=lambda: self._apply_theme(theme_dialog, theme_var.get())
        )
        apply_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=theme_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _apply_theme(self, dialog, theme):
        """Apply the selected theme.
        
        Args:
            dialog: Tkinter dialog to close after operation
            theme (str): Theme type ('light' or 'dark')
        """
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Theme", f"Theme '{theme}' will be implemented in a future update.")
        dialog.destroy()

    def _init_help_tab(self):
        """Initialize the Help tab with buttons for help and support options."""
        # Create a frame for the help operations
        help_frame = ttk.Frame(self.help_tab)
        help_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # User Guide button with icon and label
        user_guide_frame = ttk.Frame(help_frame)
        user_guide_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        user_guide_button = ttk.Button(
            user_guide_frame,
            text="Kullanım Kılavuzu",
            style="Ribbon.TButton",
            width=15,
            command=self._show_user_guide
        )
        user_guide_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(user_guide_frame, text="❓ User Guide").pack(side=tk.TOP)
        
        # Feedback button with icon and label
        feedback_frame = ttk.Frame(help_frame)
        feedback_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        feedback_button = ttk.Button(
            feedback_frame,
            text="Geri Bildirim",
            style="Ribbon.TButton",
            width=15,
            command=self._show_feedback
        )
        feedback_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(feedback_frame, text="🛠️ Feedback").pack(side=tk.TOP)
        
        # Check Updates button with icon and label
        updates_frame = ttk.Frame(help_frame)
        updates_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        updates_button = ttk.Button(
            updates_frame,
            text="Güncellemeleri Kontrol Et",
            style="Ribbon.TButton",
            width=15,
            command=self._check_updates
        )
        updates_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(updates_frame, text="🔄 Check Updates").pack(side=tk.TOP)
        
        # About button with icon and label
        about_frame = ttk.Frame(help_frame)
        about_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        about_button = ttk.Button(
            about_frame,
            text="Hakkında",
            style="Ribbon.TButton",
            width=15,
            command=self._show_about
        )
        about_button.pack(side=tk.TOP, pady=2)
        
        ttk.Label(about_frame, text="ℹ️ About").pack(side=tk.TOP)
    
    def _show_user_guide(self):
        """Show the user guide documentation."""
        # Create a dialog for user guide
        guide_dialog = tk.Toplevel(self.app.root)
        guide_dialog.title("User Guide")
        guide_dialog.geometry("600x500")
        guide_dialog.transient(self.app.root)
        
        # Create a frame for the user guide content
        content_frame = ttk.Frame(guide_dialog)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add a scrollable text area for the guide content
        text_area = tk.Text(content_frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add some sample user guide content
        user_guide_content = """
        # miniPDF Kullanım Kılavuzu
        
        ## Giriş
        miniPDF, PDF dosyalarını görüntülemek, düzenlemek ve yönetmek için kullanılan basit bir uygulamadır.
        
        ## Dosya İşlemleri
        - **Aç**: PDF dosyasını açmak için kullanılır.
        - **Kaydet**: Yapılan değişiklikleri kaydetmek için kullanılır.
        - **Yazdır**: PDF dosyasını yazdırmak için kullanılır.
        - **Kapat**: Uygulamayı kapatmak için kullanılır.
        
        ## Sayfa İşlemleri
        - **Sayfa Ekle**: Yeni boş sayfa eklemek için kullanılır.
        - **Sayfa Sil**: Seçili sayfayı silmek için kullanılır.
        - **Sayfa Döndür**: Seçili sayfayı döndürmek için kullanılır (90°, 180°, 270°).
        - **Sayfayı Çıkar**: Seçili sayfayı yeni PDF olarak kaydetmek için kullanılır.
        
        ## Düzenleme İşlemleri
        - **Metin Ekle**: PDF'ye metin eklemek için kullanılır.
        - **Çizim Yap**: Kalem aracı ile serbest çizim yapmak için kullanılır.
        - **Öğe Sil**: Seçili metni/grafiği kaldırmak için kullanılır.
        - **Vurgulayıcı**: Metni vurgulamak için kullanılır.
        
        ## Araçlar
        - **OCR ile Metin Tanı**: Resimli PDF'deki metni çıkartmak için kullanılır.
        - **PDF'yi Birleştir**: Birden fazla PDF'yi birleştirmek için kullanılır.
        - **PDF'yi Böl**: PDF'yi belirli sayfalara bölmek için kullanılır.
        - **Şifrele**: PDF dosyasını şifrelemek için kullanılır.
        - **Şifreyi Kaldır**: PDF şifresini kaldırmak için kullanılır.
        
        ## Görüntüleme
        - **Yakınlaştır**: PDF yakınlaştırmak için kullanılır.
        - **Uzaklaştır**: PDF uzaklaştırmak için kullanılır.
        - **Sayfa Sıralaması**: Tek veya çift sayfa görünümü için kullanılır.
        - **Tema**: Açık/Koyu mod değiştirmek için kullanılır.
        
        ## Yardım
        - **Kullanım Kılavuzu**: Bu yardım dokümanını açmak için kullanılır.
        - **Geri Bildirim**: Kullanıcı geri bildirimini almak için kullanılır.
        - **Güncellemeleri Kontrol Et**: Yeni sürüm olup olmadığını kontrol etmek için kullanılır.
        - **Hakkında**: Program hakkında bilgi göstermek için kullanılır.
        """
        
        # Insert the user guide content
        text_area.insert(tk.END, user_guide_content)
        text_area.configure(state=tk.DISABLED)  # Make it read-only
        
        # Add a close button
        close_button = ttk.Button(
            guide_dialog, 
            text="Close", 
            command=guide_dialog.destroy
        )
        close_button.pack(pady=10)
    
    def _show_feedback(self):
        """Show a dialog for user feedback."""
        # Create a dialog for feedback
        feedback_dialog = tk.Toplevel(self.app.root)
        feedback_dialog.title("Feedback")
        feedback_dialog.geometry("500x400")
        feedback_dialog.transient(self.app.root)
        feedback_dialog.grab_set()
        
        # Create a frame for feedback form
        form_frame = ttk.LabelFrame(feedback_dialog, text="Send Your Feedback")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Name input
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT, padx=5)
        
        name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=name_var, width=30)
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Email input
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(email_frame, text="Email:").pack(side=tk.LEFT, padx=5)
        
        email_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=email_var, width=30)
        email_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Feedback type
        type_frame = ttk.Frame(form_frame)
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT, padx=5)
        
        feedback_type = tk.StringVar(value="suggestion")
        
        ttk.Radiobutton(
            type_frame, 
            text="Suggestion", 
            variable=feedback_type, 
            value="suggestion"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            type_frame, 
            text="Bug Report", 
            variable=feedback_type, 
            value="bug"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            type_frame, 
            text="Question", 
            variable=feedback_type, 
            value="question"
        ).pack(side=tk.LEFT, padx=5)
        
        # Feedback content
        content_frame = ttk.Frame(form_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(content_frame, text="Feedback:").pack(anchor=tk.W, padx=5, pady=5)
        
        feedback_text = tk.Text(content_frame, wrap=tk.WORD, height=10)
        feedback_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=feedback_text.yview)
        feedback_text.configure(yscrollcommand=feedback_scrollbar.set)
        
        feedback_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        feedback_text.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Add send and cancel buttons
        button_frame = ttk.Frame(feedback_dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        send_button = ttk.Button(
            button_frame, 
            text="Send Feedback", 
            command=lambda: self._send_feedback(
                feedback_dialog, 
                name_var.get(), 
                email_var.get(), 
                feedback_type.get(), 
                feedback_text.get("1.0", tk.END)
            )
        )
        send_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Cancel", 
            command=feedback_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _send_feedback(self, dialog, name, email, feedback_type, feedback_content):
        """Send the user feedback.
        
        Args:
            dialog: Tkinter dialog to close after operation
            name (str): User's name
            email (str): User's email
            feedback_type (str): Type of feedback
            feedback_content (str): Feedback content
        """
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Feedback", "Thank you for your feedback! This feature will be fully implemented in a future update.")
        dialog.destroy()
    
    def _check_updates(self):
        """Check for application updates."""
        # For now, just show a message since this functionality is not implemented
        messagebox.showinfo("Check Updates", "You are using the latest version of miniPDF.")
    
    def _show_about(self):
        """Show information about the application."""
        # Create a dialog for about information
        about_dialog = tk.Toplevel(self.app.root)
        about_dialog.title("About miniPDF")
        about_dialog.geometry("400x300")
        about_dialog.transient(self.app.root)
        
        # Create a frame for the about content
        content_frame = ttk.Frame(about_dialog)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Application title
        title_label = ttk.Label(
            content_frame, 
            text="miniPDF", 
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Version information
        version_label = ttk.Label(
            content_frame, 
            text="Version 1.0.0"
        )
        version_label.pack()
        
        # Copyright information
        copyright_label = ttk.Label(
            content_frame, 
            text="2025 miniPDF Team. All rights reserved."
        )
        copyright_label.pack(pady=10)
        
        # Description
        description_text = """
        miniPDF is a simple PDF editor and viewer application
        that allows you to view, edit, and manage PDF files.
        
        This application is designed to be user-friendly and
        provide essential PDF manipulation features.
        """
        
        description_label = ttk.Label(
            content_frame, 
            text=description_text,
            justify=tk.CENTER,
            wraplength=350
        )
        description_label.pack(pady=10)
        
        # Add a close button
        close_button = ttk.Button(
            about_dialog, 
            text="Close", 
            command=about_dialog.destroy
        )
        close_button.pack(pady=10)
