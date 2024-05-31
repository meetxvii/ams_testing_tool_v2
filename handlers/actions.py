from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QLabel, QStatusBar, QWidget
from PyQt5.QtCore import QObject
from PyQt5.QtCore import Qt
from constants import shortcuts
import webbrowser

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
        self.widgets['shortcuts_bar'] = self.create_shortcuts_bar()

    def create_action_button(self, text, action):
        button = QPushButton(text)
        button.clicked.connect(lambda :action(self.display_object))
        return button
    
    def create_image_name(self):
        label = QLabel()
        label.mousePressEvent = lambda event : self.on_link_click(event)
        return label
    
    def on_link_click(self,event):
        
        if self.widgets["image_name"].text().startswith("http"):        
            self.clipboard.setText(f'image:"{self.widgets["image_name"].text()}"')
            webbrowser.open(self.widgets["image_name"].text())        
            

    def create_image_counter(self):
        label = QLabel("0/0")
        return label
    
    def create_status_bar(self):
        status_bar = QStatusBar()
        status_bar.addWidget(self.widgets['image_name'])
        status_bar.addPermanentWidget(self.widgets['image_counter'])
        return status_bar
    
    def create_shortcuts_bar(self):
        main_hbox = QHBoxLayout()

        for name,shortcut in shortcuts.items():
            inner_hbox = QHBoxLayout()
            label = QLabel(shortcut["name"])
            btn = QPushButton(shortcut["key"])
            btn.setStyleSheet("""
                            background-color: #333;
                            color: #fff;
                            border-radius: 4px;
                            padding: 4px 8px;
                            width: 50px;
                              """)

            inner_hbox.addWidget(label)
            inner_hbox.addWidget(btn)
            inner_hbox.setContentsMargins(0,0,20,0)
            main_hbox.addLayout(inner_hbox)

        main_hbox.setAlignment(Qt.AlignCenter)
        
        return main_hbox
