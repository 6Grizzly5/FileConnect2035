from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QFrame
)

from PyQt5.QtCore import Qt

import requests

from configuration.services_window import ServicesWindow


class ConfigurationWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Smart Queue 2035"
        )

        self.resize(500, 700)

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
            "Configuration Agence"
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
        # NOM
        # =========================

        self.label_agence = QLabel(
            "Nom Agence"
        )

        self.input_agence = QLineEdit()

        self.input_agence.setPlaceholderText(
            "BOA Talatamaty"
        )

        self.layout.addWidget(
            self.label_agence
        )

        self.layout.addWidget(
            self.input_agence
        )

        # =========================
        # TYPE
        # =========================

        self.label_type = QLabel(
            "Type"
        )

        self.input_type = QLineEdit()

        self.input_type.setPlaceholderText(
            "Banque"
        )

        self.layout.addWidget(
            self.label_type
        )

        self.layout.addWidget(
            self.input_type
        )

        # =========================
        # VILLE
        # =========================

        self.label_ville = QLabel(
            "Ville"
        )

        self.input_ville = QLineEdit()

        self.input_ville.setPlaceholderText(
            "Antananarivo"
        )

        self.layout.addWidget(
            self.label_ville
        )

        self.layout.addWidget(
            self.input_ville
        )

        # =========================
        # ADRESSE
        # =========================

        self.label_adresse = QLabel(
            "Adresse"
        )

        self.input_adresse = QLineEdit()

        self.input_adresse.setPlaceholderText(
            "Talatamaty"
        )

        self.layout.addWidget(
            self.label_adresse
        )

        self.layout.addWidget(
            self.input_adresse
        )

        # =========================
        # TELEPHONE
        # =========================

        self.label_telephone = QLabel(
            "Téléphone"
        )

        self.input_telephone = QLineEdit()

        self.input_telephone.setPlaceholderText(
            "0340000000"
        )

        self.layout.addWidget(
            self.label_telephone
        )

        self.layout.addWidget(
            self.input_telephone
        )

        # =========================
        # BTN
        # =========================

        self.btn_agence = QPushButton(
            "Créer Agence"
        )

        self.btn_agence.clicked.connect(
            self.creer_agence
        )

        self.layout.addWidget(
            self.btn_agence
        )

        self.setLayout(
            self.layout
        )

    # ==================================
    # CREATION AGENCE
    # ==================================

    def creer_agence(self):

        data = {

            'nom': self.input_agence.text(),

            'type': self.input_type.text(),

            'ville': self.input_ville.text(),

            'adresse': self.input_adresse.text(),

            'telephone': self.input_telephone.text()
        }

        try:

            response = requests.post(
                'http://127.0.0.1:5000/create_agence',
                json=data
            )

            if response.ok:

                QMessageBox.information(
                    self,
                    "Succès",
                    "Agence créée avec succès"
                )

                data_response = response.json()

                id_agence = data_response[
                    'id_agence'
                ]

                # -------------------------
                # OUVERTURE SERVICES
                # -------------------------

                self.services_window = (
                    ServicesWindow(
                        id_agence
                    )
                )

                self.services_window.show()

                self.close()

            else:

                QMessageBox.warning(
                    self,
                    "Erreur",
                    "Erreur création agence"
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur Flask",
                str(e)
            )