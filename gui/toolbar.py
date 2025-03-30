"""
Toolbar implementation.
"""
from PyQt6.QtWidgets import QTabWidget
from .toolbar_tabs.file_tab import FileTab
from .toolbar_tabs.edit_tab import EditTab
from .toolbar_tabs.view_tab import ViewTab
from .toolbar_tabs.help_tab import HelpTab
from .toolbar_tabs.annotation_tab import AnnotationTab

class Toolbar(QTabWidget):
    """Main toolbar widget."""
    
    def __init__(self, parent=None):
        """Initialize toolbar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Create tabs
        self.file_tab = FileTab(parent)
        self.edit_tab = EditTab(parent)
        self.view_tab = ViewTab(parent)
        self.annotation_tab = AnnotationTab(parent)
        self.help_tab = HelpTab(parent)
        
        # Add tabs
        self.addTab(self.file_tab, "File")
        self.addTab(self.edit_tab, "Edit")
        self.addTab(self.view_tab, "View")
        self.addTab(self.annotation_tab, "Annotate")
        self.addTab(self.help_tab, "Help")
        
        # Connect annotation signals
        self.annotation_tab.text_annotation_requested.connect(
            self.on_text_annotation_requested
        )
        self.annotation_tab.highlight_annotation_requested.connect(
            self.on_highlight_annotation_requested
        )
        self.annotation_tab.ink_annotation_requested.connect(
            self.on_ink_annotation_requested
        )
        self.annotation_tab.delete_annotation_requested.connect(
            self.on_delete_annotation_requested
        )
        
    def on_text_annotation_requested(self, color, text):
        """Handle text annotation request."""
        self.parent().preview.start_text_annotation(color, text)
        
    def on_highlight_annotation_requested(self, color):
        """Handle highlight annotation request."""
        self.parent().preview.start_highlight_annotation(color)
        
    def on_ink_annotation_requested(self, color, width):
        """Handle ink annotation request."""
        self.parent().preview.start_ink_annotation(color, width)
        
    def on_delete_annotation_requested(self):
        """Handle delete annotation request."""
        self.parent().on_delete_annotation()
