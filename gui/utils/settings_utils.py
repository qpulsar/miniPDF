"""Tema ve kullanıcı ayarları yönetimi için merkezi yardımcı fonksiyonlar.

Bu modül, miniPDF uygulamasının tüm tema ve kullanıcı ayarları yönetimini sağlar.
Tema değişiklikleri, zoom seviyesi, sidebar genişliği gibi kullanıcı tercihlerinin
kaydedilmesi ve yüklenmesi için gerekli tüm fonksiyonları içerir.

Kullanıcı tercihleri user_settings.json dosyasında saklanır ve uygulama başlatıldığında
otomatik olarak yüklenir. Tema değişiklikleri tüm bileşenlere uygulanır.
"""

import os
import json
import logging
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QComboBox, QLabel, QListWidget, QFrame
from PyQt6.QtCore import QSize
from qt_material import apply_stylesheet, list_themes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Ayarlar dosyası yolu - projenin kök dizininde olmalı
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'user_settings.json')

# Varsayılan ayarlar
DEFAULT_SETTINGS = {
    'theme': 'light_blue',
    'language': 'tr',
    'zoom_level': 100,
    'sidebar_width': 250,
    'recent_files': []
}


def load_settings():
    """Kullanıcı ayarlarını dosyadan yükle.
    
    Returns:
        dict: Kullanıcı ayarları
    """
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        # Dosya yoksa varsayılan ayarları kaydet ve döndür
        settings = DEFAULT_SETTINGS.copy()
        save_settings(settings)
        return settings
    except Exception as e:
        logger.error(f"Ayarlar yüklenirken hata oluştu: {e}")
        import traceback
        logger.error(traceback.format_exc())
        # Hata durumunda varsayılan ayarları döndür
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Kullanıcı ayarlarını dosyaya kaydet.
    
    Args:
        settings (dict): Kaydedilecek ayarlar
    """
    try:
        # Dosyanın bulunduğu dizinin varlığını kontrol et ve gerekirse oluştur
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        logger.debug("Ayarlar başarıyla kaydedildi")
    except Exception as e:
        logger.error(f"Ayarlar kaydedilirken hata oluştu: {e}")
        import traceback
        logger.error(traceback.format_exc())


def get_setting(key, default=None):
    """Belirli bir ayarı getir.
    
    Args:
        key (str): Ayar anahtarı
        default: Ayar bulunamazsa dönecek varsayılan değer
        
    Returns:
        Ayar değeri veya varsayılan değer
    """
    settings = load_settings()
    return settings.get(key, default if default is not None else DEFAULT_SETTINGS.get(key))


def set_setting(key, value):
    """Belirli bir ayarı güncelle ve kaydet.
    
    Args:
        key (str): Ayar anahtarı
        value: Ayar değeri
    """
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
    logger.debug(f"Ayar güncellendi: {key} = {value}")


def update_settings(settings_dict):
    """Birden fazla ayarı aynı anda güncelle ve kaydet.
    
    Args:
        settings_dict (dict): Güncellenecek ayarlar sözlüğü
    """
    settings = load_settings()
    settings.update(settings_dict)
    save_settings(settings)
    logger.debug(f"Ayarlar toplu olarak güncellendi: {list(settings_dict.keys())}")


def apply_theme_to_application(theme_name):
    """Temayı tüm uygulamaya uygula.
    
    Args:
        theme_name: Uygulanacak tema adı
        
    Returns:
        bool: Başarılı ise True, değilse False
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
        
        # Ayarları güncelle
        set_setting('theme', theme_name.replace('.xml', ''))
        
        logger.debug(f"Tema başarıyla uygulandı: {theme_name}")
        return True
    except Exception as e:
        logger.error(f"Tema uygulama hatası: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def apply_theme_to_all_components(app_instance):
    """Temayı uygulamanın tüm bileşenlerine uygula.
    
    Bu fonksiyon, tema değişikliği sinyali yayınlandığında çağrılır ve
    uygulamanın tüm bileşenlerine tema değişikliklerini uygular.
    
    Args:
        app_instance: Uygulama örneği (App sınıfı örneği)
        
    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        # Mevcut temayı al
        current_theme = get_setting('theme')
        logger.debug(f"Tüm bileşenlere tema uygulanıyor: {current_theme}")
        
        # Tema değişikliği sinyalini yayınla
        # Bu sinyal, tüm bileşenlerin kendi apply_theme metodlarını çağıracak
        app_instance.theme_changed.emit()
        
        return True
    except Exception as e:
        logger.error(f"Tüm bileşenlere tema uygulama hatası: {e}")
        return False


def apply_theme_to_widget(widget, theme_name=None):
    """Temayı belirli bir widget'a uygula.
    
    Args:
        widget: Tema uygulanacak widget
        theme_name: Uygulanacak tema adı, None ise kaydedilmiş tema kullanılır
        
    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        # Tema adı belirtilmemişse kaydedilmiş temayı kullan
        if theme_name is None:
            theme_name = get_setting('theme')
        
        # Tema adının .xml uzantısını kontrol et
        if not theme_name.endswith('.xml'):
            theme_name = f"{theme_name}.xml"
            
        # Temayı widget'a uygula
        apply_stylesheet(widget, theme=theme_name)
        
        # Widget'ın alt bileşenlerine stil uygula
        apply_styles_to_components(widget)
        
        logger.debug(f"Tema widget'a başarıyla uygulandı: {theme_name}")
        return True
    except Exception as e:
        logger.error(f"Widget'a tema uygulama hatası: {e}")
        return False


def apply_styles_to_components(parent_widget):
    """Bir widget içindeki tüm bileşenlere stil uygula.
    
    Args:
        parent_widget: Bileşenleri içeren üst widget
    """
    # Butonlara stil uygula
    apply_button_styles(parent_widget)
    
    # Etiketlere stil uygula
    for label in parent_widget.findChildren(QLabel):
        apply_label_style(label)
    
    # ComboBox'lara stil uygula
    for combo in parent_widget.findChildren(QComboBox):
        apply_combo_style(combo)
        
    # QListWidget'lara stil uygula
    for list_widget in parent_widget.findChildren(QListWidget):
        apply_list_widget_style(list_widget)
    
    # QFrame'lere stil uygula (ayırıcılar dahil)
    for frame in parent_widget.findChildren(QFrame):
        apply_frame_style(frame)
        
    # Diğer QWidget'lara stil uygula
    for widget in parent_widget.findChildren(QWidget):
        # Sadece doğrudan QWidget sınıfından türetilmiş olanları ele al
        if widget.__class__.__name__ == "QWidget":
            apply_widget_style(widget)


def get_available_themes():
    """Kullanılabilir temaları döndür.
    
    Returns:
        dict: Tema adı ve görünen adı eşleşmeleri
    """
    themes = {}
    for theme in list_themes():
        # XML uzantısını kaldır
        name = theme.replace('.xml', '')
        # Görünen adı oluştur
        display_name = name.replace('_', ' ').title()
        themes[name] = display_name
    return themes
    
    # Mevcut temanın açık/koyu versiyonunu bul
    themes = get_available_themes()
    if is_dark:
        # Koyu temadan açık temaya geç
        new_theme = current_theme.replace('dark', 'light')
    else:
        # Açık temadan koyu temaya geç
        new_theme = current_theme.replace('light', 'dark')
    
    # Yeni tema mevcutsa uygula, değilse varsayılan temaya geç
    if new_theme in themes:
        apply_theme_to_application(new_theme)
        return new_theme
    else:
        default_theme = 'light_blue' if is_dark else 'dark_blue'
        apply_theme_to_application(default_theme)
        return default_theme

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
    if not theme_name:
        return False
        
    # .xml uzantısını kaldır
    if theme_name.endswith('.xml'):
        theme_name = theme_name[:-4]
        
    return theme_name.startswith('dark_')


def toggle_theme():
    """Koyu ve açık tema arasında geçiş yap.
    
    Returns:
        str: Yeni tema adı
    """
    current_theme = get_setting('theme')
    
    # Tema adının .xml uzantısını kaldır
    if current_theme.endswith('.xml'):
        current_theme = current_theme[:-4]
    
    # Koyu/açık tema geçişi
    if is_dark_theme(current_theme):
        new_theme = current_theme.replace('dark_', 'light_')
    else:
        new_theme = current_theme.replace('light_', 'dark_')
    
    # Yeni temayı uygula ve kaydet
    apply_theme_to_application(new_theme)
    
    return new_theme


def get_available_themes():
    """Kullanılabilir temaları getir.
    
    Returns:
        dict: Tema adları ve görüntüleme adları
    """
    all_themes = list_themes()
    theme_dict = {}
    
    # Koyu temalar
    for theme in [t for t in all_themes if t.startswith('dark_')]:
        name = theme.replace('dark_', '').replace('.xml', '').capitalize()
        display_name = f"Koyu {name}"
        theme_dict[theme] = display_name
    
    # Açık temalar
    for theme in [t for t in all_themes if t.startswith('light_')]:
        name = theme.replace('light_', '').replace('.xml', '').replace('_500', '').capitalize()
        display_name = f"Açık {name}"
        theme_dict[theme] = display_name
    
    return theme_dict


def save_zoom_level(zoom_level):
    """Zoom seviyesini kaydet.
    
    Args:
        zoom_level (int): Zoom seviyesi (yüzde olarak)
    """
    set_setting('zoom_level', zoom_level)


def load_zoom_level():
    """Kaydedilmiş zoom seviyesini yükle.
    
    Returns:
        int: Zoom seviyesi (yüzde olarak)
    """
    return get_setting('zoom_level', DEFAULT_SETTINGS['zoom_level'])


def save_sidebar_width(width):
    """Sidebar genişliğini kaydet.
    
    Args:
        width (int): Sidebar genişliği (piksel olarak)
    """
    set_setting('sidebar_width', width)


def load_sidebar_width():
    """Kaydedilmiş sidebar genişliğini yükle.
    
    Returns:
        int: Sidebar genişliği (piksel olarak)
    """
    return get_setting('sidebar_width', DEFAULT_SETTINGS['sidebar_width'])


def apply_settings_to_app(app_instance):
    """Kaydedilmiş ayarları uygulamaya uygula.
    
    Bu fonksiyon, uygulama başlatıldığında çağrılır ve
    kaydedilmiş tüm ayarları uygular.
    
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
        
        logger.debug(f"Tüm ayarlar başarıyla uygulandı")
        return True
    except Exception as e:
        logger.error(f"Ayarları uygulama hatası: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def apply_label_style(label):
    """Etiketlere stil uygula.
    
    Args:
        label: Stil uygulanacak QLabel
    """
    # Etiket stilini uygula
    label.setStyleSheet("""
        QLabel {
            color: palette(text);
        }
    """)


def apply_combo_style(combo):
    """ComboBox'lara stil uygula.
    
    Args:
        combo: Stil uygulanacak QComboBox
    """
    # ComboBox stilini uygula
    combo.setStyleSheet("""
        QComboBox {
            border: 1px solid palette(mid);
            border-radius: 4px;
            padding: 2px 4px;
            min-height: 24px;
        }
        QComboBox:hover {
            border-color: palette(highlight);
        }
        QComboBox:focus {
            border-color: palette(highlight);
            border-width: 2px;
        }
    """)
    

def apply_list_widget_style(list_widget):
    """QListWidget'lara stil uygula.
    
    Args:
        list_widget: Stil uygulanacak QListWidget
    """
    # QListWidget stilini uygula
    list_widget.setStyleSheet("""
        QListWidget {
            border: 1px solid palette(mid);
            border-radius: 4px;
            background-color: palette(base);
        }
        QListWidget::item {
            border-radius: 2px;
            padding: 2px;
        }
        QListWidget::item:selected {
            background-color: palette(highlight);
            color: palette(highlighted-text);
        }
        QListWidget::item:hover:!selected {
            background-color: palette(alternate-base);
        }
    """)


def apply_frame_style(frame):
    """QFrame'lere stil uygula.
    
    Args:
        frame: Stil uygulanacak QFrame
    """
    # QFrame stilini uygula (ayırıcılar için)
    if frame.frameShape() == QFrame.Shape.HLine:
        frame.setStyleSheet("""
            QFrame[frameShape="5"] { /* HLine */
                color: palette(mid);
                max-height: 1px;
            }
        """)
    elif frame.frameShape() == QFrame.Shape.VLine:
        frame.setStyleSheet("""
            QFrame[frameShape="6"] { /* VLine */
                color: palette(mid);
                max-width: 1px;
            }
        """)


def apply_widget_style(widget):
    """Genel QWidget'lara stil uygula.
    
    Args:
        widget: Stil uygulanacak QWidget
    """
    # Genel widget stilini uygula
    widget.setStyleSheet("""
        QWidget {
            background-color: palette(window);
            color: palette(window-text);
        }
    """)