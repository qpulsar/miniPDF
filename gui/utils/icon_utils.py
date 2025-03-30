"""
Icon utilities for the PDF Editor.
"""
import os
import logging
from PyQt6.QtGui import QIcon, QPainter, QPen, QColor, QPixmap
from PyQt6.QtCore import Qt, QSize

class IconProvider:
    """Provider for Material Design icons."""
    
    ICON_SIZE = 24
    ICON_COLOR = "#000000"
    
    @classmethod
    def get_icon(cls, name):
        """Get icon by name.
        
        Args:
            name: Icon name
            
        Returns:
            QIcon: Icon instance
        """
        icon_map = {
            # File menu
            "open": cls._create_folder_icon,
            "save": cls._create_save_icon,
            "save_as": cls._create_save_as_icon,
            "print": cls._create_print_icon,
            "exit": cls._create_exit_icon,
            
            # Page menu
            "add": cls._create_add_icon,
            "delete": cls._create_delete_icon,
            "rotate": cls._create_rotate_icon,
            "move": cls._create_move_icon,
            "export": cls._create_export_icon,
            
            # Edit menu
            "text": cls._create_text_icon,
            "draw": cls._create_draw_icon,
            "highlight": cls._create_highlight_icon,
            
            # Tools menu
            "ocr": cls._create_ocr_icon,
            "merge": cls._create_merge_icon,
            "split": cls._create_split_icon,
            "lock": cls._create_lock_icon,
            "unlock": cls._create_unlock_icon,
            
            # View menu
            "zoom": cls._create_zoom_icon,
            "layout": cls._create_layout_icon,
            "theme": cls._create_theme_icon,
            
            # Help menu
            "help": cls._create_help_icon,
            "about": cls._create_about_icon,
            "feedback": cls._create_feedback_icon,
        }
        
        if name not in icon_map:
            return QIcon()
            
        return icon_map[name]()
        
    @classmethod
    def _create_pixmap(cls):
        """Create a base pixmap."""
        pixmap = QPixmap(cls.ICON_SIZE, cls.ICON_SIZE)
        pixmap.fill(Qt.GlobalColor.transparent)
        return pixmap
        
    @classmethod
    def _create_painter(cls, pixmap):
        """Create a painter for the pixmap."""
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(cls.ICON_COLOR), 2))
        return painter
        
    @classmethod
    def _create_folder_icon(cls):
        """Create folder icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw folder shape
        painter.drawRect(4, 6, 16, 14)
        painter.drawLine(4, 6, 8, 2)
        painter.drawLine(8, 2, 12, 2)
        painter.drawLine(12, 2, 12, 6)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_save_icon(cls):
        """Create save icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw floppy disk shape
        painter.drawRect(4, 4, 16, 16)
        painter.drawRect(6, 6, 12, 6)
        painter.drawRect(14, 14, 4, 4)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_save_as_icon(cls):
        """Create save as icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw floppy disk with plus
        painter.drawRect(2, 4, 14, 14)
        painter.drawRect(4, 6, 10, 4)
        painter.drawRect(12, 12, 2, 4)
        
        # Draw plus
        painter.drawLine(18, 14, 22, 14)
        painter.drawLine(20, 12, 20, 16)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_print_icon(cls):
        """Create print icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw printer shape
        painter.drawRect(4, 8, 16, 10)
        painter.drawRect(6, 2, 12, 6)
        painter.drawRect(6, 14, 12, 6)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_exit_icon(cls):
        """Create exit icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw door with arrow
        painter.drawRect(4, 2, 12, 20)
        painter.drawLine(16, 12, 20, 12)
        painter.drawLine(18, 10, 20, 12)
        painter.drawLine(18, 14, 20, 12)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_add_icon(cls):
        """Create add icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw plus
        painter.drawLine(12, 4, 12, 20)
        painter.drawLine(4, 12, 20, 12)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_delete_icon(cls):
        """Create delete icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw trash can
        painter.drawRect(6, 6, 12, 16)
        painter.drawLine(4, 6, 20, 6)
        painter.drawLine(8, 2, 16, 2)
        painter.drawLine(8, 2, 8, 6)
        painter.drawLine(16, 2, 16, 6)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_rotate_icon(cls):
        """Create rotate icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw circular arrow
        painter.drawArc(4, 4, 16, 16, 30 * 16, 300 * 16)
        painter.drawLine(18, 8, 20, 4)
        painter.drawLine(18, 8, 14, 8)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_move_icon(cls):
        """Create move icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw four-way arrow
        painter.drawLine(12, 4, 12, 20)
        painter.drawLine(4, 12, 20, 12)
        painter.drawLine(8, 8, 4, 12)
        painter.drawLine(8, 16, 4, 12)
        painter.drawLine(16, 8, 20, 12)
        painter.drawLine(16, 16, 20, 12)
        painter.drawLine(8, 8, 12, 4)
        painter.drawLine(16, 8, 12, 4)
        painter.drawLine(8, 16, 12, 20)
        painter.drawLine(16, 16, 12, 20)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_export_icon(cls):
        """Create export icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw export arrow
        painter.drawRect(4, 4, 16, 16)
        painter.drawLine(12, 8, 12, 16)
        painter.drawLine(8, 12, 12, 16)
        painter.drawLine(16, 12, 12, 16)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_text_icon(cls):
        """Create text icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw T shape
        painter.drawLine(4, 4, 20, 4)
        painter.drawLine(12, 4, 12, 20)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_draw_icon(cls):
        """Create draw icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw pencil
        painter.drawLine(4, 20, 16, 8)
        painter.drawLine(16, 8, 20, 4)
        painter.drawLine(18, 6, 14, 10)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_highlight_icon(cls):
        """Create highlight icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw highlighter
        painter.drawRect(4, 12, 16, 8)
        painter.drawLine(4, 12, 12, 4)
        painter.drawLine(20, 12, 12, 4)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_ocr_icon(cls):
        """Create OCR icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw OCR symbol
        painter.drawText(4, 18, "OCR")
        painter.drawRect(2, 2, 20, 20)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_merge_icon(cls):
        """Create merge icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw merge arrows
        painter.drawLine(4, 4, 12, 12)
        painter.drawLine(20, 4, 12, 12)
        painter.drawLine(12, 12, 12, 20)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_split_icon(cls):
        """Create split icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw split arrows
        painter.drawLine(12, 4, 12, 12)
        painter.drawLine(12, 12, 4, 20)
        painter.drawLine(12, 12, 20, 20)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_lock_icon(cls):
        """Create lock icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw lock
        painter.drawRect(6, 10, 12, 12)
        painter.drawArc(8, 4, 8, 8, 180 * 16, 180 * 16)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_unlock_icon(cls):
        """Create unlock icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw unlocked lock
        painter.drawRect(6, 10, 12, 12)
        painter.drawArc(4, 4, 8, 8, 270 * 16, 180 * 16)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_zoom_icon(cls):
        """Create zoom icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw magnifying glass
        painter.drawEllipse(4, 4, 12, 12)
        painter.drawLine(14, 14, 20, 20)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_layout_icon(cls):
        """Create layout icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw layout rectangles
        painter.drawRect(4, 4, 7, 16)
        painter.drawRect(13, 4, 7, 16)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_theme_icon(cls):
        """Create theme icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw sun/moon
        painter.drawEllipse(4, 4, 16, 16)
        painter.drawEllipse(8, 8, 8, 8)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_help_icon(cls):
        """Create help icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw question mark
        painter.drawText(8, 18, "?")
        painter.drawEllipse(4, 4, 16, 16)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_about_icon(cls):
        """Create about icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw info symbol
        painter.drawText(10, 18, "i")
        painter.drawEllipse(4, 4, 16, 16)
        
        painter.end()
        return QIcon(pixmap)
        
    @classmethod
    def _create_feedback_icon(cls):
        """Create feedback icon."""
        pixmap = cls._create_pixmap()
        painter = cls._create_painter(pixmap)
        
        # Draw speech bubble
        painter.drawRect(4, 4, 16, 12)
        painter.drawLine(8, 16, 12, 20)
        painter.drawLine(12, 20, 16, 16)
        
        painter.end()
        return QIcon(pixmap)
