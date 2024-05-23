from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from controller import Controller
class Display:
    def __init__(self,controller) -> None:
        self.layout = QHBoxLayout()
        self.widgets = dict()
        self.controller = controller

        self.widgets['next_btn'] = self.create_action_button("<", self.controller.on_previous_button_click)
        self.layout.addWidget(self.widgets['next_btn'])

        self.widgets['view'] = self.create_view()
        self.layout.addWidget(self.widgets['view'])

        self.widgets['previous_btn'] = self.create_action_button(">", self.controller.on_next_button_click)
        self.layout.addWidget(self.widgets['previous_btn'])

    def create_action_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(lambda : action(self))
        return button
    
    def create_view(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setFixedSize(1100,800)
        self.view.setScene(self.scene)
        self.view.show()

        self.view.mousePressEvent = lambda event : self.controller.mousePressEvent(event,self)
        self.view.mouseMoveEvent = lambda event : self.controller.mouseMoveEvent(event,self)
        self.view.mouseReleaseEvent = lambda event : self.controller.mouseReleaseEvent(event,self)
        self.view.keyPressEvent = lambda event : self.controller.keyPressEvent (event,self)
        self.view.keyReleaseEvent = lambda event : self.controller.keyReleaseEvent(event,self)
        self.view.wheelEvent = lambda event : self.controller.wheelEvent(event,self)
        return self.view