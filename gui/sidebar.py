"""
Sidebar implementation for the PDF Editor.
"""
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal

class Sidebar(QListWidget):
    """Sidebar showing list of PDF pages."""
    
    page_selected = pyqtSignal(int)  # Signal emitted when page is selected
    
    def __init__(self, parent=None):
        """Initialize sidebar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        
        # Connect signals
        self.currentRowChanged.connect(self.on_page_selected)
        
    def update_page_list(self):
        """Update the list of pages."""
        self.clear()
        
        if not self.parent.pdf_manager.doc:
            return
            
        for i in range(self.parent.pdf_manager.get_page_count()):
            item = QListWidgetItem(f"Page {i + 1}")
            self.addItem(item)
            
    def on_page_selected(self, current_row):
        """Handle page selection.
        
        Args:
            current_row: Selected row index
        """
        if current_row >= 0:
            self.page_selected.emit(current_row)
