"""
Sidebar implementation.
"""
from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon

class Sidebar(QListWidget):
    """Sidebar widget for displaying page thumbnails."""
    
    page_selected = pyqtSignal(int)  # Signal emitted when page is selected
    
    def __init__(self, parent=None):
        """Initialize sidebar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.app = parent
        
        # Set up appearance
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setIconSize(Qt.QSize(120, 160))  # Thumbnail size
        self.setSpacing(10)
        self.setMovement(QListWidget.Movement.Static)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)
        
        # Connect signals
        self.currentRowChanged.connect(self.on_page_selected)
        
    def update_pages(self):
        """Update page thumbnails."""
        self.clear()
        
        if not self.app.pdf_manager.doc:
            return
            
        # Add thumbnails for each page
        for i in range(self.app.pdf_manager.get_page_count()):
            # Create thumbnail
            pixmap = self.app.pdf_manager.get_page_thumbnail(i)
            if pixmap:
                # Create item
                item = QListWidgetItem()
                item.setIcon(QIcon(pixmap))
                item.setText(f"Page {i + 1}")
                self.addItem(item)
                
    def on_page_selected(self, row):
        """Handle page selection.
        
        Args:
            row: Selected row index
        """
        if row >= 0:
            self.page_selected.emit(row)
