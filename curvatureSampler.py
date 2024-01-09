from svgPathOperator import SvgPathOperator
from svgPathReader import SvgPathReader
import numpy as np


class CurvatureSampler:
    def __init__(self, svgPathOperator):
        self.svgPathOperator = svgPathOperator
        self.svgPathOperator.set_curvatures_list()
        self.svgPathOperator.set_maille_conncetors_intersections()
        self.svgPathOperator.set_maille_conncetors_seg_intersections()
        self.svgPathOperator.set_maille_conncetors_t_intersections()


    def curvature_based_sampling(self, i, bezier_curves_to_poly, total_points):
        tD = self.svgPathOperator.intersections_t_list[0][0]
        tG = self.svgPathOperator.intersections_t_list[1][0]
        seg1 = self.svgPathOperator.intersections_seg_list[0]
        segG = self.svgPathOperator.intersections_seg_list[1]
        sampled_points_curv = []
        total_curvature = self.svgPathOperator.set_total_curvature()
        itD = 0
        itG = 0
        t_intersection = 0
        t_values_list = []
        for j in range(len(bezier_curves_to_poly)):
            num_samples = int((self.svgPathOperator.curvatures_list[i][j]/total_curvature)*total_points) 
            # print(num_samples)
            if num_samples == 0:
                num_samples = 4
            t_values = np.linspace(0, 1, num_samples)
            
            # curve_poly_points = [bezier_curves_to_poly(t) for t in t_values]
            if bezier_curves_to_poly[j] == seg1[0].poly() and itD == 0 :
                print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CD")
                t_values_list = t_values.tolist()
                t_intersection = tD
                position = next((k for k, v in enumerate(t_values_list) if v > t_intersection), len(t_values_list))
                t_values_list.insert(position, t_intersection)
                t_values = np.array(t_values_list)
                itD+=1
            if bezier_curves_to_poly[j] == segG[0].poly() and itG == 0:
                print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CG")
                t_values_list = t_values.tolist()
                t_intersection = tG
                position = next((k for k, v in enumerate(t_values_list) if v > t_intersection), len(t_values_list))
                t_values_list.insert(position, t_intersection)
                t_values = np.array(t_values_list)
                itG+=1
            
            sampled_points_curv.extend(bezier_curves_to_poly[j](t) for t in t_values)
        
        return sampled_points_curv