from model import Model
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Controller:
    def __init__(self) -> None:
        self.model = Model()
        self.current_position = 0
        self.data = []

    # Filters handler
    def add_sites_options(self, filter_object):
        widget = filter_object.widgets["site"]
        sites = self.model.get_unique_sites()
        widget.addItems(sites)

    def on_site_change(self, filter_object):
        site_widget = filter_object.widgets["site"]
        floor_widget = filter_object.widgets["floor"]
        selected_site = site_widget.currentText()
        floors = self.model.get_floors(selected_site)
        floor_widget.clear()
        floor_widget.addItems(floors)

    def on_next_button_click(self, display_object):
        if len(self.data) == self.current_position:
            return
        self.current_position += 1
        self.update_view(display_object)

    def on_previous_button_click(self, display_object):
        if self.current_position == 0:
            return
        self.current_position -= 1
        self.update_view(display_object)

    def mousePressEvent(self, event, display_object):
        pass

    def mouseMoveEvent(self, event, display_object):
        pass

    def mouseReleaseEvent(self, event, display_object):
        pass

    def keyPressEvent(self, event, display_object):
        pass

    def keyReleaseEvent(self, event, display_object):
        pass

    def wheelEvent(self, event, display_object):
        change = event.angleDelta().y()//120
        display_object.view.scale(1+change/10,1+change/10)
        display_object.view.centerOn(display_object.view.mapToScene(event.pos()))

