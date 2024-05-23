from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import constants
from handlers.filters import Filters
from handlers.display import Display
from handlers.actions import Actions
from controllers.occupancy_classification import OccupancyClassification
from controllers.mobile_detection import MobileDetection

class View(QObject):
    close_signal = pyqtSignal()
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.create_window()

        self.contoller = self.create_controller()
        
        self.filters = Filters(self.contoller)
        self.layout.addLayout(self.filters.layout)
        
        self.display = Display(self.contoller)
        self.layout.addLayout(self.display.layout)

        self.actions = Actions(self.contoller)
        self.layout.addLayout(self.actions.layout)

        self.create_signals()

        
    def create_window(self):
        self.window = QWidget()
        self.window.setWindowTitle(constants.MODEL)
        screen = self.app.primaryScreen()
        size = screen.availableSize()
        self.window.setFixedSize(size.width(), size.height())
        self.layout = QVBoxLayout()
    
    def create_signals(self):
        self.filters.on_filter_change.connect(lambda:self.contoller.update_view(self.display))
        QShortcut(QKeySequence("Ctrl+Q"), self.window).activated.connect(self.on_window_close)
    
    def create_controller(self):
        if constants.MODEL == "Mobile Detection":
            return MobileDetection()
        elif constants.MODEL == "Occupancy Classification":
            return OccupancyClassification()
        
    def show_window(self):
        self.window.setLayout(self.layout)
        self.window.show()
    
    def on_window_close(self):
        self.window.close()
        self.close_signal.emit()
