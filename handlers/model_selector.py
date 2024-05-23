from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDesktopWidget
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QFont
import constants
class ModelSelector(QObject):
    on_model_selection = pyqtSignal(str)
    def __init__(self,app) -> None:
        super().__init__()
        self.app = app
        self.create_window()
        self.models = ["Mobile Detection", "Occupancy Classification"]
        for model in self.models:
            self.add_model(model)
        self.window.setLayout(self.layout)
    
    def create_window(self):
        self.window = QWidget()
        self.window.setWindowTitle("Model Selector")
        self.layout = QVBoxLayout()

    def add_model(self,model):
        button = QPushButton(model)
        button.setFixedHeight(50)
        button.setFont(QFont("Arial", 11))
        button.clicked.connect(lambda: self.select_model(model))
        self.layout.addWidget(button)      
    
    def select_model(self,model):
        self.window.close()
        constants.MODEL = model
        self.on_model_selection.emit(model)
        
    def show_window(self):
        self.window.setFixedSize(300,200)
        self.window.show()
        qr = self.window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.window.move(qr.topLeft())
