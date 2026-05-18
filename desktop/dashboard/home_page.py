from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QSizePolicy
)

from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

from datetime import datetime
import qtawesome as qta
import requests


class HomePage(QWidget):

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)

        # =========================
        # HEADER ROW
        # =========================

        header_row = QHBoxLayout()

        # Logo
        self.logo = QLabel()
        pixmap = QPixmap("assets/logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaledToWidth(
                80, Qt.SmoothTransformation
            ))
        self.logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Date/heure
        self.date_frame = QFrame()
        self.date_frame.setStyleSheet("""
        QFrame {
            background: white;
            border-radius: 14px;
        }
        """)
        date_inner = QHBoxLayout()
        date_inner.setContentsMargins(16, 10, 16, 10)

        clock_icon = QLabel()
        clock_icon.setPixmap(
            qta.icon('fa5s.clock', color='#2563eb').pixmap(18, 18)
        )

        self.date_lbl = QLabel(
            datetime.now().strftime("%d %B %Y  •  %H:%M")
        )
        self.date_lbl.setStyleSheet(
            "font-size:14px; font-weight:bold; color:#1e293b;"
        )

        date_inner.addWidget(clock_icon)
        date_inner.addWidget(self.date_lbl)
        self.date_frame.setLayout(date_inner)

        header_row.addWidget(self.logo)
        header_row.addStretch()
        header_row.addWidget(self.date_frame)

        self.layout.addLayout(header_row)

        # =========================
        # TITRE BIENVENUE
        # =========================

        self.title = QLabel("Bienvenue sur FileConnect")
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #0f172a;
            margin-top: 4px;
        """)

        self.subtitle = QLabel(
            "Système intelligent de gestion de file d'attente — 2035"
        )
        self.subtitle.setStyleSheet(
            "font-size:15px; color:#64748b; margin-bottom: 8px;"
        )

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)

        # =========================
        # CARD AGENCE
        # =========================

        self.agence_card = QFrame()
        self.agence_card.setStyleSheet("""
        QFrame {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #1e40af,
                stop:1 #3b82f6
            );
            border-radius: 22px;
        }
        """)
        self.agence_card.setMinimumHeight(130)

        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(16)

        bldg_icon = QLabel()
        bldg_icon.setPixmap(
            qta.icon('fa5s.building', color='rgba(255,255,255,0.6)').pixmap(40, 40)
        )
        bldg_icon.setAlignment(Qt.AlignVCenter)

        text_block = QVBoxLayout()
        text_block.setSpacing(4)

        self.agence_name = QLabel("Chargement...")
        self.agence_name.setStyleSheet(
            "font-size:22px; font-weight:bold; color:white;"
        )

        self.agence_info = QLabel("")
        self.agence_info.setStyleSheet(
            "font-size:13px; color:rgba(255,255,255,0.75);"
        )

        text_block.addWidget(self.agence_name)
        text_block.addWidget(self.agence_info)

        card_layout.addWidget(bldg_icon)
        card_layout.addLayout(text_block)
        card_layout.addStretch()

        self.agence_card.setLayout(card_layout)
        self.layout.addWidget(self.agence_card)

        # =========================
        # STATS RAPIDES
        # =========================

        quick_label = QLabel("Aperçu du jour")
        quick_label.setStyleSheet(
            "font-size:16px; font-weight:bold; color:#0f172a; margin-top:4px;"
        )
        self.layout.addWidget(quick_label)

        stats_row = QHBoxLayout()
        stats_row.setSpacing(14)

        self.stat_total = self._make_stat_card(
            "Tickets aujourd'hui", "0", "#6366f1", "fa5s.ticket-alt"
        )
        self.stat_attente = self._make_stat_card(
            "En attente", "0", "#f59e0b", "fa5s.hourglass-half"
        )
        self.stat_done = self._make_stat_card(
            "Terminés", "0", "#10b981", "fa5s.check-circle"
        )

        stats_row.addWidget(self.stat_total)
        stats_row.addWidget(self.stat_attente)
        stats_row.addWidget(self.stat_done)

        self.layout.addLayout(stats_row)

        # =========================
        # NEXT TICKET BUTTON
        # =========================

        self.next_btn = QPushButton(
            qta.icon('fa5s.step-forward', color='white'),
            "  Appeler le prochain ticket"
        )
        self.next_btn.setObjectName("nextBtn")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setMinimumHeight(54)
        self.next_btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #059669,
                stop:1 #10b981
            );
            color: white;
            border: none;
            border-radius: 16px;
            font-size: 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #047857,
                stop:1 #059669
            );
        }
        QPushButton:pressed {
            background-color: #047857;
        }
        """)
        self.next_btn.clicked.connect(self.call_next_ticket)
        self.layout.addWidget(self.next_btn)

        self.layout.addStretch()

        self.setLayout(self.layout)

        self.load_agence()
        self.load_stats()

        # Refresh heure toutes les 60s
        self.timer = QTimer()
        self.timer.timeout.connect(self._refresh_clock)
        self.timer.start(60000)

    # ================================
    # MAKE STAT CARD
    # ================================

    def _make_stat_card(self, label, value, color, icon_name):

        frame = QFrame()
        frame.setMinimumHeight(90)
        frame.setStyleSheet(f"""
        QFrame {{
            background: white;
            border-radius: 16px;
            border-top: 4px solid {color};
        }}
        """)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        top = QHBoxLayout()
        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            qta.icon(icon_name, color=color).pixmap(18, 18)
        )
        lbl = QLabel(label)
        lbl.setStyleSheet(
            f"font-size:11px; color:{color}; font-weight:bold;"
        )
        top.addWidget(icon_lbl)
        top.addWidget(lbl)
        top.addStretch()

        val = QLabel(value)
        val.setStyleSheet(
            f"font-size:28px; font-weight:bold; color:#0f172a;"
        )

        layout.addLayout(top)
        layout.addWidget(val)
        frame.setLayout(layout)
        frame._val = val
        return frame

    # ================================
    # LOAD AGENCE
    # ================================

    def load_agence(self):

        try:
            response = requests.get(
                "http://127.0.0.1:5000/get_agence",
                timeout=3
            )

            if response.ok:
                agence = response.json()

                self.agence_name.setText(
                    f"Agence {agence['nom']}"
                )
                self.agence_info.setText(
                    f"{agence['type']}  •  {agence['ville']}  •  {agence['telephone']}"
                )

        except Exception as e:
            print("Erreur agence :", e)

    # ================================
    # LOAD STATS
    # ================================

    def load_stats(self):

        try:
            response = requests.get(
                "http://127.0.0.1:5000/dashboard_stats",
                timeout=3
            )

            if response.ok:
                data = response.json()
                self.stat_total._val.setText(
                    str(data.get('clients_today', 0))
                )
                self.stat_attente._val.setText(
                    str(data.get('active_tickets', 0))
                )
                self.stat_done._val.setText(
                    str(data.get('finished_tickets', 0))
                )

        except Exception as e:
            print("Erreur stats home :", e)

    # ================================
    # CALL NEXT TICKET
    # ================================

    def call_next_ticket(self):

        try:
            response = requests.post(
                "http://127.0.0.1:5000/next_ticket",
                timeout=3
            )

            if response.ok:
                self.load_stats()

        except Exception as e:
            print("Erreur next ticket :", e)

    # ================================
    # REFRESH CLOCK
    # ================================

    def _refresh_clock(self):

        self.date_lbl.setText(
            datetime.now().strftime("%d %B %Y  •  %H:%M")
        )

    # ──────────────────────────────────
    # REFRESH (appelé par timer global)
    # ──────────────────────────────────

    def refresh(self):
        self.load_agence()
        self.load_stats()
        self._refresh_clock()
