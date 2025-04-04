"""
Sidebar implementation for miniPDF.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QListWidgetItem, QToolButton,
                             QLabel, QFrame, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QEvent
from PyQt6.QtGui import QPixmap, QIcon
from .utils.icon_utils import IconProvider
from .utils.settings_utils import (
    apply_theme_to_widget, apply_button_styles,
    save_sidebar_width, load_sidebar_width
)
from .settings import Settings

settings = Settings()

class Sidebar(QWidget):
    """Sidebar widget for displaying page thumbnails and navigation."""
    
    # Signal emitted when page is selected
    page_selected = pyqtSignal(int)
    
    def __init__(self, parent=None):
        """Initialize sidebar.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.app = parent
        self.settings = Settings()
        
        # Set up layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create navigation buttons at the top
        self.create_navigation_buttons()
        
        # Create page list
        self.create_page_list()
        
        # Create page movement buttons at the bottom
        self.create_page_movement_buttons()
        
        # Uygulama başlangıcında tema ve ayarları uygula
        self.apply_theme()
        
        # Connect theme change signal
        if parent:
            parent.theme_changed.connect(self.apply_theme)
        
        # Yüklenen genişliği uygula (settings_utils kullanarak)
        saved_width = load_sidebar_width()
        if saved_width > 0:
            self.setMinimumWidth(saved_width)
            self.setMaximumWidth(saved_width)
        
        # Genişlik değişikliklerini izle
        self.installEventFilter(self)
        
    def create_navigation_buttons(self):
        """Create navigation buttons at the top of the sidebar."""
        # Create container for navigation buttons
        nav_container = QWidget()
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(5)
        
        # Create navigation buttons
        self.first_page_button = self.create_tool_button("İlk Sayfa", "first_page", 
                                                       lambda: self.go_to_page(0))
        self.prev_page_button = self.create_tool_button("Önceki Sayfa", "prev_page", 
                                                      self.go_to_prev_page)
        self.next_page_button = self.create_tool_button("Sonraki Sayfa", "next_page", 
                                                      self.go_to_next_page)
        self.last_page_button = self.create_tool_button("Son Sayfa", "last_page", 
                                                      self.go_to_last_page)

        # Add buttons to layout
        nav_layout.addWidget(self.first_page_button)
        nav_layout.addWidget(self.prev_page_button)
        nav_layout.addWidget(self.next_page_button)
        nav_layout.addWidget(self.last_page_button)

        # Add container to main layout
        self.layout.addWidget(nav_container)

        # Add separator
        self.layout.addWidget(self.create_separator())
        
    def create_page_list(self):
        """Create page list widget."""
        # Create list widget for page thumbnails
        self.page_list = QListWidget()
        self.page_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.page_list.setIconSize(QSize(120, 160))
        self.page_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.page_list.setMovement(QListWidget.Movement.Static)
        self.page_list.setSpacing(10)
        self.page_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.page_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Connect signals
        self.page_list.currentRowChanged.connect(self.on_page_selected)
        
        # Add to layout
        self.layout.addWidget(self.page_list, 1)  # Give it stretch factor
        
        # Add separator
        self.layout.addWidget(self.create_separator())
        
    def create_page_movement_buttons(self):
        """Create page movement buttons at the bottom of the sidebar."""
        # Create container for movement buttons
        move_container = QWidget()
        move_layout = QHBoxLayout(move_container)
        move_layout.setContentsMargins(5, 5, 5, 5)
        move_layout.setSpacing(5)
        
        # Create movement buttons
        self.move_up_button = self.create_tool_button("Move Up", "move_up", 
                                                    self.move_page_up)
        self.move_down_button = self.create_tool_button("Move Down", "move_down", 
                                                      self.move_page_down)
        
        # Add buttons to layout
        move_layout.addWidget(self.move_up_button)
        move_layout.addWidget(self.move_down_button)
        
        # Add container to main layout
        self.layout.addWidget(move_container)
        
    def create_tool_button(self, tooltip, icon_name, slot):
        """Create a tool button.
        
        Args:
            tooltip: Button tooltip
            icon_name: Icon name
            slot: Function to call when clicked
            
        Returns:
            QPushButton: Created button
        """
        button = QPushButton()
        button.setIcon(IconProvider.get_icon(icon_name))
        button.setIconSize(QSize(24, 24))
        button.setToolTip(tooltip)
        button.setFixedSize(QSize(32, 32))
        button.clicked.connect(slot)
        return button
        
    def create_separator(self):
        """Create a horizontal separator line.
        
        Returns:
            QFrame: Separator line
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setObjectName("separator")
        return separator
        
    def update_pages(self):
        """Update page thumbnails."""
        self.page_list.clear()
        
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
                item.setText(f"Sayfa {i + 1}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.page_list.addItem(item)
                
    def update_thumbnail(self, page_num):
        """Update a specific page thumbnail.
        
        Args:
            page_num: Page number to update
        """
        if not self.app.pdf_manager.doc or page_num < 0 or page_num >= self.page_list.count():
            return
            
        # Get updated thumbnail
        pixmap = self.app.pdf_manager.get_page_thumbnail(page_num)
        if pixmap:
            # Update item
            item = self.page_list.item(page_num)
            item.setIcon(QIcon(pixmap))
            
    def on_page_selected(self, row):
        """Handle page selection.
        
        Args:
            row: Selected row index
        """
        if row >= 0:
            self.page_selected.emit(row)
            
    def go_to_page(self, page_num):
        """Go to a specific page.
        
        Args:
            page_num: Page number to go to
        """
        if not self.app.pdf_manager.doc:
            return
            
        if 0 <= page_num < self.page_list.count():
            self.page_list.setCurrentRow(page_num)
            
    def go_to_prev_page(self):
        """Go to the previous page."""
        if not self.app.pdf_manager.doc:
            return
            
        current = self.page_list.currentRow()
        if current > 0:
            self.page_list.setCurrentRow(current - 1)
            
    def go_to_next_page(self):
        """Go to the next page."""
        if not self.app.pdf_manager.doc:
            return
            
        current = self.page_list.currentRow()
        if current < self.page_list.count() - 1:
            self.page_list.setCurrentRow(current + 1)
            
    def go_to_last_page(self):
        """Go to the last page."""
        if not self.app.pdf_manager.doc:
            return
            
        if self.page_list.count() > 0:
            self.page_list.setCurrentRow(self.page_list.count() - 1)
            
    def move_page_up(self):
        """Move the current page up in the document."""
        if not self.app.pdf_manager.doc:
            return
            
        current = self.page_list.currentRow()
        if current > 0:
            # Implementation will be added later
            # For now, just show a message in the status bar
            self.app.status_bar.showMessage("Move page up functionality not implemented yet")
            
    def move_page_down(self):
        """Move the current page down in the document."""
        if not self.app.pdf_manager.doc:
            return
            
        current = self.page_list.currentRow()
        if current < self.page_list.count() - 1:
            # Implementation will be added later
            # For now, just show a message in the status bar
            self.app.status_bar.showMessage("Move page down functionality not implemented yet")
            
    def clear(self):
        """Clear the page list."""
        self.page_list.clear()
        
    def apply_theme(self):
        """Apply current theme to sidebar elements."""
        # Get theme from settings_utils instead of using get_theme method
        from .utils.settings_utils import get_setting, is_dark_theme
        
        # Get current theme
        current_theme = get_setting('theme')
        
        # Apply theme to main widget
        apply_theme_to_widget(self)
        # Apply theme to page list
        apply_theme_to_widget(self.page_list)
        
        # Apply theme styles to buttons using settings_utils helper
        apply_button_styles(self.first_page_button)
        apply_button_styles(self.prev_page_button)
        apply_button_styles(self.next_page_button)
        apply_button_styles(self.last_page_button)
        apply_button_styles(self.move_up_button)
        apply_button_styles(self.move_down_button)
        
        # Apply theme to separators
        separators = self.findChildren(QFrame, "separator")
        
        # Determine separator color based on theme
        is_dark = is_dark_theme(current_theme)
        separator_color = "#444444" if is_dark else "#cccccc"
        
        for sep in separators:
            sep.setStyleSheet(f"""
                QFrame#separator {{
                    color: {separator_color};
                    background-color: {separator_color};
                    height: 1px;
                }}
            """)
            
        # Update page list item colors if needed
        # (Currently handled by QListWidget styling, but could add specific item styling here)
        
    def eventFilter(self, obj, event):
        """Genişlik değişikliklerini izle ve kaydet.
        
        Args:
            obj: İzlenen nesne
            event: Olay
            
        Returns:
            bool: Olay işlendi mi?
        """
        if obj == self and event.type() == QEvent.Type.Resize:
            # Genişlik değişikliğini kaydet (settings_utils kullanarak)
            width = self.width()
            if width > 0:
                save_sidebar_width(width)
                
        return super().eventFilter(obj, event)
