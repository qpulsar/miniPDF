"""
Menu system for the PDF Editor.
"""
from PyQt6.QtWidgets import QMenuBar, QMenu, QMessageBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from .utils.icon_utils import IconProvider

class MenuBar(QMenuBar):
    """Main menu bar for the application."""
    
    def __init__(self, parent=None):
        """Initialize menu bar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        
        # Create menus
        self.create_file_menu()
        self.create_page_menu()
        self.create_edit_menu()
        self.create_tools_menu()
        self.create_view_menu()
        self.create_help_menu()
        
    def create_file_menu(self):
        """Create file menu."""
        file_menu = QMenu("&File", self)
        
        # Open PDF
        open_action = QAction(IconProvider.get_icon("open"), "Open PDF...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.parent.on_open)
        file_menu.addAction(open_action)
        
        # Save PDF
        save_action = QAction(IconProvider.get_icon("save"), "Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.parent.on_save)
        file_menu.addAction(save_action)
        
        # Save As
        save_as_action = QAction(IconProvider.get_icon("save_as"), "Save As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.parent.on_save_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Print
        print_action = QAction(IconProvider.get_icon("print"), "Print...", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.parent.on_print)
        file_menu.addAction(print_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction(IconProvider.get_icon("exit"), "Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)
        
        self.addMenu(file_menu)
        
    def create_page_menu(self):
        """Create page menu."""
        page_menu = QMenu("&Page", self)
        
        # Add Page
        add_page_action = QAction(IconProvider.get_icon("add"), "Add Page...", self)
        add_page_action.triggered.connect(self.parent.on_add_page)
        page_menu.addAction(add_page_action)
        
        # Delete Page
        delete_page_action = QAction(IconProvider.get_icon("delete"), "Delete Page", self)
        delete_page_action.triggered.connect(self.parent.on_delete_page)
        page_menu.addAction(delete_page_action)
        
        page_menu.addSeparator()
        
        # Rotate submenu
        rotate_menu = QMenu("Rotate", self)
        rotate_menu.setIcon(IconProvider.get_icon("rotate"))
        
        rotate_left_action = QAction("Rotate Left", self)
        rotate_left_action.triggered.connect(lambda: self.parent.on_rotate_page(-90))
        rotate_menu.addAction(rotate_left_action)
        
        rotate_right_action = QAction("Rotate Right", self)
        rotate_right_action.triggered.connect(lambda: self.parent.on_rotate_page(90))
        rotate_menu.addAction(rotate_right_action)
        
        rotate_180_action = QAction("Rotate 180°", self)
        rotate_180_action.triggered.connect(lambda: self.parent.on_rotate_page(180))
        rotate_menu.addAction(rotate_180_action)
        
        page_menu.addMenu(rotate_menu)
        
        # Move Page
        move_page_action = QAction(IconProvider.get_icon("move"), "Move Page", self)
        move_page_action.triggered.connect(self.parent.on_move_page)
        page_menu.addAction(move_page_action)
        
        # Export Page
        export_page_action = QAction(IconProvider.get_icon("export"), "Export Page...", self)
        export_page_action.triggered.connect(self.parent.on_export_page)
        page_menu.addAction(export_page_action)
        
        self.addMenu(page_menu)
        
    def create_edit_menu(self):
        """Create edit menu."""
        edit_menu = QMenu("&Edit", self)
        
        # Add Text
        add_text_action = QAction(IconProvider.get_icon("text"), "Add Text", self)
        add_text_action.triggered.connect(self.parent.on_add_text)
        edit_menu.addAction(add_text_action)
        
        # Draw
        draw_action = QAction(IconProvider.get_icon("draw"), "Draw", self)
        draw_action.triggered.connect(self.parent.on_draw)
        edit_menu.addAction(draw_action)
        
        # Highlight
        highlight_action = QAction(IconProvider.get_icon("highlight"), "Highlight", self)
        highlight_action.triggered.connect(self.parent.on_highlight)
        edit_menu.addAction(highlight_action)
        
        edit_menu.addSeparator()
        
        # Delete Annotation
        delete_annotation_action = QAction(IconProvider.get_icon("delete"), "Delete Annotation", self)
        delete_annotation_action.triggered.connect(self.parent.on_delete_annotation)
        edit_menu.addAction(delete_annotation_action)
        
        self.addMenu(edit_menu)
        
    def create_tools_menu(self):
        """Create tools menu."""
        tools_menu = QMenu("&Tools", self)
        
        # OCR
        ocr_action = QAction(IconProvider.get_icon("ocr"), "OCR Text Recognition", self)
        ocr_action.triggered.connect(self.parent.on_ocr)
        tools_menu.addAction(ocr_action)
        
        tools_menu.addSeparator()
        
        # Merge PDF
        merge_action = QAction(IconProvider.get_icon("merge"), "Merge PDFs...", self)
        merge_action.triggered.connect(self.parent.on_merge)
        tools_menu.addAction(merge_action)
        
        # Split PDF
        split_action = QAction(IconProvider.get_icon("split"), "Split PDF...", self)
        split_action.triggered.connect(self.parent.on_split)
        tools_menu.addAction(split_action)
        
        tools_menu.addSeparator()
        
        # Encrypt PDF
        encrypt_action = QAction(IconProvider.get_icon("lock"), "Encrypt PDF...", self)
        encrypt_action.triggered.connect(self.parent.on_encrypt)
        tools_menu.addAction(encrypt_action)
        
        # Decrypt PDF
        decrypt_action = QAction(IconProvider.get_icon("unlock"), "Remove Password...", self)
        decrypt_action.triggered.connect(self.parent.on_decrypt)
        tools_menu.addAction(decrypt_action)
        
        self.addMenu(tools_menu)
        
    def create_view_menu(self):
        """Create view menu."""
        view_menu = QMenu("&View", self)
        
        # Zoom submenu
        zoom_menu = QMenu("Zoom", self)
        zoom_menu.setIcon(IconProvider.get_icon("zoom"))
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(self.parent.on_zoom_in)
        zoom_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(self.parent.on_zoom_out)
        zoom_menu.addAction(zoom_out_action)
        
        zoom_menu.addSeparator()
        
        fit_width_action = QAction("Fit Width", self)
        fit_width_action.triggered.connect(self.parent.on_fit_width)
        zoom_menu.addAction(fit_width_action)
        
        view_menu.addMenu(zoom_menu)
        
        # Page Layout submenu
        layout_menu = QMenu("Page Layout", self)
        layout_menu.setIcon(IconProvider.get_icon("layout"))
        
        single_page_action = QAction("Single Page", self)
        single_page_action.setCheckable(True)
        single_page_action.setChecked(True)
        single_page_action.triggered.connect(lambda: self.parent.on_page_layout("single"))
        layout_menu.addAction(single_page_action)
        
        double_page_action = QAction("Double Page", self)
        double_page_action.setCheckable(True)
        double_page_action.triggered.connect(lambda: self.parent.on_page_layout("double"))
        layout_menu.addAction(double_page_action)
        
        view_menu.addMenu(layout_menu)
        
        view_menu.addSeparator()
        
        # Theme submenu
        theme_menu = QMenu("Theme", self)
        theme_menu.setIcon(IconProvider.get_icon("theme"))
        
        light_theme_action = QAction("Light", self)
        light_theme_action.setCheckable(True)
        light_theme_action.setChecked(True)
        light_theme_action.triggered.connect(lambda: self.parent.on_theme("light"))
        theme_menu.addAction(light_theme_action)
        
        dark_theme_action = QAction("Dark", self)
        dark_theme_action.setCheckable(True)
        dark_theme_action.triggered.connect(lambda: self.parent.on_theme("dark"))
        theme_menu.addAction(dark_theme_action)
        
        view_menu.addMenu(theme_menu)
        
        self.addMenu(view_menu)
        
    def create_help_menu(self):
        """Create help menu."""
        help_menu = QMenu("&Help", self)
        
        # Help
        help_action = QAction(IconProvider.get_icon("help"), "Help", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        # About
        about_action = QAction(IconProvider.get_icon("about"), "About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Feedback
        feedback_action = QAction(IconProvider.get_icon("feedback"), "Send Feedback", self)
        feedback_action.triggered.connect(self.show_feedback)
        help_menu.addAction(feedback_action)
        
        self.addMenu(help_menu)
        
    def show_help(self):
        """Show help dialog."""
        QMessageBox.information(
            self,
            "Help",
            "Keyboard Shortcuts:\n\n"
            "Ctrl+O - Open PDF\n"
            "Ctrl+S - Save PDF\n"
            "Ctrl+Shift+S - Save As\n"
            "Ctrl+P - Print\n"
            "Ctrl+Q - Exit\n"
            "Ctrl++ - Zoom In\n"
            "Ctrl+- - Zoom Out\n"
            "F1 - Help"
        )
        
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About miniPDF",
            "miniPDF Editor\n\n"
            "Version: 2.0.0\n"
            "A simple PDF editor built with PyQt6\n\n"
            "© 2025 miniPDF Team"
        )
        
    def show_feedback(self):
        """Show feedback dialog."""
        QMessageBox.information(
            self,
            "Feedback",
            "Please send your feedback to:\n"
            "feedback@minipdf.com"
        )
