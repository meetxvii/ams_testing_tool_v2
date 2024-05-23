from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
from controller import Controller


class OccupancyClassification(Controller):
    def on_filter_button_click(self, filter_object):
        site_name = filter_object.widgets["site"].currentText()
        floor_name = filter_object.widgets["floor"].currentText()
        start_time = (
            filter_object.widgets["start_datetime"].dateTime().toString(Qt.ISODate)
        )
        end_time = filter_object.widgets["end_datetime"].dateTime().toString(Qt.ISODate)
        self.data = list(
            self.model.get_occupancy_data(site_name, floor_name, start_time, end_time)
        )

    def update_view(self, display_object):
        display_object.scene.clear()
        documents = self.data[self.current_position]

        image_url = documents["_id"]
        print(image_url)
        image = QPixmap()
        image.loadFromData(requests.get(image_url).content)
        image = image.scaled(1100, 1100, Qt.KeepAspectRatio)
        self.current_image_size = image.size()
        display_object.scene.addPixmap(image)

        width, height = image.width(), image.height()
        display_object.view.setFixedSize(width + 2, height + 2)

        self.display_roi(display_object)

    def display_roi(self, display_object):
        width, height = (
            self.current_image_size.width(),
            self.current_image_size.height(),
        )
        current_data = self.data[self.current_position]
        self.roi_values = []
        self.status_dic = {}
        for document in current_data["documents"]:
            polygons = []
            for rois in document["img_data"]["rois"]:
                if rois["status"] == "full":
                    self.color = Qt.green
                elif rois["status"] == "empty":
                    self.color = Qt.red
                else:
                    self.color = Qt.blue
                polygon = QPolygonF()
                for point in rois["points"]:
                    x, y = point[0] * width, point[1] * height
                    polygon.append(QPointF(x, y))

                polygons.append(polygon)

            for polygon in polygons:
                self.item = CustomPolygon(polygon, self.color)
                self.item.setPen(QPen(self.color, 3, Qt.SolidLine))
                display_object.scene.addItem(self.item)
                self.status_dic[document["_id"]] = self.item
                self.roi_values.append(document["_id"])

    def on_approve_button_click(self, display_object):
        for database_id in self.roi_values:
            
            self.model.occupancy_classification_update_date(database_id, self.status_dic[database_id].status,"prink hapaliya")

        if self.current_position == len(self.data) - 1:
            return
        self.current_position += 1
        self.update_view(display_object)

    def on_skip_button_click(self, display_object):
        if self.current_position == len(self.data) - 1:
            return
        self.current_position += 1
        self.update_view(display_object)


class CustomPolygon(QGraphicsPolygonItem):
    def __init__(
        self,
        polygon=None,
        color=None,
    ):
        super().__init__(polygon)

        self.color = color
        self.polygon = polygon
        self.count_ = 0
        self.status = True

    def check_status(self):
        if self.count_ % 2 == 0:
            self.status = True
        else:
            self.status = False

    def mousePressEvent(self, event) -> None:
        self.count_ = self.count_ + 1
        self.check_status()
        if self.color == Qt.red:
            self.color = Qt.green
            self.setPen(QPen(Qt.green, 3, Qt.SolidLine))
        elif self.color == Qt.green:
            self.color = Qt.red
            self.setPen(QPen(Qt.red, 3, Qt.SolidLine))

