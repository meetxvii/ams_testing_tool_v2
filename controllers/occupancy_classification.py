from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
from handlers.drawable_rect import DrawableRectItem
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

        # print(self.data[0])

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

        self.display_roi(display_object)

    def display_roi(self, display_object):
        width, height = (
            self.current_image_size.width(),
            self.current_image_size.height(),
        )
        current_data = self.data[self.current_position]
        for document in current_data["documents"]:
            print(document["_id"])
            polygons = []
            for rois in document["img_data"]["rois"]:
                # print(rois["points"])
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
                # self.status_dic[roi_id]=self.item


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

    # def update_database(self, id_, status):
    #     self.id_ = id_
    #     self.database_object.update_date(self.id_, status)
