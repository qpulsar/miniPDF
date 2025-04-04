"""
Main application window for miniPDF.
"""
import sys
import os
import json
import logging
from qt_material import list_themes, apply_stylesheet
import tempfile
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QMessageBox, QStatusBar, QLabel,
                             QPushButton, QToolBar, QFrame, QSplitter,
                             QGridLayout, QComboBox, QApplication, QInputDialog)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from core.pdf_manager import PDFManager
from core.annotation import PDFAnnotator
from core.extractions import TextExtractor
from core.merge_split import PDFMergeSplit
from core.security import PDFSecurity
from .utils.icon_utils import IconProvider
from .utils.settings_utils import (
    get_available_themes, toggle_theme, is_dark_theme, get_setting
)
from .utils.settings_manager import (
    initialize_app_settings, change_theme, update_zoom_level,
    update_sidebar_width, save_all_settings
)
from .preview import PDFPreview
from .sidebar import Sidebar
from .settings import Settings

settings = Settings()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class App(QMainWindow):
    """Main application window for miniPDF."""

    # Signal emitted when theme is changed
    theme_changed = pyqtSignal()

    def __init__(self):
        """Initialize the application window."""
        super().__init__()

        # Initialize PDF manager
        self.pdf_manager = PDFManager()

        # Initialize theme-related attributes
        self.current_theme = ""
        self.theme_combo = None

        # Setup UI
        self.setup_ui()
        
        # Apply all saved settings (theme, zoom, sidebar width, etc.)
        initialize_app_settings(self)

    # Bu metod artık kullanılmıyor, tüm ayarlar settings_utils üzerinden yönetiliyor

    def setup_ui(self):
        """Setup the user interface."""
        # Ana uygulamaya setStyleSheet uygulamıyoruz, qt_material'in kendi stillerini kullanabilmesi için

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create menu toolbar with action groups
        self.create_menu_toolbar()

        # Create content splitter for sidebar and preview
        self.content_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.content_splitter)

        # Add sidebar to left
        self.sidebar = Sidebar(self)
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(300)
        self.content_splitter.addWidget(self.sidebar)

        # Add preview to right
        self.preview = PDFPreview(self)
        self.content_splitter.addWidget(self.preview)

        # Set splitter proportions
        self.content_splitter.setSizes([1, 3])

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Connect sidebar signals
        self.sidebar.page_selected.connect(self.preview.show_page)

    def create_menu_toolbar(self):
        """Create the menu toolbar with action groups (title above, buttons below)."""
        # Create container widget for the toolbar content
        menu_widget = QWidget()
        menu_layout = QHBoxLayout(menu_widget)
        menu_layout.setContentsMargins(5, 2, 5, 2)
        menu_layout.setSpacing(5)

        # Define actions for each group
        file_actions = [
            # text, slot, function, row, column
            ("Open", "open", self.open_pdf, 0, 0),
            ("Save", "save", self.save_pdf, 0, 1),
            ("Save As", "save_as", self.save_pdf_as, 0, 2),
            ("Close", "exit", self.close_pdf, 1, 0),
            ("Print", "print", self.print_pdf, 1, 1)
        ]
        page_actions = [
            ("Add Page", "add", self.add_page, 0, 0),
            ("Delete Page", "delete", self.delete_page, 0, 1),
            ("Extract Page", "export", self.extract_page, 0, 2),
            ("Rotate Right", "rotate", lambda: self.rotate_page(90), 1, 0),
            ("Rotate Left", "rotate", lambda: self.rotate_page(-90), 1, 1),
            ("Rotate 180", "rotate", lambda: self.rotate_page(180), 1, 2)
        ]
        view_actions = [
            ("Zoom In", "zoom", self.zoom_in, 0, 0),
            ("Zoom Out", "zoom", self.zoom_out, 0, 1),
            ("Fit Page", "layout", self.fit_page, 0, 2),
            ("Fit Width", "layout", self.fit_width, 0, 3),
        ]
        edit_actions = [
            ("Add Text", "text", self.add_text, 0, 0),
            ("Draw Line", "draw", self.draw_line, 0, 1),
            ("Draw Circle", "draw", self.draw_circle, 0, 2),
            ("Highlight", "highlight", self.highlight_text, 1, 0),
            ("Erase", "delete", self.erase_annotation, 1, 1),
            ("Clear", "delete", self.clear_annotations, 1, 2)
        ]

        # Create and add action groups
        menu_layout.addWidget(self.create_action_group("File", file_actions))
        self.add_layout_separator(menu_layout)
        menu_layout.addWidget(self.create_action_group("Page", page_actions))
        self.add_layout_separator(menu_layout)

        # Create View group with theme controls
        view_group = self.create_view_group(view_actions)
        menu_layout.addWidget(view_group)
        self.add_layout_separator(menu_layout)

        menu_layout.addWidget(self.create_action_group("Edit", edit_actions))

        menu_layout.addStretch()

        # Add menu widget to a toolbar
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.create_toolbar_from_widget(menu_widget))

    def create_view_group(self, actions):
        """Create View group with theme controls."""
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        # Title
        title = QLabel("View")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Buttons grid
        buttons_widget = QWidget()
        buttons_layout = QGridLayout()
        buttons_layout.setContentsMargins(5, 5, 5, 5)
        buttons_layout.setVerticalSpacing(5)
        buttons_widget.setLayout(buttons_layout)

        # Add buttons for actions
        for text, icon_name, slot, row, col in actions:
            btn = QPushButton()
            btn.setIcon(IconProvider.get_icon(icon_name))
            btn.setIconSize(QSize(20, 20))
            btn.setToolTip(text)
            btn.clicked.connect(slot)
            btn.setFixedSize(QSize(32, 32))
            buttons_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create theme combo box
        self.theme_combo = QComboBox()
        self.theme_combo.setFixedWidth(140)
        self.theme_combo.setMinimumHeight(28)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid palette(mid);
                border-radius: 4px;
                padding: 2px 4px;
                height: 28px;
            }
            QComboBox::drop-down {
                border: 1px solid palette(mid);
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(:/icons/down_arrow.png);
                width: 12px;
                height: 10px;
            }
            QComboBox:hover {
                border-color: palette(highlight);
            }
            QComboBox:focus {
                border-color: palette(highlight);
                border-width: 2px;
            }
        """)

        # Kullanılabilir temaları settings_utils'den al
        theme_dict = get_available_themes()
        logger.debug(f"Available themes: {theme_dict}")

        # Temaları combobox'a ekle
        for theme, display_name in theme_dict.items():
            self.theme_combo.addItem(display_name, theme)
            logger.debug(f"Added theme: {display_name} -> {theme}")

        # Theme dropdown
        self.theme_combo.setToolTip("Select Theme")
        buttons_layout.addWidget(self.theme_combo, 1, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)

        # Theme toggle button
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setIcon(IconProvider.get_icon("theme"))
        self.theme_toggle_btn.setIconSize(QSize(20, 20))
        self.theme_toggle_btn.setToolTip("Toggle Dark/Light Mode")
        self.theme_toggle_btn.clicked.connect(self.toggle_dark_light)
        self.theme_toggle_btn.setFixedSize(QSize(32, 32))
        buttons_layout.addWidget(self.theme_toggle_btn, 1, 3, alignment=Qt.AlignmentFlag.AlignBottom)

        layout.addWidget(buttons_widget)

        # Connect theme change signal AFTER adding to layout
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        logger.debug("Theme combo signal connected")

        return container

    def change_theme(self, index):
        """Change the application theme."""
        logger.debug(f"change_theme called with index: {index}")

        if index < 0:
            logger.debug("Invalid index, returning")
            return

        selected_theme = self.theme_combo.itemData(index)
        logger.debug(f"Selected theme: {selected_theme}")

        if selected_theme == self.current_theme:
            logger.debug("Theme unchanged, returning")
            return

        self.current_theme = selected_theme
        logger.debug(f"Current theme set to: {self.current_theme}")

        # Merkezi tema değiştirme fonksiyonunu kullan
        success = change_theme(self, selected_theme)
        
        if success:
            # Status bar'ı güncelle
            self.status_bar.showMessage(f"Tema değiştirildi: {self.theme_combo.itemText(index)}")
            logger.debug(f"Theme applied successfully: {selected_theme}")
        else:
            logger.error(f"Failed to apply theme: {selected_theme}")
            self.status_bar.showMessage("Tema değiştirilemedi!")


    def toggle_dark_light(self):
        """Toggle between dark and light mode."""
        logger.debug("toggle_dark_light called")
        
        # Tema değişimini yap
        new_theme = toggle_theme()
        logger.debug(f"New theme after toggle: {new_theme}")
        
        # ComboBox'ta yeni temayı seç
        for i in range(self.theme_combo.count()):
            theme_data = self.theme_combo.itemData(i)
            if theme_data == new_theme:
                logger.debug(f"Found matching theme at index {i}")
                self.theme_combo.setCurrentIndex(i)
                break

    def update_theme_combo(self):
        """ComboBox'ta kaydedilmiş temayı seç"""
        saved_theme = get_setting('theme')
        logger.debug(f"Updating theme combo to: {saved_theme}")
        
        if saved_theme and self.theme_combo:
            self.current_theme = saved_theme
            
            # ComboBox'ta kaydedilmiş temayı seç
            for i in range(self.theme_combo.count()):
                theme_data = self.theme_combo.itemData(i)
                if theme_data == saved_theme:
                    logger.debug(f"Found saved theme at index {i}")
                    self.theme_combo.setCurrentIndex(i)
                    break

    # Bu metod artık kullanılmıyor, tüm ayarlar settings_utils üzerinden kaydediliyor

    def create_action_group(self, title, actions):
        """Create a widget representing an action group.

        Args:
            title (str): The title of the group.
            actions (list): List of tuples (text, icon_name, slot).

        Returns:
            QWidget: The container widget for the action group.
        """
        group_container = QWidget()
        group_container.setObjectName("action-group-container")
        group_layout = QVBoxLayout(group_container)
        group_layout.setContentsMargins(2, 2, 2, 2)
        group_layout.setSpacing(1)

        # Add group title
        label = QLabel(title)
        label.setObjectName("group-header")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        group_layout.addWidget(label)

        # Create widget and layout for buttons
        buttons_widget = QWidget()
        buttons_widget.setObjectName("buttons-widget")
        buttons_layout = QGridLayout()
        buttons_widget.setLayout(buttons_layout)

        # Add action buttons to the grid (max 3 columns for better fit)
        max_cols = 3
        for i, (text, icon_name, slot, row, col) in enumerate(actions):
            button = QPushButton()
            button.setIcon(IconProvider.get_icon(icon_name))
            button.setIconSize(QSize(20, 20))
            button.setToolTip(text)
            button.clicked.connect(slot)
            button.setFixedSize(QSize(32, 32))
            row = i // max_cols
            col = i % max_cols
            buttons_layout.addWidget(button, row, col)

        group_layout.addWidget(buttons_widget)

        return group_container

    def create_toolbar_from_widget(self, widget):
        """Create a toolbar containing the given widget.

        Args:
            widget: Widget to add to toolbar

        Returns:
            QToolBar: Toolbar containing the widget
        """
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.addWidget(widget)

        return toolbar

    def add_layout_separator(self, layout):
        """Add a vertical separator to the given QHBoxLayout.

        Args:
            layout: QHBoxLayout to add separator to
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setFixedWidth(1)
        layout.addWidget(separator)

    # File actions
    def open_pdf(self):
        """Open a PDF file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open PDF File",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )

        if file_path:
            if self.pdf_manager.open_pdf(file_path):
                self.sidebar.update_pages()
                if self.pdf_manager.get_page_count() > 0:
                    self.preview.show_page(0)
                self.status_bar.showMessage(f"Opened {os.path.basename(file_path)}")
            else:
                QMessageBox.critical(self, "Error", "Failed to open PDF file.")

    def save_pdf(self):
        """Save the current PDF file."""
        if not self.pdf_manager.doc:
            return

        if self.pdf_manager.file_path:
            if self.pdf_manager.save_pdf():
                self.status_bar.showMessage("PDF saved successfully")
            else:
                QMessageBox.critical(self, "Error", "Failed to save PDF file.")
        else:
            self.save_pdf_as()

    def save_pdf_as(self):
        """Save the PDF file with a new name."""
        if not self.pdf_manager.doc:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF As",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )

        if file_path:
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'

            if self.pdf_manager.save_pdf(file_path):
                self.status_bar.showMessage(f"PDF saved as {os.path.basename(file_path)}")
            else:
                QMessageBox.critical(self, "Error", "Failed to save PDF file.")

    def close_pdf(self):
        """Close the current PDF file."""
        if self.pdf_manager.doc:
            self.pdf_manager.close()
            self.sidebar.clear()
            self.preview.clear()
            self.status_bar.showMessage("PDF closed")

    def print_pdf(self):
        """Print the current PDF file."""
        if not self.pdf_manager.doc:
            return

        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)
            
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Create a temporary PDF file with current state
                temp_fd, temp_path = tempfile.mkstemp(suffix=".pdf")
                os.close(temp_fd)
                
                if self.pdf_manager.save_pdf(temp_path):
                    # Use system's default PDF viewer for printing
                    if sys.platform == 'darwin':  # macOS
                        os.system(f"open -a 'Preview' {temp_path}")
                    elif sys.platform == 'win32':  # Windows
                        os.startfile(temp_path, 'print')
                    else:  # Linux
                        os.system(f"xdg-open {temp_path}")
                    
                    self.status_bar.showMessage("Document sent to printer")
                else:
                    QMessageBox.critical(self, "Error", "Failed to prepare document for printing")
                
                # Clean up temp file after a delay
                def cleanup_temp():
                    try:
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                    except:
                        pass
                
                # Schedule cleanup after 60 seconds
                QTimer.singleShot(60000, cleanup_temp)
        except Exception as e:
            QMessageBox.critical(self, "Print Error", f"Error during printing: {str(e)}")

    # Page actions
    def add_page(self):
        """Add a blank page to the PDF."""
        if not self.pdf_manager.doc:
            return

        try:
            # Create a blank page with PyMuPDF
            page = self.pdf_manager.doc.new_page(-1, width=595, height=842)  # A4 size in points
            
            if page:
                self.sidebar.update_pages()
                new_page_num = self.pdf_manager.get_page_count() - 1
                self.preview.show_page(new_page_num)
                self.status_bar.showMessage("Blank page added")
            else:
                QMessageBox.critical(self, "Error", "Failed to add blank page")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add blank page: {str(e)}")

    def delete_page(self):
        """Delete the current page from the PDF."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        if self.pdf_manager.delete_page(self.preview.current_page):
            self.sidebar.update_pages()
            if self.preview.current_page >= self.pdf_manager.get_page_count():
                self.preview.show_page(self.pdf_manager.get_page_count() - 1)
            else:
                self.preview.show_page(self.preview.current_page)
            self.status_bar.showMessage("Page deleted")
        else:
            QMessageBox.critical(self, "Error", "Failed to delete page.")

    def extract_page(self):
        """Extract the current page to a new PDF file."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Extracted Page As",
            "",
            "PDF Files (*.pdf);;All Files (*.*)"
        )

        if file_path:
            if not file_path.lower().endswith('.pdf'):
                file_path += '.pdf'

            # Create PDFMergeSplit instance
            merge_split = PDFMergeSplit()
            
            # Extract the current page
            if merge_split.extract_pages(
                self.pdf_manager.file_path,
                file_path,
                [self.preview.current_page]
            ):
                self.status_bar.showMessage(f"Page extracted to {os.path.basename(file_path)}")
            else:
                QMessageBox.critical(self, "Error", "Failed to extract page.")

    def rotate_page(self, angle):
        """Rotate the current page by the specified angle.

        Args:
            angle: Rotation angle in degrees
        """
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        try:
            # Get the current page
            page = self.pdf_manager.get_page(self.preview.current_page)
            if page:
                # Rotate the page
                page.set_rotation(page.rotation + angle)
                
                # Update the view
                self.preview.show_page(self.preview.current_page)
                self.sidebar.update_thumbnail(self.preview.current_page)
                self.status_bar.showMessage(f"Page rotated by {angle} degrees")
            else:
                QMessageBox.critical(self, "Error", "Failed to rotate page.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rotate page: {str(e)}")

    # View actions
    def zoom_in(self):
        """Zoom in on the current page."""
        if self.preview.current_page is not None:
            self.preview.zoom_in()
            # Merkezi zoom güncelleme fonksiyonunu kullan
            zoom_level = int(self.preview.current_zoom * 100)
            update_zoom_level(self, zoom_level)

    def zoom_out(self):
        """Zoom out on the current page."""
        if self.preview.current_page is not None:
            self.preview.zoom_out()
            # Merkezi zoom güncelleme fonksiyonunu kullan
            zoom_level = int(self.preview.current_zoom * 100)
            update_zoom_level(self, zoom_level)

    def fit_page(self):
        """Fit the current page to the view."""
        if self.preview.current_page is not None:
            self.preview.fit_page()
            # Merkezi zoom güncelleme fonksiyonunu kullan
            zoom_level = int(self.preview.current_zoom * 100)
            update_zoom_level(self, zoom_level)

    def fit_width(self):
        """Fit the current page width to the view."""
        if self.preview.current_page is not None:
            self.preview.fit_width()
            # Merkezi zoom güncelleme fonksiyonunu kullan
            zoom_level = int(self.preview.current_zoom * 100)
            update_zoom_level(self, zoom_level)

    # Edit actions
    def add_text(self):
        """Add text annotation to the current page."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        # Get text from user
        text, ok = QInputDialog.getText(
            self,
            "Add Text Annotation",
            "Enter text for annotation:"
        )

        if ok and text:
            # Get the current page
            page = self.pdf_manager.get_page(self.preview.current_page)
            
            if page:
                # Create a PDFAnnotator instance
                annotator = PDFAnnotator()
                
                # Get position from center of the page
                rect = page.rect
                position = ((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2)
                
                # Add the text annotation
                if annotator.create_note_at_position(page, position, text):
                    # Update the view
                    self.preview.show_page(self.preview.current_page)
                    self.status_bar.showMessage("Text annotation added")
                else:
                    QMessageBox.critical(self, "Error", "Failed to add text annotation.")
            else:
                QMessageBox.critical(self, "Error", "Failed to get page.")

    def draw_line(self):
        """Draw line on the current page."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        # Show message about enabling drawing mode
        QMessageBox.information(
            self,
            "Draw Line",
            "Line drawing mode will be implemented in the preview widget.\n"
            "For now, we'll add a sample line to demonstrate the functionality."
        )
        
        # Get the current page
        page = self.pdf_manager.get_page(self.preview.current_page)
        
        if page:
            # Create a PDFAnnotator instance
            annotator = PDFAnnotator()
            
            # Get page dimensions
            rect = page.rect
            
            # Create sample line points (diagonal across the page)
            start_point = (rect.x0 + 100, rect.y0 + 100)
            end_point = (rect.x1 - 100, rect.y1 - 100)
            
            # Add the line annotation
            if annotator.add_line(page, start_point, end_point, width=2.0):
                # Update the view
                self.preview.show_page(self.preview.current_page)
                self.status_bar.showMessage("Line annotation added")
            else:
                QMessageBox.critical(self, "Error", "Failed to add line annotation.")
        else:
            QMessageBox.critical(self, "Error", "Failed to get page.")

    def draw_circle(self):
        """Draw circle on the current page."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        # Show message about enabling drawing mode
        QMessageBox.information(
            self,
            "Draw Circle",
            "Circle drawing mode will be implemented in the preview widget.\n"
            "For now, we'll add a sample circle to demonstrate the functionality."
        )
        
        # Get the current page
        page = self.pdf_manager.get_page(self.preview.current_page)
        
        if page:
            # Create a PDFAnnotator instance
            annotator = PDFAnnotator()
            
            # Get page dimensions
            rect = page.rect
            
            # Create sample circle (centered on the page)
            center_x = (rect.x0 + rect.x1) / 2
            center_y = (rect.y0 + rect.y1) / 2
            radius = min((rect.x1 - rect.x0), (rect.y1 - rect.y0)) / 4
            
            circle_rect = (
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius
            )
            
            # Add the rectangle annotation (PyMuPDF doesn't have a direct circle annotation)
            if annotator.add_rectangle(page, circle_rect, width=2.0):
                # Update the view
                self.preview.show_page(self.preview.current_page)
                self.status_bar.showMessage("Circle annotation added")
            else:
                QMessageBox.critical(self, "Error", "Failed to add circle annotation.")
        else:
            QMessageBox.critical(self, "Error", "Failed to get page.")

    def highlight_text(self):
        """Highlight text on the current page."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        # Show message about text selection for highlighting
        QMessageBox.information(
            self,
            "Highlight Text",
            "Text selection for highlighting will be implemented in the preview widget.\n"
            "For now, we'll highlight a sample area to demonstrate the functionality."
        )
        
        # Get the current page
        page = self.pdf_manager.get_page(self.preview.current_page)
        
        if page:
            # Create a PDFAnnotator instance
            annotator = PDFAnnotator()
            
            # Get page dimensions
            rect = page.rect
            
            # Create sample highlight area (middle of the page)
            highlight_rect = (
                rect.x0 + (rect.x1 - rect.x0) * 0.25,
                rect.y0 + (rect.y1 - rect.y0) * 0.45,
                rect.x0 + (rect.x1 - rect.x0) * 0.75,
                rect.y0 + (rect.y1 - rect.y0) * 0.55
            )
            
            # Add the highlight annotation
            if annotator.add_highlight(page, highlight_rect, color=(1, 1, 0)):
                # Update the view
                self.preview.show_page(self.preview.current_page)
                self.status_bar.showMessage("Highlight annotation added")
            else:
                QMessageBox.critical(self, "Error", "Failed to add highlight annotation.")
        else:
            QMessageBox.critical(self, "Error", "Failed to get page.")

    def erase_annotation(self):
        """Erase annotation from the current page."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        # Get the current page
        page = self.pdf_manager.get_page(self.preview.current_page)
        
        if page:
            # Create a PDFAnnotator instance
            annotator = PDFAnnotator()
            
            # Get annotations on the page
            annotations = annotator.get_annotations(page)
            
            if annotations:
                # Delete the last annotation
                if annotator.delete_annotation(page, len(annotations) - 1):
                    # Update the view
                    self.preview.show_page(self.preview.current_page)
                    self.status_bar.showMessage("Last annotation erased")
                else:
                    QMessageBox.critical(self, "Error", "Failed to erase annotation.")
            else:
                QMessageBox.information(self, "No Annotations", "No annotations found on this page.")
        else:
            QMessageBox.critical(self, "Error", "Failed to get page.")

    def clear_annotations(self):
        """Clear all annotations from the current page."""
        if not self.pdf_manager.doc or self.preview.current_page is None:
            return

        # Get the current page
        page = self.pdf_manager.get_page(self.preview.current_page)
        
        if page:
            # Create a PDFAnnotator instance
            annotator = PDFAnnotator()
            
            # Get annotations on the page
            annotations = annotator.get_annotations(page)
            
            if annotations:
                # Delete all annotations
                success = True
                for i in range(len(annotations) - 1, -1, -1):
                    if not annotator.delete_annotation(page, i):
                        success = False
                
                # Update the view
                self.preview.show_page(self.preview.current_page)
                
                if success:
                    self.status_bar.showMessage("All annotations cleared")
                else:
                    self.status_bar.showMessage("Some annotations could not be cleared")
            else:
                QMessageBox.information(self, "No Annotations", "No annotations found on this page.")
        else:
            QMessageBox.critical(self, "Error", "Failed to get page.")
