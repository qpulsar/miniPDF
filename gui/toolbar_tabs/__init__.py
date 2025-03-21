"""
Toolbar tabs package for the miniPDF application.
"""
from gui.toolbar_tabs.file_tab import FileTab
from gui.toolbar_tabs.page_tab import PageTab
from gui.toolbar_tabs.edit_tab import EditTab
from gui.toolbar_tabs.tools_tab import ToolsTab
from gui.toolbar_tabs.view_tab import ViewTab
from gui.toolbar_tabs.help_tab import HelpTab

__all__ = [
    'FileTab',
    'PageTab',
    'EditTab',
    'ToolsTab',
    'ViewTab',
    'HelpTab'
]
