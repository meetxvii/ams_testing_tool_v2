from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import constants
class ModelSelector(QObject):
    on_model_selection = pyqtSignal(str)
    def __init__(self,app) -> None:
        super().__init__()
        self.app = app
        self.create_window()
        self.models = ["Mobile Detection", "Mobile Classification", "Occupancy Classification"]
        for model in self.models:
            self.add_model(model)
        self.window.setLayout(self.layout)
    
    def create_window(self):
        self.window = QWidget()
        self.window.setWindowTitle("Model Selector")
        self.layout = QVBoxLayout()

    def add_model(self,model):
        button = QPushButton(model)
        button.clicked.connect(lambda: self.select_model(model))
        self.layout.addWidget(button)      
    
    def select_model(self,model):
        self.window.close()
        constants.MODEL = model
        self.on_model_selection.emit(model)
        
    def show_window(self):
        self.window.show()
