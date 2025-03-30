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
        
    def create_frame(self, name, title):
        """Create a labeled frame.
        
        Args:
            name (str): Frame name
            title (str): Frame title
            
        Returns:
            QFrame: The created frame
        """
        frame = QFrame(self)
        frame.setObjectName(name)
        frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        
        layout = QVBoxLayout(frame)
        
        title_label = QLabel(title)
        layout.addWidget(title_label)
        
        return frame
        
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
