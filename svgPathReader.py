import svgpathtools

class SvgPathReader:
    def __init__(self, imagePath):
        self.paths, self.attributes = svgpathtools.svg2paths(imagePath)
        self.segments_list = []
        self.paths_list = []
        self.bezier_curves_to_poly_list = []
        self.paths_length_list = []
        self.seperated_components = []
        self.shape_length = 0
        self.paths_non_nul = []

    def set_shape_length(self):
        for path in self.paths:
            if len(path)>0:
                for segment in path:      
                    if isinstance(segment, svgpathtools.path.CubicBezier):                        
                        self.shape_length += segment.length()
        

    # Function that returns the non nul in our shape
    def set_paths(self):
        for path in self.paths:
            if len(path)>0:
                self.paths_non_nul.append(path) 


    # This function returns a list of lists 
    # where each sublist is the cubic Bezier segments of a specific path 
    def set_segments_list(self):
        for path in self.paths:
            if len(path)>0:
                path_segments = []  # Create a new list for the segments in this path
                for segment in path:      
                    if isinstance(segment, svgpathtools.path.CubicBezier):                       
                        # 
                        path_segments.append(segment)

                self.segments_list.append(path_segments)  # Add the current path's segments to the main list


    def set_paths_list(self):
        for path in self.paths:
            if len(path)>0:
                bezier_curves = []
                for segment in path:      
                    if isinstance(segment, svgpathtools.path.CubicBezier):                      
                        # Extract control points and end point of cubic Bézier curve
                        control1 = (segment.start.real, -segment.start.imag)
                        control2 = (segment.control1.real, -segment.control1.imag)
                        control3 = (segment.control2.real, -segment.control2.imag)
                        end_point = (segment.end.real, -segment.end.imag)
                        
                        # Store Bézier curve data as a tuple of control points and end point
                        bezier_curve = (control1, control2, control3, end_point)
                        bezier_curves.append(bezier_curve)    
                self.paths_list.append(bezier_curves) 

    
    def set_bezier_curves_to_poly_list(self):
        for path in self.paths:
            if len(path)>0:
                bezier_curves_to_poly = []
                for segment in path:      
                    if isinstance(segment, svgpathtools.path.CubicBezier):
                        # We convert CubicBezier object to numpy.poly1d (forme polynomiale)
                        bezier_curves_to_poly.append(segment.poly())
                self.bezier_curves_to_poly_list.append(bezier_curves_to_poly)

    
    # Calculate the length of one path in the shape
    def path_length(self, path):
        length = 0
        for segment in path:
            length+=segment.length()
        return length

    
    # Get a list of lengths of all the paths in the shape
    def set_paths_length_list(self):
        for path in self.paths:
            l = self.path_length(path)
            print("here")
            if l > 0 : # Ensure we have the same order of paths_list and paths_length_list
                self.paths_length_list.append(l)
        

    # Déterminer les xmin, xmax, ymin, ymax de chaque path
    def extremities_of_path(self, path_to_bezier_curves):
        # on va retourner la liste contenant xmin, ymin, xmax, ymax d'un path donné
        # Comme input, on va donner la liste contenant les tuplets des points de controles constituant ce path 
        # (bezier_curves corresponding to the path)
        extremities_list = []
        xmin = 1000
        xmax = 0 
        ymin = 0
        ymax = -1000 
        for bezier_curve in path_to_bezier_curves:
            for point in bezier_curve:
                if (point[0] < xmin):
                    xmin = point[0]
                if (point[0] > xmax):
                    xmax = point[0]
                if (point[1] < ymin):
                    ymin = point[1]
                if (point[1] > ymax):
                    ymax = point[1]
        
        extremities_list = [xmin, xmax, ymin, ymax]
        return extremities_list
    
    def seperate_components(self):
        # On donne comme argument la liste des courbes de Bézier représentant chacun des paths 
        # Path_list = [Bezier_curves1, bezier_curves2, .... bezier_curvesX]
        # Bezier_curves = [Bezier_curve1, Beziercurve2 ....]
        # Bezier_curve = (c1,c2,c3,cend)
        # controlPoint = (Réel, Imaginaire) (c)
        # Liste qui va contenir les index des paths selon l'ordre [Maille, CD, CG, CH, CB]
            extremities_list_all_paths = []
            max_length = 0
            connectors_index = []
            connectors_list = []
            y_max = 0
            x_max = 0
            y_min = 0 
            x_min = 0
            for i in range(len(self.paths_list)):
                l = self.path_length(self.paths[i])
                if ( l > max_length):
                    max_length = l
            #print(f"The maximum length in our shape is {max_length}, (which belongs to la maille)")
            self.seperated_components.append(self.paths_length_list.index(max_length)) # paths_length_list has the length of each one of the components

            # Create a list that have the extremities of all the paaths (Maille + Connectors)
            for i in range(len(self.paths_list)):
                extremities_list_all_paths.append(self.extremities_of_path(self.paths_list[i]))

            # Create an intermediate list that has connectors indexes
            for i in range(len(self.paths_list)):
                if (i != self.paths_length_list.index(max_length)):
                    connectors_index.append(i)
        
            # Create an intermediate list that has only the extremitie s of the connectors
            connectors_list = [extremities_list_all_paths[i] for i in connectors_index]
            
            min_values = [min(column) for column in zip(*connectors_list)] # min[xmin, xmax, ymin, ymax]
            max_values = [max(column) for column in zip(*connectors_list)] # max[xmin, xmax, ymin, ymax]

            for v in min_values:
                x_min = min_values[0]
                y_min = min_values[2]

            for v in max_values:
                x_max = max_values[1]
                y_max = max_values[3]

            # Transposing extremities_list_all_paths (to have rows of the values not the list)
            tansposed_extremities = [list(row) for row in zip(*extremities_list_all_paths)]
            self.seperated_components.append(tansposed_extremities[1].index(x_max))
            self.seperated_components.append(tansposed_extremities[0].index(x_min))
            self.seperated_components.append(tansposed_extremities[3].index(y_max))
            self.seperated_components.append(tansposed_extremities[2].index(y_min))

    