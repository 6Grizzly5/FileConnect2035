from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDialog,
    QLineEdit,
    QFrame,
    QSizePolicy
)

from PyQt5.QtCore import Qt

import qtawesome as qta
import requests


# ============================================
# DIALOG AJOUT SERVICE
# ============================================

class AddServiceDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Ajouter un Service")
        self.setFixedSize(420, 320)
        self.setStyleSheet("""
        QDialog {
            background-color: #f8fafc;
        }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QLabel("Nouveau Service")
        title.setStyleSheet(
            "font-size:20px; font-weight:bold; color:#0f172a;"
        )
        layout.addWidget(title)

        # Nom
        lbl_nom = QLabel("Nom du service")
        lbl_nom.setStyleSheet("font-size:12px; color:#64748b; font-weight:bold;")
        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Ex: Dépôt, Retrait, Virement...")
        self.input_nom.setMinimumHeight(42)
        self.input_nom.setStyleSheet("""
        QLineEdit {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 14px;
            color: #0f172a;
        }
        QLineEdit:focus {
            border: 2px solid #2563eb;
        }
        """)

        # Durée
        lbl_duree = QLabel("Durée moyenne (minutes)")
        lbl_duree.setStyleSheet("font-size:12px; color:#64748b; font-weight:bold;")
        self.input_duree = QLineEdit()
        self.input_duree.setPlaceholderText("Ex: 10")
        self.input_duree.setMinimumHeight(42)
        self.input_duree.setStyleSheet(self.input_nom.styleSheet())

        layout.addWidget(lbl_nom)
        layout.addWidget(self.input_nom)
        layout.addWidget(lbl_duree)
        layout.addWidget(self.input_duree)

        # Boutons
        btn_row = QHBoxLayout()

        cancel_btn = QPushButton("Annuler")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setMinimumHeight(42)
        cancel_btn.setStyleSheet("""
        QPushButton {
            background: #e2e8f0;
            color: #475569;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
            padding: 8px 18px;
        }
        QPushButton:hover {
            background: #cbd5e1;
        }
        """)
        cancel_btn.clicked.connect(self.reject)

        confirm_btn = QPushButton(
            qta.icon('fa5s.plus', color='white'),
            "  Ajouter"
        )
        confirm_btn.setCursor(Qt.PointingHandCursor)
        confirm_btn.setMinimumHeight(42)
        confirm_btn.setStyleSheet("""
        QPushButton {
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
            padding: 8px 18px;
        }
        QPushButton:hover {
            background: #1d4ed8;
        }
        """)
        confirm_btn.clicked.connect(self.accept)

        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(confirm_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def get_data(self):
        return self.input_nom.text().strip(), self.input_duree.text().strip()


# ============================================
# SERVICES PAGE
# ============================================

class ServicesPage(QWidget):

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # =========================
        # HEADER
        # =========================

        self.header_layout = QHBoxLayout()

        self.title = QLabel("Gestion des Services")
        self.title.setObjectName("pageTitle")

        self.add_btn = QPushButton(
            qta.icon('fa5s.plus', color='white'),
            "  Ajouter"
        )
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setMinimumHeight(44)
        self.add_btn.setStyleSheet("""
        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        """)
        self.add_btn.clicked.connect(self.open_add_dialog)

        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(qta.icon('fa5s.sync'))
        self.refresh_btn.setFixedSize(45, 45)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
        QPushButton {
            background-color: white;
            border-radius: 12px;
            border: none;
        }
        QPushButton:hover {
            background-color: #e2e8f0;
        }
        """)
        self.refresh_btn.clicked.connect(self.load_services)

        self.header_layout.addWidget(self.title)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.refresh_btn)
        self.header_layout.addWidget(self.add_btn)

        self.layout.addLayout(self.header_layout)

        # =========================
        # STATS RAPIDES
        # =========================

        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(14)

        self.card_count = self._make_mini_card("Services actifs", "0", "#2563eb")
        self.card_duree = self._make_mini_card("Durée moy. globale", "0 min", "#10b981")

        self.stats_row.addWidget(self.card_count)
        self.stats_row.addWidget(self.card_duree)
        self.stats_row.addStretch()

        self.layout.addLayout(self.stats_row)

        # =========================
        # TABLE
        # =========================

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Service", "Durée moyenne", "Tickets", "Action"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(420)
        self.table.setStyleSheet("""
        QTableWidget {
            background-color: white;
            border-radius: 18px;
            padding: 10px;
            gridline-color: transparent;
            font-size: 14px;
            border: none;
        }
        QHeaderView::section {
            background-color: #f1f5f9;
            padding: 14px;
            border: none;
            font-weight: bold;
            color: #475569;
            font-size: 13px;
        }
        QTableWidget::item {
            padding: 12px;
            border-bottom: 1px solid #f1f5f9;
        }
        QTableWidget::item:selected {
            background-color: #eff6ff;
            color: #1e40af;
        }
        QTableWidget::item:alternate {
            background-color: #fafbfc;
        }
        """)

        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.load_services()

    # ================================
    # MINI CARD
    # ================================

    def _make_mini_card(self, label, value, color):

        frame = QFrame()
        frame.setFixedHeight(70)
        frame.setMinimumWidth(180)
        frame.setStyleSheet(f"""
        QFrame {{
            background: white;
            border-radius: 12px;
            border-left: 4px solid {color};
        }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(2)

        lbl = QLabel(label)
        lbl.setStyleSheet("font-size:11px; color:#64748b; font-weight:bold;")

        val = QLabel(value)
        val.setStyleSheet(
            f"font-size:22px; font-weight:bold; color:{color};"
        )

        layout.addWidget(lbl)
        layout.addWidget(val)
        frame.setLayout(layout)
        frame._val = val
        return frame

    # ================================
    # OPEN ADD DIALOG
    # ================================

    def open_add_dialog(self):

        try:
            resp = requests.get(
                "http://127.0.0.1:5000/get_agence", timeout=3
            )
            if not resp.ok:
                QMessageBox.warning(self, "Erreur",
                    "Impossible de contacter le serveur.\n"
                    "Vérifiez que Flask est bien démarré.")
                return
            data_agence = resp.json()
            agence_id = data_agence.get('id')
            if not agence_id:
                QMessageBox.warning(self, "Erreur",
                    "Agence introuvable dans la base de données.")
                return
        except Exception as e:
            QMessageBox.critical(self, "Erreur réseau", str(e))
            return

        dialog = AddServiceDialog(self)

        if dialog.exec_() == QDialog.Accepted:

            nom, duree = dialog.get_data()

            if not nom or not duree:
                QMessageBox.warning(
                    self, "Champs manquants",
                    "Veuillez remplir tous les champs."
                )
                return

            try:
                duree_int = int(duree)
            except ValueError:
                QMessageBox.warning(
                    self, "Erreur",
                    "La durée doit être un nombre entier."
                )
                return

            try:
                response = requests.post(
                    "http://127.0.0.1:5000/create_service",
                    json={
                        'nom': nom,
                        'duree': duree_int,
                        'id_agence': agence_id
                    },
                    timeout=3
                )

                if response.ok:
                    self.load_services()
                else:
                    try:
                        err_detail = response.json().get(
                            'error', response.text
                        )
                    except Exception:
                        err_detail = response.text
                    QMessageBox.warning(
                        self, f"Erreur {response.status_code}",
                        f"Impossible d'ajouter le service :\n{err_detail}"
                    )

            except Exception as e:
                QMessageBox.critical(self, "Erreur", str(e))

    # ================================
    # LOAD SERVICES
    # ================================

    def load_services(self):

        try:
            response = requests.get(
                "http://127.0.0.1:5000/services",
                timeout=3
            )
            services = response.json()

            self.table.setRowCount(len(services))

            total_duree = 0

            for row, service in enumerate(services):

                nom_item = QTableWidgetItem(service['nom'])
                nom_item.setFont(
                    nom_item.font()
                )

                self.table.setItem(row, 0, nom_item)

                duree = service.get('duree', 0)
                total_duree += duree

                self.table.setItem(
                    row, 1,
                    QTableWidgetItem(f"⏱  {duree} min")
                )

                tickets_count = service.get('tickets', 0)
                self.table.setItem(
                    row, 2,
                    QTableWidgetItem(f"🎫  {tickets_count}")
                )

                self.table.setRowHeight(row, 56)

                delete_btn = QPushButton(
                    qta.icon('fa5s.trash-alt', color='white'),
                    "  Supprimer"
                )
                delete_btn.setCursor(Qt.PointingHandCursor)
                delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ef4444;
                    color: white;
                    border-radius: 8px;
                    padding: 7px 14px;
                    font-weight: bold;
                    font-size: 12px;
                    border: none;
                    margin: 4px;
                }
                QPushButton:hover {
                    background-color: #dc2626;
                }
                """)
                delete_btn.clicked.connect(
                    lambda _, sid=service['id']: self.delete_service(sid)
                )
                self.table.setCellWidget(row, 3, delete_btn)

            # Update mini cards
            self.card_count._val.setText(str(len(services)))

            if services:
                moy = round(total_duree / len(services))
                self.card_duree._val.setText(f"{moy} min")
            else:
                self.card_duree._val.setText("0 min")

        except Exception as e:
            print("Erreur services :", e)

    # ================================
    # DELETE SERVICE
    # ================================

    def delete_service(self, service_id):

        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer ce service ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                requests.delete(
                    f"http://127.0.0.1:5000/service/{service_id}",
                    timeout=3
                )
                self.load_services()
            except Exception as e:
                QMessageBox.warning(self, "Erreur", str(e))

    # ──────────────────────────────────
    # REFRESH (appelé par timer global)
    # ──────────────────────────────────

    def refresh(self):
        self.load_services()
