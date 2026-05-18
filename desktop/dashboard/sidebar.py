from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QWidget
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

import qtawesome as qta
import os


class Sidebar(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName("sidebar")
        self.setFixedWidth(235)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(10, 16, 10, 16)
        layout.setSpacing(3)

        # ══════════════════════════════════
        # HEADER — LOGO + NOM APP
        # ══════════════════════════════════

        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.12);
                border-radius: 18px;
            }
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(16, 16, 16, 16)
        header_layout.setSpacing(8)

        # Logo image
        logo_row = QHBoxLayout()
        logo_row.setSpacing(10)

        logo_lbl = QLabel()
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_path = os.path.join(base, "assets", "logo.png")
        pix = QPixmap(logo_path)
        if not pix.isNull():
            logo_lbl.setPixmap(
                pix.scaledToWidth(42, Qt.SmoothTransformation)
            )
        else:
            # Fallback icône si image absente
            logo_lbl.setPixmap(
                qta.icon('fa5s.network-wired',
                         color='rgba(255,255,255,0.9)').pixmap(36, 36)
            )
        logo_lbl.setFixedSize(42, 42)
        logo_lbl.setAlignment(Qt.AlignCenter)

        name_block = QVBoxLayout()
        name_block.setSpacing(1)

        app_name = QLabel("FileConnect")
        app_name.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 0.5px;
        """)

        app_year = QLabel("Smart Queue · 2035")
        app_year.setStyleSheet("""
            color: rgba(255,255,255,0.55);
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        name_block.addWidget(app_name)
        name_block.addWidget(app_year)

        logo_row.addWidget(logo_lbl)
        logo_row.addLayout(name_block)
        logo_row.addStretch()

        header_layout.addLayout(logo_row)

        # Séparateur fin
        sep0 = QFrame()
        sep0.setFixedHeight(1)
        sep0.setStyleSheet("background: rgba(255,255,255,0.18);")
        header_layout.addWidget(sep0)

        # Status chip "En ligne"
        status_row = QHBoxLayout()
        status_row.setSpacing(6)

        dot = QLabel("●")
        dot.setStyleSheet("color: #34d399; font-size: 10px;")
        dot.setFixedWidth(14)

        status_lbl = QLabel("Système en ligne")
        status_lbl.setStyleSheet(
            "color: rgba(255,255,255,0.65); font-size: 11px;"
        )

        status_row.addWidget(dot)
        status_row.addWidget(status_lbl)
        status_row.addStretch()

        header_layout.addLayout(status_row)

        header.setLayout(header_layout)
        layout.addWidget(header)

        layout.addSpacing(14)

        # ══════════════════════════════════
        # SECTION — NAVIGATION
        # ══════════════════════════════════

        self._add_section_label(layout, "NAVIGATION")

        self.btn_home      = self._btn('fa5s.home',      "Accueil")
        self.btn_dashboard = self._btn('fa5s.chart-line', "Dashboard")
        self.btn_tickets   = self._btn('fa5s.ticket-alt', "Tickets")
        self.btn_services  = self._btn('fa5s.cogs',       "Services")
        self.btn_stats     = self._btn('fa5s.chart-pie',  "Statistiques")

        for b in [self.btn_home, self.btn_dashboard,
                  self.btn_tickets, self.btn_services, self.btn_stats]:
            layout.addWidget(b)

        layout.addSpacing(10)

        sep1 = QFrame()
        sep1.setFixedHeight(1)
        sep1.setStyleSheet(
            "background: rgba(255,255,255,0.14); margin: 0 6px;"
        )
        layout.addWidget(sep1)

        layout.addSpacing(10)

        # ══════════════════════════════════
        # SECTION — OUTILS
        # ══════════════════════════════════

        self._add_section_label(layout, "OUTILS")

        self.btn_refresh  = self._btn('fa5s.sync-alt',  "Actualiser tout")
        self.btn_settings = self._btn('fa5s.sliders-h', "Paramètres")

        # Style spécial pour actualiser
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background: rgba(52,211,153,0.18);
                color: #6ee7b7;
                border: 1px solid rgba(52,211,153,0.3);
                text-align: left;
                padding: 10px 14px;
                border-radius: 14px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(52,211,153,0.30);
                color: #a7f3d0;
            }
        """)

        layout.addWidget(self.btn_refresh)
        layout.addWidget(self.btn_settings)

        layout.addStretch()

        # ══════════════════════════════════
        # BAS — ADMIN BADGE
        # ══════════════════════════════════

        sep2 = QFrame()
        sep2.setFixedHeight(1)
        sep2.setStyleSheet(
            "background: rgba(255,255,255,0.14); margin: 0 6px;"
        )
        layout.addWidget(sep2)
        layout.addSpacing(10)

        admin_frame = QFrame()
        admin_frame.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.10);
                border-radius: 14px;
            }
        """)
        admin_inner = QHBoxLayout()
        admin_inner.setContentsMargins(12, 10, 12, 10)
        admin_inner.setSpacing(10)

        avatar = QLabel("A")
        avatar.setFixedSize(34, 34)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet("""
            background: rgba(255,255,255,0.22);
            border-radius: 17px;
            color: white;
            font-size: 15px;
            font-weight: bold;
        """)

        info_v = QVBoxLayout()
        info_v.setSpacing(1)

        admin_name = QLabel("Admin")
        admin_name.setStyleSheet(
            "color:white; font-size:13px; font-weight:bold;"
        )
        admin_role = QLabel("Administrateur")
        admin_role.setStyleSheet(
            "color:rgba(255,255,255,0.55); font-size:11px;"
        )

        info_v.addWidget(admin_name)
        info_v.addWidget(admin_role)

        admin_inner.addWidget(avatar)
        admin_inner.addLayout(info_v)
        admin_inner.addStretch()

        lock_icon = QLabel()
        lock_icon.setPixmap(
            qta.icon('fa5s.shield-alt',
                     color='rgba(255,255,255,0.35)').pixmap(16, 16)
        )
        admin_inner.addWidget(lock_icon)

        admin_frame.setLayout(admin_inner)
        layout.addWidget(admin_frame)

        self.setLayout(layout)

    # ─────────────────────────────
    # HELPERS
    # ─────────────────────────────

    def _add_section_label(self, layout, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("""
            color: rgba(255,255,255,0.38);
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 2px;
            padding-left: 14px;
            margin-bottom: 2px;
        """)
        layout.addWidget(lbl)

    def _btn(self, icon_name, label):
        btn = QPushButton(
            qta.icon(icon_name, color='rgba(255,255,255,0.8)'),
            f"  {label}"
        )
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(48)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: rgba(255,255,255,0.85);
                border: none;
                text-align: left;
                padding: 10px 14px;
                border-radius: 14px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.15);
                color: white;
            }
        """)
        return btn
