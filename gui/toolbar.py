"""
Toolbar implementation for the PDF Editor.
"""
from PyQt6.QtWidgets import QToolBar, QTabWidget
from .toolbar_tabs.file_tab import FileTab
from .toolbar_tabs.edit_tab import EditTab
from .toolbar_tabs.view_tab import ViewTab

class Toolbar(QTabWidget):
    """Main toolbar with tabbed sections."""
    
    def __init__(self, parent=None):
        """Initialize toolbar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Create tabs
        self.file_tab = FileTab(self)
        self.edit_tab = EditTab(self)
        self.view_tab = ViewTab(self)
        
        # Add tabs
        self.addTab(self.file_tab, "File")
        self.addTab(self.edit_tab, "Edit")
        self.addTab(self.view_tab, "View")
        
        # Set fixed height
        self.setFixedHeight(120)
