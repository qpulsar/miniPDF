"""
Sidebar component for the PDF Editor.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class Sidebar(QWidget):
    """Sidebar widget containing the page list."""
    
    page_selected = pyqtSignal(int)  # Signal emitted when a page is selected
    
    def __init__(self, parent):
        """Initialize sidebar.
        
        Args:
            parent: Parent widget (PDFEditorApp)
        """
        super().__init__(parent)
        self.app = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Setup sidebar UI."""
        layout = QVBoxLayout(self)
        
        # Create title label
        title_label = QLabel("Pages")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Create page list
        self.page_list = QListWidget()
        self.page_list.currentRowChanged.connect(self._on_page_selected)
        layout.addWidget(self.page_list)
        
        # Add buttons for page manipulation
        button_layout = QHBoxLayout()
        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self._move_page_up)
        button_layout.addWidget(self.move_up_button)
        
        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self._move_page_down)
        button_layout.addWidget(self.move_down_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def update_page_list(self):
        """Update the page list with current PDF pages."""
        self.page_list.clear()
        
        if self.app.pdf_manager.doc:
            for i in range(len(self.app.pdf_manager.doc)):
                self.page_list.addItem(f"Page {i + 1}")
                
    def get_selected_page_index(self):
        """Get the currently selected page index.
        
        Returns:
            int: Selected page index or -1 if no selection
        """
        return self.page_list.currentRow()
        
    def _on_page_selected(self, index):
        """Handle page selection.
        
        Args:
            index (int): Selected page index
        """
        if index >= 0:
            self.page_selected.emit(index)
            self.app.preview.show_page(index)
    
    def _move_page_up(self):
        """Move the selected page up in the document order."""
        # This will be implemented later
        # For now, just show a message box
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Info", "Move Page Up functionality will be implemented soon.")
    
    def _move_page_down(self):
        """Move the selected page down in the document order."""
        # This will be implemented later
        # For now, just show a message box
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Info", "Move Page Down functionality will be implemented soon.")
