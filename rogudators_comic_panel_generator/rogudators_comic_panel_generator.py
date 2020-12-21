from .rcpg_module import RCPG
import sys
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsView, QVBoxLayout, QMainWindow, QGraphicsScene, QLabel, QPushButton, QHBoxLayout, QSpinBox, QSlider, QCheckBox, QScrollArea, QWidget, QApplication, QColorDialog, QGraphicsItem
from PyQt5.Qt import Qt
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtGui import QColor, QImage
import tempfile
from krita import *

class Clickable_gutter(QGraphicsRectItem):
    #load rcpj object and gutter index in the list
    def setRCPGObject(self, rcpg_object, i, j):
        self.rcpg_object = rcpg_object
        self.i = i
        self.j = j
    
    #hide/unhide gutter on click
    def mousePressEvent(self, event):
        if self.rcpg_object.planes[self.i][self.j]==True:
            self.rcpg_object.hide_plane(self.i,self.j)
            self.rcpg_object.refresh_vertices_connections()
            self.rcpg_object.refresh_svg_renderer()
        else:
            self.rcpg_object.unhide_plane(self.i,self.j)
            self.rcpg_object.refresh_vertices_connections()
            self.rcpg_object.refresh_svg_renderer()
        return QGraphicsRectItem.mousePressEvent(self, event)

class Page_preview(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setAlignment(Qt.AlignLeft or Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    #at what index rcpg object exists in qgraphicsscene
    def get_rcpg_object_id(self, rcpg_object_id):
        self.rcpg_object_id = rcpg_object_id
    
    #after you clicked on a gutter, refresh the image
    def mouseReleaseEvent(self, event):
        scene = self.scene()
        scene.items()[self.rcpg_object_id].update()
        r = scene.sceneRect()
        self.updateView()
        self.updateSceneRect(r)
        return QGraphicsView.mouseReleaseEvent(self, event)
    
    #make sure that preview expands without losing proprotions
    def updateView(self):
        scene = self.scene()
        rect_scene = scene.sceneRect() 
        rect_view = self.rect() 
        minheight = rect_scene.height() * rect_view.width() / rect_scene.width()
        self.fitInView(rect_scene, Qt.KeepAspectRatioByExpanding)
        self.setMinimumHeight(minheight)

    
    #call this events when window is resized
    def resizeEvent(self, event):
        self.updateView()
    
    def showEvent(self, event):
        if not event.spontaneous():
            self.updateView()

class RCPGWindow(DockWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rogudator's comic panel generator")

        mainLayout = QVBoxLayout()

        #l means label
        #b means push button
        #sp means spinbox
        #sl means slider
        #cb means combobox

        l_preview = QLabel(self)
        l_preview.setText("Preview:")
        mainLayout.addWidget(l_preview)

        self.rcpg_object = RCPG()
        self.rcpg_object.refresh_svg_renderer()

        renderer = self.rcpg_object.svg_renderer
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(renderer)

        self.preview = Page_preview()
        self.preview.scene().addItem(self.svg_item)
        mainLayout.addWidget(self.preview)

        self.set_clickable_gutters()

        l_generate = QLabel(self)
        l_generate.setText("Generate as:")
        mainLayout.addWidget(l_generate)

        b_layer = QPushButton(self)
        b_layer.setText("Layer")

        b_file = QPushButton(self)
        b_file.setText("File")

        file_and_layer = QHBoxLayout(self)
        file_and_layer.addWidget(b_layer)
        file_and_layer.addWidget(b_file)
        mainLayout.addLayout(file_and_layer)

        l_num_rows = QLabel(self)
        l_num_rows.setText("Number of rows:")
        mainLayout.addWidget(l_num_rows)

        self.sp_num_rows = QSpinBox(self)
        self.sp_num_rows.setValue(2)
        self.sp_num_rows.setMinimum(1)

        self.sl_num_rows = QSlider(self)
        self.sl_num_rows.setMinimum(1)
        self.sl_num_rows.setMaximum(6)
        self.sl_num_rows.setOrientation(Qt.Horizontal)
        self.sl_num_rows.setTickPosition(1)
        self.sl_num_rows.setTickInterval(1)
        self.sl_num_rows.setMinimumWidth(100)
        self.sl_num_rows.setValue(2)

        num_rows = QHBoxLayout(self)
        num_rows.addWidget(self.sp_num_rows)
        num_rows.addWidget(self.sl_num_rows)
        mainLayout.addLayout(num_rows)

        l_num_columns = QLabel(self)
        l_num_columns.setText("Numer of columns:")
        mainLayout.addWidget(l_num_columns)

        self.sp_num_columns = QSpinBox(self)
        self.sp_num_columns.setValue(2)
        self.sp_num_columns.setMinimum(1)

        self.sl_num_columns = QSlider(self)
        self.sl_num_columns.setMinimum(1)
        self.sl_num_columns.setMaximum(6)
        self.sl_num_columns.setOrientation(Qt.Horizontal)
        self.sl_num_columns.setTickPosition(1)
        self.sl_num_columns.setTickInterval(1)
        self.sl_num_columns.setMinimumWidth(100)
        self.sl_num_columns.setValue(2)

        num_columns = QHBoxLayout(self)
        num_columns.addWidget(self.sp_num_columns)
        num_columns.addWidget(self.sl_num_columns)
        mainLayout.addLayout(num_columns)

        l_gutter = QLabel(self)
        l_gutter.setText("Gutters")
        mainLayout.addWidget(l_gutter)

        self.cb_gutter_equal = QCheckBox(self)
        self.cb_gutter_equal.setText("Horizontal and vertical gutters are equal")
        self.cb_gutter_equal.setChecked(True)
        mainLayout.addWidget(self.cb_gutter_equal)

        l_hgutter = QLabel(self)
        l_hgutter.setText("Size of a horizontal gutter:")
        mainLayout.addWidget(l_hgutter)

        self.hgutter_updated = True

        self.hgutter_max = int(self.rcpg_object.height_page / (self.rcpg_object.rows + 1))

        self.sp_hgutter = QSpinBox(self)
        self.sp_hgutter.setValue(30)
        self.sp_hgutter.setMinimum(1)
        self.sp_hgutter.setMaximum(self.hgutter_max)

        self.sl_hgutter = QSlider(self)
        self.sl_hgutter.setMaximum(1)
        self.sl_hgutter.setMaximum(self.hgutter_max)
        self.sl_hgutter.setOrientation(Qt.Horizontal)
        self.sl_hgutter.setTickInterval(1)
        self.sl_hgutter.setMinimumWidth(100)
        self.sl_hgutter.setValue(30)

        hgutter = QHBoxLayout(self)
        hgutter.addWidget(self.sp_hgutter)
        hgutter.addWidget(self.sl_hgutter)
        mainLayout.addLayout(hgutter)

        l_vgutter = QLabel(self)
        l_vgutter.setText("Size of a vertical gutter:")
        mainLayout.addWidget(l_vgutter)

        self.vgutter_updated = True

        self.vgutter_max = int(self.rcpg_object.width_page / (self.rcpg_object.columns + 1))

        self.sp_vgutter = QSpinBox(self)
        self.sp_vgutter.setValue(30)
        self.sp_vgutter.setMinimum(1)
        self.sp_vgutter.setMaximum(self.vgutter_max)

        self.sl_vgutter = QSlider(self)
        self.sl_vgutter.setMaximum(1)
        self.sl_vgutter.setMaximum(self.vgutter_max)
        self.sl_vgutter.setOrientation(Qt.Horizontal)
        self.sl_vgutter.setTickInterval(1)
        self.sl_vgutter.setMinimumWidth(100)
        self.sl_vgutter.setValue(30)

        vgutter = QHBoxLayout(self)
        vgutter.addWidget(self.sp_vgutter)
        vgutter.addWidget(self.sl_vgutter)
        mainLayout.addLayout(vgutter)

        l_cgutter = QLabel(self)
        l_cgutter.setText("Color of the gutter:")
        mainLayout.addWidget(l_cgutter)

        self.l_color_gutter = QLabel(self)
        self.l_color_gutter.setText("#000000")

        b_color_gutter = QPushButton(self)
        b_color_gutter.setText("Change")

        color_of_gutter = QHBoxLayout(self)
        color_of_gutter.addWidget(self.l_color_gutter)
        color_of_gutter.addWidget(b_color_gutter)
        mainLayout.addLayout(color_of_gutter)

        l_outline = QLabel(self)
        l_outline.setText("Size of panel outline:")
        mainLayout.addWidget(l_outline)

        self.sp_outline = QSpinBox(self)
        self.sp_outline.setValue(6)
        self.sp_outline.setMinimum(0)

        self.sl_outline = QSlider(self)
        self.sl_outline.setMinimum(0)
        self.sl_outline.setMaximum(98)
        self.sl_outline.setOrientation(Qt.Horizontal)
        self.sl_outline.setTickInterval(1)
        self.sl_outline.setMinimumWidth(100)
        self.sl_outline.setValue(6)

        outline = QHBoxLayout(self)
        outline.addWidget(self.sp_outline)
        outline.addWidget(self.sl_outline)
        mainLayout.addLayout(outline)

        l_color_outline = QLabel(self)
        l_color_outline.setText("Color of panel outline:")
        mainLayout.addWidget(l_color_outline)

        self.l_color_outline = QLabel(self)
        self.l_color_outline.setText("#ffffff")

        b_color_outline = QPushButton(self)
        b_color_outline.setText("Change")

        color_of_outline = QHBoxLayout(self)
        color_of_outline.addWidget(self.l_color_outline)
        color_of_outline.addWidget(b_color_outline)
        mainLayout.addLayout(color_of_outline)

        self.scrollMainLayout = QScrollArea(self)
        self.scrollMainLayout.setWidgetResizable(True)
        self.scrollMainLayout.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        b_file.clicked.connect(self.b_file_create)
        b_layer.clicked.connect(self.b_layer_create)
        self.sp_num_rows.valueChanged.connect(self.upd_sp_num_rows)
        self.sl_num_rows.valueChanged.connect(self.upd_sl_num_rows)
        self.sp_num_columns.valueChanged.connect(self.upd_sp_num_columns)
        self.sl_num_columns.valueChanged.connect(self.upd_sl_num_columns)
        self.sp_hgutter.valueChanged.connect(self.upd_sp_hgutter)
        self.sl_hgutter.valueChanged.connect(self.upd_sl_hgutter)
        self.sp_vgutter.valueChanged.connect(self.upd_sp_vgutter)
        self.sl_vgutter.valueChanged.connect(self.upd_sl_vgutter)
        b_color_gutter.clicked.connect(self.color_gutter_dialog)
        self.sp_outline.valueChanged.connect(self.upd_sp_outline)
        self.sl_outline.valueChanged.connect(self.upd_sl_outline)
        b_color_outline.clicked.connect(self.color_outline_dialog)
        

        self.window = QWidget(self)
        self.window.setLayout(mainLayout)
        self.scrollMainLayout.setWidget(self.window)
        self.setWidget(self.scrollMainLayout)
        self.show()
    
    def b_file_create(self):
        temp_dir = tempfile.gettempdir() + "/rcpg10.svg"
        body = self.rcpg_object.get_svg_string()
        with open(temp_dir, 'w', encoding='utf-8') as f:
            f.write(body)
        file = Krita.instance().openDocument(temp_dir)
        Krita.instance().activeWindow().addView(file)
        file.refreshProjection()
            
    
    def b_layer_create(self):
        temp_dir = tempfile.gettempdir() + "/rcpg10.svg"
        body = self.rcpg_object.get_svg_string()
        with open(temp_dir, 'w', encoding='utf-8') as f:
            f.write(body)
        app = Krita.instance()
        doc = app.activeDocument()
        if doc != None:
            root = doc.rootNode()
            layer = doc.createNode("Panels", "paintLayer")
            img = QImage(temp_dir)
            img = img.scaled(doc.width(), doc.height(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            if not img.isNull():
                img.convertToFormat(QImage.Format_RGBA8888)
                ptr = img.constBits()
                ptr.setsize(img.byteCount())
                layer.setPixelData(bytes(ptr.asarray()), 0, 0, img.width(), img.height())
            root.addChildNode(layer, None)
            doc.refreshProjection()
    
    def upd_sp_num_rows(self):
        self.preview.scene().clear()
        rows = self.sp_num_rows.value()
        if rows>0 and rows<7:
            self.sl_num_rows.setValue(rows)
        
        self.hgutter_max = int(self.rcpg_object.height_page / (rows+1))
        self.sp_hgutter.setMaximum(self.hgutter_max)
        self.sl_hgutter.setMaximum(self.hgutter_max)

        self.rcpg_object.rows = rows
        self.rcpg_object.upd_everything()
        self.rcpg_object.standard_grid()
        self.rcpg_object.refresh_svg_renderer()
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.rcpg_object.svg_renderer)
        self.preview.scene().addItem(self.svg_item)
        self.set_clickable_gutters()
        self.svg_item.update()

    def upd_sl_num_rows(self):
        self.sp_num_rows.setValue(self.sl_num_rows.value())
    
    def upd_sp_num_columns(self):
        self.preview.scene().clear()
        columns = self.sp_num_columns.value()
        if columns>0 and columns<7:
            self.sl_num_columns.setValue(columns)
        
        self.vgutter_max = int(self.rcpg_object.width_page / (columns+1))
        self.sp_vgutter.setMaximum(self.vgutter_max)
        self.sl_vgutter.setMaximum(self.vgutter_max)

        self.rcpg_object.columns = columns
        self.rcpg_object.upd_everything()
        self.rcpg_object.standard_grid()
        self.rcpg_object.refresh_svg_renderer()
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.rcpg_object.svg_renderer)
        self.preview.scene().addItem(self.svg_item)
        self.set_clickable_gutters()
        self.svg_item.update()

    def upd_sl_num_columns(self):
        self.sp_num_columns.setValue(self.sl_num_columns.value())
    
    def upd_sp_hgutter(self):
        horizontal_gutter = self.sp_hgutter.value()
        if horizontal_gutter>0 and horizontal_gutter<self.hgutter_max:
            self.sl_hgutter.setValue(horizontal_gutter)
        self.rcpg_object.horizontal_gutter = horizontal_gutter

        if self.cb_gutter_equal.isChecked() == True:
            self.hgutter_updated = False
            self.sp_vgutter.setValue(horizontal_gutter)
            if horizontal_gutter>0 and horizontal_gutter<self.vgutter_max:
                self.sl_vgutter.setValue(horizontal_gutter)
            self.rcpg_object.vertical_gutter = horizontal_gutter
        
        if self.hgutter_updated == True:
            self.preview.scene().clear()
            self.rcpg_object.upd_everything()
            self.rcpg_object.standard_grid()
            self.rcpg_object.refresh_svg_renderer()
            self.svg_item = QGraphicsSvgItem()
            self.svg_item.setSharedRenderer(self.rcpg_object.svg_renderer)
            self.preview.scene().addItem(self.svg_item)
            self.set_clickable_gutters()
            self.svg_item.update()
        else:
            self.hgutter_updated = True
    
    def upd_sl_hgutter(self):
        horizontal_gutter = self.sl_hgutter.value()
        self.sp_hgutter.setValue(horizontal_gutter)
        self.rcpg_object.horizontal_gutter = horizontal_gutter

        if self.cb_gutter_equal.isChecked() == True:
            self.sp_vgutter.setValue(horizontal_gutter)
            if horizontal_gutter>0 and horizontal_gutter<self.vgutter_max:
                self.sl_vgutter.setValue(horizontal_gutter)
            self.rcpg_object.vertical_gutter = horizontal_gutter

    def upd_sp_vgutter(self):
        vertical_gutter = self.sp_vgutter.value()
        if vertical_gutter>0 and vertical_gutter<self.vgutter_max:
            self.sl_vgutter.setValue(vertical_gutter)
        self.rcpg_object.vertical_gutter = vertical_gutter

        if self.cb_gutter_equal.isChecked() == True:
            self.hgutter_updated = False
            self.sp_hgutter.setValue(vertical_gutter)
            if vertical_gutter>0 and vertical_gutter<self.hgutter_max:
                self.sl_hgutter.setValue(vertical_gutter)
            self.rcpg_object.horizontal_gutter = vertical_gutter
        
        if self.vgutter_updated == True:
            self.preview.scene().clear()
            self.rcpg_object.upd_everything()
            self.rcpg_object.standard_grid()
            self.rcpg_object.refresh_svg_renderer()
            self.svg_item = QGraphicsSvgItem()
            self.svg_item.setSharedRenderer(self.rcpg_object.svg_renderer)
            self.preview.scene().addItem(self.svg_item)
            self.set_clickable_gutters()
            self.svg_item.update()
        else:
            self.vgutter_max = True
        
    def upd_sl_vgutter(self):
        vertical_gutter = self.sl_vgutter.value()
        self.sp_vgutter.setValue(vertical_gutter)
        self.rcpg_object.vertical_gutter = vertical_gutter

        if self.cb_gutter_equal.isChecked() == True:
            self.sp_hgutter.setValue(vertical_gutter)
            if vertical_gutter>0 and vertical_gutter<self.hgutter_max:
                self.sl_hgutter.setValue(vertical_gutter)
            self.rcpg_object.vertical_gutter = vertical_gutter
    
    def color_gutter_dialog(self):
        color = QColorDialog.getColor(QColor(self.l_color_gutter.text()))
        self.l_color_gutter.setText(color.name())
        self.rcpg_object.gutter_color = self.l_color_gutter.text()
        self.rcpg_object.refresh_svg_renderer()
        self.svg_item.update()
        self.update()

    def upd_sp_outline(self):
        self.preview.scene().clear()
        outline = self.sp_outline.value()
        self.rcpg_object.outline = outline

        self.rcpg_object.upd_everything()
        self.rcpg_object.standard_grid()
        self.rcpg_object.refresh_svg_renderer()
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.rcpg_object.svg_renderer)
        self.preview.scene().addItem(self.svg_item)
        self.set_clickable_gutters()
        self.svg_item.update()

    def upd_sl_outline(self):
        outline = self.sl_outline.value()
        self.sp_outline.setValue(outline)    

    def color_outline_dialog(self):
        color = QColorDialog.getColor(QColor(self.l_color_outline.text()))
        self.l_color_outline.setText(color.name())
        self.rcpg_object.outline_color = self.l_color_outline.text()
        self.rcpg_object.refresh_svg_renderer()
        self.svg_item.update()
        self.update()
    
    def set_clickable_gutters(self):
        for i in range(self.rcpg_object.rows_vertices-1):
            for j in range(self.rcpg_object.columns_vertices-1):
                x = self.rcpg_object.vertex_coordinate_x[j]
                y = self.rcpg_object.vertex_coordinate_y[i]
                width = self.rcpg_object.vertex_coordinate_x[j+1] - self.rcpg_object.vertex_coordinate_x[j]
                height = self.rcpg_object.vertex_coordinate_y[i+1] - self.rcpg_object.vertex_coordinate_y[i]
                gutter_plane = Clickable_gutter(x,y,width,height)
                gutter_plane.setAcceptHoverEvents(True)
                gutter_plane.setRCPGObject(self.rcpg_object, i, j)
                gutter_plane.setFlag(QGraphicsItem.ItemIsSelectable)
                self.preview.scene().addItem(gutter_plane)
        self.preview.get_rcpg_object_id((self.rcpg_object.rows_vertices-1)*(self.rcpg_object.columns_vertices-1))
    

    def canvasChanged(self, canvas):
        app = Krita.instance()
        doc = app.activeDocument()
        if doc != None:
            self.preview.scene().clear()
            self.rcpg_object.height_page= doc.height()
            self.rcpg_object.width_page = doc.width()
            self.rcpg_object.upd_everything()
            self.rcpg_object.standard_grid()
            self.rcpg_object.refresh_svg_renderer()
            self.svg_item = QGraphicsSvgItem()
            self.svg_item.setSharedRenderer(self.rcpg_object.svg_renderer)
            self.preview.scene().addItem(self.svg_item)
            self.set_clickable_gutters()
            self.svg_item.update()
            iii = self.preview.scene().sceneRect()
            if doc.height()>doc.width():
                iii.setHeight(doc.height())
            else:
                iii.setHeight(doc.height())
                iii.setWidth(doc.width())
            self.preview.scene().setSceneRect(iii)
            self.preview.updateView()



