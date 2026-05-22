import geocoder
import requests
import sys
from datetime import *
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

base_url = "https://api.aladhan.com/v1"
now = datetime.now()
date = now.strftime("%d-%m-%Y")


class Salah(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sulatk")
        self.setGeometry(0, 0, 320, 400)
        self.setStyleSheet(
            "background-color: #1a1a1a;")
        self.setWindowFlags(Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.get_prayer()
        self.UI()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.pos() - self.offset
            self.move(self.pos() + delta)

    def get_prayer(self):
        g = geocoder.ip('me')
        city = g.city
        country = g.country

        url = f"{base_url}/timingsByCity/{date}?city={city.lower().strip()}&country={country.lower().strip()}"

        try:
            response = requests.get(url, timeout=50)
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Couldn't retrieve data, failed: {e}")

        data = response.json()
        prayer = data["data"]["timings"]
        hijri = data["data"]["date"]["hijri"]

        self.fajr = prayer["Fajr"]
        self.dhuhr = prayer["Dhuhr"]
        self.asr = prayer["Asr"]
        self.maghrib = prayer["Maghrib"]
        self.isha = prayer["Isha"]

        self.hijri_month = hijri["month"]["ar"]
        self.hijri_day = hijri["day"]
        self.hijri_year = hijri["year"]

    def UI(self):
        main_layout = QVBoxLayout(self)
        date_group = QGroupBox()
        date_group.setStyleSheet("""
        border:none;
        border-bottom:2px solid #1c1c1c;
        """)
        date_layout = QHBoxLayout()
        hijri_date = QLabel(f"{self.hijri_day} {self.hijri_month} {self.hijri_year} هـ")
        hijri_date.setAlignment(Qt.AlignHCenter)
        hijri_date.setStyleSheet("""
        color:#ffd700;
        font-weight:bold;
        font-family:'IBM Plex Sans Arabic';
        font-size:18px;
        """)
        date_layout.addWidget(hijri_date)
        date_group.setLayout(date_layout)

        salah_group = QGroupBox()
        salah_group.setStyleSheet("""
        border:none;
        """)
        salah_layout = QVBoxLayout()
        salah_layout.setSpacing(10)

        def salah_card(text, time):
            container = QWidget()
            layout = QHBoxLayout(container)
            name = QLabel(text)
            prayer_time = QLabel(time)
            name.setStyleSheet("""
                color:#ffffff;
                font-family:'IBM Plex Sans Arabic';
                font-size:16px;
                font-weight:600;
            """)
            prayer_time.setStyleSheet("""
                color:#ffffff;
                font-family:'IBM Plex Sans Arabic';
                font-size:16px;
                font-weight:600;
            """)
            layout.addWidget(name)
            layout.addStretch()
            layout.addWidget(prayer_time)
            layout.setContentsMargins(10,10,10,10)
            return container

        salah_layout.addWidget(salah_card("صلاة الفجر", self.fajr))
        salah_layout.addWidget(salah_card("صلاة الظهر", self.dhuhr))
        salah_layout.addWidget(salah_card("صلاة العصر", self.asr))
        salah_layout.addWidget(salah_card("صلاة المغرب", self.maghrib))
        salah_layout.addWidget(salah_card("صلاة العشاء", self.isha))
        salah_group.setLayout(salah_layout)

        main_layout.addWidget(date_group)
        main_layout.addWidget(salah_group)

app = QApplication(sys.argv)
window = Salah()
window.show()
sys.exit(app.exec_())
