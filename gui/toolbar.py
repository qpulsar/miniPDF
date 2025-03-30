"""
Toolbar module for the PDF Editor application.
This is the main toolbar class that uses the modular tab implementations.
"""
from PyQt6.QtWidgets import QToolBar, QTabWidget, QWidget
from PyQt6.QtGui import QIcon
import qt_material
import os
from gui.toolbar_style import apply_toolbar_style
from gui.toolbar_tabs import FileTab, PageTab, EditTab, ToolsTab, ViewTab, HelpTab

class Toolbar(QToolBar):
    """Toolbar widget with MS Office-style ribbon interface for PDF operations."""
    
    def __init__(self, parent):
        """Initialize the toolbar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.app = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Setup toolbar UI and actions."""
        # Create the main notebook for the ribbon
        self.ribbon = QTabWidget()
        self.ribbon.setTabsClosable(False)
        
        # Create tabs for each category
        self.file_tab = QWidget()
        self.page_tab = QWidget()
        self.edit_tab = QWidget()
        self.tools_tab = QWidget()
        self.view_tab = QWidget()
        self.help_tab = QWidget()
        
        # Add tabs to the notebook
        self.ribbon.addTab(self.file_tab, "Dosya")
        self.ribbon.addTab(self.page_tab, "Sayfa")
        self.ribbon.addTab(self.edit_tab, "Düzenleme")
        self.ribbon.addTab(self.tools_tab, "Araçlar")
        self.ribbon.addTab(self.view_tab, "Görüntüleme")
        self.ribbon.addTab(self.help_tab, "Yardım")
        
        # Initialize all ribbon tabs with their respective classes
        self.file_tab_controller = FileTab(self.file_tab, self.app)
        self.page_tab_controller = PageTab(self.page_tab, self.app)
        self.edit_tab_controller = EditTab(self.edit_tab, self.app)
        self.tools_tab_controller = ToolsTab(self.tools_tab, self.app)
        self.view_tab_controller = ViewTab(self.view_tab, self.app)
        self.help_tab_controller = HelpTab(self.help_tab, self.app)
        
        # Open PDF action
        self.open_action = QAction(QIcon.fromTheme("document-open"), "Open PDF", self)
        self.open_action.setStatusTip("Open a PDF file")
        self.open_action.triggered.connect(self.app.open_pdf)
        self.addAction(self.open_action)
        
        # Save PDF action
        self.save_action = QAction(QIcon.fromTheme("document-save"), "Save", self)
        self.save_action.setStatusTip("Save the current PDF")
        self.save_action.triggered.connect(self.app.save_pdf)
        self.addAction(self.save_action)
        
        # Save As action
        self.save_as_action = QAction(QIcon.fromTheme("document-save-as"), "Save As", self)
        self.save_as_action.setStatusTip("Save the PDF with a new name")
        self.save_as_action.triggered.connect(self.app.save_pdf_as)
        self.addAction(self.save_as_action)
        
        self.addSeparator()
        
        # Delete page action
        self.delete_page_action = QAction(QIcon.fromTheme("edit-delete"), "Delete Page", self)
        self.delete_page_action.setStatusTip("Delete the current page")
        self.delete_page_action.triggered.connect(self.app.delete_current_page)
        self.addAction(self.delete_page_action)
        
        self.addSeparator()
        
        # Reload PDF action
        self.reload_action = QAction(QIcon.fromTheme("view-refresh"), "Reload", self)
        self.reload_action.setStatusTip("Reload the current PDF")
        self.reload_action.triggered.connect(self.app.reload_pdf)
        self.addAction(self.reload_action)
