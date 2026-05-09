import sys
import requests

from PyQt5.QtWidgets import QApplication

from configuration import ConfigurationWindow
from dashboard import Dashboard

app = QApplication(sys.argv)

response = requests.get(
    'http://127.0.0.1:5000/check_agence'
)

data = response.json()

if data['configured']:

    window = Dashboard()

else:

    window = ConfigurationWindow()

window.show()

sys.exit(app.exec_())