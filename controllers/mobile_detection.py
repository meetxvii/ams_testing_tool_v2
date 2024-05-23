from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from controller import Controller
import requests

class DrawableRectItem(QGraphicsRectItem):
    def __init__(self, rect=QRectF(), pen=QPen(Qt.red, 3), brush=QBrush(Qt.NoBrush)):
        super().__init__(rect)
        self.setPen(pen)
        self.setBrush(brush)
        self.initial_pen = pen  # Store the initial pen
        self.is_hovering = False  # Track hover state
        self.is_creating = True
        self.offset = []
        self.data = None
        self.is_changed = False
        self.is_created = True
    
    def hoverEnterEvent(self, event):
        self.is_hovering = True
        hover_pen = QPen(Qt.blue, self.pen().width())  # Create a red pen with the same line width
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

        self.display_bboxes(documents['documents'], display_object)

    def display_bboxes(self, documents, display_object):
        self.old_bboxes = dict()
        self.created_bboxes = []
        self.removed_bboxes = dict()
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
                
                display_object.scene.addItem(rect_item)
                self.old_bboxes[document['_id']] = self.old_bboxes.get(document['_id'],[]) + [rect_item]
        display_object.view.setFocus()

       
    def on_approve_button_click(self, display_object):
        print('-'*100)
        print(f"Old Bboxes: {self.old_bboxes}")
        print(f"Created Bboxes: {self.created_bboxes}")
        print(f"Removed Bboxes: {self.removed_bboxes}")
    
    def on_skip_button_click(self, display_object):
        if self.current_position > 0:
            self.current_position -= 1
            self.update_view(display_object)


    def mousePressEvent(self, event, display_object):
        scene_event = display_object.view.mapToScene(event.pos()) 
        

        if event.button() == Qt.LeftButton:
            item = display_object.scene.itemAt(scene_event, QTransform())
            if isinstance(item, DrawableRectItem):  
                # If there's already bbox present
                self.current_rect = item
                self.start_pos = scene_event
                self.current_rect.hoverEnterEvent(event)
                self.current_rect.is_creating = False
                self.current_rect.offset = [event.pos().x()-self.current_rect.rect().x(), 
                                         event.pos().y()-self.current_rect.rect().y() ]                    
            else:                                   
                # create New DrawableRectItem Object
                self.start_pos = scene_event
                rect = QRectF(self.start_pos, self.start_pos)
                self.current_rect = DrawableRectItem(rect)
                display_object.scene.addItem(self.current_rect)
                self.created_bboxes.append(self.current_rect)  
    
    def mouseMoveEvent(self, event, display_object):
        
        if (not event.buttons() & Qt.LeftButton) or self.current_rect is None:
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
        else:
            # Moving bbox
            self.current_rect.is_changed = True
            new_position = [event.pos().x()-self.current_rect.offset[0],
                            event.pos().y()-self.current_rect.offset[1]]
            self.current_rect.setRect(QRectF(new_position[0],new_position[1],self.current_rect.rect().width(),self.current_rect.rect().height()))
            

    def mouseReleaseEvent(self, event, display_object):
        
        if event.button() == Qt.LeftButton:
            if self.current_rect is not None:
                self.current_rect.hoverLeaveEvent(event)
            self.start_pos = None
            self.current_rect = None
        
    def keyPressEvent(self, event, display_object):
        if event.key() == Qt.Key_Delete:
            if self.current_rect:
                display_object.scene.removeItem(self.current_rect)
                if self.current_rect.is_created:
                    self.created_bboxes.remove(self.current_rect)
                else:
                    parent_doc = self.current_rect.parent_document
                    self.old_bboxes[parent_doc].remove(self.current_rect)
                    self.removed_bboxes[parent_doc] = self.removed_bboxes.get(parent_doc,[]) + [self.current_rect]

                self.current_rect = None    
        

   