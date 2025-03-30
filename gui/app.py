"""
Main application window for the PDF Editor.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QFileDialog, QMessageBox, QStatusBar, QMenuBar, QInputDialog, QColorDialog)
from PyQt6.QtCore import Qt
from .toolbar import Toolbar
from .sidebar import Sidebar
from .preview import PDFPreview
from core.pdf_manager import PDFManager
from .menu import MenuBar

class PDFEditorApp(QMainWindow):
    """Main window class for the PDF Editor application."""
    
    def __init__(self):
        """Initialize the application window."""
        super().__init__()
        
        # Initialize PDF manager
        self.pdf_manager = PDFManager()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # Create toolbar
        self.toolbar = Toolbar(self)
        main_layout.addWidget(self.toolbar)
        
        # Create content area with sidebar and preview
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        main_layout.addWidget(content_widget)
        
        # Create sidebar for page list
        self.sidebar = Sidebar(self)
        self.sidebar.setFixedWidth(150)
        content_layout.insertWidget(0, self.sidebar)
        
        # Create preview area
        self.preview = PDFPreview(self)
        content_layout.addWidget(self.preview)
        
        # Connect signals
        self.sidebar.page_selected.connect(self.preview.show_page)
        
        # Set content layout stretch factors
        content_layout.setStretch(0, 1)  # Sidebar
        content_layout.setStretch(1, 4)  # Preview
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def open_pdf(self):
        """Open a PDF file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "PDF Dosyası Aç",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.open_pdf(file_path):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    self.preview.show_page(0)
                self.status_bar.showMessage(f"Opened: {file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not open PDF file."
                )
                
    def save_pdf(self):
        """Save the current PDF file."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "No PDF file is open."
            )
            return False
            
        if self.pdf_manager.file_path:
            if self.pdf_manager.save_pdf():
                self.status_bar.showMessage(f"Saved: {self.pdf_manager.file_path}")
                return True
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not save PDF file."
                )
                return False
                
        return self.save_pdf_as()
        
    def save_pdf_as(self):
        """Save the current PDF file with a new name."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "No PDF file is open."
            )
            return False
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF File As",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.save_pdf_as(file_path):
                self.status_bar.showMessage(f"Saved: {file_path}")
                return True
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not save PDF file."
                )
        return False
        
    def on_open(self):
        """Handle open file action."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.open_pdf(file_path):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    self.preview.show_page(0)
                self.status_bar.showMessage(f"Opened {file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not open PDF file."
                )
                
    def on_save(self):
        """Handle save action."""
        if not self.pdf_manager.file_path:
            self.on_save_as()
            return
            
        if self.pdf_manager.save_pdf():
            self.status_bar.showMessage("File saved successfully")
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not save PDF file."
            )
            
    def on_save_as(self):
        """Handle save as action."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if file_path:
            if self.pdf_manager.save_pdf_as(file_path):
                self.status_bar.showMessage(f"File saved as {file_path}")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not save PDF file."
                )
                
    def on_print(self):
        """Handle print action."""
        QMessageBox.information(
            self,
            "Info",
            "Printing will be implemented in a future version."
        )
        
    def on_add_page(self):
        """Handle add page action."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "Please open a PDF file first."
            )
            return
            
        # Ask for page position
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            current_page = self.pdf_manager.get_page_count()
            
        position, ok = QInputDialog.getInt(
            self,
            "Add Page",
            "Enter page position (1 to add at start, or leave as is to add at current position):",
            value=current_page + 1,
            min=1,
            max=self.pdf_manager.get_page_count() + 1
        )
        
        if not ok:
            return
            
        # Ask for page source
        source_options = ["Blank Page", "From Another PDF"]
        source, ok = QInputDialog.getItem(
            self,
            "Add Page",
            "Select page source:",
            source_options,
            current=0,
            editable=False
        )
        
        if not ok:
            return
            
        if source == "Blank Page":
            # Add blank page
            if self.pdf_manager.add_blank_page(position=position - 1):
                self.sidebar.update_page_list()
                self.preview.show_page(position - 1)
                self.sidebar.setCurrentRow(position - 1)
                self.status_bar.showMessage("Blank page added")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not add blank page."
                )
        else:
            # Get source PDF
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Source PDF",
                "",
                "PDF Files (*.pdf);;All Files (*.*)"
            )
            
            if not file_path:
                return
                
            # Get page number from source PDF
            try:
                src_doc = fitz.open(file_path)
                page_num, ok = QInputDialog.getInt(
                    self,
                    "Add Page",
                    "Enter page number to copy (1 to last page):",
                    value=1,
                    min=1,
                    max=len(src_doc)
                )
                src_doc.close()
                
                if not ok:
                    return
                    
                # Add page from source PDF
                if self.pdf_manager.add_page_from_pdf(file_path, page_num - 1, position - 1):
                    self.sidebar.update_page_list()
                    self.preview.show_page(position - 1)
                    self.sidebar.setCurrentRow(position - 1)
                    self.status_bar.showMessage("Page added from source PDF")
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "Could not add page from source PDF."
                    )
            except Exception:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not read source PDF."
                )
                
    def on_delete_page(self):
        """Handle delete page action."""
        if not self.pdf_manager.doc:
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to delete."
            )
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this page?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.pdf_manager.delete_page(current_page):
                self.sidebar.update_page_list()
                if self.pdf_manager.get_page_count() > 0:
                    new_page = min(current_page, self.pdf_manager.get_page_count() - 1)
                    self.preview.show_page(new_page)
                    self.sidebar.setCurrentRow(new_page)
                self.status_bar.showMessage("Page deleted")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not delete page."
                )
                
    def on_rotate_page(self, angle):
        """Handle rotate page action."""
        if not self.pdf_manager.doc:
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to rotate."
            )
            return
            
        if self.pdf_manager.rotate_page(current_page, angle):
            self.preview.show_page(current_page)
            self.status_bar.showMessage(f"Page rotated by {angle}°")
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not rotate page."
            )
            
    def on_move_page(self):
        """Handle move page action."""
        QMessageBox.information(
            self,
            "Info",
            "Page moving will be implemented in a future version."
        )
        
    def on_export_page(self):
        """Handle export page action."""
        QMessageBox.information(
            self,
            "Info",
            "Page export will be implemented in a future version."
        )
        
    def on_add_text(self):
        """Handle add text action."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "Please open a PDF file first."
            )
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page first."
            )
            return
            
        # Get text content
        text, ok = QInputDialog.getText(
            self,
            "Add Text Annotation",
            "Enter text:"
        )
        
        if not ok or not text:
            return
            
        # Get color
        color = QColorDialog.getColor(
            QColor(255, 255, 0),  # Default: yellow
            self,
            "Select Text Color"
        )
        
        if color.isValid():
            self.preview.start_text_annotation(color, text)
            self.status_bar.showMessage("Click and drag to add text annotation")
            
    def on_highlight(self):
        """Handle highlight action."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "Please open a PDF file first."
            )
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page first."
            )
            return
            
        # Get color
        color = QColorDialog.getColor(
            QColor(255, 255, 0),  # Default: yellow
            self,
            "Select Highlight Color"
        )
        
        if color.isValid():
            self.preview.start_highlight_annotation(color)
            self.status_bar.showMessage("Click and drag to highlight")
            
    def on_draw(self):
        """Handle draw action."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "Please open a PDF file first."
            )
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page first."
            )
            return
            
        # Get line width
        width, ok = QInputDialog.getDouble(
            self,
            "Drawing Settings",
            "Line width:",
            value=2.0,
            min=0.1,
            max=10.0,
            decimals=1
        )
        
        if not ok:
            return
            
        # Get color
        color = QColorDialog.getColor(
            QColor(0, 0, 255),  # Default: blue
            self,
            "Select Drawing Color"
        )
        
        if color.isValid():
            self.preview.start_ink_annotation(color, width)
            self.status_bar.showMessage("Click and drag to draw")
            
    def on_delete_annotation(self):
        """Handle delete annotation action."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "Please open a PDF file first."
            )
            return
            
        current_page = self.sidebar.currentRow()
        if current_page < 0:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page first."
            )
            return
            
        # Get annotations on current page
        annots = self.pdf_manager.get_annotations(current_page)
        if not annots:
            QMessageBox.information(
                self,
                "Info",
                "No annotations found on this page."
            )
            return
            
        # Ask which annotation to delete
        items = []
        for i, annot in enumerate(annots):
            annot_type = annot.type[1]  # Remove leading '/'
            items.append(f"{i + 1}: {annot_type}")
            
        item, ok = QInputDialog.getItem(
            self,
            "Delete Annotation",
            "Select annotation to delete:",
            items,
            current=0,
            editable=False
        )
        
        if ok and item:
            # Extract index from selected item
            index = int(item.split(":")[0]) - 1
            
            if self.pdf_manager.delete_annotation(current_page, index):
                self.preview.show_page(current_page)
                self.status_bar.showMessage("Annotation deleted")
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Could not delete annotation."
                )
        
    def on_ocr(self):
        """Handle OCR action."""
        QMessageBox.information(
            self,
            "Info",
            "OCR will be implemented in a future version."
        )
        
    def on_merge(self):
        """Handle merge PDFs action."""
        # Get list of PDFs to merge
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDFs to Merge",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )
        
        if not file_paths:
            return
            
        # Create merged PDF
        if self.pdf_manager.merge_pdfs(file_paths):
            self.sidebar.update_page_list()
            if self.pdf_manager.get_page_count() > 0:
                self.preview.show_page(0)
                self.sidebar.setCurrentRow(0)
            self.status_bar.showMessage("PDFs merged successfully")
            
            # Ask to save merged PDF
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Merged PDF As",
                "",
                "PDF Files (*.pdf);;All Files (*.*)"
            )
            
            if file_path:
                if self.pdf_manager.save_pdf_as(file_path):
                    self.status_bar.showMessage(f"Merged PDF saved as {file_path}")
                else:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "Could not save merged PDF."
                    )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not merge PDFs."
            )
        
    def on_split(self):
        """Handle split PDF action."""
        if not self.pdf_manager.doc:
            QMessageBox.information(
                self,
                "Info",
                "Please open a PDF file first."
            )
            return
            
        # Get output directory
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            ""
        )
        
        if not output_dir:
            return
            
        # Ask for split mode
        split_modes = ["One PDF per page", "Custom page ranges"]
        mode, ok = QInputDialog.getItem(
            self,
            "Split PDF",
            "Select split mode:",
            split_modes,
            current=0,
            editable=False
        )
        
        if not ok:
            return
            
        split_ranges = None
        if mode == "Custom page ranges":
            # Get page ranges
            ranges_text, ok = QInputDialog.getText(
                self,
                "Split PDF",
                "Enter page ranges (e.g., '1-3, 4-6' or '1, 2, 3-5'):",
                text="1-" + str(self.pdf_manager.get_page_count())
            )
            
            if not ok:
                return
                
            try:
                # Parse page ranges
                split_ranges = []
                for range_str in ranges_text.split(","):
                    range_str = range_str.strip()
                    if "-" in range_str:
                        start, end = map(int, range_str.split("-"))
                        split_ranges.append((start - 1, end - 1))
                    else:
                        page = int(range_str)
                        split_ranges.append((page - 1, page - 1))
            except ValueError:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Invalid page range format."
                )
                return
                
        # Split PDF
        output_files = self.pdf_manager.split_pdf(output_dir, split_ranges)
        
        if output_files:
            QMessageBox.information(
                self,
                "Success",
                f"PDF split into {len(output_files)} files.\nSaved in: {output_dir}"
            )
            self.status_bar.showMessage(f"PDF split into {len(output_files)} files")
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not split PDF."
            )
        
    def on_encrypt(self):
        """Handle encrypt PDF action."""
        QMessageBox.information(
            self,
            "Info",
            "PDF encryption will be implemented in a future version."
        )
        
    def on_decrypt(self):
        """Handle decrypt PDF action."""
        QMessageBox.information(
            self,
            "Info",
            "PDF decryption will be implemented in a future version."
        )
        
    def on_zoom_in(self):
        """Handle zoom in action."""
        self.toolbar.view_tab.zoom_in()
        
    def on_zoom_out(self):
        """Handle zoom out action."""
        self.toolbar.view_tab.zoom_out()
        
    def on_fit_width(self):
        """Handle fit width action."""
        QMessageBox.information(
            self,
            "Info",
            "Fit width will be implemented in a future version."
        )
        
    def on_page_layout(self, layout):
        """Handle page layout change."""
        QMessageBox.information(
            self,
            "Info",
            "Page layout will be implemented in a future version."
        )
        
    def on_theme(self, theme):
        """Handle theme change."""
        QMessageBox.information(
            self,
            "Info",
            "Theme change will be implemented in a future version."
        )
        
    def closeEvent(self, event):
        """Handle window close event."""
        if self.pdf_manager.doc and self.pdf_manager.has_changes():
            reply = QMessageBox.question(
                self,
                "Save Changes?",
                "The PDF file has unsaved changes. Do you want to save them?",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            elif reply == QMessageBox.StandardButton.Yes:
                if not self.save_pdf():
                    event.ignore()
                    return
                    
        event.accept()
