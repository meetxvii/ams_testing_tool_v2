from PyQt5.QtWidgets import QHBoxLayout,QComboBox,QDateTimeEdit,QPushButton
from PyQt5.QtCore import QObject,pyqtSignal,QDate,QDateTime,QTime
from PyQt5.QtGui import QIcon

class Filters(QObject):
    on_filter_change = pyqtSignal()
    def __init__(self,controller) -> None:
        super().__init__()
        self.layout = QHBoxLayout()
        self.widgets = dict()
        self.controller = controller

        self.widgets['floor'] = self.create_floor_filter()

        self.widgets['site'] = self.create_site_filter()
        self.controller.add_sites_options(self)
        self.layout.addWidget(self.widgets['site'])

        self.controller.on_site_change(self)
        self.layout.addWidget(self.widgets['floor'])

        self.widgets['start_datetime'] = self.create_date_filter(QDate().currentDate().addDays(-15))
        self.layout.addWidget(self.widgets['start_datetime'])

        self.widgets['end_datetime'] = self.create_date_filter(QDate().currentDate())
        self.layout.addWidget(self.widgets['end_datetime'])

        self.widgets['filter_button'] = self.create_filter_button()
        self.layout.addWidget(self.widgets['filter_button'])

        self.widgets['config_button'] = self.create_config_button()

        self.layout.addWidget(self.widgets['config_button'])

    def create_site_filter(self):
        site = QComboBox()
        site.currentTextChanged.connect(lambda : self.controller.on_site_change(self))
        return site
    
    def create_floor_filter(self):
        floor = QComboBox()
        return floor

    def create_date_filter(self,date):
        date_filter = QDateTimeEdit()
        date_filter.setDateTime(QDateTime(date,QTime()))
        date_filter.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        date_filter.setCalendarPopup(True)
        return date_filter
    
    def create_filter_button(self):
        filter_button = QPushButton('Filter')
        filter_button.clicked.connect(self.on_filter_button_click)
        return filter_button
    
    def create_config_button(self):
        config_button = QPushButton('')
        settings_icon= QIcon('icons/settings.png')
        config_button.setIcon(settings_icon)
        config_button.clicked.connect(self.on_settings_button_click)
        config_button.setFixedWidth(30)
        return config_button
    
    def on_settings_button_click(self):
        self.controller.on_settings_button_click()

    def on_filter_button_click(self):
        self.controller.on_filter_button_click(self)
        self.on_filter_change.emit()