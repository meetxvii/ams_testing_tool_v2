from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Actions(QObject):
    def __init__(self, controller,display) -> None:
        super().__init__()
        self.widgets = dict()
        self.layout = QHBoxLayout()
        self.controller = controller
        self.display_object=display

        self.widgets['skip_btn'] = self.create_action_button("Skip", self.controller.on_skip_button_click)
        self.layout.addWidget(self.widgets['skip_btn'])
        
        self.widgets['approve_btn'] = self.create_action_button("Approve", self.controller.on_approve_button_click)
        self.layout.addWidget(self.widgets['approve_btn'])       

        self.widgets['image_counter'] = self.create_statusbar_widget()
        self.widgets['status_bar'] = self.create_status_bar()

    def create_action_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(lambda :action(self.display_object))
        return button
    
    def create_statusbar_widget(self):
        label = QLabel("0/0")
        return label
    
    def create_status_bar(self):
        status_bar = QStatusBar()
        status_bar.addPermanentWidget(self.widgets['image_counter'])
        return status_bar