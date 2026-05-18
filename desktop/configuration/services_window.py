from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from PyQt5.QtCore import Qt

import requests


class ServicesWindow(QWidget):

    def __init__(self, id_agence):

        super().__init__()

        self.id_agence = id_agence

        self.setWindowTitle(
            "Ajout Services"
        )

        self.resize(500, 500)

        # =========================
        # STYLE
        # =========================

        self.setStyleSheet("""

            QWidget {
                background-color: #0f172a;
                color: white;
                font-size: 15px;
            }

            QLabel {
                margin-top: 10px;
                color: #cbd5e1;
            }

            QLineEdit {
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #38bdf8;
            }

            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 12px;
                padding: 14px;
                color: white;
                font-weight: bold;
                margin-top: 20px;
            }

            QPushButton:hover {
                background-color: #3b82f6;
            }

        """)

        # =========================
        # LAYOUT
        # =========================

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            40,
            40,
            40,
            40
        )

        self.layout.setSpacing(10)

        # =========================
        # TITRE
        # =========================

        self.title = QLabel(
            "Ajout des Services"
        )

        self.title.setStyleSheet("""

            font-size: 28px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;

        """)

        self.layout.addWidget(
            self.title,
            alignment=Qt.AlignCenter
        )

        # =========================
        # NOM SERVICE
        # =========================

        self.label_service = QLabel(
            "Nom Service"
        )

        self.input_service = QLineEdit()

        self.input_service.setPlaceholderText(
            "Ex: Dépôt"
        )

        self.layout.addWidget(
            self.label_service
        )

        self.layout.addWidget(
            self.input_service
        )

        # =========================
        # DUREE
        # =========================

        self.label_duree = QLabel(
            "Durée moyenne"
        )

        self.input_duree = QLineEdit()

        self.input_duree.setPlaceholderText(
            "Ex: 10"
        )

        self.layout.addWidget(
            self.label_duree
        )

        self.layout.addWidget(
            self.input_duree
        )

        # =========================
        # BTN AJOUT
        # =========================

        self.btn_add = QPushButton(
            "Ajouter Service"
        )

        self.btn_add.clicked.connect(
            self.add_service
        )

        self.layout.addWidget(
            self.btn_add
        )

        # =========================
        # BTN TERMINER
        # =========================

        self.btn_finish = QPushButton(
            "Terminer"
        )

        self.btn_finish.setStyleSheet("""

            QPushButton {
                background-color: #16a34a;
                border: none;
                border-radius: 12px;
                padding: 14px;
                color: white;
                font-weight: bold;
                margin-top: 10px;
            }

            QPushButton:hover {
                background-color: #22c55e;
            }

        """)

        self.btn_finish.clicked.connect(
            self.close
        )

        self.layout.addWidget(
            self.btn_finish
        )

        self.setLayout(
            self.layout
        )

    # ==================================
    # AJOUT SERVICE
    # ==================================

    def add_service(self):

        try:

            data = {

                'nom': self.input_service.text(),

                'duree': int(
                    self.input_duree.text()
                ),

                'id_agence': self.id_agence
            }

            response = requests.post(
                'http://127.0.0.1:5000/create_service',
                json=data
            )

            if response.ok:

                QMessageBox.information(
                    self,
                    "Succès",
                    "Service ajouté"
                )

                self.input_service.clear()

                self.input_duree.clear()

            else:

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Impossible d'ajouter"
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur",
                str(e)
            )