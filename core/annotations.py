"""
Module for adding annotations, notes, and drawings to PDF files.
"""
import fitz  # PyMuPDF

class PDFAnnotator:
    """Class for adding annotations to PDF files."""
    
    def __init__(self):
        """Initialize the PDF annotator."""
        pass
    
    def add_text_annotation(self, page, rect, text, title="Note", icon="note"):
        """Add a text annotation (sticky note) to a PDF page.
        
        Args:
            page: PyMuPDF Page object
            rect (tuple): Rectangle coordinates (x0, y0, x1, y1)
            text (str): Annotation text content
            title (str, optional): Annotation title. Defaults to "Note".
            icon (str, optional): Icon type. Defaults to "note".
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            annot = page.add_text_annot(rect[:2], text, icon=icon)
            annot.set_info(title=title)
            annot.update()
            return True
        except Exception as e:
            print(f"Error adding text annotation: {e}")
            return False
    
    def add_highlight(self, page, rect, color=(1, 1, 0)):
        """Add a highlight annotation to a PDF page.
        
        Args:
            page: PyMuPDF Page object
            rect (tuple): Rectangle coordinates (x0, y0, x1, y1)
            color (tuple, optional): RGB color tuple (0-1 range). Defaults to yellow (1,1,0).
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            annot = page.add_highlight_annot(rect)
            annot.set_colors(stroke=color)
            annot.update()
            return True
        except Exception as e:
            print(f"Error adding highlight: {e}")
            return False
    
    def add_rectangle(self, page, rect, width=1.0, color=(0, 0, 0)):
        """Add a rectangle annotation to a PDF page.
        
        Args:
            page: PyMuPDF Page object
            rect (tuple): Rectangle coordinates (x0, y0, x1, y1)
            width (float, optional): Line width. Defaults to 1.0.
            color (tuple, optional): RGB color tuple (0-1 range). Defaults to black.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            annot = page.add_rect_annot(rect)
            annot.set_border(width=width)
            annot.set_colors(stroke=color)
            annot.update()
            return True
        except Exception as e:
            print(f"Error adding rectangle: {e}")
            return False
    
    def add_line(self, page, start_point, end_point, width=1.0, color=(0, 0, 0)):
        """Add a line annotation to a PDF page.
        
        Args:
            page: PyMuPDF Page object
            start_point (tuple): Start point coordinates (x, y)
            end_point (tuple): End point coordinates (x, y)
            width (float, optional): Line width. Defaults to 1.0.
            color (tuple, optional): RGB color tuple (0-1 range). Defaults to black.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            annot = page.add_line_annot(start_point, end_point)
            annot.set_border(width=width)
            annot.set_colors(stroke=color)
            annot.update()
            return True
        except Exception as e:
            print(f"Error adding line: {e}")
            return False
    
    def add_freehand_drawing(self, page, points, width=1.0, color=(0, 0, 0)):
        """Add a freehand drawing annotation to a PDF page.
        
        Args:
            page: PyMuPDF Page object
            points (list): List of point coordinates [(x1, y1), (x2, y2), ...]
            width (float, optional): Line width. Defaults to 1.0.
            color (tuple, optional): RGB color tuple (0-1 range). Defaults to black.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if len(points) < 2:
                return False
                
            annot = page.add_polyline_annot(points)
            annot.set_border(width=width)
            annot.set_colors(stroke=color)
            annot.update()
            return True
        except Exception as e:
            print(f"Error adding freehand drawing: {e}")
            return False
    
    def delete_annotation(self, page, annot_index):
        """Delete an annotation from a PDF page.
        
        Args:
            page: PyMuPDF Page object
            annot_index (int): Index of the annotation to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            annots = page.annots()
            if 0 <= annot_index < len(annots):
                page.delete_annot(annots[annot_index])
                return True
            return False
        except Exception as e:
            print(f"Error deleting annotation: {e}")
            return False
