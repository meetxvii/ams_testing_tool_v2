from PyQt5.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QPushButton,QDesktopWidget
from PyQt5.QtCore import QObject,pyqtSignal
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
        self.layout = QVBoxLayout()
        self.validator_name = QLineEdit()
        self.validator_name.setPlaceholderText("Enter validator name")
        self.submit = QPushButton("Submit")
        self.submit.setFixedHeight(50)
        self.submit.clicked.connect(self.submit_form)
        self.layout.addWidget(self.validator_name)
        self.layout.addWidget(self.submit)
    
    def start_authentication(self):
        self.window.setLayout(self.layout)
        self.window.setFixedSize(300,200)
        self.window.show()

        qr = self.window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.window.move(qr.topLeft())

    def submit_form(self):
        validator_name = self.validator_name.text()
        if validator_name == "":
            return            
        constants.VALIDATOR_NAME = validator_name
        self.window.close()
        self.authentication_signal.emit(constants.VALIDATOR_NAME)