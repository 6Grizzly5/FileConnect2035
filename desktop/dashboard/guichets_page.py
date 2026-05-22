from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QFrame,
    QScrollArea
)
from PyQt5.QtGui import QDesktopServices

from PyQt5.QtCore import Qt, QUrl

import requests


class GuichetsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setStyleSheet("""

            QWidget {
                background-color: #f3f6fb;
                color: #1e293b;
                font-size: 14px;
            }

            QLabel {
                color: #1e293b;
            }

            QPushButton {
                border: none;
                border-radius: 12px;
                padding: 10px 16px;
                font-weight: bold;
            }

        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(20)

        # =========================
        # HEADER
        # =========================

        header_layout = QHBoxLayout()

        self.title = QLabel("Gestion des Guichets")
        self.title.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #0f172a;
        """)

        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.btn_refresh = QPushButton("⟳")
        self.btn_refresh.setFixedSize(50, 50)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: white;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)
        self.btn_refresh.clicked.connect(self.load_guichets)

        self.btn_add = QPushButton("+ Ajouter")
        self.btn_add.setFixedHeight(50)
        self.btn_add.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                padding-left: 20px;
                padding-right: 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
        """)
        self.btn_add.clicked.connect(self.add_guichet)

        header_layout.addWidget(self.btn_refresh)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.btn_add)

        self.layout.addLayout(header_layout)

        # =========================
        # SCROLL AREA
        # =========================

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)

        self.container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setSpacing(15)
        self.container.setLayout(self.cards_layout)
        self.scroll.setWidget(self.container)

        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)

        self.load_guichets()

    # ==================================
    # LOAD GUICHETS
    # ==================================

    def load_guichets(self):

        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        try:
            response = requests.get('http://127.0.0.1:5000/guichets')
            data = response.json()
            for g in data:
                self.create_card(g)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    # ==================================
    # CARD
    # ==================================

    def create_card(self, g):

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 18px;
                border: 1px solid #dbe4f0;
            }
        """)

        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(25, 20, 25, 20)

        # =========================
        # INFOS
        # =========================

        infos_layout = QVBoxLayout()

        title = QLabel(f"Guichet {g['numero']}")
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #0f172a;
        """)

        statut = QLabel(f"Statut : {g['statut']}")
        statut.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)

        infos_layout.addWidget(title)
        infos_layout.addWidget(statut)

        url_guichet = (
            f"http://192.168.43.26:5000/"
            f"guichet/{g['id_agence']}/{g['id']}"
        )

        url_label = QLabel(url_guichet)
        url_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #2563eb;
                background-color: #eff6ff;
                padding: 8px;
                border-radius: 10px;
            }
        """)
        url_label.setWordWrap(True)
        url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        infos_layout.addWidget(url_label)
        card_layout.addLayout(infos_layout)
        card_layout.addStretch()

        # =========================
        # BTN COPIER  — bleu clair
        # =========================

        btn_copy = QPushButton("Copier URL")
        btn_copy.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        btn_copy.clicked.connect(lambda: self.copy_url(url_guichet))

        # =========================
        # BTN OUVRIR  — bleu indigo
        # =========================

        btn_open = QPushButton("Ouvrir")
        btn_open.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        btn_open.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(url_guichet))
        )

        # =========================
        # BTN DISPONIBLE
        # =========================

        btn_dispo = QPushButton("Disponible")
        btn_dispo.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
        """)
        btn_dispo.clicked.connect(
            lambda: self.change_status(g['id'], 'disponible')
        )

        # =========================
        # BTN PAUSE
        # =========================

        btn_pause = QPushButton("Pause")
        btn_pause.setStyleSheet("""
            QPushButton {
                background-color: #e2e8f0;
                color: #1e293b;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #cbd5e1;
            }
        """)
        btn_pause.clicked.connect(
            lambda: self.change_status(g['id'], 'pause')
        )

        # =========================
        # BTN DELETE
        # =========================

        btn_delete = QPushButton("Supprimer")
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #f87171;
            }
        """)
        btn_delete.clicked.connect(lambda: self.delete_guichet(g['id']))

        card_layout.addWidget(btn_copy)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_open)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_dispo)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_pause)
        card_layout.addSpacing(10)
        card_layout.addWidget(btn_delete)

        card.setLayout(card_layout)
        self.cards_layout.addWidget(card)

    # ==================================
    # COPY URL
    # ==================================

    def copy_url(self, url):
        clipboard = QApplication.clipboard()
        clipboard.setText(url)
        QMessageBox.information(self, "URL copiée", "Lien du guichet copié.")

    # ==================================
    # AJOUT
    # ==================================

    def add_guichet(self):

        try:
            agence_resp = requests.get('http://127.0.0.1:5000/get_agence')
            agence = agence_resp.json()
            id_agence = agence.get('id')

            response = requests.post(
                'http://127.0.0.1:5000/add_guichet',
                json={'id_agence': id_agence}
            )

            if response.ok:
                self.load_guichets()
            else:
                QMessageBox.warning(self, "Erreur", response.text)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    # ==================================
    # STATUS
    # ==================================

    def change_status(self, id_guichet, statut):

        try:
            requests.put(
                f'http://127.0.0.1:5000/guichet/{id_guichet}/status',
                json={'statut': statut}
            )
            self.load_guichets()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    # ==================================
    # DELETE
    # ==================================

    def delete_guichet(self, id_guichet):

        reply = QMessageBox.question(
            self, "Confirmation", "Supprimer ce guichet ?"
        )

        if reply != QMessageBox.Yes:
            return

        try:
            requests.delete(f'http://127.0.0.1:5000/guichet/{id_guichet}')
            self.load_guichets()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))