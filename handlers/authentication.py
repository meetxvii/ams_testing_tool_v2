from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import constants
class AuthenticationHandler(QObject):
    authentication_signal = pyqtSignal(str)
    def __init__(self,app) -> None:
        super().__init__()
        self.app = app
        self.create_window()
        self.create_login_form()
    
    def create_window(self):
        self.window = QWidget()
        self.window.setWindowTitle("Authentication")
        
    def create_login_form(self):
        self.login_form = QFormLayout()
        self.validator_name = QLineEdit()
        self.validator_name.setPlaceholderText("Enter your validator name")
        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.submit_form)
        self.login_form.addRow("validator_name",self.validator_name)
        self.login_form.addRow(self.submit)
    
    def start_authentication(self):
        self.window.setLayout(self.login_form)
        self.window.show()

    def submit_form(self):
        constants.VALIDATOR_NAME = self.validator_name.text()
        self.window.close()
        self.authentication_signal.emit(constants.VALIDATOR_NAME)