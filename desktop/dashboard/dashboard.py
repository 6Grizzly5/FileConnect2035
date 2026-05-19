from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QScrollArea,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFrame
)

from PyQt5.QtCore import Qt, QTimer

import qtawesome as qta

from dashboard.sidebar import Sidebar
from dashboard.home_page import HomePage
from dashboard.dashboard_page import DashboardPage
from dashboard.tickets_page import TicketsPage
from dashboard.stats_page import StatsPage
from dashboard.sevices_page import ServicesPage
from dashboard.settings_page import SettingsPage
from dashboard.guichets_page import GuichetsPage


class Dashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("FileConnect 2035")
        self.resize(1500, 900)

        # ─────────────────────────────
        # MAIN LAYOUT
        # ─────────────────────────────

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(12)
        self.setLayout(self.main_layout)

        # ─────────────────────────────
        # SIDEBAR
        # ─────────────────────────────

        self.sidebar = Sidebar()

        # ─────────────────────────────
        # PAGES
        # ─────────────────────────────

        self.home_page      = HomePage()
        self.dashboard_page = DashboardPage()
        self.tickets_page   = TicketsPage()
        self.stats_page     = StatsPage()
        self.services_page  = ServicesPage()
        self.guichets_page  = GuichetsPage()
        self.settings_page  = SettingsPage()

        self.pages = QStackedWidget()
        for p in [
            self.home_page, self.dashboard_page,
            self.tickets_page, self.stats_page,
            self.services_page, self.guichets_page, self.settings_page
        ]:
            self.pages.addWidget(p)

        # ─────────────────────────────
        # SCROLL
        # ─────────────────────────────

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.pages)
        self.scroll.setStyleSheet(
            "QScrollArea { border:none; background:transparent; }"
        )

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.scroll, 1)

        # ─────────────────────────────
        # NAVIGATION
        # ─────────────────────────────

        self._btns = [
            self.sidebar.btn_home,
            self.sidebar.btn_dashboard,
            self.sidebar.btn_tickets,
            self.sidebar.btn_stats,
            self.sidebar.btn_services,
            self.sidebar.btn_guichets,
            self.sidebar.btn_settings,
        ]

        nav_pairs = zip(self._btns, [
            self.home_page, self.dashboard_page,
            self.tickets_page, self.stats_page,
            self.services_page, self.guichets_page, self.settings_page
        ])

        for i, (btn, page) in enumerate(nav_pairs):
            btn.clicked.connect(
                lambda _, p=page, b=btn: self._navigate(p, b)
            )

        # ─────────────────────────────
        # BOUTON REFRESH GLOBAL (sidebar)
        # ─────────────────────────────

        self.sidebar.btn_refresh.clicked.connect(self.refresh_all)

        # ─────────────────────────────
        # AUTO-REFRESH (toutes les 30s)
        # ─────────────────────────────

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh_all)
        self._timer.start(30_000)   # 30 secondes

        # Page par défaut
        self._navigate(self.home_page, self.sidebar.btn_home)

    # ──────────────────────────────────
    # NAVIGATE
    # ──────────────────────────────────

    def _navigate(self, page, active_btn):

        self.pages.setCurrentWidget(page)

        ACTIVE = """
            QPushButton {
                background: rgba(255,255,255,0.95);
                color: #2563eb;
                border: none;
                text-align: left;
                padding: 10px 14px;
                border-radius: 14px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background: white; }
        """
        NORMAL = """
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
            QPushButton:hover { background: rgba(255,255,255,0.15); color:white; }
        """

        for btn in self._btns:
            btn.setStyleSheet(NORMAL if btn is not active_btn else ACTIVE)

    # ──────────────────────────────────
    # REFRESH ALL PAGES
    # ──────────────────────────────────

    def refresh_all(self):
        """Actualise toutes les pages en une fois."""

        pages_with_refresh = [
            self.home_page,
            self.dashboard_page,
            self.tickets_page,
            self.stats_page,
            self.guichets_page,
            self.services_page,
        ]

        for page in pages_with_refresh:
            if hasattr(page, 'refresh'):
                try:
                    page.refresh()
                except Exception as e:
                    print(f"Refresh erreur {page.__class__.__name__} :", e)
