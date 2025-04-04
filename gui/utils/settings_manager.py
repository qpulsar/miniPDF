"""
Merkezi ayarlar yönetimi için yardımcı fonksiyonlar.

Bu modül, miniPDF uygulamasının tüm ayarlarını merkezi olarak yönetmek için
yüksek seviyeli fonksiyonlar sağlar. Tema değişiklikleri, zoom seviyesi,
sidebar genişliği gibi ayarların tüm bileşenlere tutarlı bir şekilde
uygulanmasını sağlar.
"""

import logging
from PyQt6.QtWidgets import QApplication
from .settings_utils import (
    apply_theme_to_application, apply_theme_to_all_components,
    get_setting, set_setting, update_settings,
    save_zoom_level, load_zoom_level,
    save_sidebar_width, load_sidebar_width
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def initialize_app_settings(app_instance):
    """Uygulama başlatıldığında tüm ayarları yükle ve uygula.
    
    Args:
        app_instance: Uygulama örneği (App sınıfı örneği)
        
    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        # Temayı uygula
        theme = get_setting('theme')
        apply_theme_to_application(theme)
        
        # Tema değişikliği sinyalini yayınla
        app_instance.theme_changed.emit()
        
        # Sidebar genişliğini ayarla
        sidebar_width = load_sidebar_width()
        if hasattr(app_instance, 'sidebar') and sidebar_width > 0:
            app_instance.sidebar.setMinimumWidth(sidebar_width)
            app_instance.sidebar.setMaximumWidth(sidebar_width)
        
        # Zoom seviyesini ayarla
        zoom_level = load_zoom_level()
        if hasattr(app_instance, 'preview'):
            app_instance.preview.set_zoom(zoom_level / 100.0)
        
        # ComboBox'ta kaydedilmiş temayı seç
        if hasattr(app_instance, 'update_theme_combo'):
            app_instance.update_theme_combo()
        
        logger.debug(f"Tüm ayarlar başarıyla uygulandı")
        return True
    except Exception as e:
        logger.error(f"Ayarları uygulama hatası: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def change_theme(app_instance, theme_name):
    """Temayı değiştir ve tüm bileşenlere uygula.
    
    Args:
        app_instance: Uygulama örneği (App sınıfı örneği)
        theme_name: Uygulanacak tema adı
        
    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        # Temayı uygula
        success = apply_theme_to_application(theme_name)
        
        if success:
            # Tema değişikliğini tüm bileşenlere uygula
            apply_theme_to_all_components(app_instance)
            
            # ComboBox'ta kaydedilmiş temayı seç
            if hasattr(app_instance, 'update_theme_combo'):
                app_instance.update_theme_combo()
            
            logger.debug(f"Tema başarıyla değiştirildi: {theme_name}")
            return True
        else:
            logger.error(f"Tema değiştirilemedi: {theme_name}")
            return False
    except Exception as e:
        logger.error(f"Tema değiştirme hatası: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def update_zoom_level(app_instance, zoom_level):
    """Zoom seviyesini güncelle ve kaydet.
    
    Args:
        app_instance: Uygulama örneği (App sınıfı örneği)
        zoom_level: Zoom seviyesi (yüzde olarak)
        
    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        # Zoom seviyesini kaydet
        save_zoom_level(zoom_level)
        
        # Preview'a zoom seviyesini uygula
        if hasattr(app_instance, 'preview'):
            app_instance.preview.set_zoom(zoom_level / 100.0)
        
        logger.debug(f"Zoom seviyesi güncellendi: {zoom_level}")
        return True
    except Exception as e:
        logger.error(f"Zoom seviyesi güncelleme hatası: {e}")
        return False


def update_sidebar_width(app_instance, width):
    """Sidebar genişliğini güncelle ve kaydet.
    
    Args:
        app_instance: Uygulama örneği (App sınıfı örneği)
        width: Sidebar genişliği (piksel olarak)
        
    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        # Sidebar genişliğini kaydet
        save_sidebar_width(width)
        
        # Sidebar'a genişliği uygula
        if hasattr(app_instance, 'sidebar') and width > 0:
            app_instance.sidebar.setMinimumWidth(width)
            app_instance.sidebar.setMaximumWidth(width)
        
        logger.debug(f"Sidebar genişliği güncellendi: {width}")
        return True
    except Exception as e:
        logger.error(f"Sidebar genişliği güncelleme hatası: {e}")
        return False


def save_all_settings(app_instance):
    """Tüm mevcut ayarları kaydet.
    
    Args:
        app_instance: Uygulama örneği (App sınıfı örneği)
        
    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        settings = {}
        
        # Tema ayarını al
        if hasattr(app_instance, 'current_theme'):
            settings['theme'] = app_instance.current_theme
        
        # Zoom seviyesini al
        if hasattr(app_instance, 'preview') and hasattr(app_instance.preview, 'current_zoom'):
            settings['zoom_level'] = int(app_instance.preview.current_zoom * 100)
        
        # Sidebar genişliğini al
        if hasattr(app_instance, 'sidebar'):
            settings['sidebar_width'] = app_instance.sidebar.width()
        
        # Ayarları toplu olarak güncelle
        update_settings(settings)
        
        logger.debug(f"Tüm ayarlar başarıyla kaydedildi: {settings}")
        return True
    except Exception as e:
        logger.error(f"Ayarları kaydetme hatası: {e}")
        return False
