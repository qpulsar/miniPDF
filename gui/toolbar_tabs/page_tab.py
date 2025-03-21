"""
Page tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from gui.toolbar_tabs.base_tab import BaseTab
from gui.utils import create_icon_button
from core.pdf_operations import PDFOperations

class PageTab(BaseTab):
    """Page tab for the toolbar."""
    
    def __init__(self, parent, app):
        """
        Initialize the page tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        super().__init__(parent, app)
        self.pdf_operations = PDFOperations()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the page tab."""
        # Page navigation frame
        nav_frame = self.create_frame("navigation", "Sayfa Gezinti")
        
        # Previous page button with icon
        create_icon_button(
            nav_frame,
            icon_name="navigate_before",
            text="Önceki Sayfa",
            command=self._prev_page,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Next page button with icon
        create_icon_button(
            nav_frame,
            icon_name="navigate_next",
            text="Sonraki Sayfa",
            command=self._next_page,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Page operations frame
        page_frame = self.create_frame("page_operations", "Sayfa İşlemleri")
        
        # Add blank page button with icon
        create_icon_button(
            page_frame,
            icon_name="add_page",
            text="Boş Sayfa Ekle",
            command=self._add_blank_page,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Delete page button with icon
        create_icon_button(
            page_frame,
            icon_name="delete_page",
            text="Sayfayı Sil",
            command=self.app.delete_current_page,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Extract page button with icon
        create_icon_button(
            page_frame,
            icon_name="extract_page",
            text="Sayfayı Çıkart",
            command=self._extract_page,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Rotate page button with icon
        create_icon_button(
            page_frame,
            icon_name="rotate",
            text="Sayfa Döndür",
            command=self._rotate_page,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # PDF operations frame
        pdf_frame = self.create_frame("pdf_operations", "PDF İşlemleri")
        
        # Split PDF button with icon
        create_icon_button(
            pdf_frame,
            icon_name="split",
            text="PDF Böl",
            command=self._split_pdf,
            compound=tk.LEFT,
            padx=5,
            pady=5
        ).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Merge PDFs button with icon
        create_icon_button(
            pdf_frame,
            icon_name="merge",
            text="PDF Birleştir",
            command=self._merge_pdfs,
            compound=tk.LEFT,
            padx=5,
            pady=5,
            bg="#e3f2fd"  # Light blue background for accent
        ).pack(side=tk.LEFT, padx=2, pady=2)
    
    def _prev_page(self):
        """Go to the previous page."""
        if not self.check_pdf_open():
            return
        
        self.app.pdf_manager.prev_page()
        self.app.preview.refresh()
    
    def _next_page(self):
        """Go to the next page."""
        if not self.check_pdf_open():
            return
        
        self.app.pdf_manager.next_page()
        self.app.preview.refresh()
    
    def _add_blank_page(self):
        """Add a blank page to the PDF."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        # Add a blank page using the PDFOperations class
        if PDFOperations.add_blank_page(self.app.pdf_manager.current_file):
            # Reload the PDF to show the changes
            self.app.reload_pdf()
            messagebox.showinfo("Başarılı", "Boş sayfa eklendi.")
        else:
            messagebox.showerror("Hata", "Boş sayfa eklenirken bir hata oluştu.")
    
    def _extract_page(self):
        """Extract the current page to a new PDF file."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        # Ask for the output file
        output_file = filedialog.asksaveasfilename(
            title="Sayfayı Kaydet",
            defaultextension=".pdf",
            filetypes=[("PDF Dosyaları", "*.pdf")],
            initialdir=os.path.dirname(self.app.pdf_manager.current_file),
            initialfile=f"sayfa_{self.app.pdf_manager.current_page_index + 1}.pdf"
        )
        
        if not output_file:
            return
        
        # Extract the page using the PDFOperations class
        if PDFOperations.extract_page(
            self.app.pdf_manager.current_file,
            self.app.pdf_manager.current_page_index,
            output_file
        ):
            messagebox.showinfo("Başarılı", f"Sayfa başarıyla çıkartıldı ve {output_file} olarak kaydedildi.")
        else:
            messagebox.showerror("Hata", "Sayfa çıkartılırken bir hata oluştu.")
    
    def _rotate_page(self):
        """Rotate the current page."""
        if not self.app.pdf_manager.current_file:
            messagebox.showinfo("Bilgi", "Lütfen önce bir PDF dosyası açın.")
            return
        
        # Create a dialog to select rotation angle
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Sayfayı Döndür")
        dialog.geometry("300x200")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Add a label
        ttk.Label(
            dialog,
            text="Döndürme açısını seçin:",
            font=("Arial", 12)
        ).pack(pady=10)
        
        # Create a variable for the rotation angle
        angle_var = tk.IntVar(value=90)
        
        # Create radio buttons for rotation angles
        angles = [(90, "90° Saat Yönünde"), 
                 (180, "180° Çevir"), 
                 (270, "90° Saat Yönünün Tersine")]
        
        for angle, text in angles:
            ttk.Radiobutton(
                dialog,
                text=text,
                variable=angle_var,
                value=angle
            ).pack(anchor=tk.W, padx=20, pady=5)
        
        # Add buttons frame
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Add apply button
        ttk.Button(
            buttons_frame,
            text="Uygula",
            command=lambda: self._perform_rotation(
                dialog,
                self.app.pdf_manager.current_page_index,
                angle_var.get()
            )
        ).pack(side=tk.RIGHT, padx=10)
        
        # Add cancel button
        ttk.Button(
            buttons_frame,
            text="İptal",
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=10)
    
    def _perform_rotation(self, dialog, page_index, angle):
        """
        Perform the rotation operation.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            page_index (int): Index of the page to rotate
            angle (int): Rotation angle
        """
        if PDFOperations.rotate_page(self.app.pdf_manager.current_file, page_index, angle):
            # Close the dialog
            dialog.destroy()
            
            # Reload the PDF to show the changes
            self.app.reload_pdf()
            messagebox.showinfo("Başarılı", f"Sayfa {angle}° döndürüldü.")
        else:
            messagebox.showerror("Hata", "Sayfa döndürülürken bir hata oluştu.")
    
    def _split_pdf(self):
        """Split the PDF into multiple files."""
        if not self.check_pdf_open():
            return
        
        self.show_not_implemented()
    
    def _merge_pdfs(self):
        """Merge multiple PDFs into one."""
        self.show_not_implemented()
