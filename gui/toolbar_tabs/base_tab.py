"""
Base tab class for toolbar tabs in the miniPDF application.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QHBoxLayout, QMessageBox
from gui.utils import PDF_OPEN_REQUIRED, FEATURE_NOT_IMPLEMENTED, INFO_TITLE, SUCCESS_TITLE

class BaseTab(QWidget):
    """Base class for toolbar tabs."""
    
    def __init__(self, parent, app):
        """Initialize base tab.
        
        Args:
            parent: Parent widget
            app: Main application instance
        """
        super().__init__(parent)
        self.app = app
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        
    def create_frame(self, name, title):
        """Create a labeled frame.
        
        Args:
            name (str): Frame name
            title (str): Frame title
            
        Returns:
            QWidget: Created frame content area
        """
        frame = QFrame(self)
        frame.setObjectName(name)
        frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        
        frame_layout = QVBoxLayout(frame)
        
        # Add title
        title_label = QLabel(title)
        title_label.setObjectName(f"{name}_title")
        frame_layout.addWidget(title_label)
        
        # Add content area
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content.setLayout(content_layout)
        frame_layout.addWidget(content)
        
        self.layout.addWidget(frame)
        return content
    
    def add_button(self, frame, text, command):
        """
        Add a button to a frame.
        
        Args:
            frame (QWidget): Frame to add the button to
            text (str): Button text
            command: Button command
        """
        from PyQt6.QtWidgets import QPushButton
        button = QPushButton(text, frame)
        button.clicked.connect(command)
        frame.layout().addWidget(button)
    
    def check_pdf_open(self):
        """
        Check if a PDF file is open.
        
        Returns:
            bool: True if a PDF is open, False otherwise
        """
        if not self.app.pdf_manager.current_file:
            QMessageBox.information(self, INFO_TITLE, PDF_OPEN_REQUIRED)
            return False
        return True
    
    def show_not_implemented(self):
        """Show a message for features that are not yet implemented."""
        QMessageBox.information(self, INFO_TITLE, FEATURE_NOT_IMPLEMENTED)
    
    def show_success_message(self, message):
        """
        Show a success message.
        
        Args:
            message (str): Success message to show
        """
        QMessageBox.information(self, SUCCESS_TITLE, message)
