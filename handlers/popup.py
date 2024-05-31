from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import constants
class PopUpWindow(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.create_window()
    
    def create_window(self):
        self.window = QWidget(flags=
                                Qt.Window  
                              | Qt.FramelessWindowHint 
                              | Qt.Popup 
                              | Qt.WindowStaysOnTopHint)
        
        # center the window 
        self.window.setFixedSize(350,300)
        self.window.move(QApplication.desktop().screen().rect().center() - self.window.rect().center())
        self.layout = QVBoxLayout()

class SettingsPopup(PopUpWindow):
    on_settings_saved = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.widgets = dict()

        self.layout.addStretch()

        self.widgets['header'] = self.create_header()
        self.layout.addWidget(self.widgets['header'])

        self.layout.addStretch()

        self.widgets['validator_settings'] = self.create_validator_settings()
        self.layout.addLayout(self.widgets['validator_settings'])

        self.widgets['database_settings'] = self.create_database_settings()
        self.layout.addLayout(self.widgets['database_settings'])

        self.widgets['database_name'] = self.create_database_name()
        self.layout.addLayout(self.widgets['database_name'])

        self.layout.addStretch()
        
        self.widgets['save_button'] = self.create_save_button()
        self.layout.addWidget(self.widgets['save_button'])
        
        self.layout.addStretch()


        self.layout.addStretch()

        self.window.setLayout(self.layout)

    
    def create_header(self):
        label = QLabel('Settings')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 20px;')
        return label
    
    def create_validator_settings(self):
        hbox = QHBoxLayout()
        label = QLabel('Validator Name')
         
        label.setFixedWidth(150)
        
        self.validator_name = QLineEdit()
        self.validator_name.setText(constants.VALIDATOR_NAME)
        self.validator_name.setFixedWidth(150)

        hbox.addWidget(label)
        hbox.addWidget(self.validator_name)
        return hbox
    
    def create_database_settings(self):
        hbox = QHBoxLayout()
        label = QLabel('Database URL')
        label.setFixedWidth(150)

        self.data_base_url = QLineEdit()
        self.data_base_url.setText(constants.DATABASE_URL)
        self.data_base_url.setFixedWidth(150)

        hbox.addWidget(label)
        hbox.addWidget(self.data_base_url)
        return hbox
    
    def create_database_name(self):
        hbox = QHBoxLayout()
        label = QLabel('Database Name')
        label.setFixedWidth(150)

        self.database_name = QLineEdit()
        self.database_name.setText(constants.DATABASE_NAME)
        self.database_name.setFixedWidth(150)

        hbox.addWidget(label)
        hbox.addWidget(self.database_name)
        return hbox
    
    def create_save_button(self):
        button = QPushButton('Save')
        button.clicked.connect(self.on_save_button_click)
        return button
    
    def on_save_button_click(self):
        constants.VALIDATOR_NAME = self.validator_name.text()
        constants.DATABASE_URL = self.data_base_url.text()
        constants.DATABASE_NAME = self.database_name.text()
        self.window.hide()
        self.on_settings_saved.emit()

