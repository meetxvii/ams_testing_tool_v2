from model import Model
from handlers.popup import SettingsPopup
import constants

class Controller:
    def __init__(self) -> None:
        self.connect_database()
        self.current_position = 0
        self.data = []
        self.settings_window = SettingsPopup()
        self.settings_window.on_settings_saved.connect(self.on_settings_saved)
        self.filter_object = None

    def connect_database(self):
        self.model = Model()
        if not self.model.connected:
            return

    # Filters handler
    def add_sites_options(self, filter_object):
        if self.filter_object is None:
            self.filter_object = filter_object
        
        widget = filter_object.widgets["site"]
        sites = self.model.get_unique_sites()
        widget.addItems(sites)

    def on_site_change(self, filter_object):
        if self.filter_object is None:
            self.filter_object = filter_object
        site_widget = filter_object.widgets["site"]
        floor_widget = filter_object.widgets["floor"]
        selected_site = site_widget.currentText()
        floors = self.model.get_floors(selected_site)
        floor_widget.clear()
        floor_widget.addItems(floors)
    
    def on_settings_button_click(self):
        self.settings_window.window.show()

    def on_settings_saved(self):
        self.connect_database()
        self.current_position = 0
        self.data = []
        self.actions.widgets['status_bar'].showMessage('Changed settings')
        if self.model.connected and not self.model.database_present:
            self.actions.widgets['status_bar'].showMessage('Database not present')
        self.add_sites_options(self.filter_object)
        self.on_site_change(self.filter_object)
        self.scene.clear()

    def on_next_button_click(self, display_object):
        if len(self.data) == self.current_position:
            return
        self.current_position += 1
        self.update_view(display_object)
        self.update_status_bar()

    def on_previous_button_click(self, display_object):
        if self.current_position == 0:
            return
        self.current_position -= 1
        self.update_view(display_object)
        self.update_status_bar()

    def update_status_bar(self):
        if len(self.data) != 0:
            self.actions.widgets['image_name'].setText(self.data[self.current_position]['_id'])
        
        self.actions.widgets['image_counter'].setText(f"{self.current_position+1}/{len(self.data)}")


    def enterEvent(self, event, display_object):
        pass

    def leaveEvent(self, event, display_object):
        pass

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

