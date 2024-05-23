from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from controller import Controller

class DrawableRectItem(QGraphicsRectItem):
    def __init__(self, rect=QRectF(), pen=QPen(Qt.white, 3), brush=QBrush(Qt.NoBrush)):
        super().__init__(rect)
        self.setPen(pen)
        self.setBrush(brush)
        self.initial_pen = pen  # Store the initial pen
        self.is_hovering = False  # Track hover state
        self.is_createing = True
        self.offset = []
        self.data = None
        self.is_changed = False
        self.is_created = True
    
    def hoverEnterEvent(self, event):
        self.is_hovering = True
        hover_pen = QPen(Qt.red, self.pen().width())  # Create a red pen with the same line width
        self.setPen(hover_pen)
    
    def hoverLeaveEvent(self, event):
        self.is_hovering = False
        self.setPen(self.initial_pen)  

class MobileDetection(Controller):
    def on_filter_button_click(self, filter_object):
        site_name = filter_object.widgets["site"].currentText()
        floor_name = filter_object.widgets["floor"].currentText()
        start_time = (
            filter_object.widgets["start_datetime"].dateTime().toString(Qt.ISODate)
        )
        end_time = filter_object.widgets["end_datetime"].dateTime().toString(Qt.ISODate)
        self.data = list(
            self.model.get_mobile_usages(site_name, floor_name, start_time, end_time)
        )

    def update_view(self, display_object):
        display_object.scene.clear()
        documents = self.data[self.current_position]

        image_url = documents["_id"]
        image = QPixmap()
        image.loadFromData(requests.get(image_url).content)
        image = image.scaled(1100, 1100, Qt.KeepAspectRatio)
        self.current_image_size = image.size()
        display_object.scene.addPixmap(image)

        width, height = image.width(), image.height()
        display_object.view.setFixedSize(width + 2, height + 2)

        self.display_bboxes(display_object)

    def display_bboxes(self, display_object):
        current_data = self.data[self.current_position]
        for document in current_data["documents"]:
            for bbox in document["img_data"]["phone_results"]:
                bbox = bbox["bbox"]
                x1, y1, x2, y2 = bbox
                width, height = (
                    self.current_image_size.width(),
                    self.current_image_size.height(),
                )
                x1 = x1 * width
                y1 = y1 * height
                x2 = x2 * width
                y2 = y2 * height
                rect = QRectF(x1, y1, x2 - x1, y2 - y1)
                rect_item = DrawableRectItem(rect)
                rect_item.setPen(QPen(Qt.red, 2))
                display_object.scene.addItem(rect_item)

