from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from handlers.authentication import AuthenticationHandler
from handlers.model_selector import ModelSelector
from view import View
import sys

class App(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        self.view = View(self.app)
        self.view.show_window()
        # self.auth_handler = AuthenticationHandler(self.app)
        # self.auth_handler.start_authentication()
        # self.auth_handler.authentication_signal.connect(self.select_model)

    def select_model(self):
        self.model_selector = ModelSelector(self.app)
        self.model_selector.show_window()
        self.model_selector.on_model_selection.connect(self.start_app)

    def start_app(self):
        self.view = View(self.app)
        self.view.close_signal.connect(self.model_selector.show_window)
        self.view.show_window()


if __name__ == "__main__":
    app = App()
    sys.exit(app.app.exec_())