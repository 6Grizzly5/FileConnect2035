from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QSizePolicy
)

from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import qtawesome as qta
import requests


class StatsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # =========================
        # HEADER
        # =========================

        header_layout = QHBoxLayout()

        self.title = QLabel("Statistiques Avancées")
        self.title.setObjectName("pageTitle")

        self.refresh_btn = QPushButton()
        self.refresh_btn.setIcon(qta.icon('fa5s.sync-alt'))
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
        self.refresh_btn.clicked.connect(self.load_stats)

        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_btn)

        self.layout.addLayout(header_layout)

        # =========================
        # KPI ROW
        # =========================

        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(16)

        self.kpi_total = self._make_kpi("Total Tickets", "0", "#6366f1")
        self.kpi_attente = self._make_kpi("En Attente", "0", "#f59e0b")
        self.kpi_cours = self._make_kpi("En Cours", "0", "#3b82f6")
        self.kpi_termine = self._make_kpi("Terminés", "0", "#10b981")

        kpi_layout.addWidget(self.kpi_total)
        kpi_layout.addWidget(self.kpi_attente)
        kpi_layout.addWidget(self.kpi_cours)
        kpi_layout.addWidget(self.kpi_termine)

        self.layout.addLayout(kpi_layout)

        # =========================
        # CHARTS ROW
        # =========================

        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(16)

        # --- PIE CHART ---
        self.pie_frame = QFrame()
        self.pie_frame.setStyleSheet("""
        QFrame {
            background: white;
            border-radius: 20px;
        }
        """)
        pie_layout = QVBoxLayout()
        pie_layout.setContentsMargins(16, 16, 16, 16)

        pie_label = QLabel("Répartition des Statuts")
        pie_label.setStyleSheet(
            "font-size:16px; font-weight:bold; color:#0f172a;"
        )
        pie_layout.addWidget(pie_label)

        self.pie_figure = Figure(figsize=(4, 3))
        self.pie_figure.patch.set_facecolor('none')
        self.pie_canvas = FigureCanvasQTAgg(self.pie_figure)
        self.pie_canvas.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        pie_layout.addWidget(self.pie_canvas)
        self.pie_frame.setLayout(pie_layout)

        # --- BAR CHART ---
        self.bar_frame = QFrame()
        self.bar_frame.setStyleSheet("""
        QFrame {
            background: white;
            border-radius: 20px;
        }
        """)
        bar_layout = QVBoxLayout()
        bar_layout.setContentsMargins(16, 16, 16, 16)

        bar_label = QLabel("Tickets par Service")
        bar_label.setStyleSheet(
            "font-size:16px; font-weight:bold; color:#0f172a;"
        )
        bar_layout.addWidget(bar_label)

        self.bar_figure = Figure(figsize=(4, 3))
        self.bar_figure.patch.set_facecolor('none')
        self.bar_canvas = FigureCanvasQTAgg(self.bar_figure)
        self.bar_canvas.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        bar_layout.addWidget(self.bar_canvas)
        self.bar_frame.setLayout(bar_layout)

        charts_layout.addWidget(self.pie_frame)
        charts_layout.addWidget(self.bar_frame)

        self.layout.addLayout(charts_layout)

        self.setLayout(self.layout)

        self.load_stats()

    # ================================
    # MAKE KPI CARD
    # ================================

    def _make_kpi(self, label, value, color):

        frame = QFrame()
        frame.setMinimumHeight(90)
        frame.setStyleSheet(f"""
        QFrame {{
            background: white;
            border-radius: 16px;
            border-left: 5px solid {color};
        }}
        """)
        frame.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(4)

        lbl = QLabel(label)
        lbl.setStyleSheet("font-size:12px; color:#64748b; font-weight:bold;")

        val = QLabel(value)
        val.setStyleSheet(
            f"font-size:30px; font-weight:bold; color:{color};"
        )
        val.setAlignment(Qt.AlignLeft)

        layout.addWidget(lbl)
        layout.addWidget(val)
        frame.setLayout(layout)

        frame._value_label = val
        return frame

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

                total = data.get('clients_today', 0)
                active = data.get('active_tickets', 0)
                finished = data.get('finished_tickets', 0)
                en_cours = max(0, total - active - finished)

                self.kpi_total._value_label.setText(str(total))
                self.kpi_attente._value_label.setText(str(active))
                self.kpi_cours._value_label.setText(str(en_cours))
                self.kpi_termine._value_label.setText(str(finished))

                self._draw_pie(active, en_cours, finished)

        except Exception as e:
            print("Erreur stats :", e)

        try:
            resp2 = requests.get(
                "http://127.0.0.1:5000/services",
                timeout=3
            )
            if resp2.ok:
                services = resp2.json()
                self._draw_bar(services)
        except Exception as e:
            print("Erreur services :", e)

    # ================================
    # DRAW PIE
    # ================================

    def _draw_pie(self, attente, en_cours, termine):

        self.pie_figure.clear()
        ax = self.pie_figure.add_subplot(111)

        colors = ['#f59e0b', '#3b82f6', '#10b981']
        labels = ['En attente', 'En cours', 'Terminés']
        values = [
            max(0, int(attente)),
            max(0, int(en_cours)),
            max(0, int(termine))
        ]

        total = sum(values)

        if total == 0:
            ax.text(
                0.5, 0.5, "Aucun ticket disponible",
                ha='center', va='center',
                fontsize=11, color="#94a3b8"
            )
            ax.axis('off')
        else:
            wedges, texts, autotexts = ax.pie(
                values,
                labels=labels,
                colors=colors,
                autopct='%1.0f%%',
                startangle=90,
                wedgeprops={
                    'linewidth': 2,
                    'edgecolor': 'white'
                },
                pctdistance=0.75
            )
            for t in texts:
                t.set_fontsize(9)
                t.set_color('#475569')
            for at in autotexts:
                at.set_fontsize(9)
                at.set_color('white')
                at.set_fontweight('bold')

            ax.axis('equal')

        self.pie_figure.tight_layout()
        self.pie_canvas.draw()

    # ================================
    # DRAW BAR
    # ================================

    def _draw_bar(self, services):

        self.bar_figure.clear()
        ax = self.bar_figure.add_subplot(111)

        if not services:
            ax.text(
                0.5, 0.5, "Aucun service",
                ha='center', va='center',
                fontsize=11, color="#94a3b8"
            )
            ax.axis('off')
            self.bar_canvas.draw()
            return

        noms = [s['nom'] for s in services]
        durees = [s.get('duree', 0) for s in services]

        palette = [
            '#6366f1', '#3b82f6', '#10b981',
            '#f59e0b', '#ef4444', '#8b5cf6'
        ]

        colors = [
            palette[i % len(palette)]
            for i in range(len(noms))
        ]

        bars = ax.bar(
            noms, durees,
            color=colors,
            width=0.55,
            edgecolor='white',
            linewidth=1.5
        )

        ax.set_facecolor('#f8fafc')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e2e8f0')
        ax.spines['bottom'].set_color('#e2e8f0')
        ax.tick_params(colors='#64748b', labelsize=8)
        ax.set_ylabel("Durée moy. (min)", fontsize=9, color='#64748b')

        for bar, val in zip(bars, durees):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                str(val),
                ha='center', va='bottom',
                fontsize=9, color='#0f172a',
                fontweight='bold'
            )

        self.bar_figure.tight_layout()
        self.bar_canvas.draw()

    # ──────────────────────────────────
    # REFRESH (appelé par timer global)
    # ──────────────────────────────────

    def refresh(self):
        self.load_stats()
