from model import Model
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import constants
import requests
from handlers.drawable_rect import DrawableRectItem


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


class OccupancyDetection(Controller):
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
            # print(document["_id"])
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
