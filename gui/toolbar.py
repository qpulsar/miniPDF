"""
Toolbar module for the PDF Editor application.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from core.merge_split import PDFMergeSplit
import os

class Toolbar(ttk.Frame):
    """Toolbar widget with buttons for common operations."""
    
    def __init__(self, parent, app):
        """Initialize the toolbar.
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent)
        self.app = app
        self.merge_split = PDFMergeSplit()
        
        # File operations
        self.file_frame = ttk.LabelFrame(self, text="File")
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
        self.page_frame = ttk.LabelFrame(self, text="Page")
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
        self.merge_frame = ttk.LabelFrame(self, text="Merge/Split")
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
        self.text_frame = ttk.LabelFrame(self, text="Text")
        self.text_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)
        
        self.extract_text_button = ttk.Button(
            self.text_frame,
            text="Extract Text",
            command=self._extract_text
        )
        self.extract_text_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Annotation operations
        self.annot_frame = ttk.LabelFrame(self, text="Annotations")
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
