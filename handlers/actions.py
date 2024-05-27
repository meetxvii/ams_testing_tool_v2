from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QLabel, QStatusBar
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt

class Actions(QObject):
    def __init__(self, controller,display) -> None:
        super().__init__()
        self.widgets = dict()
        self.layout = QHBoxLayout()
        self.controller = controller
        self.display_object=display
        self.clipboard = QApplication.clipboard()

        self.widgets['skip_btn'] = self.create_action_button("Skip", self.controller.on_skip_button_click)
        self.layout.addWidget(self.widgets['skip_btn'])
        
        self.widgets['approve_btn'] = self.create_action_button("Approve", self.controller.on_approve_button_click)
        self.layout.addWidget(self.widgets['approve_btn'])       
        
        self.widgets['image_name'] = self.create_image_name()
        self.widgets['image_counter'] = self.create_image_counter()
        self.widgets['status_bar'] = self.create_status_bar()

    def create_action_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(lambda :action(self.display_object))
        return button
    
    def create_image_name(self):
        label = QLabel()
        label.mousePressEvent = lambda event : self.clipboard.setText(label.text())
        return label

    def create_image_counter(self):
        label = QLabel("0/0")
        return label
    
    def create_status_bar(self):
        status_bar = QStatusBar()
        status_bar.addWidget(self.widgets['image_name'])
        status_bar.addPermanentWidget(self.widgets['image_counter'])
        return status_bar