from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

import requests


class ConfigurationWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Configuration Smart Queue 2035"
        )

        self.setGeometry(300, 200, 500, 500)

        self.layout = QVBoxLayout()

        # -------------------------
        # AGENCE
        # -------------------------

        self.label_agence = QLabel("Nom Agence")

        self.input_agence = QLineEdit()

        self.layout.addWidget(self.label_agence)

        self.layout.addWidget(self.input_agence)

        self.label_type = QLabel("Type")

        self.input_type = QLineEdit()

        self.layout.addWidget(self.label_type)

        self.layout.addWidget(self.input_type)

        self.label_adresse = QLabel("Adresse")

        self.input_adresse = QLineEdit()

        self.layout.addWidget(self.label_adresse)

        self.layout.addWidget(self.input_adresse)

        self.btn_agence = QPushButton(
            "Créer Agence"
        )
        self.btn_agence.setEnabled(False)

        self.input_agence.setEnabled(False)

        self.input_type.setEnabled(False)

        self.input_adresse.setEnabled(False)

        self.btn_agence.clicked.connect(
            self.creer_agence
        )

        self.layout.addWidget(self.btn_agence)

        # -------------------------
        # SERVICE
        # -------------------------

        self.label_service = QLabel("Nom Service")

        self.input_service = QLineEdit()

        self.layout.addWidget(self.label_service)

        self.layout.addWidget(self.input_service)

        self.label_duree = QLabel(
            "Durée Moyenne"
        )

        self.input_duree = QLineEdit()

        self.layout.addWidget(self.label_duree)

        self.layout.addWidget(self.input_duree)

        self.btn_service = QPushButton(
            "Ajouter Service"
        )

        self.btn_service.clicked.connect(
            self.creer_service
        )

        self.layout.addWidget(self.btn_service)

        self.setLayout(self.layout)

        self.id_agence = None

    # --------------------------------
    # CREATION AGENCE
    # --------------------------------

    def creer_agence(self):

        data = {
            'nom': self.input_agence.text(),
            'type': self.input_type.text(),
            'adresse': self.input_adresse.text()
        }

        response = requests.post(
            'http://127.0.0.1:5000/agence',
            json=data
        )

        if response.status_code == 201:

            QMessageBox.information(
                self,
                "Succès",
                "Agence créée"
            )

            data_response = response.json()

            self.id_agence = data_response['id_agence']

        else:

            QMessageBox.warning(
                self,
                "Erreur",
                "Erreur création agence"
            )

    # --------------------------------
    # CREATION SERVICE
    # --------------------------------

    def creer_service(self):

        if not self.id_agence:

            QMessageBox.warning(
                self,
                "Erreur",
                "Créez une agence d'abord"
            )

            return

        data = {
            'nom': self.input_service.text(),
            'duree': int(self.input_duree.text()),
            'id_agence': self.id_agence
        }

        response = requests.post(
            'http://127.0.0.1:5000/service',
            json=data
        )

        if response.status_code == 201:

            QMessageBox.information(
                self,
                "Succès",
                "Service ajouté"
            )

        else:

            QMessageBox.warning(
                self,
                "Erreur",
                "Erreur ajout service"
            )