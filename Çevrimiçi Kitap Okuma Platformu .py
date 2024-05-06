import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QMessageBox
import sqlite3

# Veritabanı sınıfı tanımı
class Veritabani:
    def __init__(self, dosya):
        # Veritabanı dosyasını belirle ve bağlantıyı oluştur
        self.dosya = dosya
        self.baglanti = sqlite3.connect(dosya)
        self.cursor = self.baglanti.cursor()

    # Tabloları oluştur
    def tablo_olustur(self):
        # kullanicilar, kitaplar ve yorumlar tablolarını oluştur
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
                                kullanici_adi TEXT PRIMARY KEY,
                                sifre TEXT
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kitaplar (
                                kitap_adi TEXT PRIMARY KEY,
                                yazar TEXT,
                                yayinevi TEXT
                                )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS yorumlar (
                                kullanici_adi TEXT,
                                yorum TEXT,
                                FOREIGN KEY (kullanici_adi) REFERENCES kullanicilar(kullanici_adi)
                                )''')
        self.baglanti.commit()

    # Kullanıcı ekleme metodu
    def kullanici_ekle(self, kullanici_adi, sifre):
        # Kullanıcı ekleme sorgusu
        self.cursor.execute("INSERT INTO kullanicilar VALUES (?, ?)", (kullanici_adi, sifre))
        self.baglanti.commit()

    # Kitap ekleme metodu
    def kitap_ekle(self, kitap_adi, yazar, yayinevi):
        # Kitap ekleme sorgusu
        self.cursor.execute("INSERT INTO kitaplar VALUES (?, ?, ?)", (kitap_adi, yazar, yayinevi))
        self.baglanti.commit()

    # Yorum ekleme metodu
    def yorum_ekle(self, kullanici_adi, yorum):
        # Yorum ekleme sorgusu
        self.cursor.execute("INSERT INTO yorumlar VALUES (?, ?)", (kullanici_adi, yorum))
        self.baglanti.commit()

    # Giriş kontrolü metodu
    def giris_kontrol(self, kullanici_adi, sifre):
        # Kullanıcı giriş bilgilerini kontrol et
        self.cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
        if self.cursor.fetchone():
            return True
        else:
            return False

# Kitap Okuma Platformu sınıfı tanımı
class KitapOkumaPlatformu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Veritabanı bağlantısı oluştur
        self.veritabani = Veritabani("kitap_okuma_veritabani.db")
        self.veritabani.tablo_olustur()

        # Pencere özelliklerini ayarla
        self.setWindowTitle("Çevrimiçi Kitap Okuma ve Paylaşım Platformu")
        self.setGeometry(100, 100, 600, 400)

        # Merkezi widget oluştur
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Dikey bir düzen oluştur
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Kullanıcı adı giriş kutusu ve etiketi
        self.kullanici_adi_label = QLabel("Kullanıcı Adı:")
        self.layout.addWidget(self.kullanici_adi_label)
        self.kullanici_adi_input = QLineEdit()
        self.layout.addWidget(self.kullanici_adi_input)

        # Şifre giriş kutusu ve etiketi
        self.sifre_label = QLabel("Şifre:")
        self.layout.addWidget(self.sifre_label)
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.sifre_input)

        # Kayıt ol butonu ve işlevi
        self.kayit_ol_button = QPushButton("Kayıt Ol")
        self.kayit_ol_button.clicked.connect(self.kayit_ol)
        self.layout.addWidget(self.kayit_ol_button)

        # Kitap bilgileri giriş kutuları ve etiketleri
        self.kitap_adi_label = QLabel("Kitap Adı:")
        self.layout.addWidget(self.kitap_adi_label)
        self.kitap_adi_input = QLineEdit()
        self.layout.addWidget(self.kitap_adi_input)

        self.yazar_label = QLabel("Yazar:")
        self.layout.addWidget(self.yazar_label)
        self.yazar_input = QLineEdit()
        self.layout.addWidget(self.yazar_input)

        self.yayinevi_label = QLabel("Yayınevi:")
        self.layout.addWidget(self.yayinevi_label)
        self.yayinevi_input = QLineEdit()
        self.layout.addWidget(self.yayinevi_input)

        # Kitap ekle butonu ve işlevi
        self.kitap_ekle_button = QPushButton("Kitap Ekle")
        self.kitap_ekle_button.clicked.connect(self.kitap_ekle)
        self.layout.addWidget(self.kitap_ekle_button)

        # Kitap listesi widget'i
        self.kitaplar_listWidget = QListWidget()
        self.layout.addWidget(self.kitaplar_listWidget)

        # Yorum giriş kutusu ve etiketi
        self.yorum_label = QLabel("Yorumunuz:")
        self.layout.addWidget(self.yorum_label)
        self.yorum_input = QTextEdit()
        self.layout.addWidget(self.yorum_input)

        # Yorum ekle butonu ve işlevi
        self.yorum_ekle_button = QPushButton("Yorum Ekle")
        self.yorum_ekle_button.clicked.connect(self.yorum_ekle)
        self.layout.addWidget(self.yorum_ekle_button)

        # Yorum listesi widget'i
        self.yorumlar_listWidget = QListWidget()
        self.layout.addWidget(self.yorumlar_listWidget)

        # Giriş yap butonu ve işlevi
        self.giris_button = QPushButton("Giriş Yap")
        self.giris_button.clicked.connect(self.giris_yap)
        self.layout.addWidget(self.giris_button)

    # Kayıt ol metodu
    def kayit_ol(self):
        # Kullanıcı adı ve şifre al
        kullanici_adi = self.kullanici_adi_input.text()
        sifre = self.sifre_input.text()
        # Veritabanına kullanıcı ekle
        self.veritabani.kullanici_ekle(kullanici_adi, sifre)
        # Bilgilendirme mesajı göster
        QMessageBox.information(self, "Bilgi", "Kayıt Başarılı!")

    # Kitap ekle metodu
    def kitap_ekle(self):
        # Kitap bilgilerini al
        kitap_adi = self.kitap_adi_input.text()
        yazar = self.yazar_input.text()
        yayinevi = self.yayinevi_input.text()
        # Veritabanına kitap ekle
        self.veritabani.kitap_ekle(kitap_adi, yazar, yayinevi)
        # Kitap listesine yeni kitabı ekle
        self.kitaplar_listWidget.addItem(kitap_adi)
        # Bilgilendirme mesajı göster
        QMessageBox.information(self, "Bilgi", f"{kitap_adi} kitabı eklendi.")

    # Yorum ekle metodu
    def yorum_ekle(self):
        # Kullanıcı adını ve yorumu al
        kullanici_adi = self.kullanici_adi_input.text()
        yorum = self.yorum_input.toPlainText()
        # Veritabanına yorumu ekle
        self.veritabani.yorum_ekle(kullanici_adi, yorum)
        # Yorum listesini temizle
        self.yorumlar_listWidget.clear()
        # Tüm yorumları al ve listeye ekle
        yorumlar = self.veritabani.cursor.execute("SELECT * FROM yorumlar").fetchall()
        for kullanici, yorum_metni in yorumlar:
            item = QListWidgetItem(f"{kullanici}: {yorum_metni}")
            self.yorumlar_listWidget.addItem(item)
        # Bilgilendirme mesajı göster
        QMessageBox.information(self, "Bilgi", "Yorum Eklendi.")

    # Giriş yap metodu
    def giris_yap(self):
        # Kullanıcı adını ve şifreyi al
        kullanici_adi = self.kullanici_adi_input.text()
        sifre = self.sifre_input.text()
        # Kullanıcı giriş bilgilerini kontrol et
        if self.veritabani.giris_kontrol(kullanici_adi, sifre):
            QMessageBox.information(self, "Bilgi", "Giriş Başarılı!")
        else:
            QMessageBox.warning(self, "Uyarı", "Kullanıcı adı veya şifre yanlış!")

# Ana program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KitapOkumaPlatformu()
    window.show()
    sys.exit(app.exec_())
