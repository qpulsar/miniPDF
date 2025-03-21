"""
Help tab for the toolbar in the miniPDF application.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from gui.toolbar_tabs.base_tab import BaseTab

class HelpTab(BaseTab):
    """Help tab for the toolbar."""
    
    def __init__(self, parent, app):
        """
        Initialize the help tab.
        
        Args:
            parent (ttk.Frame): Parent frame for the tab
            app: Main application instance
        """
        super().__init__(parent, app)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the help tab."""
        # Documentation frame
        docs_frame = self.create_frame("docs", "Dokümantasyon")
        
        # User guide button
        self.add_button(
            docs_frame,
            text="Kullanım Kılavuzu",
            command=self._show_user_guide
        )
        
        # FAQ button
        self.add_button(
            docs_frame,
            text="Sık Sorulan Sorular",
            command=self._show_faq
        )
        
        # Support frame
        support_frame = self.create_frame("support", "Destek")
        
        # Feedback button
        self.add_button(
            support_frame,
            text="Geri Bildirim",
            command=self._show_feedback
        )
        
        # Check for updates button
        self.add_button(
            support_frame,
            text="Güncellemeleri Kontrol Et",
            command=self._check_updates
        )
        
        # About frame
        about_frame = self.create_frame("about", "Hakkında")
        
        # About button
        self.add_button(
            about_frame,
            text="miniPDF Hakkında",
            command=self._show_about
        )
    
    def _show_user_guide(self):
        """Show the user guide."""
        # Create a dialog for the user guide
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Kullanım Kılavuzu")
        dialog.geometry("700x500")
        dialog.transient(self.app.root)
        
        # Create a notebook for different sections
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs for different sections
        sections = [
            ("Başlangıç", self._get_getting_started_content()),
            ("PDF Açma ve Kaydetme", self._get_file_operations_content()),
            ("Sayfa İşlemleri", self._get_page_operations_content()),
            ("Metin İşlemleri", self._get_text_operations_content()),
            ("Birleştirme ve Bölme", self._get_merge_split_content()),
            ("Güvenlik", self._get_security_content())
        ]
        
        for title, content in sections:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=title)
            
            # Add a text widget for the content
            text = tk.Text(frame, wrap=tk.WORD, padx=10, pady=10)
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
            text.configure(yscrollcommand=scrollbar.set)
            
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Insert the content
            text.insert(tk.END, content)
            text.config(state=tk.DISABLED)
        
        # Add a close button
        ttk.Button(
            dialog,
            text="Kapat",
            command=dialog.destroy
        ).pack(pady=10)
    
    def _get_getting_started_content(self):
        """Get the content for the getting started section."""
        return """# miniPDF Kullanım Kılavuzu - Başlangıç

miniPDF, PDF dosyalarını görüntülemenizi, düzenlemenizi ve yönetmenizi sağlayan kullanımı kolay bir uygulamadır.

## Başlarken

1. Uygulamayı başlatın
2. "Dosya" sekmesinden "PDF Aç" düğmesine tıklayarak bir PDF dosyası açın
3. PDF içeriği ana görüntüleme alanında gösterilecektir
4. Sayfa numaraları alt kısımda gösterilir ve sayfalar arasında gezinmek için kullanılabilir

## Arayüz Tanıtımı

- **Şerit Menü**: Üst kısımda bulunan sekmeli menü, tüm işlevlere erişim sağlar
- **Görüntüleme Alanı**: PDF içeriğinin gösterildiği ana alan
- **Durum Çubuğu**: Alt kısımda bulunan, sayfa numarası ve yakınlaştırma bilgilerini gösteren çubuk
"""
    
    def _get_file_operations_content(self):
        """Get the content for the file operations section."""
        return """# PDF Açma ve Kaydetme

## PDF Dosyası Açma

1. "Dosya" sekmesindeki "PDF Aç" düğmesine tıklayın
2. Dosya seçim penceresinden bir PDF dosyası seçin
3. PDF dosyası ana görüntüleme alanında açılacaktır

## PDF Dosyası Kaydetme

1. "Dosya" sekmesindeki "PDF Kaydet" düğmesine tıklayın
2. Eğer dosya daha önce kaydedilmişse, aynı konuma kaydedilecektir
3. Eğer yeni bir dosya ise veya "Farklı Kaydet" seçeneğini kullanıyorsanız, kayıt konumunu seçmeniz istenecektir

## PDF Dosyasını Farklı Kaydetme

1. "Dosya" sekmesindeki "Farklı Kaydet" düğmesine tıklayın
2. Dosya seçim penceresinden kayıt konumunu ve dosya adını belirleyin
3. "Kaydet" düğmesine tıklayın

## PDF Dosyasını Dışa Aktarma

1. "Dosya" sekmesindeki "Dışa Aktar" bölümünden istediğiniz formatı seçin
2. Kayıt konumunu ve dosya adını belirleyin
3. "Kaydet" düğmesine tıklayın
"""
    
    def _get_page_operations_content(self):
        """Get the content for the page operations section."""
        return """# Sayfa İşlemleri

## Sayfalar Arasında Gezinme

- Durum çubuğundaki sayfa numaralarını kullanarak sayfalar arasında gezinebilirsiniz
- Klavyeden Sağ/Sol ok tuşlarını kullanarak sonraki/önceki sayfaya geçebilirsiniz
- Klavyeden Page Up/Page Down tuşlarını kullanarak sayfalar arasında hızlıca gezinebilirsiniz

## Sayfa Silme

1. Silmek istediğiniz sayfaya gidin
2. "Sayfa" sekmesindeki "Sayfayı Sil" düğmesine tıklayın
3. Onay penceresinde "Evet" seçeneğini tıklayın

## Boş Sayfa Ekleme

1. "Sayfa" sekmesindeki "Boş Sayfa Ekle" düğmesine tıklayın
2. Boş sayfa, mevcut sayfanın sonuna eklenecektir

## Sayfa Döndürme

1. Döndürmek istediğiniz sayfaya gidin
2. "Sayfa" sekmesindeki "Sayfayı Döndür" düğmesine tıklayın
3. Açılan pencereden döndürme açısını seçin (90°, 180° veya 270°)
4. "Uygula" düğmesine tıklayın

## Sayfa Çıkartma

1. Çıkartmak istediğiniz sayfaya gidin
2. "Sayfa" sekmesindeki "Sayfayı Çıkart" düğmesine tıklayın
3. Kayıt konumunu ve dosya adını belirleyin
4. "Kaydet" düğmesine tıklayın
"""
    
    def _get_text_operations_content(self):
        """Get the content for the text operations section."""
        return """# Metin İşlemleri

## Metin Çıkartma

1. "Düzenleme" sekmesindeki "Metin Çıkart" düğmesine tıklayın
2. Açılan pencereden çıkartma kapsamını seçin (mevcut sayfa veya tüm belge)
3. "Çıkart" düğmesine tıklayın
4. Çıkartılan metin pencerede gösterilecektir
5. Metni kopyalamak veya kaydetmek için ilgili düğmeleri kullanabilirsiniz

## Metin Ekleme

1. "Düzenleme" sekmesindeki "Metin Ekle" düğmesine tıklayın
2. Açılan pencereden metin eklemek istediğiniz konumu belirleyin
3. Metni girin ve formatını ayarlayın
4. "Uygula" düğmesine tıklayın

## Metin Vurgulama

1. "Düzenleme" sekmesindeki "Metni Vurgula" düğmesine tıklayın
2. Açılan pencereden vurgulamak istediğiniz metni seçin
3. Vurgulama rengini ve stilini ayarlayın
4. "Uygula" düğmesine tıklayın
"""
    
    def _get_merge_split_content(self):
        """Get the content for the merge and split section."""
        return """# Birleştirme ve Bölme

## PDF Dosyalarını Birleştirme

1. "Araçlar" sekmesindeki "PDF'leri Birleştir" düğmesine tıklayın
2. Açılan pencereden birleştirmek istediğiniz PDF dosyalarını seçin
3. Dosyaları sürükleyerek veya "Yukarı Taşı" ve "Aşağı Taşı" düğmelerini kullanarak sıralayın
4. "PDF'leri Birleştir" düğmesine tıklayın
5. Kayıt konumunu ve dosya adını belirleyin
6. "Kaydet" düğmesine tıklayın

## PDF Dosyasını Bölme

1. Bölmek istediğiniz PDF dosyasını açın
2. "Araçlar" sekmesindeki "PDF'i Böl" düğmesine tıklayın
3. Açılan pencereden bölme yöntemini seçin:
   - "Eşit Sayıda Sayfaya Böl": Her dosyada belirli sayıda sayfa olacak şekilde böler
   - "Belirli Sayfa Aralıklarına Böl": Belirttiğiniz sayfa aralıklarına göre böler
4. Bölme seçeneklerini ayarlayın
5. Çıktı dizinini belirleyin
6. "PDF'i Böl" düğmesine tıklayın
"""
    
    def _get_security_content(self):
        """Get the content for the security section."""
        return """# Güvenlik

## PDF Dosyasını Şifreleme

1. "Araçlar" sekmesindeki "PDF'i Şifrele" düğmesine tıklayın
2. Açılan pencereden kullanıcı şifresini girin (PDF'i açmak için gerekli)
3. İsteğe bağlı olarak sahip şifresini girin (PDF'i düzenlemek için gerekli)
4. "Şifrele" düğmesine tıklayın

## PDF Dosyasının Şifresini Çözme

1. Şifreli PDF dosyasını açın
2. "Araçlar" sekmesindeki "PDF Şifresini Çöz" düğmesine tıklayın
3. Açılan pencereden şifreyi girin
4. "Şifreyi Çöz" düğmesine tıklayın
"""
    
    def _show_faq(self):
        """Show the FAQ."""
        # Create a dialog for the FAQ
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Sık Sorulan Sorular")
        dialog.geometry("600x400")
        dialog.transient(self.app.root)
        
        # Create a frame for the FAQ
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a text widget for the FAQ
        text = tk.Text(frame, wrap=tk.WORD, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Insert the FAQ content
        faq_content = """# Sık Sorulan Sorular

## Genel Sorular

### miniPDF nedir?
miniPDF, PDF dosyalarını görüntülemenizi, düzenlemenizi ve yönetmenizi sağlayan kullanımı kolay bir uygulamadır.

### miniPDF hangi işletim sistemlerinde çalışır?
miniPDF, Windows, macOS ve Linux işletim sistemlerinde çalışır.

### miniPDF ücretsiz mi?
Evet, miniPDF tamamen ücretsiz ve açık kaynaklı bir uygulamadır.

## Teknik Sorular

### Hangi PDF sürümleri destekleniyor?
miniPDF, PDF 1.0 ile 1.7 arasındaki tüm PDF sürümlerini destekler.

### Şifreli PDF dosyalarını açabilir miyim?
Evet, şifreli PDF dosyalarını açabilirsiniz. Dosyayı açarken şifre girmeniz istenecektir.

### PDF dosyalarını birleştirirken dosya boyutu sınırı var mı?
Hayır, teorik olarak bir sınır yoktur, ancak çok büyük dosyaları birleştirirken bilgisayarınızın performansına bağlı olarak işlem süresi uzayabilir.

## Sorun Giderme

### PDF dosyası açılmıyor, ne yapmalıyım?
1. Dosyanın bozuk olmadığından emin olun
2. Dosyanın şifreli olup olmadığını kontrol edin
3. Dosyayı başka bir PDF görüntüleyicide açmayı deneyin
4. Hala sorun yaşıyorsanız, destek ekibimizle iletişime geçin

### Programı güncellerken hata alıyorum, ne yapmalıyım?
1. İnternet bağlantınızı kontrol edin
2. Güvenlik duvarı veya antivirüs programınızın güncellemeyi engellemediğinden emin olun
3. Programı kapatıp yeniden açmayı deneyin
4. Hala sorun yaşıyorsanız, web sitemizden manuel olarak güncellemeyi indirin

### PDF dosyasını kaydederken hata alıyorum, ne yapmalıyım?
1. Kaydetmeye çalıştığınız konumda yazma izninizin olduğundan emin olun
2. Dosyanın başka bir program tarafından kullanılmadığından emin olun
3. Farklı bir konuma kaydetmeyi deneyin
4. Hala sorun yaşıyorsanız, destek ekibimizle iletişime geçin
"""
        
        text.insert(tk.END, faq_content)
        text.config(state=tk.DISABLED)
        
        # Add a close button
        ttk.Button(
            dialog,
            text="Kapat",
            command=dialog.destroy
        ).pack(pady=10)
    
    def _show_feedback(self):
        """Show the feedback form."""
        # Create a dialog for the feedback form
        dialog = tk.Toplevel(self.app.root)
        dialog.title("Geri Bildirim")
        dialog.geometry("500x400")
        dialog.transient(self.app.root)
        dialog.grab_set()
        
        # Create a frame for the feedback form
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a label
        ttk.Label(
            frame,
            text="Geri bildiriminiz için teşekkür ederiz!",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Add name field
        name_frame = ttk.Frame(frame)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            name_frame,
            text="Adınız:",
            width=15
        ).pack(side=tk.LEFT)
        
        name_var = tk.StringVar()
        ttk.Entry(
            name_frame,
            textvariable=name_var,
            width=30
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add email field
        email_frame = ttk.Frame(frame)
        email_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            email_frame,
            text="E-posta:",
            width=15
        ).pack(side=tk.LEFT)
        
        email_var = tk.StringVar()
        ttk.Entry(
            email_frame,
            textvariable=email_var,
            width=30
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add feedback type field
        type_frame = ttk.Frame(frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            type_frame,
            text="Geri Bildirim Türü:",
            width=15
        ).pack(side=tk.LEFT)
        
        feedback_type_var = tk.StringVar(value="feature")
        feedback_type_combo = ttk.Combobox(
            type_frame,
            textvariable=feedback_type_var,
            values=["Özellik İsteği", "Hata Bildirimi", "Öneri", "Diğer"],
            state="readonly",
            width=28
        )
        feedback_type_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add feedback content field
        content_frame = ttk.LabelFrame(frame, text="Geri Bildirim İçeriği")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        feedback_content = tk.Text(content_frame, wrap=tk.WORD, height=10)
        content_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=feedback_content.yview)
        feedback_content.configure(yscrollcommand=content_scrollbar.set)
        
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        feedback_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add buttons frame
        buttons_frame = ttk.Frame(dialog)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Add send button
        ttk.Button(
            buttons_frame,
            text="Gönder",
            command=lambda: self._send_feedback(
                dialog,
                name_var.get(),
                email_var.get(),
                feedback_type_var.get(),
                feedback_content.get(1.0, tk.END)
            )
        ).pack(side=tk.RIGHT, padx=5)
        
        # Add cancel button
        ttk.Button(
            buttons_frame,
            text="İptal",
            command=dialog.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def _send_feedback(self, dialog, name, email, feedback_type, feedback_content):
        """
        Send the feedback.
        
        Args:
            dialog (tk.Toplevel): Dialog window
            name (str): User name
            email (str): User email
            feedback_type (str): Type of feedback
            feedback_content (str): Feedback content
        """
        # Validate the input
        if not name or not email or not feedback_content.strip():
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return
        
        # Here you would normally send the feedback to a server
        # For now, just show a success message
        messagebox.showinfo("Başarılı", "Geri bildiriminiz için teşekkür ederiz! En kısa sürede değerlendireceğiz.")
        
        # Close the dialog
        dialog.destroy()
    
    def _check_updates(self):
        """Check for updates."""
        # Here you would normally check for updates from a server
        # For now, just show a message
        messagebox.showinfo("Güncellemeler", "miniPDF'in en son sürümünü kullanıyorsunuz.")
    
    def _show_about(self):
        """Show information about the application."""
        # Create a dialog for the about information
        dialog = tk.Toplevel(self.app.root)
        dialog.title("miniPDF Hakkında")
        dialog.geometry("400x300")
        dialog.transient(self.app.root)
        
        # Create a frame for the about information
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add the application name
        ttk.Label(
            frame,
            text="miniPDF",
            font=("Arial", 16, "bold")
        ).pack(pady=5)
        
        # Add the version
        ttk.Label(
            frame,
            text="Sürüm 1.0.0"
        ).pack()
        
        # Add the description
        ttk.Label(
            frame,
            text="PDF görüntüleme, düzenleme ve yönetme uygulaması",
            wraplength=300
        ).pack(pady=10)
        
        # Add the copyright
        ttk.Label(
            frame,
            text="© 2025 miniPDF Geliştirici Ekibi"
        ).pack(pady=5)
        
        # Add the license
        ttk.Label(
            frame,
            text="Bu uygulama MIT lisansı altında dağıtılmaktadır.",
            wraplength=300
        ).pack(pady=5)
        
        # Add a link to the website
        website_frame = ttk.Frame(frame)
        website_frame.pack(pady=10)
        
        ttk.Label(
            website_frame,
            text="Web sitesi:"
        ).pack(side=tk.LEFT)
        
        website_link = ttk.Label(
            website_frame,
            text="www.minipdf.com",
            foreground="blue",
            cursor="hand2"
        )
        website_link.pack(side=tk.LEFT, padx=5)
        website_link.bind("<Button-1>", lambda e: webbrowser.open("http://www.minipdf.com"))
        
        # Add a close button
        ttk.Button(
            dialog,
            text="Kapat",
            command=dialog.destroy
        ).pack(pady=10)
