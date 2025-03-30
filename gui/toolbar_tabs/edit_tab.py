"""
Edit operations tab for the toolbar.
"""
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, 
                           QMessageBox, QInputDialog, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from ..utils.icon_utils import IconProvider

class EditTab(QWidget):
    """Tab for edit operations."""
    
    def __init__(self, parent=None):
        """Initialize edit tab.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        
        # Create layout
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)
        
        # Create buttons
        rotate_left_btn = QPushButton("Rotate Left")
        rotate_left_btn.setIcon(IconProvider.get_icon("rotate"))
        rotate_left_btn.clicked.connect(lambda: self.rotate_page(-90))
        layout.addWidget(rotate_left_btn)
        
        rotate_right_btn = QPushButton("Rotate Right")
        rotate_right_btn.setIcon(IconProvider.get_icon("rotate"))
        rotate_right_btn.clicked.connect(lambda: self.rotate_page(90))
        layout.addWidget(rotate_right_btn)
        
        delete_btn = QPushButton("Delete Page")
        delete_btn.setIcon(IconProvider.get_icon("delete"))
        delete_btn.clicked.connect(self.delete_page)
        layout.addWidget(delete_btn)
        
        extract_text_btn = QPushButton("Extract Text")
        extract_text_btn.setIcon(IconProvider.get_icon("text"))
        extract_text_btn.clicked.connect(self.extract_text)
        layout.addWidget(extract_text_btn)
        
        save_image_btn = QPushButton("Save as Image")
        save_image_btn.setIcon(IconProvider.get_icon("image"))
        save_image_btn.clicked.connect(self.save_as_image)
        layout.addWidget(save_image_btn)
        
    def get_current_page(self):
        """Get the currently selected page number."""
        sidebar = self.parent.parent().sidebar
        current_row = sidebar.currentRow()
        return current_row if current_row >= 0 else None
        
    def rotate_page(self, angle):
        """Rotate current page by angle.
        
        Args:
            angle: Rotation angle in degrees
        """
        page_num = self.get_current_page()
        if page_num is None:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to rotate."
            )
            return
            
        pdf_manager = self.parent.parent().pdf_manager
        if pdf_manager.rotate_page(page_num, angle):
            # Update preview
            self.parent.parent().preview.show_page(page_num)
            
    def delete_page(self):
        """Delete current page."""
        page_num = self.get_current_page()
        if page_num is None:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to delete."
            )
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this page?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            pdf_manager = self.parent.parent().pdf_manager
            if pdf_manager.delete_page(page_num):
                # Update sidebar and preview
                self.parent.parent().sidebar.update_page_list()
                if pdf_manager.get_page_count() > 0:
                    new_page = min(page_num, pdf_manager.get_page_count() - 1)
                    self.parent.parent().preview.show_page(new_page)
                    self.parent.parent().sidebar.setCurrentRow(new_page)
                    
    def extract_text(self):
        """Extract text from current page."""
        page_num = self.get_current_page()
        if page_num is None:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to extract text from."
            )
            return
            
        pdf_manager = self.parent.parent().pdf_manager
        text = pdf_manager.extract_text(page_num)
        
        if text:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Text As",
                "",
                "Text Files (*.txt);;All Files (*.*)"
            )
            
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    QMessageBox.information(
                        self,
                        "Success",
                        "Text has been saved successfully."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Could not save text: {e}"
                    )
        else:
            QMessageBox.information(
                self,
                "Info",
                "No text found on this page."
            )
            
    def save_as_image(self):
        """Save current page as image."""
        page_num = self.get_current_page()
        if page_num is None:
            QMessageBox.information(
                self,
                "Info",
                "Please select a page to save as image."
            )
            return
            
        # Get zoom factor
        zoom, ok = QInputDialog.getDouble(
            self,
            "Zoom Factor",
            "Enter zoom factor (1.0 = 100%):",
            value=2.0,
            min=0.1,
            max=10.0,
            decimals=1
        )
        
        if not ok:
            return
            
        pdf_manager = self.parent.parent().pdf_manager
        image_data = pdf_manager.extract_image(page_num, zoom)
        
        if image_data:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Image As",
                "",
                "PNG Files (*.png);;All Files (*.*)"
            )
            
            if file_path:
                try:
                    with open(file_path, 'wb') as f:
                        f.write(image_data)
                    QMessageBox.information(
                        self,
                        "Success",
                        "Image has been saved successfully."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Could not save image: {e}"
                    )
        else:
            QMessageBox.critical(
                self,
                "Error",
                "Could not create image from page."
            )
