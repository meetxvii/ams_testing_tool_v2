from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QApplication
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
import constants
class Display:
    def __init__(self,controller) -> None:
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        # set padding to zero 
        self.layout.setSpacing(0)
        self.widgets = dict()
        self.controller = controller

        screen_size = QApplication.primaryScreen().availableSize()

        self.widgets['next_btn'] = self.create_action_button("<", self.controller.on_previous_button_click)
        self.widgets['next_btn'].setFixedWidth(50)
        self.layout.addWidget(self.widgets['next_btn'])

        self.widgets['view'] = self.create_view()
        self.widgets['view'].setFixedHeight(screen_size.height() * 0.85)
        self.layout.addWidget(self.widgets['view'])

        self.widgets['previous_btn'] = self.create_action_button(">", self.controller.on_next_button_click)
        self.widgets['previous_btn'].setFixedWidth(50)
        self.layout.addWidget(self.widgets['previous_btn'])

    def create_action_button(self, text, action):
        button = QPushButton(text)
        button.setFixedSize(50,100)
        button.clicked.connect(lambda : action(self))
        return button
    
    def create_view(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setFixedSize(1100,600)
        self.view.setScene(self.scene)
        self.controller.view = self.view
        self.controller.scene = self.scene
        self.view.setMouseTracking(True)
        self.view.show()

        self.view.enterEvent = lambda event : self.controller.enterEvent(event,self)
        self.view.leaveEvent = lambda event : self.controller.leaveEvent(event,self)
        self.view.mousePressEvent = lambda event : self.controller.mousePressEvent(event,self)
        self.view.mouseMoveEvent = lambda event : self.controller.mouseMoveEvent(event,self)
        self.view.mouseReleaseEvent = lambda event : self.controller.mouseReleaseEvent(event,self)
        self.view.keyPressEvent = lambda event : self.controller.keyPressEvent (event,self)
        self.view.keyReleaseEvent = lambda event : self.controller.keyReleaseEvent(event,self)
        self.view.wheelEvent = lambda event : self.controller.wheelEvent(event,self)
        return self.view