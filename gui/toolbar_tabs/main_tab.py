"""
Main toolbar tab combining all operations.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from ..widgets.ribbon import RibbonSection
from ..utils.icon_utils import IconProvider
from ..utils.theme_utils import apply_theme_to_widget, apply_button_styles
from ..settings import Settings

class MainTab(QWidget):
    """Main tab containing all operations."""
    
    # File signals
    open_requested = pyqtSignal()
    save_requested = pyqtSignal()
    close_requested = pyqtSignal()
    
    # Page signals
    add_page_requested = pyqtSignal()
    delete_page_requested = pyqtSignal()
    rotate_page_requested = pyqtSignal(int)  # angle
    move_page_requested = pyqtSignal(str)  # direction
    export_page_requested = pyqtSignal()
    
    # Edit signals
    add_text_requested = pyqtSignal()
    draw_requested = pyqtSignal()
    highlight_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    
    # View signals
    zoom_in_requested = pyqtSignal()
    zoom_out_requested = pyqtSignal()
    theme_toggle_requested = pyqtSignal()
    page_layout_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize main tab."""
        super().__init__(parent)
        self.app = parent
        self.settings = Settings()
        
        # Tema değişikliklerini dinle
        if parent:
            parent.theme_changed.connect(self.update_theme)
            
        # Başlangıç ayarlarını yükle ve uygula
        self.update_theme()
        
        # Create layout
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(layout)
        
        # Fixed button size
        button_size = QSize(32, 32)
        
        # Create File Operations section
        file_section = RibbonSection("Dosya", self)
        file_layout = QHBoxLayout()
        file_section.setLayout(file_layout)
        
        # File buttons
        open_btn = QPushButton()
        open_btn.setIcon(IconProvider.IconProvider.get_icon("folder"))
        open_btn.setToolTip("PDF Dosyası Aç")
        open_btn.clicked.connect(self.open_requested.emit)
        open_btn.setFixedSize(button_size)
        file_layout.addWidget(open_btn)
        
        save_btn = QPushButton()
        save_btn.setIcon(IconProvider.get_icon("save"))
        save_btn.setToolTip("PDF Dosyasını Kaydet")
        save_btn.clicked.connect(self.save_requested.emit)
        save_btn.setFixedSize(button_size)
        file_layout.addWidget(save_btn)
        
        close_btn = QPushButton()
        close_btn.setIcon(IconProvider.get_icon("close"))
        close_btn.setToolTip("PDF Dosyasını Kapat")
        close_btn.clicked.connect(self.close_requested.emit)
        close_btn.setFixedSize(button_size)
        file_layout.addWidget(close_btn)
        
        # Create Page Operations section
        page_section = RibbonSection("Sayfa", self)
        page_layout = QHBoxLayout()
        page_section.setLayout(page_layout)
        
        # Page buttons
        add_btn = QPushButton()
        add_btn.setIcon(IconProvider.get_icon("addpage"))
        add_btn.setToolTip("Yeni Sayfa Ekle")
        add_btn.clicked.connect(self.add_page_requested.emit)
        add_btn.setFixedSize(button_size)
        page_layout.addWidget(add_btn)
        
        delete_btn = QPushButton()
        delete_btn.setIcon(IconProvider.get_icon("delete"))
        delete_btn.setToolTip("Seçili Sayfayı Sil")
        delete_btn.clicked.connect(self.delete_page_requested.emit)
        delete_btn.setFixedSize(button_size)
        page_layout.addWidget(delete_btn)
        
        rotate_btn = QPushButton()
        rotate_btn.setIcon(IconProvider.get_icon("rotate"))
        rotate_btn.setToolTip("Sayfayı Döndür")
        rotate_btn.clicked.connect(lambda: self.rotate_page_requested.emit(90))
        rotate_btn.setFixedSize(button_size)
        page_layout.addWidget(rotate_btn)
        
        move_btn = QPushButton()
        move_btn.setIcon(IconProvider.get_icon("move"))
        move_btn.setToolTip("Sayfayı Taşı")
        move_btn.clicked.connect(lambda: self.move_page_requested.emit("up"))
        move_btn.setFixedSize(button_size)
        page_layout.addWidget(move_btn)
        
        export_btn = QPushButton()
        export_btn.setIcon(IconProvider.get_icon("export"))
        export_btn.setToolTip("Sayfayı Dışa Aktar")
        export_btn.clicked.connect(self.export_page_requested.emit)
        export_btn.setFixedSize(button_size)
        page_layout.addWidget(export_btn)
        
        # Create Edit Operations section
        edit_section = RibbonSection("Düzenleme", self)
        edit_layout = QHBoxLayout()
        edit_section.setLayout(edit_layout)
        
        # Edit buttons
        text_btn = QPushButton()
        text_btn.setIcon(IconProvider.get_icon("text"))
        text_btn.setToolTip("Metin Ekle")
        text_btn.clicked.connect(self.add_text_requested.emit)
        text_btn.setFixedSize(button_size)
        edit_layout.addWidget(text_btn)
        
        draw_btn = QPushButton()
        draw_btn.setIcon(IconProvider.get_icon("draw"))
        draw_btn.setToolTip("Çizim Aracı")
        draw_btn.clicked.connect(self.draw_requested.emit)
        draw_btn.setFixedSize(button_size)
        edit_layout.addWidget(draw_btn)
        
        highlight_btn = QPushButton()
        highlight_btn.setIcon(IconProvider.get_icon("highlight"))
        highlight_btn.setToolTip("Metni Vurgula")
        highlight_btn.clicked.connect(self.highlight_requested.emit)
        highlight_btn.setFixedSize(button_size)
        edit_layout.addWidget(highlight_btn)
        
        clear_btn = QPushButton()
        clear_btn.setIcon(IconProvider.get_icon("clear"))
        clear_btn.setToolTip("Düzenlemeleri Temizle")
        clear_btn.clicked.connect(self.clear_requested.emit)
        clear_btn.setFixedSize(button_size)
        edit_layout.addWidget(clear_btn)
        
        # Create View Operations section
        view_section = RibbonSection("Görünüm", self)
        view_layout = QHBoxLayout()
        view_section.setLayout(view_layout)
        
        # View buttons
        zoom_in_btn = QPushButton()
        zoom_in_btn.setIcon(IconProvider.get_icon("zoom_in"))
        zoom_in_btn.setToolTip("Yakınlaştır")
        zoom_in_btn.clicked.connect(self.zoom_in_requested.emit)
        zoom_in_btn.setFixedSize(button_size)
        view_layout.addWidget(zoom_in_btn)
        
        zoom_out_btn = QPushButton()
        zoom_out_btn.setIcon(IconProvider.get_icon("zoom_out"))
        zoom_out_btn.setToolTip("Uzaklaştır")
        zoom_out_btn.clicked.connect(self.zoom_out_requested.emit)
        zoom_out_btn.setFixedSize(button_size)
        view_layout.addWidget(zoom_out_btn)
        
        theme_btn = QPushButton()
        theme_btn.setIcon(IconProvider.get_icon("theme"))
        theme_btn.setToolTip("Tema Değiştir")
        theme_btn.clicked.connect(self.theme_toggle_requested.emit)
        theme_btn.setFixedSize(button_size)
        view_layout.addWidget(theme_btn)
        
        layout_btn = QPushButton()
        layout_btn.setIcon(IconProvider.get_icon("layout"))
        layout_btn.setToolTip("Sayfa Düzenini Değiştir")
        layout_btn.clicked.connect(self.page_layout_requested.emit)
        layout_btn.setFixedSize(button_size)
        view_layout.addWidget(layout_btn)
        
        # Add all sections to layout
        layout.addWidget(file_section)
        layout.addWidget(page_section)
        layout.addWidget(edit_section)
        layout.addWidget(view_section)
        layout.addStretch()
        
    def update_theme(self):
        """Tema ve diğer kullanıcı ayarlarını uygula."""
        try:
            # settings_utils modülünü kullanarak tema ayarlarını uygula
            from ..utils.settings_utils import get_setting, apply_theme_to_widget, apply_button_styles, load_zoom_level, load_sidebar_width
            
            # Mevcut temayı al
            current_theme = get_setting('theme')
            self.app.sidebar.apply_theme()
            # Tüm butonlara stili uygula
            for section in self.findChildren(RibbonSection):
                apply_button_styles(section)
                    
            # Tema değişikliğini sekmeye uygula
            apply_theme_to_widget(self, current_theme)
            
            # Zoom seviyesi ayarlarını uygula
            zoom_level = load_zoom_level()
            # Zoom seviyesi değişikliğini ana uygulamaya bildir
            if self.app and hasattr(self.app, 'set_zoom_level'):
                self.app.set_zoom_level(zoom_level)
            
            # Diğer ayarları uygula (sidebar genişliği vb.)
            sidebar_width = load_sidebar_width()
            if self.app and hasattr(self.app, 'set_sidebar_width'):
                self.app.set_sidebar_width(sidebar_width)
            
        except Exception as e:
            print(f"Ayarları uygulama hatası: {e}")
            import traceback
            print(traceback.format_exc())
