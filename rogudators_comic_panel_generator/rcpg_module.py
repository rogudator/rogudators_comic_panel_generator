from PyQt5.QtSvg import QSvgRenderer

class RCPG():

    def upd_panel_sizes(self):
        self.width_panel = int((self.width_page - ((self.columns+1) * self.vertical_gutter) - self.extra_space_left - self.extra_space_right) / self.columns)
        self.height_panel = int((self.height_page - ((self.rows+1) * self.horizontal_gutter) - self.extra_space_top - self.extra_space_bottom) / self.rows)

    def upd_vertices(self):
        self.rows_vertices = self.rows*2+2
        self.columns_vertices = self.columns*2+2
        self.vertices_amount = self.rows_vertices * self.columns_vertices
        vertices = []
        for i in range(self.vertices_amount):
            vertices.append([])
            for j in range(self.vertices_amount):
                vertices[i].append(False)
        self.vertices = vertices

    def upd_coordinate_x(self):
        panel_corner_left = 0
        panel_corner_right = 0
        vertex_coordinate_x = []
        for i in range(self.columns_vertices):
            x = (panel_corner_left * self.vertical_gutter) + (panel_corner_right * self.width_panel)
            if i == 0:
                x = x - self.outline
            elif i == (self.columns_vertices-1):
                x = x + self.outline
            elif i == 1:
                x = x + self.extra_space_left
            elif i == (self.columns_vertices - 2):
                x = x - self.extra_space_right
            vertex_coordinate_x.append(x)
            if (i%2) == 0:
                panel_corner_left += 1
            else:
                panel_corner_right += 1
        self.vertex_coordinate_x = vertex_coordinate_x
    
    def upd_coordinate_y(self):
        panel_corner_left = 0
        panel_corner_right = 0
        vertex_coordinate_y = []
        for i in range(self.rows_vertices):
            y = (panel_corner_left * self.horizontal_gutter) + (panel_corner_right * self.height_panel)
            if i == 0:
                y = y - self.outline
            elif i == (self.columns_vertices-1):
                y = y + self.outline
            elif i == 1:
                y = y + self.extra_space_top
            elif i == (self.columns_vertices - 2):
                y = y - self.extra_space_bottom
            vertex_coordinate_y.append(y)
            if (i%2) == 0:
                panel_corner_left += 1
            else:
                panel_corner_right += 1
        self.vertex_coordinate_y = vertex_coordinate_y
    
    def standard_grid(self):
        def to_v(vi, vj):
            return(vi*self.columns_vertices+vj)
        
        def join_v(vn,vm):
            self.vertices[vn][vm] = True
            self.vertices[vm][vn] = True

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
    
    def upd_planes(self):
        planes = []
        for i in range(self.rows_vertices-1):
            planes.append([])
            for j in range(self.columns_vertices-1):
                planes[i].append(True)
        self.planes = planes
            
    def upd_everything(self):
        self.upd_panel_sizes()
        self.upd_vertices()
        self.upd_coordinate_x()
        self.upd_coordinate_y()
        self.upd_planes()

    def __init__(self):
        self.width_page = 800
        self.height_page = 1280
        self.rows = 2
        self.columns = 2
        self.horizontal_gutter = 30
        self.vertical_gutter = 30
        self.gutter_color = "#ffffff"
        self.outline = 6
        self.outline_color = "#000000"
        self.extra_space_top = 0
        self.extra_space_bottom = 0
        self.extra_space_left = 0
        self.extra_space_right = 0

        self.upd_everything()
        self.standard_grid()

        self.svg_renderer = QSvgRenderer()
    
    def get_svg_string(self):
        path = ""
        drawn = []
        vertices = self.vertices

        for i in range(self.vertices_amount):
            for j in range(self.vertices_amount):
                if i in drawn:
                    pass
                elif(vertices[i][j]==True):
                    drawn.append(i)
                    n = int(i/self.columns_vertices)
                    m = int(i - n*self.columns_vertices)
                    path = path + "M" + str(self.vertex_coordinate_x[m]) + "," + str(self.vertex_coordinate_y[n]) + " "
                    v = j
                    lap = 0
                    while(v!=i):
                        for k in range(self.vertices_amount):
                            if k in drawn:
                                pass
                            elif (vertices[v][k] == True):
                                drawn.append(v)
                                n = int(v/self.columns_vertices)
                                m = int(v - n*self.columns_vertices)
                                path = path + str(self.vertex_coordinate_x[m]) + "," + str(self.vertex_coordinate_y[n]) + " "
                                v = k
                                lap = 0
                                if (vertices[v][i] == True):
                                    drawn.append(v)
                                    n = int(v/self.columns_vertices)
                                    m = int(v - n*self.columns_vertices)
                                    path = path + str(self.vertex_coordinate_x[m]) + "," + str(self.vertex_coordinate_y[n]) + "Z "
                                    v = i
                        lap += 1
                        if lap > 3:
                            # n = int(v/self.columns_vertices)
                            # m = int(v - n*self.columns_vertices)
                            # print("Panel's verices not fully connected at "+str(n)+","+str(m))
                            # circle = "<circle cx=\"{}\" cy=\"{}\" r=\"10\" stroke=\"black\" stroke-width=\"3\" fill=\"green\" />"
                            # print(circle.format(self.vertex_coordinate_x[m],self.vertex_coordinate_y[n]))
                            break
        
        svg_file_text = "<?xml version=\"1.0\" encoding=\"utf-8\" ?><svg baseProfile=\"full\" height=\"{}px\" version=\"1.1\" width=\"{}px\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:ev=\"http://www.w3.org/2001/xml-events\" xmlns:xlink=\"http://www.w3.org/1999/xlink\"><defs /><path d=\"{}\" fill=\"{}\" fill-rule=\"evenodd\" stroke=\"{}\" stroke-width=\"{}\" style=\"stroke-linejoin:round;stroke-linecap:round\" /></svg>"

        page_corner_x = str(self.width_page + self.outline)
        page_corner_y = str(self.height_page + self.outline)
        page_beg = str(0 - self.outline)
        page = "M"+ page_beg +","+ page_beg +" "+ page_corner_x +","+ page_beg +" "+ page_corner_x +","+ page_corner_y +" "+ page_beg +","+ page_corner_y +"Z "

        path = page + path

        svg_text = svg_file_text.format(self.height_page, self.width_page, path, self.gutter_color, self.outline_color, self.outline)

        return svg_text
    
    def refresh_svg_renderer(self):
        self.svg_renderer.load(bytearray(self.get_svg_string(), encoding='utf-8'))
    
    def hide_plane(self, pn, pm):
        planes = self.planes
        rows_planes = self.rows_vertices - 2
        columns_planes = self.columns_vertices - 2
        if ((pn%2)==0) and ((pm%2)==0):
            
            if (pn == 0) and (pm == 0):
                planes[pn][pm] = False
                planes[pn][pm+1] = False
                planes[pn+1][pm] = False
            elif (pn == 0) and (pm == columns_planes):
                planes[pn][pm] = False
                planes[pn][pm-1] = False
                planes[pn+1][pm] = False
            elif (pn == rows_planes) and (pm == 0):
                planes[pn][pm] = False
                planes[pn][pm+1] = False
                planes[pn-1][pm] = False
            elif (pn == rows_planes) and (pm == columns_planes):
                planes[pn][pm] = False
                planes[pn][pm-1] = False
                planes[pn-1][pm] = False
            elif (pn == 0):
                planes[pn][pm] = False
                planes[pn][pm-1] = False
                planes[pn][pm+1] = False
                planes[pn+1][pm] = False
            elif(pm == 0):
                planes[pn][pm] = False
                planes[pn-1][pm] = False
                planes[pn+1][pm] = False
                planes[pn][pm+1] = False
            elif (pm == columns_planes):
                planes[pn][pm] = False
                planes[pn-1][pm] = False
                planes[pn+1][pm] = False
                planes[pn][pm-1] = False
            elif (pn == rows_planes):
                planes[pn][pm] = False
                planes[pn][pm-1] = False
                planes[pn][pm+1] = False
                planes[pn-1][pm] = False
            else:
                planes[pn][pm] = False
                planes[pn+1][pm] = False
                planes[pn-1][pm] = False
                planes[pn][pm+1] = False
                planes[pn][pm-1] = False
        elif ((pn%2)==0) and  ((pm%2)!=0):
            planes[pn][pm] = False
            
        elif ((pn%2)!=0) and ((pm%2)==0):
            planes[pn][pm] = False
        self.planes = planes
        
    def unhide_plane(self, pn, pm):
        planes = self.planes
        rows_planes = self.rows_vertices - 2
        columns_planes = self.columns_vertices - 2
        if ((pn%2)==0) and ((pm%2)==0):
            if (pn == 0) and (pm == 0):
                planes[pn][pm] = True
                planes[pn][pm+1] = True
                planes[pn+1][pm] = True
            elif (pn == 0) and (pm == columns_planes):
                planes[pn][pm] = True
                planes[pn][pm-1] = True
                planes[pn+1][pm] = True
            elif (pn == rows_planes) and (pm == 0):
                planes[pn][pm] = True
                planes[pn][pm+1] = True
                planes[pn-1][pm] = True
            elif (pn == rows_planes) and (pm == columns_planes):
                planes[pn][pm] = True
                planes[pn][pm-1] = True
                planes[pn-1][pm] = True
            elif (pn == 0):
                planes[pn][pm] = True
                planes[pn][pm-1] = True
                planes[pn][pm+1] = True
                planes[pn+1][pm] = True
            elif(pm == 0):
                planes[pn][pm] = True
                planes[pn-1][pm] = True
                planes[pn+1][pm] = True
                planes[pn][pm+1] = True
            elif (pm == columns_planes):
                planes[pn][pm] = True
                planes[pn-1][pm] = True
                planes[pn+1][pm] = True
                planes[pn][pm-1] = True
            elif (pn == rows_planes):
                planes[pn][pm] = True
                planes[pn][pm-1] = True
                planes[pn][pm+1] = True
                planes[pn-1][pm] = True
            else:
                planes[pn][pm] = True
                planes[pn+1][pm] = True
                planes[pn-1][pm] = True
                planes[pn][pm+1] = True
                planes[pn][pm-1] = True
        elif ((pn%2)==0) and  ((pm%2)!=0):
            planes[pn][pm] = True
            planes[pn][pm-1] = True
            planes[pn][pm+1] = True
        elif ((pn%2)!=0) and ((pm%2)==0):
            planes[pn][pm] = True
            planes[pn-1][pm] = True
            planes[pn+1][pm] = True
        
        self.planes = planes
    
    def refresh_vertices_connections(self):
        planes = self.planes
        vertices = self.vertices

        rows_planes = self.rows_vertices - 2
        columns_planes = self.columns_vertices - 2

        def to_v(vi, vj):
            return(vi*self.columns_vertices+vj)
        
        def join_v(vn,vm):
            vertices[vn][vm] = True
            vertices[vm][vn] = True
        
        def disjoin_v(vn,vm):
            vertices[vn][vm] = False
            vertices[vm][vn] = False

        for i in range(self.rows_vertices-1):
            for j in range(self.columns_vertices-1):
                #square gutter
                if ((i%2)==0) and ((j%2)==0):
                    #square gutter top left
                    if i==0 and j==0:
                        if planes[i][j] == True:
                            if (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                #should hide this plane?
                                #planes[i][j] = False
                        elif planes[i][j] == False:
                            if (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                #should connect gutters
                                planes[i][j] = True
                            elif (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                    #square gutter top right
                    elif i==0 and j==columns_planes:
                        if planes[i][j]==True:
                            if (planes[i+1][j] == True) and (planes[i][j-1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i+1][j] == True) and (planes[i][j-1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i+1][j] == False) and (planes[i][j-1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i+1][j] == False) and (planes[i][j-1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i+1][j] == True) and (planes[i][j-1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                #should connect vertices
                                planes[i][j] = True
                            elif (planes[i+1][j] == True) and (planes[i][j-1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i+1][j] == False) and (planes[i][j-1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i+1][j] == False) and (planes[i][j-1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #square gutter bottom left
                    elif i==rows_planes and j==0:
                        if planes[i][j]==True:
                            if (planes[i-1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i-1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]==True
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                    #square gutter top right
                    elif i==rows_planes and j==columns_planes:
                        if planes[i][j]==True:
                            if (planes[i-1][j] == True) and (planes[i][j-1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i-1][j] == True) and (planes[i][j-1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]==True
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #square gutter top
                    elif i==0:
                        if planes[i][j]==True:
                            if (planes[i][j-1] == True) and (planes[i+1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == False) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == True) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == False) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == False) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == True) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == False) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j] == False:
                            if (planes[i][j-1] == True) and (planes[i+1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == False) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == True) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == False) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == False) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == True) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == False) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #square gutter left
                    elif j==0:
                        if planes[i][j]==True:
                            if (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j] == False:
                            if (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                    #square gutter right
                    elif j==columns_planes:
                        if planes[i][j]==True:
                            if (planes[i-1][j] == True) and (planes[i][j-1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == True) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == False) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == True) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == False) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j] == False:
                            if (planes[i-1][j] == True) and (planes[i][j-1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == True) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == True) and (planes[i][j-1] == False) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j] == False) and (planes[i][j-1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #square gutter bottom
                    elif i == rows_planes:
                        if planes[i][j]==True:
                            if (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j] = True
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #any other square gutter
                    else:
                        if planes[i][j]==True:
                            if (planes[i][j-1] == True) and (planes[i+1][j] == True) and (planes[i][j+1] == True) and (planes[i-1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i+1][j] == True) and (planes[i][j+1] == True) and (planes[i-1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == False) and (planes[i][j+1] == True) and (planes[i-1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == True) and (planes[i][j+1] == False) and (planes[i-1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i+1][j] == True) and (planes[i][j+1] == True) and (planes[i-1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            
                            if (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == False) and (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == False) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == False) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True
                            elif (planes[i][j-1] == True) and (planes[i-1][j] == True) and (planes[i][j+1] == True) and (planes[i+1][j] == True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                                planes[i][j]=True

                #horizontal gutter
                elif ((i%2)==0) and ((j%2)!=0):
                    #top horizontal gutter
                    if i==0:
                        if planes[i][j]==True:
                            if (planes[i][j-1]==True) and (planes[i][j+1]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==True) and (planes[i][j+1]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            
                            if (planes[i][j-1]==True) and (planes[i][j+1]==True):
                                
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==True) and (planes[i][j+1]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #bottom horizontal gutter
                    elif i==rows_planes:
                        if planes[i][j]==True:
                            if (planes[i][j-1]==True) and (planes[i][j+1]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==True) and (planes[i][j+1]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i][j-1]==True) and (planes[i][j+1]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==True) and (planes[i][j+1]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #middle horizontal gutter
                    else:
                        if planes[i][j]==True:
                            if (planes[i][j-1]==True) and (planes[i][j+1]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==True) and (planes[i][j+1]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i][j-1]==True) and (planes[i][j+1]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==True) and (planes[i][j+1]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i][j-1]==False) and (planes[i][j+1]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                #vertical gutter
                elif ((i%2)!=0) and ((j%2)==0):
                    #left vertical gutter
                    if j==0:
                        if planes[i][j]==True:
                            if (planes[i-1][j]==True) and (planes[i+1][j]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==True) and (planes[i+1][j]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i-1][j]==True) and (planes[i+1][j]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==True) and (planes[i+1][j]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                    #right vertical gutter
                    elif j==columns_planes:
                        if planes[i][j]==True:
                            if (planes[i-1][j]==True) and (planes[i+1][j]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==True) and (planes[i+1][j]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i-1][j]==True) and (planes[i+1][j]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==True) and (planes[i+1][j]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                    #middle vertical gutter
                    else:
                        if planes[i][j]==True:
                            if (planes[i-1][j]==True) and (planes[i+1][j]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==True) and (planes[i+1][j]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                join_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                join_v(to_v(i+1,j),to_v(i,j))
                        elif planes[i][j]==False:
                            if (planes[i-1][j]==True) and (planes[i+1][j]==True):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==True) and (planes[i+1][j]==False):
                                #top
                                join_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==True):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                join_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))
                            elif (planes[i-1][j]==False) and (planes[i+1][j]==False):
                                #top
                                disjoin_v(to_v(i,j),to_v(i,j+1))
                                #right
                                disjoin_v(to_v(i,j+1),to_v(i+1,j+1))
                                #bottom
                                disjoin_v(to_v(i+1,j+1),to_v(i+1,j))
                                #left
                                disjoin_v(to_v(i+1,j),to_v(i,j))

        self.planes = planes
        self.vertices = vertices    
