import sys
import os
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox
)

from configuration.configuration import (
    ConfigurationWindow
)

from dashboard.dashboard import Dashboard

# -----------------------------------
# APP QT
# -----------------------------------

app = QApplication(sys.argv)

# -----------------------------------
# CHEMIN BASE
# -----------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# -----------------------------------
# STYLE GLOBAL
# -----------------------------------

style_path = os.path.join(
    BASE_DIR,
    "styles",
    "style.qss"
)

with open(style_path, "r") as style:

    app.setStyleSheet(style.read())

# -----------------------------------
# VERIFICATION BACKEND
# -----------------------------------

try:

    response = requests.get(
        'http://127.0.0.1:5000/check_agence'
    )

    data = response.json()

except Exception:

    erreur = QMessageBox()

    erreur.setWindowTitle(
        "Erreur Backend"
    )

    erreur.setText(
        "Impossible de contacter le serveur Flask."
    )

    erreur.exec_()

    sys.exit()

# -----------------------------------
# CHOIX FENETRE
# -----------------------------------

if data['configured']:

    window = Dashboard()

else:

    window = ConfigurationWindow()

# -----------------------------------
# SHOW WINDOW
# -----------------------------------

window.show()

sys.exit(app.exec_())