from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QSpinBox
)

from PyQt5.QtCore import Qt

import requests


class GuichetsWindow(QWidget):

    def __init__(self, id_agence):

        super().__init__()

        self.id_agence = id_agence

        self.setWindowTitle(
            "Configuration des Guichets"
        )

        self.resize(500, 400)

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

            QSpinBox {
                background-color: #1e293b;
                border: 2px solid #334155;
                border-radius: 10px;
                padding: 12px;
                color: white;
                font-size: 18px;
            }

            QSpinBox:focus {
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

        self.layout.setSpacing(15)

        # =========================
        # TITRE
        # =========================

        self.title = QLabel(
            "Configuration des Guichets"
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
        # LABEL
        # =========================

        self.label = QLabel(
            "Nombre de guichets"
        )

        self.layout.addWidget(
            self.label
        )

        # =========================
        # SPINBOX
        # =========================

        self.spin = QSpinBox()

        self.spin.setMinimum(1)
        self.spin.setMaximum(50)
        self.spin.setValue(2)

        self.layout.addWidget(
            self.spin
        )

        # =========================
        # BOUTON
        # =========================

        self.btn_create = QPushButton(
            "Créer les Guichets"
        )

        self.btn_create.clicked.connect(
            self.create_guichets
        )

        self.layout.addWidget(
            self.btn_create
        )

        self.setLayout(
            self.layout
        )

    # ==================================
    # CREATE GUICHETS
    # ==================================

    def create_guichets(self):

        try:

            total = self.spin.value()

            response = requests.post(
                'http://127.0.0.1:5000/create_guichet',
                json={
                    'nombre': total,
                    'id_agence': self.id_agence
                }
            )

            if response.status_code == 201:

                QMessageBox.information(
                    self,
                    "Succès",
                    "Guichets créés"
                )

                # 🔥 OUVERTURE DASHBOARD
                from dashboard.dashboard import Dashboard

                self.dashboard = Dashboard()

                self.dashboard.show()

                self.close()

            else:

                QMessageBox.warning(
                    self,
                    "Erreur",
                    response.text
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur",
                str(e)
            )