from krita import DockWidget


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QPushButton, QCheckBox, QScrollArea, QSpinBox, QSlider, QColorDialog, QGraphicsView, QGraphicsScene, QGraphicsRectItem,  QGraphicsItem
from PyQt5.Qt import Qt
from PyQt5.QtGui import QImage, QPen, QBrush, QColor
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5 import QtGui, QtCore
import tempfile

temp_dir = tempfile.gettempdir() + "/rcpg.svg"


#this class is responsible for creating comic panels
class RCPG():

    def upd_panel_sizes(self):
        self.width_panel = int(( self.width_page - ( self.horizontal_gutter * (self.columns+1) ))/ self.columns )
        self.height_panel = int(( self.height_page - ( self.vertical_gutter * (self.rows+1) ) )/ self.rows )
    
    def upd_vertices_amount(self):
        self.rows_vertices = self.rows*2+2
        self.columns_vertices = self.columns*2+2
        self.vertices_amount = self.rows_vertices * self.columns_vertices

    #creating adjacency matrix
    def upd_vertices(self):
        vertices = []
        vertices_amount = self.vertices_amount
        for i in range(vertices_amount):
            vertices.append([])
            for j in range(vertices_amount):
                vertices[i].append(False)
        self.vertices = vertices
    
    def update_vertex_coordinate(self):
        vertex_coordinate = []
        panel_corner_left_x = 0
        panel_corner_right_x = 0
        panel_corner_left_y = 0
        panel_corner_right_y = 0
        for i in range(self.rows_vertices):
            y = (panel_corner_left_y * self.vertical_gutter) + (panel_corner_right_y * self.height_panel)
            if i == 0:
                y = y - self.outline_size
            elif i == (self.rows_vertices-1):
                y = y + self.outline_size
            vertex_coordinate.append([])
            for j in range(self.columns_vertices):
                x = (panel_corner_left_x * self.horizontal_gutter) + (panel_corner_right_x * self.width_panel)
                if j == 0:
                    x = x - self.outline_size
                elif j == (self.columns_vertices-1):
                    x = x + self.outline_size
                coordinate = str(x) + "," + str(y)
                vertex_coordinate[i].append(coordinate)
                if (j%2) == 0:
                    panel_corner_left_x += 1
                else:
                    panel_corner_right_x += 1
            if (i%2) == 0:
                panel_corner_left_y += 1
            else:
                panel_corner_right_y += 1
            panel_corner_left_x = 0
            panel_corner_right_x = 0
        self.vertex_coordinate = vertex_coordinate
        panel_corner_left_x = 0
        panel_corner_right_x = 0
        panel_corner_left_y = 0
        panel_corner_right_y = 0
        vertex_coordinate_y = []
        vertex_coordinate_x = []
        for i in range(self.rows_vertices):
            y = (panel_corner_left_y * self.vertical_gutter) + (panel_corner_right_y * self.height_panel)
            vertex_coordinate_y.append(y)
            if (i%2) == 0:
                panel_corner_left_y += 1
            else:
                panel_corner_right_y += 1
        
        for i in range(self.columns_vertices):
            x = (panel_corner_left_x * self.horizontal_gutter) + (panel_corner_right_x * self.width_panel)
            vertex_coordinate_x.append(x)
            if (i%2) == 0:
                panel_corner_left_x += 1
            else:
                panel_corner_right_x += 1
        self.vertex_coordinate_y = vertex_coordinate_y
        self.vertex_coordinate_x = vertex_coordinate_x

    def standard_grid(self):
        # function to connect two vertices
        def to_v(vi, vj):
            return (vi*self.columns_vertices+vj)
        def join_v(vn,vm):
            self.vertices[vn][vm] = True
            self.vertices[vm][vn] = True

        # loop that makes standart 3x3 like layout when we first open plugin
        i = 1
        j = 1
        while i < (self.rows_vertices-1):
            while j < (self.columns_vertices-1):
                join_v(to_v( (i), (j) ), to_v( (i), (j+1) ))
                join_v(to_v( (i), (j+1) ), to_v( (i+1), (j+1) ))
                join_v(to_v( (i+1), (j+1) ), to_v( (i+1), (j) ))
                join_v(to_v( (i+1), (j) ), to_v( (i), (j) ))
                j += 2
            j = 1
            i += 2
    
    def upd_panels(self):
        planes = []
        for i in range(self.rows_vertices-1):
            planes.append([])
            for j in range(self.columns_vertices-1):
                planes[i].append(True)
        self.planes = planes

    def __init__(self):
        self.width_page =  800
        self.height_page = 1280
        self.rows = 3
        self.columns = 3
        self.horizontal_gutter = 30 
        self.vertical_gutter = 30
        self.color_gutter = "#FFFFFF"
        self.outline_size = 10
        self.outline_color = "#000000"

        self.upd_panel_sizes()
        self.upd_vertices_amount()
        self.upd_vertices()
        self.update_vertex_coordinate()
        self.standard_grid()
        self.upd_panels()

        self.svg_renderer = QSvgRenderer()
    
    def get_svg_string(self):
        #all coordinates will be added here
        path = ""
        #when added add vertex to this list, so we can see that it was used
        drawn = []
        vertices = self.vertices
        columns_vertices = self.columns_vertices
        vertex_coordinate = self.vertex_coordinate
        for i in range(self.vertices_amount):
            for j in range(self.vertices_amount):
                if (i in drawn):
                    pass
                elif (vertices[i][j] == True):
                    drawn.append(i)
                    n = int(i/columns_vertices)
                    m = int(i - n*columns_vertices)
                    path = path + "M" + vertex_coordinate[n][m] + " "
                    v = j
                    while(v!=i):
                        for k in range(self.vertices_amount):
                            if (k in drawn):
                                continue
                            elif (vertices[v][k] == True):
                                drawn.append(v)
                                n = int(v/columns_vertices)
                                m = int(v-n*columns_vertices)
                                path = path + vertex_coordinate[n][m] + " "
                                v = k
                                if(vertices[v][i] == True):
                                    drawn.append(v)
                                    n = int(v/columns_vertices)
                                    m = int(v-n*columns_vertices)
                                    path = path + vertex_coordinate[n][m] + "Z "
                                    v=i


        svg_file_text = "<?xml version=\"1.0\" encoding=\"utf-8\" ?><svg baseProfile=\"full\" height=\"{}px\" version=\"1.1\" width=\"{}px\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:ev=\"http://www.w3.org/2001/xml-events\" xmlns:xlink=\"http://www.w3.org/1999/xlink\"><defs /><path d=\"{}\" fill=\"{}\" fill-rule=\"evenodd\" stroke=\"{}\" stroke-width=\"{}\" style=\"stroke-linejoin:round;stroke-linecap:round\" /></svg>"

        page_corner_x = str(self.width_page + self.outline_size)
        page_corner_y = str(self.height_page + self.outline_size)
        page_beg = str(0 - self.outline_size)
        page = "M"+ page_beg +","+ page_beg +" "+ page_corner_x +","+ page_beg +" "+ page_corner_x +","+ page_corner_y +" "+ page_beg +","+ page_corner_y +"Z "


        path = page + path

        svg_file = svg_file_text.format(self.height_page, self.width_page, path, self.color_gutter, self.outline_color, self.outline_size)

        return svg_file
    
    def hide_plane(self, i, j):
        def to_v(vi, vj):
            return (vi*self.columns_vertices+vj)
        def join_v(vn,vm):
            self.vertices[vn][vm] = True
            self.vertices[vm][vn] = True
        def disjoin_v(vn,vm):
            self.vertices[vn][vm] = False
            self.vertices[vm][vn] = False
        tl = to_v(i,j) #top left corner
        tr = to_v(i,j+1) #top right corner
        bl = to_v(i+1,j) #bottom left corner
        br = to_v(i+1,j+1) #bottom right corner
        rows_vertices = self.rows_vertices
        columns_vertices = self.columns_vertices
        if (i%2==0) and (j%2!=0): #horizontal gutter
            if (i == 0):
                #join top left corner and top right corner
                join_v(tl, tr)
                #disconnect top left and bottom left corner
                join_v(tl,bl)
                join_v(tr,br)
                disjoin_v(bl,br)
            elif (i == (rows_vertices-2) ):
                join_v(bl,br)
                join_v(bl,tl)
                join_v(br,tr)
                disjoin_v(tl,tr)
            else:
                join_v(tl,bl)
                join_v(tr,br)
                disjoin_v(tl,tr)
                disjoin_v(bl,br)
        elif (i%2!=0) and (j%2==0): #vertical gutter
            if (j == 0):
                join_v(tl,bl)
                join_v(tl,tr)
                join_v(bl,br)
                disjoin_v(tr,br)
            elif (j == (columns_vertices-2) ):
                join_v(tr,br)
                disjoin_v(tl,bl)
                join_v(tl,tr)
                join_v(bl,br)
            else:
                join_v(tl,tr)
                join_v(bl,br)
                disjoin_v(tl,bl)
                disjoin_v(tr,br)
        elif (i%2==0) and (j%2==0): #square gutter
            if (i == 0) and  (j == 0):
                join_v(tl,tr)
                join_v(tl,bl)
                disjoin_v(bl,br)
                disjoin_v(tr,br)
            elif (i == 0) and (j == (columns_vertices-2) ):
                join_v(tl,tr)
                join_v(tr,br)
                disjoin_v(tl,bl)
                disjoin_v(bl,br)
            elif (i == (rows_vertices-2) ) and (j == 0):
                join_v(tl,bl)
                join_v(bl,br)
                disjoin_v(tl,tr)
                disjoin_v(tr,br)
            elif (i == (rows_vertices-2) ) and (j == (columns_vertices-2) ):
                join_v(tr,br)
                join_v(bl,br)
                disjoin_v(tl,tr)
                disjoin_v(tl,bl)
            elif (i == 0):
                join_v(tl,tr)
                disjoin_v(tl,bl)
                disjoin_v(tr,br)
                disjoin_v(bl,br)
            elif (j == 0):
                disjoin_v(tl,tr)
                join_v(tl,bl)
                disjoin_v(tr,br)
                disjoin_v(bl,br)
            elif (i == (rows_vertices-2) ):
                join_v(bl,br)
                disjoin_v(tr,tl)
                disjoin_v(tr,br)
                disjoin_v(tl,bl)
            elif (j == (columns_vertices-2) ):
                join_v(tr,br)
                disjoin_v(tl,tr)
                disjoin_v(bl,br)
                disjoin_v(tl,bl)
            else:
                disjoin_v(tl,tr)
                disjoin_v(bl,br)
                disjoin_v(tl,bl)
                disjoin_v(tr,br)
        self.planes[i][j] = False
    
    def hide_planes(self,i,j):
        planes = self.planes
        columns_vertices = self.columns_vertices
        rows_vertices = self.rows_vertices
        if (i%2==0) and (j%2==0):
            if (i == 0) and (j == 0):
                if planes[i+1][j] == True:
                    self.hide_plane(i+1,j)
                if planes[i][j+1] == True:
                    self.hide_plane(i,j+1)
            elif (i == 0) and (j == (columns_vertices-2) ):
                if planes[i+1][j] == True:
                    self.hide_plane(i+1,j)
                if planes[i][j-1] == True:
                    self.hide_plane(i,j-1)
            elif (i == (rows_vertices-2) ) and (j == 0):
                if planes[i-1][j] == True:
                    self.hide_plane(i-1,j)
                if planes[i][j+1] == True:
                    self.hide_plane(i,j+1)
            elif (i == (rows_vertices-2) ) and (j == (columns_vertices-2) ):
                if planes[i-1][j] == True:
                    self.hide_plane(i-1,j)
                if planes[i][j-1] == True:
                    self.hide_plane(i,j-1)
            elif (i == 0):
                if planes[i+1][j] == True:
                    self.hide_plane(i+1,j)
                if planes[i][j+1] == True:
                    self.hide_plane(i,j+1)
                if planes[i][j-1] == True:
                    self.hide_plane(i,j-1)
            elif (i == (rows_vertices-2) ):
                if planes[i-1][j] == True:
                    self.hide_plane(i-1,j)
                if planes[i][j+1] == True:
                    self.hide_plane(i,j+1)
                if planes[i][j-1] == True:
                    self.hide_plane(i,j-1)
            elif (j == 0):
                if planes[i+1][j] == True:
                    self.hide_plane(i+1,j)
                if planes[i-1][j] == True:
                    self.hide_plane(i-1,j)
                if planes[i][j+1] == True:
                    self.hide_plane(i,j+1)
            elif (j == (columns_vertices-2) ):
                if planes[i+1][j] == True:
                    self.hide_plane(i+1,j)
                if planes[i-1][j] == True:
                    self.hide_plane(i-1,j)
                if planes[i][j-1] == True:
                    self.hide_plane(i,j-1)
            else:
                if planes[i+1][j] == True:
                    self.hide_plane(i+1,j)
                if planes[i][j+1] == True:
                    self.hide_plane(i,j+1)
                if planes[i-1][j] == True:
                    self.hide_plane(i-1,j)
                if planes[i][j-1] == True:
                    self.hide_plane(i,j-1)
            self.hide_plane(i,j)
        elif (i%2==0) and (j%2!=0):
            self.hide_plane(i,j)
        elif (i%2!=0) and (j%2==0):
            self.hide_plane(i,j)
    

    def unhide_plane(self, i, j):
        def to_v(vi, vj):
            return (vi*self.columns_vertices+vj)
        def join_v(vn,vm):
            self.vertices[vn][vm] = True
            self.vertices[vm][vn] = True
        def disjoin_v(vn,vm):
            self.vertices[vn][vm] = False
            self.vertices[vm][vn] = False
        tl = to_v(i,j) #top left corner
        tr = to_v(i,j+1) #top right corner
        bl = to_v(i+1,j) #bottom left corner
        br = to_v(i+1,j+1) #bottom right corner
        rows_vertices = self.rows_vertices
        columns_vertices = self.columns_vertices
        if (i%2==0) and (j%2!=0): #horizontal gutter
            if (i == 0):
                #join top left corner and top right corner
                disjoin_v(tl, tr)
                #disconnect top left and bottom left corner
                disjoin_v(tl,bl)
                disjoin_v(tr,br)
                join_v(bl,br)
            elif (i == (rows_vertices-2) ):
                disjoin_v(bl,br)
                disjoin_v(bl,tl)
                disjoin_v(br,tr)
                join_v(tl,tr)
            else:
                disjoin_v(tl,bl)
                disjoin_v(tr,br)
                join_v(tl,tr)
                join_v(bl,br)
        elif (i%2!=0) and (j%2==0): #vertical gutter
            if (j == 0):
                disjoin_v(tl,bl)
                disjoin_v(tl,tr)
                disjoin_v(bl,br)
                join_v(tr,br)
            elif (j == (columns_vertices-2) ):
                disjoin_v(tr,br)
                join_v(tl,bl)
                disjoin_v(tl,tr)
                disjoin_v(bl,br)
            else:
                disjoin_v(tl,tr)
                disjoin_v(bl,br)
                join_v(tl,bl)
                join_v(tr,br)
        elif (i%2==0) and (j%2==0): #square gutter
            if (i == 0) and  (j == 0):
                disjoin_v(tl,tr)
                disjoin_v(tl,bl)
                join_v(bl,br)
                join_v(tr,br)
            elif (i == 0) and (j == (columns_vertices-2) ):
                disjoin_v(tl,tr)
                disjoin_v(tr,br)
                join_v(tl,bl)
                join_v(bl,br)
            elif (i == (rows_vertices-2) ) and (j == 0):
                disjoin_v(tl,bl)
                disjoin_v(bl,br)
                join_v(tl,tr)
                join_v(tr,br)
            elif (i == (rows_vertices-2) ) and (j == (columns_vertices-2) ):
                disjoin_v(tr,br)
                disjoin_v(bl,br)
                join_v(tl,tr)
                join_v(tl,bl)
            elif (i == 0):
                disjoin_v(tl,tr)
                join_v(tl,bl)
                join_v(tr,br)
                join_v(bl,br)
            elif (j == 0):
                join_v(tl,tr)
                disjoin_v(tl,bl)
                join_v(tr,br)
                join_v(bl,br)
            elif (i == (rows_vertices-2) ):
                disjoin_v(bl,br)
                join_v(tr,tl)
                join_v(tr,br)
                join_v(tl,bl)
            elif (j == (columns_vertices-2) ):
                disjoin_v(tr,br)
                join_v(tl,tr)
                join_v(bl,br)
                join_v(tl,bl)
            else:
                join_v(tl,tr)
                join_v(bl,br)
                join_v(tl,bl)
                join_v(tr,br)
        self.planes[i][j] = True
    
    def unhide_planes(self,i,j):
        planes = self.planes
        columns_vertices = self.columns_vertices
        rows_vertices = self.rows_vertices
        if (i%2==0) and (j%2==0):
            self.unhide_plane(i,j)
            if (i == 0) and (j == 0):
                if planes[i+1][j] == False:
                    self.unhide_plane(i+1,j)
                if planes[i][j+1] == False:
                    self.unhide_plane(i,j+1)
            elif (i == 0) and (j == (columns_vertices-2) ):
                if planes[i+1][j] == False:
                    self.unhide_plane(i+1,j)
                if planes[i][j-1] == False:
                    self.unhide_plane(i,j-1)
            elif (i == (rows_vertices-2) ) and (j == 0):
                if planes[i-1][j] == False:
                    self.unhide_plane(i-1,j)
                if planes[i][j+1] == False:
                    self.unhide_plane(i,j+1)
            elif (i == (rows_vertices-2) ) and (j == (columns_vertices-2) ):
                if planes[i-1][j] == False:
                    self.unhide_plane(i-1,j)
                if planes[i][j-1] == False:
                    self.unhide_plane(i,j-1)
            elif (i == 0):
                if planes[i+1][j] == False:
                    self.unhide_plane(i+1,j)
                if planes[i][j+1] == False:
                    self.unhide_plane(i,j+1)
                if planes[i][j-1] == False:
                    self.unhide_plane(i,j-1)
            elif (i == (rows_vertices-2) ):
                if planes[i-1][j] == False:
                    self.unhide_plane(i-1,j)
                if planes[i][j+1] == False:
                    self.unhide_plane(i,j+1)
                if planes[i][j-1] == False:
                    self.unhide_plane(i,j-1)
            elif (j == 0):
                if planes[i+1][j] == False:
                    self.unhide_plane(i+1,j)
                if planes[i-1][j] == False:
                    self.unhide_plane(i-1,j)
                if planes[i][j+1] == False:
                    self.unhide_plane(i,j+1)
            elif (j == (columns_vertices-2) ):
                if planes[i+1][j] == False:
                    self.unhide_plane(i+1,j)
                if planes[i-1][j] == False:
                    self.unhide_plane(i-1,j)
                if planes[i][j-1] == False:
                    self.unhide_plane(i,j-1)
            else:
                if planes[i+1][j] == False:
                    self.unhide_plane(i+1,j)
                if planes[i][j+1] == False:
                    self.unhide_plane(i,j+1)
                if planes[i-1][j] == False:
                    self.unhide_plane(i-1,j)
                if planes[i][j-1] == False:
                    self.unhide_plane(i,j-1)
        elif (i%2==0) and (j%2!=0):
            if planes[i][j-1] == False:
                
                self.unhide_plane(i,j-1)
            if planes[i][j+1] == False:
                self.unhide_plane(i,j+1)
            self.unhide_plane(i,j)
        elif (i%2!=0) and (j%2==0):
            if planes[i+1][j] == False:
                self.unhide_plane(i+1,j)
            if planes[i-1][j] == False:
                self.unhide_plane(i-1,j)
            self.unhide_plane(i,j)
    
    def upd_svg_ren(self):
        self.svg_renderer.load(bytearray(self.get_svg_string(), encoding='utf-8'))
        

#this class allows us to click on the gutter to make it dissapear
class callGutter(QGraphicsRectItem):
    
    
    def setRCPGObject(self,gutter, i, j):
        self.gutter = gutter
        self.i = i
        self.j = j
        self.sel = True

    def mousePressEvent(self, event):
        if self.gutter.planes[self.i][self.j] == True:
            self.gutter.hide_planes(self.i,self.j)
            self.gutter.upd_svg_ren()
            self.sel = False
        else:
            self.gutter.unhide_planes(self.i,self.j)
            self.gutter.upd_svg_ren()
            self.sel = True

        return QGraphicsRectItem.mousePressEvent(self, event)

#this is where we will show preview of the page
class RCPGPreview(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setAlignment(Qt.AlignLeft or Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    
    def get_svg_id(self, num):
        self.num = num
    
    def mouseReleaseEvent(self, event):
        
        scene = self.scene()
        scene.items()[self.num].update()
        r = scene.sceneRect()
        self.updateView()
        self.updateSceneRect(r)
        return QGraphicsView.mouseReleaseEvent(self, event)
    
    def updateView(self):
        scene = self.scene()
        r = scene.sceneRect()
        r1 = self.rect()
        minheight = r.height() * r1.width() / r.width()
        self.fitInView(r, Qt.KeepAspectRatioByExpanding)
        self.setMinimumHeight(minheight)
    
    def resizeEvent(self, event):
        self.updateView()

    def showEvent(self, event):
        if not event.spontaneous():
            self.updateView()
    
#this is the plugin. here will be initiated ui
class RCPGWindow(DockWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rogudator's comic panel generator")
        

        self.vertical_updated = True
        self.horizontal_updated = True


        mainLayout = QVBoxLayout()
        
        l_preview = QLabel(self)
        l_preview.setText("Preview:")
        mainLayout.addWidget(l_preview)

        self.page_svg = RCPG()
        self.page_svg.upd_svg_ren()
        
        renderer = self.page_svg.svg_renderer
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(renderer)

        self.i_preview = RCPGPreview()
        self.i_preview.scene().addItem(self.svg_item)
        mainLayout.addWidget(self.i_preview)

        self.getClickableGutters()

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
        self.sp_num_rows.setValue(3)
        self.sp_num_rows.setMinimum(1)

        self.sl_num_rows = QSlider(self)
        self.sl_num_rows.setMinimum(1)
        self.sl_num_rows.setMaximum(6)
        self.sl_num_rows.setOrientation(Qt.Horizontal)
        self.sl_num_rows.setTickPosition(2)
        self.sl_num_rows.setTickInterval(1)
        self.sl_num_rows.setMinimumWidth(100)
        self.sl_num_rows.setValue(3)

        num_rows = QHBoxLayout(self)
        num_rows.addWidget(self.sp_num_rows)
        num_rows.addWidget(self.sl_num_rows)
        mainLayout.addLayout(num_rows)

        l_num_columns = QLabel(self)
        l_num_columns.setText("Number of columns:")
        mainLayout.addWidget(l_num_columns)

        self.sp_num_columns = QSpinBox(self)
        self.sp_num_columns.setValue(3)
        self.sp_num_columns.setMinimum(1)

        self.sl_num_columns = QSlider(self)
        self.sl_num_columns.setMinimum(1)
        self.sl_num_columns.setMaximum(6)
        self.sl_num_columns.setOrientation(Qt.Horizontal)
        self.sl_num_columns.setTickPosition(2)
        self.sl_num_columns.setTickInterval(1)
        self.sl_num_columns.setMinimumWidth(100)
        self.sl_num_columns.setValue(3)

        num_columns = QHBoxLayout(self)
        num_columns.addWidget(self.sp_num_columns)
        num_columns.addWidget(self.sl_num_columns)
        mainLayout.addLayout(num_columns)

        l_gutter = QLabel(self)
        l_gutter.setText("Gutters")
        mainLayout.addWidget(l_gutter)

        self.cb_gutter_equal = QCheckBox(self)
        self.cb_gutter_equal.setText("Vetrical and Horizontal are equal")
        self.cb_gutter_equal.setChecked(True)
        mainLayout.addWidget(self.cb_gutter_equal)

        l_vgutter = QLabel(self)
        l_vgutter.setText("Size of a vertical gutter:")
        mainLayout.addWidget(l_vgutter)

        self.vgutter_max = int(self.page_svg.width_page / (self.page_svg.columns + 1))

        self.sp_vgutter = QSpinBox(self)
        self.sp_vgutter.setValue(30)
        self.sp_vgutter.setMinimum(1)
        self.sp_vgutter.setMaximum(self.vgutter_max)

        self.sl_vgutter = QSlider(self)
        self.sl_vgutter.setMinimum(1)
        self.sl_vgutter.setMaximum(self.vgutter_max)
        self.sl_vgutter.setOrientation(Qt.Horizontal)
        self.sl_vgutter.setTickInterval(1)
        self.sl_vgutter.setMinimumWidth(100)
        self.sl_vgutter.setValue(30)

        vgutter = QHBoxLayout(self)
        vgutter.addWidget(self.sp_vgutter)
        vgutter.addWidget(self.sl_vgutter)
        mainLayout.addLayout(vgutter)

        l_hgutter = QLabel(self)
        l_hgutter.setText("Size of a horizontal gutter:")
        mainLayout.addWidget(l_hgutter)

        self.hgutter_max = int(self.page_svg.height_page / (self.page_svg.rows + 1))

        self.sp_hgutter = QSpinBox(self)
        self.sp_hgutter.setValue(30)
        self.sp_hgutter.setMinimum(1)
        self.sp_hgutter.setMaximum(self.hgutter_max)

        self.sl_hgutter = QSlider(self)
        self.sl_hgutter.setMinimum(1)
        self.sl_hgutter.setMaximum(self.hgutter_max)
        self.sl_hgutter.setOrientation(Qt.Horizontal)
        self.sl_hgutter.setTickInterval(1)
        self.sl_hgutter.setMinimumWidth(100)
        self.sl_hgutter.setValue(30)

        hgutter = QHBoxLayout(self)
        hgutter.addWidget(self.sp_hgutter)
        hgutter.addWidget(self.sl_hgutter)
        mainLayout.addLayout(hgutter)

        l_cgutter = QLabel(self)
        l_cgutter.setText("Color of gutter:")
        mainLayout.addWidget(l_cgutter)

        self.l_color_of_gutter = QLabel(self)
        self.l_color_of_gutter.setText("#000000")

        p_color_of_gutter = QPushButton(self)
        p_color_of_gutter.setText("Change")

        color_of_gutter = QHBoxLayout(self)
        color_of_gutter.addWidget(self.l_color_of_gutter)
        color_of_gutter.addWidget(p_color_of_gutter)
        mainLayout.addLayout(color_of_gutter)

        l_outline = QLabel(self)
        l_outline.setText("Size of panel outline:")
        mainLayout.addWidget(l_outline)

        self.sp_outline = QSpinBox(self)
        self.sp_outline.setValue(10)
        self.sp_outline.setMinimum(0)

        self.sl_outline = QSlider(self)
        self.sl_outline.setMinimum(0)
        self.sl_outline.setMaximum(98)
        self.sl_outline.setOrientation(Qt.Horizontal)
        self.sl_outline.setTickInterval(1)
        self.sl_outline.setMinimumWidth(100)
        self.sl_outline.setValue(10)

        outline = QHBoxLayout(self)
        outline.addWidget(self.sp_outline)
        outline.addWidget(self.sl_outline)
        mainLayout.addLayout(outline)

        l_coutline = QLabel(self)
        l_coutline.setText("Color of panel outline:")
        mainLayout.addWidget(l_coutline)

        self.l_color_of_outline = QLabel(self)
        self.l_color_of_outline.setText("#ffffff")

        p_color_of_outline = QPushButton(self)
        p_color_of_outline.setText("Change")

        color_of_outline = QHBoxLayout(self)
        color_of_outline.addWidget(self.l_color_of_outline)
        color_of_outline.addWidget(p_color_of_outline)
        mainLayout.addLayout(color_of_outline)
        
        self.scrollMainLayout = QScrollArea(self)
        self.scrollMainLayout.setWidgetResizable(True)

        b_layer.clicked.connect(self.b_layer_create)
        b_file.clicked.connect(self.b_file_create)
        self.sp_num_rows.valueChanged.connect(self.sp_num_rows_upd)
        self.sl_num_rows.valueChanged.connect(self.sl_num_rows_upd)
        self.sp_num_columns.valueChanged.connect(self.sp_num_columns_upd)
        self.sl_num_columns.valueChanged.connect(self.sl_num_columns_upd)
        self.sp_vgutter.valueChanged.connect(self.sp_vgutter_upd)
        self.sl_vgutter.valueChanged.connect(self.sl_vgutter_upd)
        self.sp_hgutter.valueChanged.connect(self.sp_hgutter_upd)
        self.sl_hgutter.valueChanged.connect(self.sl_hgutter_upd)
        self.sp_outline.valueChanged.connect(self.sp_outline_upd)
        self.sl_outline.valueChanged.connect(self.sl_outline_upd)
        p_color_of_gutter.clicked.connect(self.colorGutterDialog)
        p_color_of_outline.clicked.connect(self.colorOutlineDialog)
        

        self.window = QWidget(self)
        self.window.setLayout(mainLayout)
        self.scrollMainLayout.setWidget(self.window)
        self.setWidget(self.scrollMainLayout)
        self.show()

    def colorOutlineDialog(self):
        color = QColorDialog.getColor(QColor(self.l_color_of_outline.text()))
        self.l_color_of_outline.setText(color.name())
        self.page_svg.outline_color = self.l_color_of_outline.text()
        self.page_svg.upd_svg_ren()
        self.svg_item.update()
        self.update()
    
    def colorGutterDialog(self):
        color = QColorDialog.getColor(QColor(self.l_color_of_gutter.text()))
        self.l_color_of_gutter.setText(color.name())
        self.page_svg.color_gutter = self.l_color_of_gutter.text()
        self.page_svg.upd_svg_ren()
        self.svg_item.update()
        self.update()
    
    def getClickableGutters(self):
        for i in range(self.page_svg.rows_vertices-1):
            for j in range(self.page_svg.columns_vertices-1):
                gr_item = callGutter(self.page_svg.vertex_coordinate_x[j], self.page_svg.vertex_coordinate_y[i], (self.page_svg.vertex_coordinate_x[j+1]-self.page_svg.vertex_coordinate_x[j]), (self.page_svg.vertex_coordinate_y[i+1]-self.page_svg.vertex_coordinate_y[i]))
                gr_item.setAcceptHoverEvents(True)
                gr_item.setRCPGObject(self.page_svg,i,j)
                gr_item.setFlag(QGraphicsItem.ItemIsSelectable)
                self.i_preview.scene().addItem(gr_item)
        self.i_preview.get_svg_id((self.page_svg.rows_vertices-1)*(self.page_svg.columns_vertices-1))

    def cleanClickableGutter(self):
        for i in range((self.page_svg.rows_vertices-1)*(self.page_svg.columns_vertices-1)):
            self.i_preview.scene().removeItem(self.i_preview.scene().items()[i])
    
    def sp_num_rows_upd(self):
        self.i_preview.scene().clear()
        rows = self.sp_num_rows.value()
        if rows>0 and rows<7:
            self.sl_num_rows.setValue(rows)
        
        self.hgutter_max = int(self.page_svg.height_page / (rows + 1))
        self.sp_hgutter.setMaximum(self.hgutter_max)
        self.sl_hgutter.setMaximum(self.hgutter_max)

        self.page_svg.rows = rows
        self.page_svg.upd_panel_sizes()
        self.page_svg.upd_vertices_amount()
        self.page_svg.upd_vertices()
        self.page_svg.update_vertex_coordinate()
        self.page_svg.standard_grid()
        self.page_svg.upd_panels()
        self.page_svg.upd_svg_ren()
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.page_svg.svg_renderer)
        self.i_preview.scene().addItem(self.svg_item)
        self.getClickableGutters()
        self.svg_item.update()

    def sl_num_rows_upd(self):
        rows = self.sl_num_rows.value()
        self.sp_num_rows.setValue(rows)

    def sp_num_columns_upd(self):
        self.i_preview.scene().clear()
        columns = self.sp_num_columns.value()
        if columns>0 and columns<7:
            self.sl_num_columns.setValue(columns)

        self.vgutter_max = int(self.page_svg.width_page / (columns + 1))
        self.sp_vgutter.setMaximum(self.vgutter_max)
        self.sl_vgutter.setMaximum(self.vgutter_max)
        
        self.page_svg.columns = columns
        
        self.page_svg.upd_panel_sizes()
        self.page_svg.upd_vertices_amount()
        self.page_svg.upd_vertices()
        self.page_svg.update_vertex_coordinate()
        self.page_svg.standard_grid()
        self.page_svg.upd_panels()
        self.page_svg.upd_svg_ren()
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.page_svg.svg_renderer)
        self.i_preview.scene().addItem(self.svg_item)
        self.getClickableGutters()
        self.svg_item.update()

    def sl_num_columns_upd(self):
        columns = self.sl_num_columns.value()
        self.sp_num_columns.setValue(columns)
    
    def sp_vgutter_upd(self):
        
        vertical_gutter = self.sp_vgutter.value()
        if vertical_gutter>0 and vertical_gutter<(self.vgutter_max):
            self.sl_vgutter.setValue(vertical_gutter)
        self.page_svg.horizontal_gutter = vertical_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
        
        if (self.cb_gutter_equal.isChecked() == True):
            self.horizontal_updated = False
            self.sp_hgutter.setValue(vertical_gutter)
            if vertical_gutter>0 and vertical_gutter<(self.hgutter_max):
                self.sl_hgutter.setValue(vertical_gutter)
            self.page_svg.vertical_gutter = vertical_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
        if (self.vertical_updated == True):
            self.i_preview.scene().clear()
            self.page_svg.upd_panel_sizes()
            self.page_svg.upd_vertices_amount()
            self.page_svg.upd_vertices()
            self.page_svg.update_vertex_coordinate()
            self.page_svg.standard_grid()
            self.page_svg.upd_panels()
            self.page_svg.upd_svg_ren()
            self.svg_item = QGraphicsSvgItem()
            self.svg_item.setSharedRenderer(self.page_svg.svg_renderer)
            self.i_preview.scene().addItem(self.svg_item)
            self.getClickableGutters()
            self.svg_item.update()
        else:
            self.vertical_updated = True
    
    def sl_vgutter_upd(self):
        #self.i_preview.scene().clear()
        vertical_gutter = self.sl_vgutter.value()
        self.sp_vgutter.setValue(vertical_gutter)
        self.page_svg.horizontal_gutter = vertical_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
        
        if (self.cb_gutter_equal.isChecked() == True):
            self.sp_hgutter.setValue(vertical_gutter)
            if vertical_gutter>0 and vertical_gutter<(self.hgutter_max):
                self.sl_hgutter.setValue(vertical_gutter)
            self.page_svg.vertical_gutter = vertical_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
    
    def sp_hgutter_upd(self):
        
        horizontal_gutter = self.sp_hgutter.value()
        if horizontal_gutter>0 and horizontal_gutter<(self.hgutter_max):
            self.sl_hgutter.setValue(horizontal_gutter)
        self.page_svg.vertical_gutter = horizontal_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
        
        if (self.cb_gutter_equal.isChecked() == True):
            self.horizontal_updated = False
            self.sp_vgutter.setValue(horizontal_gutter)
            if horizontal_gutter>0 and horizontal_gutter<(self.vgutter_max):
                self.sl_vgutter.setValue(horizontal_gutter)
            self.page_svg.horizontal_gutter = horizontal_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
        if (self.horizontal_updated == True):
            self.i_preview.scene().clear()
            self.page_svg.upd_panel_sizes()
            self.page_svg.upd_vertices_amount()
            self.page_svg.upd_vertices()
            self.page_svg.update_vertex_coordinate()
            self.page_svg.standard_grid()
            self.page_svg.upd_panels()
            self.page_svg.upd_svg_ren()
            self.svg_item = QGraphicsSvgItem()
            self.svg_item.setSharedRenderer(self.page_svg.svg_renderer)
            self.i_preview.scene().addItem(self.svg_item)
            self.getClickableGutters()
            self.svg_item.update()
        else:
            self.horizontal_updated = True

    def sl_hgutter_upd(self):
        # self.i_preview.scene().clear()
        horizontal_gutter = self.sl_hgutter.value()
        self.sp_hgutter.setValue(horizontal_gutter)
        self.page_svg.vertical_gutter = horizontal_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
        
        if (self.cb_gutter_equal.isChecked() == True):
            self.sp_vgutter.setValue(horizontal_gutter)
            if horizontal_gutter>0 and horizontal_gutter<(self.vgutter_max):
                self.sl_vgutter.setValue(horizontal_gutter)
            self.page_svg.horizontal_gutter = horizontal_gutter #i messed up vertical and horizontal gutter in the class, aaaa :(
    
    def sp_outline_upd(self):
        self.i_preview.scene().clear()
        outline_size = self.sp_outline.value()
        self.sl_outline.setValue(outline_size)
        self.page_svg.outline_size = outline_size
        
        self.page_svg.upd_panel_sizes()
        self.page_svg.upd_vertices_amount()
        self.page_svg.upd_vertices()
        self.page_svg.update_vertex_coordinate()
        self.page_svg.standard_grid()
        self.page_svg.upd_panels()
        self.page_svg.upd_svg_ren()
        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(self.page_svg.svg_renderer)
        self.i_preview.scene().addItem(self.svg_item)
        self.getClickableGutters()
        self.svg_item.update()

    def sl_outline_upd(self):
        outline_size = self.sl_outline.value()
        self.sp_outline.setValue(outline_size)
    
    def b_layer_create(self):
        temp_dir = tempfile.gettempdir() + "/rcpg.svg"
        body = self.page_svg.get_svg_string()
        with open(temp_dir, 'w', encoding='utf-8') as f:
            f.write(body)
        print(temp_dir)
        app = Krita.instance()
        doc = app.activeDocument()
        if doc != None:
            app = Krita.instance()
            doc = app.activeDocument()
            temp_dir = tempfile.gettempdir() + "/rcpg.svg"
            body = self.page_svg.get_svg_string()
            with open(temp_dir, 'w', encoding='utf-8') as f:
                f.write(body)
            app = Krita.instance()
            doc = app.activeDocument()
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

    def b_file_create(self):
        app = Krita.instance()
        doc = app.activeDocument()
        if doc == None:
            temp_dir = tempfile.gettempdir() + "/rcpg.svg"
            body = self.page_svg.get_svg_string()
            with open(temp_dir, 'w', encoding='utf-8') as f:
                f.write(body)
            doc = Krita.instance().openDocument(temp_dir)
            Krita.instance().activeWindow().addView(doc)
            doc.refreshProjection()
        else:
            app = Krita.instance()
            doc = app.activeDocument()
            temp_dir = tempfile.gettempdir() + "/rcpg.svg"
            body = self.page_svg.get_svg_string()
            with open(temp_dir, 'w', encoding='utf-8') as f:
                f.write(body)
            doc = Krita.instance().openDocument(temp_dir)
            Krita.instance().activeWindow().addView(doc)
            doc.refreshProjection()

    def canvasChanged(self, canvas):
        app = Krita.instance()
        doc = app.activeDocument()
        if doc == None:
            pass
        else:
            app = Krita.instance()
            doc = app.activeDocument()
            self.i_preview.scene().clear()
            self.page_svg.height_page= doc.height()
            self.page_svg.width_page = doc.width()
            self.page_svg.upd_panel_sizes()
            self.page_svg.upd_vertices_amount()
            self.page_svg.upd_vertices()
            self.page_svg.update_vertex_coordinate()
            self.page_svg.standard_grid()
            self.page_svg.upd_panels()
            self.page_svg.upd_svg_ren()
            self.svg_item = QGraphicsSvgItem()
            self.svg_item.setSharedRenderer(self.page_svg.svg_renderer)
            self.i_preview.scene().addItem(self.svg_item)
            self.getClickableGutters()
            self.svg_item.update()
            iii = self.i_preview.scene().sceneRect()
            iii.setHeight(doc.height())
            self.i_preview.scene().setSceneRect(iii)
            self.i_preview.updateView()
            
