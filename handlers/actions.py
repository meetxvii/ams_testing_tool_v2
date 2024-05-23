from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Actions(QObject):
    def __init__(self, controller) -> None:
        super().__init__()
        self.widgets = dict()
        self.layout = QHBoxLayout()
        self.controller = controller

        self.widgets['approve_btn'] = self.create_action_button("Approve", self.controller.on_approve_button_click)
        self.layout.addWidget(self.widgets['approve_btn'])
        
        self.widgets['skip_btn'] = self.create_action_button("Skip", self.controller.on_skip_button_click)
        self.layout.addWidget(self.widgets['skip_btn'])

    def create_action_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(lambda : action(self))
        return button