from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QSpinBox, QMainWindow, QWidget
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QRect
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from krita import *

class RCPG_Docker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rogudator's comic panel generator")
        self.width_document = 800
        self.height_document = 1280

        #setting up the ui
        mainWidget = QWidget(self)
        self.setWidget(mainWidget)
        mainLayout = QVBoxLayout()

        self.label0 = QLabel(self)
        self.label0.setText("Preview:")
        mainLayout.addWidget(self.label0)

        self.preview = QSvgWidget(self)
        self.preview.setMinimumHeight(300)
        mainLayout.addWidget(self.preview)

        self.generateButton = QPushButton(self)
        self.generateButton.setText("Generate")
        mainLayout.addWidget(self.generateButton)

        self.label1 = QLabel(self)
        self.label1.setText("Number of rows:")
        mainLayout.addWidget(self.label1)

        spinboxAndSlider0 = QHBoxLayout()
        self.spinbox0 = QSpinBox(self)
        self.spinbox0.setValue(1)
        spinboxAndSlider0.addWidget(self.spinbox0)
        self.slider0 = QSlider()
        self.slider0.setOrientation(Qt.Horizontal)
        self.slider0.setTickPosition(QSlider.TicksBelow)
        self.slider0.setTickInterval(1)
        self.slider0.setMinimum(1)
        self.slider0.setMaximum(5)
        spinboxAndSlider0.addWidget(self.slider0)
        mainLayout.addLayout(spinboxAndSlider0)

        self.label2 = QLabel(self)
        self.label2.setText("Number of columns:")
        mainLayout.addWidget(self.label2)

        spinboxAndSlider1 = QHBoxLayout()
        self.spinbox1 = QSpinBox(self)
        self.spinbox1.setValue(1)
        spinboxAndSlider1.addWidget(self.spinbox1)
        self.slider1 = QSlider()
        self.slider1.setOrientation(Qt.Horizontal)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider1.setTickInterval(1)
        self.slider1.setMinimum(1)
        self.slider1.setMaximum(5)
        spinboxAndSlider1.addWidget(self.slider1)
        mainLayout.addLayout(spinboxAndSlider1)

        self.label3 = QLabel(self)
        self.label3.setText("Size of the gutter:")
        mainLayout.addWidget(self.label3)

        spinboxAndSlider2 = QHBoxLayout()
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setValue(30)
        self.spinbox2.setMaximum(500)
        spinboxAndSlider2.addWidget(self.spinbox2)
        self.slider2 = QSlider()
        self.slider2.setOrientation(Qt.Horizontal)
        self.slider2.setTickInterval(1)
        self.slider2.setMinimum(1)
        self.slider2.setMaximum(500)
        spinboxAndSlider2.addWidget(self.slider2)
        mainLayout.addLayout(spinboxAndSlider2)

        self.label4 = QLabel(self)
        self.label4.setText("Panel line thickness:")
        mainLayout.addWidget(self.label4)

        spinboxAndSlider3 = QHBoxLayout()
        self.spinbox3 = QSpinBox(self)
        self.spinbox3.setValue(10)
        spinboxAndSlider3.addWidget(self.spinbox3)
        self.slider3 = QSlider()
        self.slider3.setOrientation(Qt.Horizontal)
        self.slider3.setTickInterval(1)
        self.slider3.setMinimum(1)
        self.slider3.setMaximum(30)
        spinboxAndSlider3.addWidget(self.slider3)
        mainLayout.addLayout(spinboxAndSlider3)

        #connecting signals and slots (buttons and what they supposed to do)
        self.generateButton.clicked.connect(self.generateSvg)
        self.slider0.valueChanged.connect(self.slider0Change)
        self.slider1.valueChanged.connect(self.slider1Change)
        self.slider2.valueChanged.connect(self.slider2Change)
        self.slider3.valueChanged.connect(self.slider3Change)
        self.spinbox0.valueChanged.connect(self.spinbox0Change)
        self.spinbox1.valueChanged.connect(self.spinbox1Change)
        self.spinbox2.valueChanged.connect(self.spinbox2Change)
        self.spinbox3.valueChanged.connect(self.spinbox3Change)
        self.updatePreview()

        mainWidget.setLayout(mainLayout)
        #This is the important part below. Function below creates the contents of vector file that will be comic page.
    def previewPage(self):

        #if no document is open choose the default width and height
        app = Krita.instance() # get the application
        documentsOpen = app.documents() # get the open documents
        documentCount = len( app.documents() ) # get how many documents opened
        if documentCount == 0: 
            width_document = self.width_document
            height_document = self.height_document
        else:
            width_document = app.activeDocument().width()
            height_document = app.activeDocument().height()
        rows = self.spinbox0.value()
        columns = self.spinbox1.value()
        gutter = self.spinbox2.value()
        line_thickness = self.spinbox3.value()
        width_panel = int((width_document-((columns+1)*gutter)) / columns)
        height_panel = int((height_document-((rows+1)*gutter)) / rows)
        panel_corners = []
        start_panel_x = 1
        end_panel_x = 0
        start_panel_y = 1
        end_panel_y = 0
        #this loop creates an array of corners of every panel (x,y)
        for i in range(rows*2):
            panel_corners.append([])
            #calculating y coordinate
            y = start_panel_y*gutter+end_panel_y*height_panel
            for j in range(columns*2):
                #calculating x coordinate and creating a string containing x,y type value
                coordinate = str(start_panel_x*gutter+end_panel_x*width_panel) + ',' + str(y)
                panel_corners[i].append(coordinate)
                #counting how many corners have been passed
                if j%2 != 0:
                    start_panel_x += 1
                else:
                    end_panel_x += 1
            if i%2 != 0:
                start_panel_y += 1
            else:
                end_panel_y += 1
            start_panel_x = 1
            end_panel_x = 0

        #Now that we have coordinates of the corners we can write them in a way, that vector layer will understand
        upper_left_corner_y = 0
        upper_left_corner_x = 0
        svg_path = ""
        while upper_left_corner_y < rows*2:
            upper_left_corner_x = 0
            while upper_left_corner_x < columns*2:
                svg_path = svg_path + "M"+panel_corners[upper_left_corner_y][upper_left_corner_x]+" "+panel_corners[upper_left_corner_y][upper_left_corner_x+1]+" "+panel_corners[upper_left_corner_y+1][upper_left_corner_x+1]+" "+panel_corners[upper_left_corner_y+1][upper_left_corner_x]+"Z "
                upper_left_corner_x +=2
            upper_left_corner_y += 2
        
        #Now we need to assemble all the information needed to correctly write svg
        #commented browser_tag is needed if you want to check svg file in browser
        #browser_tag = "<?xml version=\"1.0\" encoding=\"utf-8\" ?><svg baseProfile=\"full\" height=\""+str(height_document)+"px\" version=\"1.1\" width=\""+str(width_document)+"px\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:ev=\"http://www.w3.org/2001/xml-events\" xmlns:xlink=\"http://www.w3.org/1999/xlink\"><defs />"
        browser_tag = "<svg height=\""+str(height_document)+"px\"  width=\""+str(width_document)+"px\"><defs />"
        page_outline = "M-"+str(line_thickness)+",-"+str(line_thickness)+" "+ str(width_document+line_thickness) +",-"+str(line_thickness)+" "+ str(width_document+line_thickness) +","+ str(height_document+line_thickness) +" -"+str(line_thickness)+","+ str(height_document+line_thickness) +"Z "

        body = browser_tag+"<path d=\""+ page_outline + svg_path+"\" fill=\"white\" fill-rule=\"evenodd\" stroke=\"#000\" stroke-width=\""+str(line_thickness)+"\" /></svg>"
        return body
    def updatePreview(self):
        stringPreview = self.previewPage()
        svg_bytes = bytearray(stringPreview, encoding='utf-8')
        self.preview.renderer().load(svg_bytes)
    def generateSvg(self):
        stringPreview = self.previewPage()
        f = open("rcpr_alpha.svg", "w")
        f.write(stringPreview)
        f.close()
        doc = Krita.instance().openDocument("rcpr_alpha.svg")
        Krita.instance().activeWindow().addView(doc)
        #b = n.createFileLayer("Panels","drawing","ImageToPPI")
        doc.refreshProjection()
        

    def slider0Change(self):
        size = self.slider0.value()
        self.spinbox0.setValue(size)
        self.updatePreview()
    def slider1Change(self):
        size = self.slider1.value()
        self.spinbox1.setValue(size)
        self.updatePreview()
    def slider2Change(self):
        size = self.slider2.value()
        self.spinbox2.setValue(size)
        self.updatePreview()
    def slider3Change(self):
        size = self.slider3.value()
        self.spinbox3.setValue(size)
        self.updatePreview()
    
    def spinbox0Change(self):
        size = self.spinbox0.value()
        if size<5 and size>0:
            self.slider0.setValue(size)
        if size<0:
            self.spinbox0.setValue(1)
        self.updatePreview()
    def spinbox1Change(self):
        size = self.spinbox1.value()
        if size<5 and size>0:
            self.slider1.setValue(size)
        if size<0:
            self.spinbox1.setValue(1)
        self.updatePreview()
    def spinbox2Change(self):
        size = self.spinbox2.value()
        if size<500:
            self.slider2.setValue(size)
        if size<0:
            self.spinbox2.setValue(1)
        self.updatePreview()
    def spinbox3Change(self):
        size = self.spinbox3.value()
        if size<30:
            self.slider3.setValue(size)
        if size<0:
            self.spinbox3.setValue(1)
        self.updatePreview()
    def canvasChanged(self, canvas):
        pass


