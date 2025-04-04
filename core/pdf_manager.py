"""
PDF Manager module for handling PDF operations like page deletion, addition, and saving.
"""
import pymupdf as fitz
import os
import tempfile
import shutil
import logging
import time
from contextlib import contextmanager

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFManager:
    """Class for managing PDF documents."""

    def __init__(self):
        """Initialize the PDF manager."""
        self.doc = None
        self.file_path = None
        self.current_file = None

    def open_pdf(self, file_path):
        """Open a PDF file.

        Args:
            file_path (str): Path to the PDF file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.doc:
                self.close()
            self.doc = fitz.open(file_path)
            self.file_path = file_path
            self.current_file = file_path
            return True
        except Exception as e:
            logger.error(f"Error opening PDF: {e}")
            return False

    def get_page_count(self):
        """Get the number of pages in the PDF.

        Returns:
            int: Number of pages or 0 if no document is open
        """
        if self.doc:
            return len(self.doc)
        return 0

    def get_page(self, page_index):
        """Get a specific page from the PDF.

        Args:
            page_index (int): Index of the page to get

        Returns:
            Page: PyMuPDF Page object or None if invalid
        """
        if self.doc and 0 <= page_index < len(self.doc):
            return self.doc[page_index]
        return None

    def get_page_thumbnail(self, page_index):
        """Get a thumbnail of a specific page.

        Args:
            page_index (int): Index of the page to get thumbnail for

        Returns:
            QPixmap: Thumbnail of the page or None if invalid
        """
        if not self.doc or not (0 <= page_index < len(self.doc)):
            return None

        try:
            from PyQt6.QtGui import QPixmap, QImage
            page = self.doc[page_index]
            # Set zoom matrix for thumbnail size (120x160 target size)
            zoom = min(120 / page.rect.width, 160 / page.rect.height)
            matrix = fitz.Matrix(zoom, zoom)
            # Render page to pixmap
            pix = page.get_pixmap(matrix=matrix)
            # Convert to QImage then QPixmap
            img = QImage(pix.samples, pix.width, pix.height,
                        pix.stride, QImage.Format.Format_RGB888)
            return QPixmap.fromImage(img)
        except Exception as e:
            logger.error(f"Error generating thumbnail for page {page_index}: {e}")
            return None

    def get_page_pixmap(self, page_index, zoom=1.0):
        """Get a full resolution pixmap of a specific page.

        Args:
            page_index (int): Index of the page to get pixmap for
            zoom (float, optional): Zoom factor for rendering. Defaults to 1.0.

        Returns:
            QPixmap: Full resolution pixmap of the page or None if invalid
        """
        if not self.doc or not (0 <= page_index < len(self.doc)):
            return None

        try:
            from PyQt6.QtGui import QPixmap, QImage
            page = self.doc[page_index]
            # Create matrix with zoom factor
            matrix = fitz.Matrix(zoom, zoom)
            # Render page to pixmap
            pix = page.get_pixmap(matrix=matrix)
            # Convert to QImage then QPixmap
            img = QImage(pix.samples, pix.width, pix.height,
                        pix.stride, QImage.Format.Format_RGB888)
            return QPixmap.fromImage(img)
        except Exception as e:
            logger.error(f"Error generating pixmap for page {page_index}: {e}")
            return None

    @contextmanager
    def _create_temp_doc(self):
        """Context manager to create a temporary document and handle cleanup.

        Yields:
            fitz.Document: A new temporary PDF document
        """
        temp_doc = fitz.open()
        try:
            yield temp_doc
        finally:
            if temp_doc:
                temp_doc.close()

    def delete_page(self, page_index):
        """Delete a page from the PDF.

        Args:
            page_index (int): Index of the page to delete

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc or not (0 <= page_index < len(self.doc)):
            return False

        try:
            # Create a new document without the specified page
            with self._create_temp_doc() as new_doc:
                for i in range(len(self.doc)):
                    if i != page_index:
                        new_doc.insert_pdf(self.doc, from_page=i, to_page=i)

                # Save to a temporary file
                temp_fd, temp_path = tempfile.mkstemp(suffix=".pdf")
                os.close(temp_fd)
                new_doc.save(temp_path)

            # Close the current document
            self.doc.close()

            # Open the new document
            self.doc = fitz.open(temp_path)

            # Clean up the temporary file
            os.unlink(temp_path)

            return True
        except Exception as e:
            logger.error(f"Error deleting page: {e}")
            return False

    def save_pdf(self, save_path=None):
        """Save the PDF to a file.

        Args:
            save_path (str, optional): Path to save the PDF. If None, uses the original path.

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.doc:
            return False

        try:
            path = save_path if save_path else self.file_path
            current_path = os.path.abspath(path)

            # Create a temporary file
            fd, temp_path = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)

            try:
                # Save to the temporary file with cleanup options
                # garbage=4: agresif PDF temizleme (xref tablosunu yeniden oluşturur)
                # deflate=True: içeriği sıkıştırır ve dosya boyutunu küçültür
                self.doc.save(temp_path, garbage=4, deflate=True, clean=True)
            except Exception as e:
                logger.warning(f"PDF kaydetme hatası, onarım deneniyor: {e}")
                # Onarım için yeni bir belge oluşturup sayfaları kopyalama
                try:
                    repair_doc = fitz.open()
                    for page_num in range(len(self.doc)):
                        try:
                            repair_doc.insert_pdf(self.doc, from_page=page_num, to_page=page_num)
                        except Exception as page_error:
                            logger.warning(f"Sayfa {page_num} kopyalanamadı: {page_error}")
                    repair_doc.save(temp_path, garbage=4, deflate=True, clean=True)
                    repair_doc.close()
                except Exception as repair_error:
                    logger.error(f"PDF onarım hatası: {repair_error}")
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    raise repair_error

            # Hedef dosya yolunu kontrol et
            if os.path.exists(current_path):
                # Dosya zaten varsa, yedek oluştur
                backup_fd, backup_path = tempfile.mkstemp(suffix=".pdf.bak")
                os.close(backup_fd)

                # Yedekleme işlemi - dosya kullanımda hatası için yeniden deneme
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        shutil.copy2(current_path, backup_path)
                        break
                    except PermissionError as pe:
                        if attempt < max_attempts - 1:
                            logger.warning(f"Dosya kullanımda, {attempt+1}. deneme: {pe}")
                            time.sleep(1)  # Kısa bir bekleme
                        else:
                            logger.error(f"Yedekleme başarısız, dosya kullanımda: {pe}")
                            if os.path.exists(temp_path):
                                os.unlink(temp_path)
                            if os.path.exists(backup_path):
                                os.unlink(backup_path)
                            return False
            else:
                backup_path = None

            try:
                # Belgeyi kapatmadan önce referansını saklayalım
                doc_path = self.doc.name

                # Belgeyi şimdi kapatıyoruz
                self.doc.close()

                # Hedef dosyaya taşıma - dosya kullanımda hatası için yeniden deneme
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        # Hedef dosya varsa ve kullanımdaysa, alternatif strateji kullan
                        if os.path.exists(current_path):
                            # Önce hedef dosyayı silmeyi dene
                            try:
                                os.unlink(current_path)
                            except PermissionError:
                                # Dosya silinemiyorsa, farklı bir isimle kaydet
                                alt_path = f"{current_path}.new"
                                shutil.move(temp_path, alt_path)
                                temp_path = alt_path
                                # Dosya kullanımda uyarısı
                                logger.warning(f"Hedef dosya kullanımda, alternatif kaydetme: {alt_path}")

                        # Geçici dosyayı hedefe taşı
                        shutil.move(temp_path, current_path)
                        break
                    except PermissionError as pe:
                        if attempt < max_attempts - 1:
                            logger.warning(f"Dosya taşıma hatası, {attempt+1}. deneme: {pe}")
                            time.sleep(1)  # Kısa bir bekleme
                        else:
                            logger.error(f"Dosya taşıma başarısız, dosya kullanımda: {pe}")
                            # Yedek varsa geri yükle
                            if backup_path and os.path.exists(backup_path):
                                self.doc = fitz.open(backup_path)
                                if os.path.exists(temp_path):
                                    os.unlink(temp_path)
                            return False

                # Belgeyi yeniden aç
                self.doc = fitz.open(current_path)

                # İşlem başarılıysa yedeği sil
                if backup_path and os.path.exists(backup_path):
                    try:
                        os.unlink(backup_path)
                    except:
                        pass  # Yedek silinmezse önemli değil

                if save_path:  # Update file path if saving to a new location
                    self.file_path = save_path

                return True
            except Exception as e:
                # Hata durumunda yedeği geri yükle
                if backup_path and os.path.exists(backup_path):
                    try:
                        if os.path.exists(current_path):
                            os.unlink(current_path)
                        shutil.move(backup_path, current_path)
                    except:
                        logger.error(f"Yedek geri yükleme hatası: {e}")

                # Orijinal belgeyi yeniden açmayı dene
                if self.file_path:
                    try:
                        self.doc = fitz.open(self.file_path)
                    except Exception as reopen_error:
                        logger.error(f"Orijinal belgeyi yeniden açma hatası: {reopen_error}")

                # Geçici dosyaları temizle
                for path in [temp_path, backup_path]:
                    if path and os.path.exists(path):
                        try:
                            os.unlink(path)
                        except:
                            pass

                raise e

        except Exception as e:
            logger.error(f"Error saving PDF: {e}")
            return False

    def close(self):
        """Close the current PDF document."""
        if self.doc:
            self.doc.close()
            self.doc = None
            self.file_path = None
            self.current_file = None