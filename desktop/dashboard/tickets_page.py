from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import qtawesome as qta
import requests


STATUT_STYLE = {
    "En attente": ("#f59e0b", "#fffbeb"),
    "En cours":   ("#3b82f6", "#eff6ff"),
    "Terminé":    ("#10b981", "#ecfdf5"),
}

# Tous les tickets possibles + "Tous"
FILTRES = ["Tous", "En attente", "En cours", "Terminé"]


class TicketsPage(QWidget):

    def __init__(self):
        super().__init__()

        self._filtre_actif = "Tous"
        self._tous_tickets = []        # cache complet

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        # ─────────────────────────────
        # HEADER
        # ─────────────────────────────

        hdr = QHBoxLayout()

        title = QLabel("Gestion des Tickets")
        title.setObjectName("pageTitle")

        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(qta.icon('fa5s.sync'))
        self.refresh_btn.setFixedSize(45, 45)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
            QPushButton { background:white; border-radius:12px; border:none; }
            QPushButton:hover { background:#e2e8f0; }
        """)
        self.refresh_btn.clicked.connect(self.refresh)

        self.next_btn = QPushButton(
            qta.icon('fa5s.step-forward', color='white'),
            "  Appeler le suivant"
        )
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setMinimumHeight(44)
        self.next_btn.setStyleSheet("""
            QPushButton { background:#10b981; color:white; border:none;
                border-radius:12px; padding:10px 20px;
                font-size:14px; font-weight:bold; }
            QPushButton:hover { background:#059669; }
        """)
        self.next_btn.clicked.connect(self.call_next)

        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.refresh_btn)
        hdr.addWidget(self.next_btn)
        layout.addLayout(hdr)

        # ─────────────────────────────
        # FILTRES par statut
        # ─────────────────────────────

        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        self._filter_btns = {}

        for f in FILTRES:
            btn = QPushButton(f)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            btn.setMinimumHeight(36)
            btn.clicked.connect(lambda _, fv=f: self._apply_filter(fv))
            self._filter_btns[f] = btn
            filter_row.addWidget(btn)

        filter_row.addStretch()

        # Badge SPT
        spt = QLabel("  ⚡ SPT — service le plus court en premier  ")
        spt.setStyleSheet("""
            background:#f0f4ff; color:#4f46e5;
            border-radius:10px; font-size:12px; font-weight:bold;
            padding:4px 12px; border:1.5px solid #c7d2fe;
        """)
        filter_row.addWidget(spt)

        layout.addLayout(filter_row)

        # Style initial des boutons de filtre
        self._style_filter_btns()

        # ─────────────────────────────
        # TABLEAU — 7 colonnes
        # ─────────────────────────────

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Numéro", "Client", "Service",
            "Durée svc", "Position", "Attente estimée", "Statut"
        ])

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.Stretch)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setMinimumHeight(480)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background:white; border-radius:20px;
                padding:10px; font-size:14px;
                gridline-color:transparent; border:none;
            }
            QHeaderView::section {
                background:#f8fafc; color:#475569;
                padding:14px; border:none;
                font-size:13px; font-weight:bold;
            }
            QTableWidget::item {
                padding:12px;
                border-bottom:1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background:#eff6ff; color:#1e40af;
            }
        """)

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_tickets()

    # ─────────────────────────────
    # STYLE FILTER BUTTONS
    # ─────────────────────────────

    def _style_filter_btns(self):

        COLORS = {
            "Tous":       ("#2563eb", "#eff6ff"),
            "En attente": ("#f59e0b", "#fffbeb"),
            "En cours":   ("#3b82f6", "#eff6ff"),
            "Terminé":    ("#10b981", "#ecfdf5"),
        }

        for fname, btn in self._filter_btns.items():
            color, bg = COLORS.get(fname, ("#64748b", "#f8fafc"))

            if fname == self._filtre_actif:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background:{color}; color:white;
                        border:none; border-radius:10px;
                        padding:6px 16px; font-size:13px;
                        font-weight:bold;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background:{bg}; color:{color};
                        border:1.5px solid {color}44;
                        border-radius:10px;
                        padding:6px 16px; font-size:13px;
                        font-weight:bold;
                    }}
                    QPushButton:hover {{
                        background:{color}22;
                        border:1.5px solid {color};
                    }}
                """)

    # ─────────────────────────────
    # APPLY FILTER
    # ─────────────────────────────

    def _apply_filter(self, filtre):
        self._filtre_actif = filtre
        self._style_filter_btns()
        self._fill_table(self._tous_tickets)

    # ─────────────────────────────
    # REFRESH
    # ─────────────────────────────

    def refresh(self):
        self.load_tickets()

    # ─────────────────────────────
    # LOAD TICKETS
    # ─────────────────────────────

    def load_tickets(self):
        try:
            resp = requests.get(
                'http://127.0.0.1:5000/admin/tickets', timeout=3
            )
            self._tous_tickets = resp.json()
        except Exception as e:
            print("Erreur tickets :", e)
            return

        self._fill_table(self._tous_tickets)

    # ─────────────────────────────
    # FILL TABLE (avec filtre)
    # ─────────────────────────────

    def _fill_table(self, tickets):

        if self._filtre_actif == "Tous":
            visible = tickets
        else:
            visible = [
                t for t in tickets
                if t.get('statut') == self._filtre_actif
            ]

        self.table.setRowCount(len(visible))

        for row, t in enumerate(visible):
            self.table.setRowHeight(row, 54)

            statut = t.get('statut', 'En attente')
            color, bg = STATUT_STYLE.get(statut, ("#64748b", "#f1f5f9"))

            # — Numéro —
            num = QTableWidgetItem(t['numero'])
            num.setFont(QFont("Segoe UI", 13, QFont.Bold))
            num.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, num)

            # — Client  (vrai nom, jamais "Anonyme" si dispo) —
            nom_client = (t.get('client') or '').strip()
            if not nom_client:
                nom_client = "—"
            ci = QTableWidgetItem(f"👤  {nom_client}")
            ci.setFont(QFont("Segoe UI", 13))
            self.table.setItem(row, 1, ci)

            # — Service —
            self.table.setItem(row, 2, QTableWidgetItem(t['service']))

            # — Durée service —
            d = QTableWidgetItem(f"⏱  {t.get('duree_service', 0)} min")
            d.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, d)

            # — Position —
            pos = t.get('position', 0)
            if statut in ("En cours", "Terminé") or pos == 0:
                pos_txt = "—"
            else:
                pos_txt = f"#{pos}"
            pi = QTableWidgetItem(pos_txt)
            pi.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, pi)

            # — Temps estimé —
            temps = t.get('temps_estime', 0)
            if statut == "Terminé":
                t_txt = "✓ Servi"
            elif statut == "En cours":
                t_txt = "🔵 En service"
            else:
                t_txt = f"~{temps} min"
            ti = QTableWidgetItem(t_txt)
            ti.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, ti)

            # — Statut badge coloré —
            si = QTableWidgetItem(statut)
            si.setTextAlignment(Qt.AlignCenter)
            si.setForeground(QColor(color))
            si.setBackground(QColor(bg))
            si.setFont(QFont("Segoe UI", 12, QFont.Bold))
            self.table.setItem(row, 6, si)

    # ─────────────────────────────
    # NEXT TICKET
    # ─────────────────────────────

    def call_next(self):
        try:
            requests.post("http://127.0.0.1:5000/next_ticket", timeout=3)
            self.load_tickets()
        except Exception as e:
            print("Erreur next :", e)
