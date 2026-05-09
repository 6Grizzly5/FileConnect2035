from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget
)

import requests


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Smart Queue 2035")

        self.setGeometry(200, 200, 600, 500)

        self.layout = QVBoxLayout()

        self.titre = QLabel("Dashboard Admin")

        self.layout.addWidget(self.titre)

        self.liste_tickets = QListWidget()

        self.layout.addWidget(self.liste_tickets)

        self.bouton_refresh = QPushButton(
            "Actualiser Tickets"
        )

        self.bouton_refresh.clicked.connect(
            self.charger_tickets
        )

        self.layout.addWidget(self.bouton_refresh)

        self.setLayout(self.layout)

    def charger_tickets(self):

        self.liste_tickets.clear()

        response = requests.get(
            'http://127.0.0.1:5000/admin/tickets'
        )

        tickets = response.json()

        for ticket in tickets:

            texte = (
                f"{ticket['numero']} | "
                f"Service : {ticket['service']} | "
                f"Position : {ticket['position']} | "
                f"Temps : {ticket['temps']} min"
            )

            self.liste_tickets.addItem(texte)