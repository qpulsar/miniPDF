"""
Tools tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from gui.toolbar_tabs.base_tab import BaseTab
from core.merge_split import PDFMergeSplit
from core.security import PDFSecurity

class ToolsTab(BaseTab):
    """Tools tab for the toolbar."""
    
    def __init__(self, parent, app):
        """
        Initialize the tools tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        super().__init__(parent, app)
        self.merge_split = PDFMergeSplit()
        self.security = PDFSecurity()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the tools tab."""
        # Merge/Split frame
        merge_frame = self.create_frame("merge", "Birleştir/Böl")
        
        # Merge PDFs button
        self.add_button(
            merge_frame,
            text="PDF'leri Birleştir",
            command=self._merge_pdfs
        )
        
        # Split PDF button
        self.add_button(
            merge_frame,
            text="PDF'i Böl",
            command=self._split_pdf
        )
        
        # Security frame
        security_frame = self.create_frame("security", "Güvenlik")
        
        # Encrypt PDF button
        self.add_button(
            security_frame,
            text="PDF'i Şifrele",
            command=self._encrypt_pdf
        )
        
        # Decrypt PDF button
        self.add_button(
            security_frame,
            text="PDF Şifresini Çöz",
            command=self._decrypt_pdf
        )
        
        # Optimize frame
        optimize_frame = self.create_frame("optimize", "Optimize Et")
        
        # Compress PDF button
        self.add_button(
            optimize_frame,
            text="PDF'i Sıkıştır",
            command=self._compress_pdf
        )
    
    def _merge_pdfs(self):
        """Merge multiple PDFs into a single PDF file."""
        # Ask user to select PDF files to merge
        pdf_files = filedialog.askopenfilenames(
            title="Birleştirilecek PDF dosyalarını seçin",
            filetypes=[("PDF Dosyaları", "*.pdf")]
        )
        
        if not pdf_files or len(pdf_files) < 2:
            messagebox.showinfo("Bilgi", "Birleştirmek için en az iki PDF dosyası seçmelisiniz.")
            return
        
        # Create a dialog to allow reordering files
        self._show_merge_dialog(pdf_files)
    
    def _show_merge_dialog(self, pdf_files):
        """
        Show a dialog to reorder PDF files before merging.
        
        Args:
            pdf_files (tuple): Tuple of selected PDF file paths
        """
        # Create a new top-level window
        merge_dialog = tk.Toplevel(self.app.root)
        merge_dialog.title("PDF'leri Birleştir")
        merge_dialog.geometry("500x400")
        merge_dialog.transient(self.app.root)
        merge_dialog.grab_set()
        
        # Create a frame for the file list
        list_frame = ttk.LabelFrame(merge_dialog, text="PDF Dosyaları (Yeniden sıralamak için sürükleyin)")
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
            text="Yukarı Taşı", 
            command=lambda: self._move_item_up(file_listbox, file_paths)
        )
        move_up_button.pack(side=tk.LEFT, padx=5)
        
        move_down_button = ttk.Button(
            button_frame, 
            text="Aşağı Taşı", 
            command=lambda: self._move_item_down(file_listbox, file_paths)
        )
        move_down_button.pack(side=tk.LEFT, padx=5)
        
        # Add merge and cancel buttons
        action_frame = ttk.Frame(merge_dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        merge_button = ttk.Button(
            action_frame, 
            text="PDF'leri Birleştir", 
            command=lambda: self._perform_merge(merge_dialog, file_paths)
        )
        merge_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            action_frame, 
            text="İptal", 
            command=merge_dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _move_item_up(self, listbox, file_paths):
        """
        Move the selected item up in the listbox.
        
        Args:
            listbox (tk.Listbox): Listbox widget
            file_paths (list): List of file paths
        """
        selected_idx = listbox.curselection()
        if not selected_idx or selected_idx[0] == 0:
            return
        
        idx = selected_idx[0]
        
        # Swap items in the listbox
        text = listbox.get(idx)
        listbox.delete(idx)
        listbox.insert(idx - 1, text)
        listbox.selection_set(idx - 1)
        
        # Swap items in the file_paths list
        file_paths[idx], file_paths[idx - 1] = file_paths[idx - 1], file_paths[idx]
    
    def _move_item_down(self, listbox, file_paths):
        """
        Move the selected item down in the listbox.
        
        Args:
            listbox (tk.Listbox): Listbox widget
            file_paths (list): List of file paths
        """
        selected_idx = listbox.curselection()
        if not selected_idx or selected_idx[0] == listbox.size() - 1:
            return
        
        idx = selected_idx[0]
        
        # Swap items in the listbox
        text = listbox.get(idx)
        listbox.delete(idx)
        listbox.insert(idx + 1, text)
        listbox.selection_set(idx + 1)
        
        # Swap items in the file_paths list
        file_paths[idx], file_paths[idx + 1] = file_paths[idx + 1], file_paths[idx]
    
    def _perform_merge(self, dialog, file_paths):
        """
        Perform the merge operation.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            file_paths (list): List of PDF file paths to merge
        """
        # Ask for the output file
        output_file = filedialog.asksaveasfilename(
            title="Birleştirilmiş PDF'i Kaydet",
            defaultextension=".pdf",
            filetypes=[("PDF Dosyaları", "*.pdf")],
            initialdir=os.path.dirname(file_paths[0]),
            initialfile="birlestirilmis.pdf"
        )
        
        if not output_file:
            return
        
        # Merge the PDFs
        if self.merge_split.merge_pdfs(file_paths, output_file):
            # Close the dialog
            dialog.destroy()
            
            # Ask if the user wants to open the merged PDF
            if messagebox.askyesno("Başarılı", f"PDF'ler başarıyla birleştirildi ve {output_file} olarak kaydedildi. Birleştirilmiş PDF'i açmak ister misiniz?"):
                self.app.open_pdf(output_file)
        else:
            messagebox.showerror("Hata", "PDF'ler birleştirilirken bir hata oluştu.")
    
    def _split_pdf(self):
        """Split a PDF into multiple files."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        # Create a dialog for splitting options
        self._show_split_dialog()
    
    def _show_split_dialog(self):
        """Show a dialog for PDF splitting options."""
        # Create a new top-level window
        split_dialog = tk.Toplevel(self.app.root)
        split_dialog.title("PDF'i Böl")
        split_dialog.geometry("400x350")
        split_dialog.transient(self.app.root)
        split_dialog.grab_set()
        
        # Create a frame for splitting method
        method_frame = ttk.LabelFrame(split_dialog, text="Bölme Yöntemi")
        method_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Create a variable for the splitting method
        method_var = tk.StringVar(value="equal")
        
        # Create radio buttons for splitting methods
        ttk.Radiobutton(
            method_frame,
            text="Eşit Sayıda Sayfaya Böl",
            variable=method_var,
            value="equal"
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Radiobutton(
            method_frame,
            text="Belirli Sayfa Aralıklarına Böl",
            variable=method_var,
            value="range"
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # Create a frame for splitting options
        options_frame = ttk.LabelFrame(split_dialog, text="Bölme Seçenekleri")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Pages per file option (for equal method)
        pages_frame = ttk.Frame(options_frame)
        pages_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            pages_frame,
            text="Dosya Başına Sayfa Sayısı:"
        ).pack(side=tk.LEFT, padx=5)
        
        pages_var = tk.IntVar(value=1)
        pages_spinbox = ttk.Spinbox(
            pages_frame,
            from_=1,
            to=100,
            textvariable=pages_var,
            width=5
        )
        pages_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Page range option (for range method)
        range_frame = ttk.Frame(options_frame)
        range_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            range_frame,
            text="Sayfa Aralıkları (örn. 1-3,5,7-9):"
        ).pack(side=tk.LEFT, padx=5)
        
        range_var = tk.StringVar()
        range_entry = ttk.Entry(
            range_frame,
            textvariable=range_var,
            width=20
        )
        range_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Output directory option
        output_frame = ttk.Frame(options_frame)
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            output_frame,
            text="Çıktı Dizini:"
        ).pack(side=tk.LEFT, padx=5)
        
        output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(
            output_frame,
            textvariable=output_dir_var,
            width=20
        )
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(
            output_frame, 
            text="Gözat...", 
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
            text="PDF'i Böl", 
            width=10,
            command=lambda: self._perform_split(
                split_dialog,
                method_var.get(),
                pages_var.get(),
                range_var.get(),
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
        """
        Browse for an output directory.
        
        Args:
            output_dir_var (tk.StringVar): Variable to store the selected directory
        """
        directory = filedialog.askdirectory(
            title="Çıktı Dizinini Seçin",
            initialdir=output_dir_var.get() if output_dir_var.get() else os.path.dirname(self.app.pdf_manager.current_file)
        )
        
        if directory:
            output_dir_var.set(directory)
    
    def _perform_split(self, dialog, method, pages_per_file, page_range, output_dir):
        """
        Perform the split operation.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            method (str): Splitting method ('equal' or 'range')
            pages_per_file (int): Number of pages per file (for 'equal' method)
            page_range (str): Page range string (for 'range' method)
            output_dir (str): Output directory
        """
        # Validate the output directory
        if not output_dir:
            messagebox.showerror("Hata", "Lütfen bir çıktı dizini seçin.")
            return
        
        if not os.path.isdir(output_dir):
            messagebox.showerror("Hata", "Geçersiz çıktı dizini.")
            return
        
        # Get the current PDF file
        pdf_file = self.app.pdf_manager.current_file
        
        # Split the PDF based on the selected method
        if method == "equal":
            if self.merge_split.split_pdf_equal(pdf_file, output_dir, pages_per_file):
                dialog.destroy()
                messagebox.showinfo("Başarılı", f"PDF başarıyla {output_dir} dizinine bölündü.")
            else:
                messagebox.showerror("Hata", "PDF bölünürken bir hata oluştu.")
        elif method == "range":
            # Parse the page range
            page_indices = self._parse_page_range(page_range)
            
            if not page_indices:
                messagebox.showerror("Hata", "Geçersiz sayfa aralığı.")
                return
            
            if self.merge_split.split_pdf_range(pdf_file, output_dir, page_indices):
                dialog.destroy()
                messagebox.showinfo("Başarılı", f"PDF başarıyla {output_dir} dizinine bölündü.")
            else:
                messagebox.showerror("Hata", "PDF bölünürken bir hata oluştu.")
    
    def _parse_page_range(self, page_range_str):
        """
        Parse a page range string into a list of page indices.
        
        Args:
            page_range_str (str): Page range string (e.g., "1-3,5,7-9")
            
        Returns:
            list: List of page indices
        """
        from core.pdf_operations import PDFOperations
        
        # Get the total number of pages in the PDF
        total_pages = self.app.pdf_manager.get_total_pages()
        
        # Parse the page range
        return PDFOperations.parse_page_range(page_range_str, total_pages)
    
    def _encrypt_pdf(self):
        """Encrypt the current PDF."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        # Create a dialog for encryption options
        dialog = tk.Toplevel(self.app.root)
        dialog.title("PDF'i Şifrele")
        dialog.geometry("400x250")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Create a frame for passwords
        password_frame = ttk.LabelFrame(dialog, text="Şifreleme Seçenekleri")
        password_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # User password
        user_frame = ttk.Frame(password_frame)
        user_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            user_frame,
            text="Kullanıcı Şifresi:"
        ).pack(side=tk.LEFT, padx=5)
        
        user_password_var = tk.StringVar()
        user_password_entry = ttk.Entry(
            user_frame,
            textvariable=user_password_var,
            show="*",
            width=20
        )
        user_password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Owner password
        owner_frame = ttk.Frame(password_frame)
        owner_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            owner_frame,
            text="Sahip Şifresi:"
        ).pack(side=tk.LEFT, padx=5)
        
        owner_password_var = tk.StringVar()
        owner_password_entry = ttk.Entry(
            owner_frame,
            textvariable=owner_password_var,
            show="*",
            width=20
        )
        owner_password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Add encrypt and cancel buttons
        action_frame = ttk.Frame(dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        encrypt_button = ttk.Button(
            action_frame, 
            text="Şifrele", 
            width=10,
            command=lambda: self._perform_encryption(
                dialog,
                user_password_var.get(),
                owner_password_var.get()
            )
        )
        encrypt_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            action_frame, 
            text="İptal", 
            width=10,
            command=dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _perform_encryption(self, dialog, user_password, owner_password):
        """
        Perform the encryption operation.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            user_password (str): User password
            owner_password (str): Owner password
        """
        # Validate the passwords
        if not user_password:
            messagebox.showerror("Hata", "Lütfen bir kullanıcı şifresi girin.")
            return
        
        # Encrypt the PDF
        if PDFSecurity.encrypt_pdf(self.app.pdf_manager.current_file, user_password, owner_password):
            dialog.destroy()
            messagebox.showinfo("Başarılı", "PDF başarıyla şifrelendi.")
            
            # Reload the PDF
            self.app.reload_pdf()
        else:
            messagebox.showerror("Hata", "PDF şifrelenirken bir hata oluştu.")
    
    def _decrypt_pdf(self):
        """Decrypt the current PDF."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        # Create a dialog for decryption options
        dialog = tk.Toplevel(self.app.root)
        dialog.title("PDF Şifresini Çöz")
        dialog.geometry("400x150")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Create a frame for password
        password_frame = ttk.LabelFrame(dialog, text="Şifre Çözme Seçenekleri")
        password_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Password
        pass_frame = ttk.Frame(password_frame)
        pass_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(
            pass_frame,
            text="Şifre:"
        ).pack(side=tk.LEFT, padx=5)
        
        password_var = tk.StringVar()
        password_entry = ttk.Entry(
            pass_frame,
            textvariable=password_var,
            show="*",
            width=20
        )
        password_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Add decrypt and cancel buttons
        action_frame = ttk.Frame(dialog)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        decrypt_button = ttk.Button(
            action_frame, 
            text="Şifreyi Çöz", 
            width=10,
            command=lambda: self._perform_decryption(
                dialog,
                password_var.get()
            )
        )
        decrypt_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(
            action_frame, 
            text="İptal", 
            width=10,
            command=dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _perform_decryption(self, dialog, password):
        """
        Perform the decryption operation.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            password (str): Password to decrypt the PDF
        """
        # Validate the password
        if not password:
            messagebox.showerror("Hata", "Lütfen bir şifre girin.")
            return
        
        # Decrypt the PDF
        if PDFSecurity.decrypt_pdf(self.app.pdf_manager.current_file, password):
            dialog.destroy()
            messagebox.showinfo("Başarılı", "PDF şifresi başarıyla çözüldü.")
            
            # Reload the PDF
            self.app.reload_pdf()
        else:
            messagebox.showerror("Hata", "PDF şifresi çözülürken bir hata oluştu. Şifre yanlış olabilir.")
    
    def _compress_pdf(self):
        """Compress the current PDF."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        messagebox.showinfo("Bilgi", "Bu özellik henüz uygulanmadı.")
