import svgpathtools
from svgPathReader import SvgPathReader
import numpy as np
import math

class SvgPathOperator:
    def __init__(self, svgPathReader):
        self.svgPathReader = svgPathReader
        self.svgPathReader.set_paths()
        self.svgPathReader.set_paths_list()
        self.svgPathReader.set_segments_list()
        self.svgPathReader.set_bezier_curves_to_poly_list()
        self.svgPathReader.set_paths_length_list()
        self.svgPathReader.set_shape_length()
        self.svgPathReader.seperate_components()
        self.intersections_list = []
        self.intersections_seg_list = []
        self.intersections_t_list = []
        self.curvatures_list = []
        self.total_curvature = 0
    
    def set_maille_conncetors_intersections(self):
    # The goal is to return a list of lists
    # Each sub_list is the intersections between la maille and one of the connectors
    # The result is the intersections with CD, CG, CH, CB respectively
        for i in self.svgPathReader.seperated_components:
            if i!= 0:
                intersections = []
                for (T1, seg1, t1), (T2, seg2, t2) in self.svgPathReader.paths_non_nul[0].intersect(self.svgPathReader.paths_non_nul[i]):
                    intersections.append(self.svgPathReader.paths_non_nul[i].point(T2))
                self.intersections_list.append(intersections)
        

    def set_maille_conncetors_seg_intersections(self):
        for i in self.svgPathReader.seperated_components:
            if i!= 0:
                intersections = []
                for (T1, seg1, t1), (T2, seg2, t2) in self.svgPathReader.paths_non_nul[0].intersect(self.svgPathReader.paths_non_nul[i]):
                    intersections.append(seg1)
                self.intersections_seg_list.append(intersections)


    def set_maille_conncetors_t_intersections(self):
        for i in self.svgPathReader.seperated_components:
            if i!= 0:
                intersections = []
                for (T1, seg1, t1), (T2, seg2, t2) in self.svgPathReader.paths_non_nul[0].intersect(self.svgPathReader.paths_non_nul[i]):
                    intersections.append(t1)
                self.intersections_t_list.append(intersections)


    def calculate_curvature_at_one_point(self, bezier_poly, t):
        dp = bezier_poly.deriv()(t) # Premiere dérivée
        dx, dy = np.real(dp), np.imag(dp)
        denom = np.sqrt(dx**2+dy**2)**3 # le dénominateur de la courbure
        
        d2p = bezier_poly.deriv().deriv()(t) # la deuxieme dérivée 
        d2x, d2y = np.real(d2p), np.imag(d2p)
        nom = np.abs(dx*d2y - dy*d2x) # le nominateur de la courbure
        if not math.isnan(nom/denom):
            return nom/denom
        else :
            print(bezier_poly)
            return 0
        
    def calculate_curvature_of_curve(self, bezier_poly, num_points):
        total_curvature = 0
        for t in range(num_points+1):
            t /= num_points
            if not math.isnan(self.calculate_curvature_at_one_point(bezier_poly, t)):
                curvature = self.calculate_curvature_at_one_point(bezier_poly, t)
            #else:
                #print(f"t:= {t}")
                #print(f"The poly is: {bezier_poly}")
            
            total_curvature += curvature
        
        return total_curvature
    
    def set_max_curvature(self, bezier_curves_to_poly, num_points):
        max = 0
        for poly in bezier_curves_to_poly:
            curvature = self.calculate_curvature_of_curve(poly, num_points)
            if self.calculate_curvature_of_curve(poly, num_points) > max:
                max = curvature
        
        return max

    # Define the min of the curvature
    def min_curvature(self, bezier_curves_to_poly, num_points):
        min = self.max_curvature(bezier_curves_to_poly, num_points)
        for poly in bezier_curves_to_poly:
            curvature = self.calculate_curvature_of_curve(poly, num_points)
            if self.calculate_curvature_of_curve(poly, num_points) < min:
                min = curvature
        
        return min
    
    def set_curvatures_list(self):
        for list in self.svgPathReader.bezier_curves_to_poly_list:
            curvature_list = []
            for poly in list:
                curvature_list.append(self.calculate_curvature_of_curve(poly, 50))
            self.curvatures_list.append(curvature_list)
    
    def set_total_curvature(self):
        for list in self.curvatures_list:
            for curvature in list:
                self.total_curvature += curvature
        
        return self.total_curvature
    
