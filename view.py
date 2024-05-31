from PyQt5.QtWidgets import QWidget, QVBoxLayout, QShortcut
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QKeySequence
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

        self.controller = self.create_controller()
        
        self.filters = Filters(self.controller)
        self.layout.addLayout(self.filters.layout)
        self.layout.addStretch()

        self.display = Display(self.controller)
        self.layout.addLayout(self.display.layout)
        self.layout.addStretch()

        self.actions = Actions(self.controller,self.display)
        self.layout.addLayout(self.actions.layout)
        self.controller.actions = self.actions
        # self.layout.addStretch()

        self.layout.addWidget(self.actions.widgets['status_bar'])
        
        self.layout.addLayout(self.actions.widgets['shortcuts_bar'])
        self.layout.addStretch()

        self.create_signals()

        
    def create_window(self):
        self.window = QWidget()
        self.window.setWindowTitle(constants.MODEL)
        screen = self.app.primaryScreen()
        size = screen.availableSize()
        self.window.setFixedSize(size.width(), size.height())
        self.window.closeEvent = self.on_window_close
        self.layout = QVBoxLayout()
    
    def create_signals(self):
        self.filters.on_filter_change.connect(lambda:self.controller.update_view(self.display))
        QShortcut("s", self.window).activated.connect(lambda:self.controller.on_approve_button_click(self.display))
        QShortcut("right",self.window).activated.connect(lambda:self.controller.on_next_button_click(self.display))
        QShortcut("left",self.window).activated.connect(lambda:self.controller.on_previous_button_click(self.display))
        QShortcut(QKeySequence("Ctrl+Q"), self.window).activated.connect(self.on_window_change)
    
    def create_controller(self):
        if constants.MODEL == "Mobile Detection":
            return MobileDetection()
        elif constants.MODEL == "Occupancy Classification":
            return OccupancyClassification()
        
    def show_window(self):
        if self.controller.model.connected and not self.controller.model.database_present:
            self.actions.widgets['status_bar'].showMessage('Database not present')
        self.window.setLayout(self.layout)
        self.window.show()
    
    def on_window_change(self):
        self.window.close()
        self.close_signal.emit()

    def on_window_close(self,event):
        self.controller.settings_window.window.close()