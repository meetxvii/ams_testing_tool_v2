from PyQt5.QtWidgets import QApplication,QGraphicsRectItem
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPen, QBrush, QTransform, QPixmap
from controller import Controller
import requests
from pprint import pprint

class DrawableRectItem(QGraphicsRectItem):
    def __init__(self, rect=QRectF(), pen=QPen(Qt.green, 3), brush=QBrush(Qt.NoBrush)):
        super().__init__(rect)
        self.setPen(pen)
        self.setBrush(brush)

        self.initial_pen = pen  
        self.is_hovering = False  
        self.is_creating = False
        self.offset = []
        self.data = None
        self.is_created = False
        self.is_correct = True        
        self.parent_document = None
        self.index_in_document = None

    def hoverEnterEvent(self, event):
        self.is_hovering = True
        hover_pen = QPen(Qt.blue, self.pen().width())  
        self.setPen(hover_pen)
    
    def hoverLeaveEvent(self, event):
        self.is_hovering = False
        self.setPen(self.initial_pen)  
    
    def change_color(self):
        if self.is_correct:
            self.setPen(QPen(Qt.green, 3))
        else:
            self.setPen(QPen(Qt.red, 3))

class MobileDetection(Controller):
    def __init__(self) -> None:
        super().__init__()

        self.old_bboxes = dict()
        self.created_bboxes = []
        self.drawing_mode = False
        self.current_rect = None 

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
        self.update_status_bar()

    def update_view(self, display_object):
        if len(self.data) == 0 :
            self.actions.widgets["status_bar"].showMessage("No data found")
            return
        
        elif self.current_position >= len(self.data)-1:
            self.actions.widgets["status_bar"].showMessage("End of data")
            return

        display_object.scene.clear()
        documents = self.data[self.current_position]

        image_url = documents["_id"]
        image = QPixmap()
        try:
            image.loadFromData(requests.get(image_url).content)
        except Exception as e:
            self.actions.widgets["status_bar"].showMessage("Error loading image")
            return
        image = image.scaled(1100, 1100, Qt.KeepAspectRatio)
        self.current_image_size = image.size()
        display_object.scene.addPixmap(image)

        width, height = image.width(), image.height()
        display_object.view.setFixedSize(width + 2, height + 2)

        self.display_bboxes(documents['documents'], display_object)
        self.actions.widgets["status_bar"].clearMessage()

    def display_bboxes(self, documents, display_object):
        self.old_bboxes = dict()
        self.created_bboxes = []

        for document in documents:
            self.current_data = document
            for index,phone in enumerate(document['img_data']['phone_results']):
                bbox = phone['bbox']
                

                x1 = round(bbox[0]*self.current_image_size.width())
                y1 = round(bbox[1]*self.current_image_size.height())
                w = round(bbox[2]*self.current_image_size.width()) - x1
                h = round(bbox[3]*self.current_image_size.height()) - y1
                rect = QRectF(x1,y1,w,h)

                rect_item = DrawableRectItem(rect)
                rect_item.data = document
                rect_item.is_created = False
                rect_item.parent_document = document['_id']
                rect_item.index_in_document = index

                if "is_correct" in document:
                    rect_item.is_correct = document['is_correct']
                    rect_item.change_color()
                
                display_object.scene.addItem(rect_item)
                self.old_bboxes[document['_id']] = self.old_bboxes.get(document['_id'],[]) + [rect_item]
        display_object.view.setFocus()

       
    def on_approve_button_click(self, display_object):
        correct_bboxes = []
        wrong_bboxes = []
        for document,bboxes in self.old_bboxes.items():
            for bbox in bboxes:
                if bbox.is_correct:
                    correct_bboxes.append(document)
                else:
                    self.data[self.current_position]['documents'][bbox.index_in_document]['is_correct'] = False
                    wrong_bboxes.append(document)
        self.model.update_mobile_data(correct_bboxes,wrong_bboxes)       

        new_bboxes_data = dict()
        new_bboxes_data['image'] = self.current_data['image']
        new_bboxes_data['site_name'] = self.current_data['site_name']
        new_bboxes_data['workspace_name'] = self.current_data['workspace_name']

        if 'camera_name' in self.current_data:
            new_bboxes_data['camera_name'] = self.current_data['camera_name']

        new_bboxes_data['bboxes'] = []
        
        for bbox in self.created_bboxes:
            x1,y1,x2,y2 = bbox.boundingRect().getCoords()
            x1 /= self.current_image_size.width()
            y1 /= self.current_image_size.height()
            x2 /= self.current_image_size.width()
            y2 /= self.current_image_size.height()
            new_bboxes_data['bboxes'].append([x1,y1,x2,y2])

        self.model.store_new_bboxes(new_bboxes_data)

        self.on_next_button_click(display_object)

    
    def on_skip_button_click(self, display_object):
        self.on_next_button_click(display_object)

    def enterEvent(self, event, display_object):
        if self.drawing_mode:
            QApplication.setOverrideCursor(Qt.CrossCursor)

    def leaveEvent(self, event, display_object):
        if self.drawing_mode:
            QApplication.restoreOverrideCursor()
        
    def keyPressEvent(self, event, display_object):
        if event.key() == Qt.Key_C:
            self.drawing_mode = not self.drawing_mode
            if self.drawing_mode:
                QApplication.setOverrideCursor(Qt.CrossCursor)
            else:
                QApplication.restoreOverrideCursor()        

    def mousePressEvent(self, event, display_object):
        scene_event = display_object.view.mapToScene(event.pos()) 

        if event.button() == Qt.LeftButton:
                                 
            item = display_object.scene.itemAt(scene_event, QTransform())
            if isinstance(item, DrawableRectItem) and not item.is_created:
                self.current_rect = item
                self.current_rect.is_correct = not self.current_rect.is_correct
                self.current_rect.change_color()

            elif self.drawing_mode:                                   
                # create New DrawableRectItem Object
                self.start_pos = scene_event
                rect = QRectF(self.start_pos, self.start_pos)
                self.current_rect = DrawableRectItem(rect)
                self.current_rect.setPen(QPen(Qt.cyan, 3))
                self.current_rect.is_creating = True
                self.current_rect.is_created = True
                display_object.scene.addItem(self.current_rect)
                self.created_bboxes.append(self.current_rect)

        elif event.button() == Qt.RightButton:
            item = display_object.scene.itemAt(scene_event, QTransform())
            if isinstance(item, DrawableRectItem) and item.is_created:
                display_object.scene.removeItem(item)
                self.created_bboxes.remove(item)
                self.current_rect = None
           
            
    def mouseMoveEvent(self, event, display_object):
        if not event.buttons() & Qt.LeftButton or self.current_rect is None:
            return
        if self.current_rect.is_creating:
            # creating new bbox
            scene_event = display_object.view.mapToScene(event.pos())
            view_rect = display_object.view.mapToScene(display_object.view.rect()).boundingRect()

            if self.current_rect and event.buttons() & Qt.LeftButton:
                if isinstance(self.current_rect, DrawableRectItem):
                    rect = QRectF(self.start_pos, scene_event).normalized()
                    clamped_rect = rect.intersected(view_rect)
                    self.current_rect.setRect(clamped_rect)
        
      
    def mouseReleaseEvent(self, event, display_object):
        if event.button() == Qt.LeftButton:
            self.start_pos = None
            self.current_rect = None
            self.drawing_mode = False
            QApplication.restoreOverrideCursor()