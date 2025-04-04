"""Tema ve kullanıcı ayarları yönetimi için yardımcı fonksiyonlar."""

from PyQt6.QtWidgets import QApplication, QPushButton, QWidget
from PyQt6.QtCore import QSize
from qt_material import apply_stylesheet
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def apply_theme_to_application(theme_name):
    """Temayı tüm uygulamaya uygula.
    
    Args:
        theme_name: Uygulanacak tema adı
    """
    try:
        # Tema adının .xml uzantısını kontrol et
        if not theme_name.endswith('.xml'):
            theme_name = f"{theme_name}.xml"
            
        # Temayı uygula
        apply_stylesheet(
            app=QApplication.instance(),
            theme=theme_name
        )
        logger.debug(f"Tema başarıyla uygulandı: {theme_name}")
        return True
    except Exception as e:
        logger.error(f"Tema uygulama hatası: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def apply_theme_to_widget(widget, theme_name):
    """Temayı belirli bir widget'a uygula.
    
    Args:
        widget: Tema uygulanacak widget
        theme_name: Uygulanacak tema adı
    """
    try:
        # Tema adının .xml uzantısını kontrol et
        if not theme_name.endswith('.xml'):
            theme_name = f"{theme_name}.xml"
            
        # Temayı widget'a uygula
        apply_stylesheet(widget, theme=theme_name)
        logger.debug(f"Tema widget'a başarıyla uygulandı: {theme_name}")
        return True
    except Exception as e:
        logger.error(f"Widget'a tema uygulama hatası: {e}")
        return False

def get_button_style(is_dark=False):
    """Butonlar için tema stilini döndür.
    
    Args:
        is_dark: Koyu tema mı?
        
    Returns:
        str: Buton stil tanımı
    """
    # Buton stilleri için tema renkleri
    return """
        QPushButton {
            background-color: transparent;
            border: 1px solid palette(mid);
            border-radius: 4px;
            padding: 4px;
        }
        QPushButton:hover {
            background-color: palette(highlight);
            border-color: palette(highlight);
        }
        QPushButton:pressed {
            background-color: palette(dark);
        }
    """

def apply_button_styles(parent_widget):
    """Bir widget içindeki tüm butonlara stil uygula.
    
    Args:
        parent_widget: Butonları içeren üst widget
    """
    button_style = get_button_style()
    for button in parent_widget.findChildren(QPushButton):
        button.setStyleSheet(button_style)

def is_dark_theme(theme_name):
    """Temanın koyu tema olup olmadığını kontrol et.
    
    Args:
        theme_name: Tema adı
        
    Returns:
        bool: Koyu tema ise True, değilse False
    """
    return theme_name.startswith('dark_')

def toggle_theme(current_theme):
    """Açık ve koyu tema arasında geçiş yap.
    
    Args:
        current_theme: Mevcut tema adı
        
    Returns:
        str: Yeni tema adı
    """
    is_dark = is_dark_theme(current_theme)
    
    # Açık/koyu tema varyantları arasında geçiş yap
    if is_dark:
        new_theme = current_theme.replace('dark_', 'light_')
    else:
        new_theme = current_theme.replace('light_', 'dark_')
        
    return new_theme