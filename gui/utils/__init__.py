"""
Utility modules for the miniPDF application.
"""
from gui.utils.form_utils import (
    create_labeled_frame,
    create_text_area,
    create_buttons_frame,
    add_button,
    create_form_row
)
from gui.utils.messages import (
    # Information messages
    PDF_OPEN_REQUIRED,
    PAGE_SELECTION_REQUIRED,
    FEATURE_NOT_IMPLEMENTED,
    OPERATION_SUCCESSFUL,
    OPERATION_FAILED,
    
    # Success messages
    PDF_SAVED,
    TEXT_EXTRACTED,
    TEXT_SAVED,
    NOTE_ADDED,
    PAGE_ADDED,
    PAGE_DELETED,
    PAGE_ROTATED,
    PDF_SPLIT,
    PDF_MERGED,
    PDF_ENCRYPTED,
    PDF_DECRYPTED,
    
    # Error messages
    ERROR_OPENING_FILE,
    ERROR_SAVING_FILE,
    ERROR_PROCESSING_PDF,
    
    # Dialog titles
    INFO_TITLE,
    SUCCESS_TITLE,
    ERROR_TITLE,
    WARNING_TITLE
)
from gui.utils.icon_utils import (
    load_svg_icon,
    create_icon_button,
    save_svg_to_file,
    MATERIAL_ICONS
)

__all__ = [
    # Form utilities
    'create_labeled_frame',
    'create_text_area',
    'create_buttons_frame',
    'add_button',
    'create_form_row',
    
    # Message strings
    'PDF_OPEN_REQUIRED',
    'PAGE_SELECTION_REQUIRED',
    'FEATURE_NOT_IMPLEMENTED',
    'OPERATION_SUCCESSFUL',
    'OPERATION_FAILED',
    'PDF_SAVED',
    'TEXT_EXTRACTED',
    'TEXT_SAVED',
    'NOTE_ADDED',
    'PAGE_ADDED',
    'PAGE_DELETED',
    'PAGE_ROTATED',
    'PDF_SPLIT',
    'PDF_MERGED',
    'PDF_ENCRYPTED',
    'PDF_DECRYPTED',
    'ERROR_OPENING_FILE',
    'ERROR_SAVING_FILE',
    'ERROR_PROCESSING_PDF',
    'INFO_TITLE',
    'SUCCESS_TITLE',
    'ERROR_TITLE',
    'WARNING_TITLE',
    
    # Icon utilities
    'load_svg_icon',
    'create_icon_button',
    'save_svg_to_file',
    'MATERIAL_ICONS'
]
