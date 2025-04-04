import os
import json
from .utils.settings_utils import (
    load_settings, save_settings, get_setting, set_setting,
    save_zoom_level, load_zoom_level, save_sidebar_width, load_sidebar_width
)

class Settings:
    def __init__(self):
        self.settings_file = os.path.join(os.path.dirname(__file__), 'user_settings.json')
        self.default_settings = {
            'theme': 'light',
            'language': 'tr',
            'zoom_level': 100,
            'sidebar_width': 250,
            'recent_files': []
        }
        self.settings = load_settings()

    def _load_settings(self):
        # Eski yöntem, artık settings_utils kullanılıyor
        return load_settings()

    def _save_settings(self):
        # Eski yöntem, artık settings_utils kullanılıyor
        save_settings(self.settings)

    def save_theme(self, theme):
        if theme.endswith('.xml'):
            theme = theme[:-4]
        self.settings['theme'] = theme
        set_setting('theme', theme)

    def load_theme(self):
        return self.settings.get('theme', self.default_settings['theme'])

    def save_language(self, language):
        self.settings['language'] = language
        self._save_settings()

    def load_language(self):
        return self.settings.get('language', self.default_settings['language'])

    def save_zoom_level(self, zoom_level):
        self.settings['zoom_level'] = zoom_level
        save_zoom_level(zoom_level)

    def load_zoom_level(self):
        return load_zoom_level()
        
    def save_sidebar_width(self, width):
        self.settings['sidebar_width'] = width
        save_sidebar_width(width)
        
    def load_sidebar_width(self):
        return load_sidebar_width()

    def add_recent_file(self, file_path):
        recent_files = self.settings.get('recent_files', [])
        if file_path in recent_files:
            recent_files.remove(file_path)
        recent_files.insert(0, file_path)
        recent_files = recent_files[:10]  # Keep last 10 files
        self.settings['recent_files'] = recent_files
        set_setting('recent_files', recent_files)

    def get_recent_files(self):
        return get_setting('recent_files', [])
