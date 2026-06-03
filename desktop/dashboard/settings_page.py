from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton,
    QLineEdit, QMessageBox, QScrollArea,
    QFileDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import qtawesome as qta
import requests
import os
import shutil
import webbrowser


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        self._agence_id = None      # rempli au load
        self._qr_path   = None      # chemin absolu du QR code

        # Racine du projet : settings_page.py est dans
        # FileConnect2035/desktop/dashboard/
        # dirname x3 → FileConnect2035/
        _here = os.path.dirname(os.path.abspath(__file__))
        self._project_root = os.path.dirname(os.path.dirname(_here))

        outer = QVBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border:none; background:transparent; }")

        container = QWidget()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(24)

        # ─────────────────────────────
        # TITRE
        # ─────────────────────────────

        self.layout.addWidget(
            self._page_title("Paramètres")
        )

        # ─────────────────────────────
        # SECTION — INFOS AGENCE
        # ─────────────────────────────

        agence_sec = self._section("Informations de l'agence", "fa5s.building")
        body = QVBoxLayout()
        body.setSpacing(14)

        self.f_nom       = self._input("Nom de l'agence",  "BOA Talatamaty")
        self.f_type      = self._input("Type",             "Banque")
        self.f_ville     = self._input("Ville",            "Antananarivo")
        self.f_adresse   = self._input("Adresse",          "Talatamaty")
        self.f_telephone = self._input("Téléphone",        "034 00 000 00")

        for w in [self.f_nom, self.f_type,
                  self.f_ville, self.f_adresse, self.f_telephone]:
            body.addWidget(w)

        save_btn = self._action_btn(
            "fa5s.save", "  Enregistrer les modifications", "#2563eb", "#1d4ed8"
        )
        save_btn.clicked.connect(self.save_agence)
        body.addWidget(save_btn)

        agence_sec.layout().addLayout(body)
        self.layout.addWidget(agence_sec)

        # ─────────────────────────────
        # SECTION — QR CODE
        # ─────────────────────────────

        qr_sec = self._section("QR Code Mobile", "fa5s.qrcode")
        qr_body = QVBoxLayout()
        qr_body.setSpacing(14)

        info = QLabel(
            "Imprimez ce QR code et affichez-le à l'entrée de l'agence.\n"
            "Les clients le scannent pour prendre un ticket depuis leur téléphone."
        )
        info.setStyleSheet("font-size:13px; color:#64748b;")
        info.setWordWrap(True)
        qr_body.addWidget(info)

        # Image QR + bouton télécharger côte à côte
        qr_row = QHBoxLayout()
        qr_row.setSpacing(20)

        # Cadre image
        qr_img_frame = QFrame()
        qr_img_frame.setFixedSize(200, 200)
        qr_img_frame.setStyleSheet("""
            QFrame {
                background:#f8fafc;
                border-radius:14px;
                border:2px dashed #cbd5e1;
            }
        """)
        qr_img_layout = QVBoxLayout()
        qr_img_layout.setContentsMargins(10, 10, 10, 10)

        self.qr_label = QLabel("QR code\nnon disponible")
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.qr_label.setStyleSheet("color:#94a3b8; font-size:13px;")
        qr_img_layout.addWidget(self.qr_label)
        qr_img_frame.setLayout(qr_img_layout)

        # Actions QR
        qr_actions = QVBoxLayout()
        qr_actions.setSpacing(10)
        qr_actions.setAlignment(Qt.AlignTop)

        self.qr_path_label = QLabel("Chemin : —")
        self.qr_path_label.setStyleSheet(
            "font-size:11px; color:#94a3b8; font-style:italic;"
        )
        self.qr_path_label.setWordWrap(True)

        dl_btn = self._action_btn(
            "fa5s.download", "  Télécharger / Imprimer", "#0ea5e9", "#0284c7"
        )
        dl_btn.clicked.connect(self.download_qr)

        regen_btn = self._action_btn(
            "fa5s.sync-alt", "  Régénérer le QR code", "#8b5cf6", "#7c3aed"
        )
        regen_btn.clicked.connect(self.regen_qr)
        display_btn = self._action_btn(
            "fa5s.tv",
            "  Ouvrir l'affichage public",
            "#10b981",
            "#059669"
        )

        display_btn.clicked.connect(
            self.open_display
        )

        qr_actions.addWidget(self.qr_path_label)
        qr_actions.addWidget(dl_btn)
        qr_actions.addWidget(regen_btn)
        qr_actions.addWidget(display_btn)
        qr_actions.addStretch()

        qr_row.addWidget(qr_img_frame)
        qr_row.addLayout(qr_actions)
        qr_row.addStretch()

        qr_body.addLayout(qr_row)
        qr_sec.layout().addLayout(qr_body)
        self.layout.addWidget(qr_sec)

        # ─────────────────────────────
        # SECTION — ZONE DANGEREUSE
        # ─────────────────────────────

        danger_sec = self._section(
            "Zone Dangereuse", "fa5s.exclamation-triangle",
            border_color="#ef4444"
        )
        d_body = QVBoxLayout()
        d_body.setSpacing(16)

        # Reset tickets
        reset_block = QVBoxLayout()
        reset_block.setSpacing(6)
        reset_lbl = QLabel(
            "🗑  Vider tous les tickets — Efface uniquement les tickets "
            "sans toucher aux services ni à l'agence."
        )
        reset_lbl.setStyleSheet("font-size:13px; color:#64748b;")
        reset_lbl.setWordWrap(True)
        reset_btn = self._action_btn(
            "fa5s.trash-alt", "  Vider les tickets", "#ef4444", "#dc2626"
        )
        reset_btn.clicked.connect(self.confirm_reset_tickets)
        reset_block.addWidget(reset_lbl)
        reset_block.addWidget(reset_btn, alignment=Qt.AlignLeft)
        d_body.addLayout(reset_block)

        # Séparateur
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:#fee2e2;")
        d_body.addWidget(sep)

        # Supprimer agence
        del_block = QVBoxLayout()
        del_block.setSpacing(6)
        del_lbl = QLabel(
            "💣  Supprimer l'agence — Réinitialisation complète : "
            "tickets, services et agence sont supprimés. "
            "L'application reviendra à l'écran de configuration initiale."
        )
        del_lbl.setStyleSheet("font-size:13px; color:#991b1b; font-weight:500;")
        del_lbl.setWordWrap(True)
        del_btn = self._action_btn(
            "fa5s.bomb", "  Supprimer l'agence et tout réinitialiser",
            "#7f1d1d", "#991b1b"
        )
        del_btn.clicked.connect(self.confirm_delete_agence)
        del_block.addWidget(del_lbl)
        del_block.addWidget(del_btn, alignment=Qt.AlignLeft)
        d_body.addLayout(del_block)

        danger_sec.layout().addLayout(d_body)
        self.layout.addWidget(danger_sec)

        self.layout.addStretch()

        container.setLayout(self.layout)
        scroll.setWidget(container)
        outer.addWidget(scroll)
        self.setLayout(outer)

        self.load_agence()

    # ══════════════════════════════════════
    # UI HELPERS
    # ══════════════════════════════════════

    def _page_title(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("pageTitle")
        return lbl

    def _section(self, title, icon_name, border_color=None):
        frame = QFrame()
        border = f"border-left:5px solid {border_color};" if border_color else ""
        frame.setStyleSheet(f"""
            QFrame {{ background:white; border-radius:18px; {border} }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)

        hdr = QHBoxLayout()
        ico = QLabel()
        ico.setPixmap(
            qta.icon(icon_name,
                     color='#ef4444' if border_color else '#2563eb'
                     ).pixmap(20, 20)
        )
        t = QLabel(title)
        t.setStyleSheet("font-size:15px; font-weight:bold; color:#0f172a;")
        hdr.addWidget(ico); hdr.addWidget(t); hdr.addStretch()
        layout.addLayout(hdr)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(
            "background:#fee2e2;" if border_color else "background:#e2e8f0;"
        )
        layout.addWidget(sep)

        frame.setLayout(layout)
        return frame

    def _input(self, label, placeholder):
        wrapper = QWidget()
        lay = QVBoxLayout()
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)

        lbl = QLabel(label)
        lbl.setStyleSheet("font-size:12px; color:#64748b; font-weight:bold;")

        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setMinimumHeight(42)
        field.setStyleSheet("""
            QLineEdit {
                background:#f8fafc; border:2px solid #e2e8f0;
                border-radius:10px; padding:8px 12px;
                font-size:14px; color:#0f172a;
            }
            QLineEdit:focus {
                border:2px solid #2563eb; background:white;
            }
        """)

        lay.addWidget(lbl); lay.addWidget(field)
        wrapper.setLayout(lay)
        wrapper._field = field
        return wrapper
    def open_display(self):

        try:

            webbrowser.open(
                "http://127.0.0.1:5000/display"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur",
                str(e)
            )

    def _action_btn(self, icon_name, label, color, hover_color):
        btn = QPushButton(
            qta.icon(icon_name, color='white'), label
        )
        btn.setCursor(Qt.PointingHandCursor)
        btn.setMinimumHeight(44)
        btn.setStyleSheet(f"""
            QPushButton {{
                background:{color}; color:white; border:none;
                border-radius:12px; font-size:14px;
                font-weight:bold; padding:10px 20px;
            }}
            QPushButton:hover {{ background:{hover_color}; }}
        """)
        return btn

    # ══════════════════════════════════════
    # LOAD AGENCE
    # ══════════════════════════════════════

    def load_agence(self):
        try:
            r = requests.get("http://127.0.0.1:5000/get_agence", timeout=3)
            if r.ok:
                a = r.json()
                self._agence_id = a.get('id')

                self.f_nom._field.setText(a.get('nom', ''))
                self.f_type._field.setText(a.get('type', ''))
                self.f_ville._field.setText(a.get('ville', ''))
                self.f_adresse._field.setText(a.get('adresse', ''))
                self.f_telephone._field.setText(a.get('telephone', ''))

                self._load_qr(a.get('id'), a.get('qr_image', ''))

        except Exception as e:
            print("Settings load_agence :", e)

    def _load_qr(self, agence_id, qr_filename):
        """Charge le QR code de l'agence depuis app/static/images/agence_{id}.png."""
        if not agence_id or not qr_filename:
            self.qr_label.setText("QR code\nnon disponible")
            self.qr_path_label.setText("Agence introuvable")
            return

        qr_path = os.path.join(
            self._project_root, "app", "static", "images", qr_filename
        )

        self._qr_path = qr_path   # mémoriser pour téléchargement

        if os.path.exists(qr_path):
            pix = QPixmap(qr_path).scaled(
                176, 176,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.qr_label.setPixmap(pix)
            self.qr_label.setText("")
            self.qr_path_label.setText(f"Fichier : {qr_filename}")
        else:
            self.qr_label.setText("QR code\nnon disponible")
            self.qr_path_label.setText(
                f"Fichier introuvable : {qr_filename}"
            )

    # ══════════════════════════════════════
    # SAVE AGENCE
    # ══════════════════════════════════════

    def save_agence(self):
        data = {
            'nom':       self.f_nom._field.text().strip(),
            'type':      self.f_type._field.text().strip(),
            'ville':     self.f_ville._field.text().strip(),
            'adresse':   self.f_adresse._field.text().strip(),
            'telephone': self.f_telephone._field.text().strip(),
        }

        if not data['nom']:
            QMessageBox.warning(self, "Champ manquant",
                                "Le nom de l'agence est obligatoire.")
            return

        try:
            r = requests.put(
                "http://127.0.0.1:5000/update_agence",
                json=data, timeout=3
            )
            if r.ok:
                QMessageBox.information(
                    self, "Succès",
                    "✅ Les informations de l'agence ont été mises à jour."
                )
            else:
                QMessageBox.warning(self, "Erreur",
                                    f"Erreur serveur : {r.text}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur réseau", str(e))

    # ══════════════════════════════════════
    # DOWNLOAD QR
    # ══════════════════════════════════════

    def download_qr(self):
        src = getattr(self, '_qr_path', None)

        if not src or not os.path.exists(src):
            QMessageBox.warning(self, "QR Code",
                                "QR code introuvable. Vérifiez la configuration.")
            return

        dest, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le QR Code",
            os.path.expanduser("~/QRCode_agence.png"),
            "Images PNG (*.png)"
        )

        if dest:
            shutil.copy2(src, dest)
            QMessageBox.information(
                self, "Téléchargé",
                f"✅ QR Code enregistré :\n{dest}\n\nVous pouvez maintenant l'imprimer."
            )

    # ══════════════════════════════════════
    # REGEN QR
    # ══════════════════════════════════════

    def regen_qr(self):
        try:
            import qrcode as qc
            r = requests.get("http://127.0.0.1:5000/get_agence", timeout=3)
            if not r.ok:
                QMessageBox.warning(self, "Erreur", r.text)
                return
            a = r.json()
            agence_id = a.get('id')

            if not agence_id:
                QMessageBox.warning(self, "Erreur", "Agence introuvable.")
                return

            url = f"http://192.168.43.26:5000/mobile/{agence_id}"
            img = qc.make(url)

            images_dir = os.path.join(
                self._project_root, "app", "static", "images"
            )
            os.makedirs(images_dir, exist_ok=True)

            qr_path = os.path.join(images_dir, f"agence_{agence_id}.png")
            img.save(qr_path)

            self._load_qr(agence_id, f"agence_{agence_id}.png")

            QMessageBox.information(
                self, "QR Code régénéré",
                "✅ Nouveau QR Code généré avec succès."
            )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    # ══════════════════════════════════════
    # RESET TICKETS
    # ══════════════════════════════════════

    def confirm_reset_tickets(self):
        reply = QMessageBox.question(
            self,
            "Vider les tickets ?",
            "⚠️  Cette action supprimera TOUS les tickets enregistrés.\n\n"
            "Les services et l'agence resteront intacts.\n\n"
            "Confirmer ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                r = requests.delete(
                    "http://127.0.0.1:5000/reset_tickets", timeout=5
                )
                if r.ok:
                    QMessageBox.information(
                        self, "Réinitialisation",
                        "✅ Tous les tickets ont été supprimés."
                    )
                else:
                    QMessageBox.warning(self, "Erreur", r.text)
            except Exception as e:
                QMessageBox.critical(self, "Erreur réseau", str(e))

    # ══════════════════════════════════════
    # DELETE AGENCE (reset total)
    # ══════════════════════════════════════

    def confirm_delete_agence(self):

        # 1ère confirmation
        reply1 = QMessageBox.warning(
            self,
            "⚠️  Supprimer l'agence ?",
            "Vous êtes sur le point de SUPPRIMER COMPLÈTEMENT l'agence.\n\n"
            "• Tous les tickets seront effacés\n"
            "• Tous les services seront effacés\n"
            "• L'agence sera supprimée\n"
            "• L'application retournera à l'écran de configuration\n\n"
            "Cette action est IRRÉVERSIBLE.\n\nVoulez-vous continuer ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply1 != QMessageBox.Yes:
            return

        # 2e confirmation — saisir le nom de l'agence
        from PyQt5.QtWidgets import QInputDialog
        nom_agence = ""
        try:
            r = requests.get("http://127.0.0.1:5000/get_agence", timeout=3)
            if r.ok:
                nom_agence = r.json().get('nom', '')
        except Exception:
            pass

        texte, ok = QInputDialog.getText(
            self,
            "Confirmation finale",
            f"Tapez le nom de l'agence « {nom_agence} » pour confirmer la suppression :"
        )

        if not ok or texte.strip() != nom_agence:
            QMessageBox.information(
                self, "Annulé",
                "Suppression annulée. Le nom saisi ne correspond pas."
            )
            return

        # Supprimer
        try:
            r = requests.delete(
                "http://127.0.0.1:5000/delete_agence", timeout=5
            )
            if r.ok:
                QMessageBox.information(
                    self, "Suppression effectuée",
                    "✅ L'agence a été supprimée.\n\n"
                    "Veuillez redémarrer l'application pour reconfigurer."
                )
            else:
                QMessageBox.warning(self, "Erreur", r.text)
        except Exception as e:
            QMessageBox.critical(self, "Erreur réseau", str(e))

    # ══════════════════════════════════════
    # REFRESH
    # ══════════════════════════════════════

    def refresh(self):
        self.load_agence()
