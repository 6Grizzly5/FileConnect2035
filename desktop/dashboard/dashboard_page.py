from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import qtawesome as qta
import requests


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.main = QVBoxLayout()
        self.main.setContentsMargins(20, 20, 20, 20)
        self.main.setSpacing(20)

        # ─────────────────────────────
        # HEADER
        # ─────────────────────────────

        hdr = QHBoxLayout()

        title = QLabel("Vue Générale")
        title.setObjectName("pageTitle")

        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(qta.icon('fa5s.sync'))
        self.refresh_btn.setFixedSize(45, 45)
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setToolTip("Actualiser")
        self.refresh_btn.setStyleSheet("""
            QPushButton { background:white; border-radius:12px; border:none; }
            QPushButton:hover { background:#e2e8f0; }
        """)
        self.refresh_btn.clicked.connect(self.refresh)

        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self.refresh_btn)
        self.main.addLayout(hdr)

        # ─────────────────────────────
        # 4 KPI CARDS  (ligne unique)
        # ─────────────────────────────

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.c_total   = self._card("Clients aujourd'hui", "0",   "#6366f1", "fa5s.users")
        self.c_attente = self._card("En attente",          "0",   "#f59e0b", "fa5s.hourglass-half")
        self.c_cours   = self._card("En cours",            "0",   "#3b82f6", "fa5s.spinner")
        self.c_done    = self._card("Terminés",            "0",   "#10b981", "fa5s.check-circle")

        for c in [self.c_total, self.c_attente, self.c_cours, self.c_done]:
            cards_row.addWidget(c)

        self.main.addLayout(cards_row)

        # ─────────────────────────────
        # 2e LIGNE : temps moyen + 1 extra
        # ─────────────────────────────

        row2 = QHBoxLayout()
        row2.setSpacing(16)

        self.c_temps   = self._card("Temps Moyen",   "0 min", "#8b5cf6", "fa5s.clock")
        self.c_services = self._card("Services actifs", "0",  "#0ea5e9", "fa5s.cogs")

        row2.addWidget(self.c_temps)
        row2.addWidget(self.c_services)

        self.main.addLayout(row2)

        # ─────────────────────────────
        # GRAPHIQUE
        # ─────────────────────────────

        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame { background:white; border-radius:18px; }
        """)
        chart_inner = QVBoxLayout()
        chart_inner.setContentsMargins(20, 16, 20, 16)
        chart_inner.setSpacing(10)

        chart_title = QLabel("Répartition des Tickets")
        chart_title.setStyleSheet(
            "font-size:16px; font-weight:bold; color:#0f172a;"
        )
        chart_inner.addWidget(chart_title)

        self.figure = Figure(figsize=(6, 2.8))
        self.figure.patch.set_facecolor('none')
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chart_inner.addWidget(self.canvas)

        chart_frame.setLayout(chart_inner)
        self.main.addWidget(chart_frame, stretch=1)

        self.setLayout(self.main)
        self.load_stats()

    # ─────────────────────────────
    # CARD FACTORY
    # ─────────────────────────────

    def _card(self, label, value, color, icon_name):

        frame = QFrame()
        frame.setMinimumHeight(100)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        frame.setStyleSheet(f"""
            QFrame {{
                background: white;
                border-radius: 16px;
                border-top: 4px solid {color};
            }}
            QFrame:hover {{
                border-top: 4px solid {color};
                border-left: 2px solid {color}22;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        # Icône + label
        top = QHBoxLayout()
        icon_lbl = QLabel()
        icon_lbl.setPixmap(qta.icon(icon_name, color=color).pixmap(16, 16))
        lbl = QLabel(label)
        lbl.setStyleSheet(f"font-size:12px; color:{color}; font-weight:bold;")
        top.addWidget(icon_lbl)
        top.addWidget(lbl)
        top.addStretch()
        layout.addLayout(top)

        # Valeur — grande et visible
        val = QLabel(value)
        val.setStyleSheet(
            "font-size:38px; font-weight:bold; color:#0f172a;"
        )
        val.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(val)

        frame.setLayout(layout)
        frame._val = val
        return frame

    # ─────────────────────────────
    # LOAD / REFRESH
    # ─────────────────────────────

    def load_stats(self):
        try:
            r = requests.get(
                "http://127.0.0.1:5000/dashboard_stats", timeout=3
            )
            if r.ok:
                d = r.json()
                total    = d.get('clients_today',   0)
                attente  = d.get('active_tickets',  0)
                en_cours = d.get('en_cours',        0)
                fini     = d.get('finished_tickets',0)
                moy      = d.get('average_time',    0)

                self.c_total._val.setText(str(total))
                self.c_attente._val.setText(str(attente))
                self.c_cours._val.setText(str(en_cours))
                self.c_done._val.setText(str(fini))
                self.c_temps._val.setText(f"{moy} min")

                self._draw_chart(attente, en_cours, fini)
        except Exception as e:
            print("Dashboard stats :", e)
            self._draw_chart(0, 0, 0)

        try:
            r2 = requests.get("http://127.0.0.1:5000/services", timeout=3)
            if r2.ok:
                self.c_services._val.setText(str(len(r2.json())))
        except Exception:
            pass

    def refresh(self):
        self.load_stats()

    # ─────────────────────────────
    # DRAW CHART
    # ─────────────────────────────

    def _draw_chart(self, attente, en_cours, fini):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        values = [max(0, int(attente)),
                  max(0, int(en_cours)),
                  max(0, int(fini))]
        labels = ['En attente', 'En cours', 'Terminés']
        colors = ['#f59e0b',    '#3b82f6',  '#10b981']

        total = sum(values)

        if total == 0:
            ax.text(0.5, 0.5, "Aucun ticket pour le moment",
                    ha='center', va='center',
                    fontsize=12, color="#94a3b8")
            ax.axis('off')
        else:
            wedges, texts, autotexts = ax.pie(
                values, labels=labels, colors=colors,
                autopct='%1.0f%%', startangle=90,
                wedgeprops={'linewidth': 2, 'edgecolor': 'white'},
                pctdistance=0.78
            )
            for t in texts:
                t.set_fontsize(9); t.set_color('#475569')
            for at in autotexts:
                at.set_fontsize(9); at.set_color('white')
                at.set_fontweight('bold')
            ax.axis('equal')

        self.figure.tight_layout()
        self.canvas.draw()
