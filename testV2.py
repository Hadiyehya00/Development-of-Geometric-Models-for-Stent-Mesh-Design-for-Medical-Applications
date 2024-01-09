# import svgpathtools
# import csv
# import matplotlib.pyplot as plt
# from scipy.interpolate import CubicSpline
# import numpy as np
# import math

# # Charger le fichier SVG
# paths, attributes = svgpathtools.svg2paths('Maille 1.svg')

# # Extract cubic Bézier curve data from SVG
# maille_length = 0
# bezier_curves_to_poly_list = []
# segments_list = []

# paths_list = []
# paths_non_nulle = []
# for path in paths:
#     if len(path)>0:
#         bezier_curves = []
#         path_segments = []  # Create a new list for the segments in this path
#         bezier_curves_to_poly = []
#         for segment in path:      
#             if isinstance(segment, svgpathtools.path.CubicBezier):
#                 # We convert CubicBezier object to numpy.poly1d (forme polynomiale)
#                 bezier_curves_to_poly.append(segment.poly())
#                 path_segments.append(segment)
                
#                 # Extract control points and end point of cubic Bézier curve
#                 control1 = (segment.start.real, -segment.start.imag)
#                 control2 = (segment.control1.real, -segment.control1.imag)
#                 control3 = (segment.control2.real, -segment.control2.imag)
#                 end_point = (segment.end.real, -segment.end.imag)
                
#                 # Store Bézier curve data as a tuple of control points and end point
#                 bezier_curve = (control1, control2, control3, end_point)
#                 bezier_curves.append(bezier_curve)
#                 maille_length += segment.length()
#         paths_non_nulle.append(path)        
#         paths_list.append(bezier_curves)
#         segments_list.append(path_segments)  # Add the current path's segments to the main list
#         bezier_curves_to_poly_list.append(bezier_curves_to_poly)

# print(f"We have {len(paths)} paths in our maille")
# print(f"We have {len(paths_list)} paths in our maille which are not nulle")
# print(f"We have {len(segments_list)} segments list in segments_lists")


# # Distinguer les différentes composants de la maille

# # Créer une liste qui contient les longueurs des différents paths
# def path_length(path):
#     length = 0
#     for segment in path:
#         length+=segment.length()

#     return length

# paths_length_list = []

# for path in paths:
#     if path_length(path) > 0 : # Ensure we have the same order of paths_list and paths_length_list
#         paths_length_list.append(path_length(path))

# # for i in range(len(paths_length_list)):
# #     print(f"The length of path {i} is {paths_length_list[i]}")

# # Déterminer les xmin, xmax, ymin, ymax de chaque path
# def extremities_of_path(path_to_bezier_curves):
#     # on va retourner la liste contenant xmin, ymin, xmax, ymax d'un path donné
#     # Comme input, on va donner la liste contenant les tuplets des points de controles constituant ce path 
#     # (bezier_curves corresponding to the path)
#     extremities_list = []
#     xmin = 1000
#     xmax = 0 
#     ymin = 0
#     ymax = -1000 
#     for bezier_curve in path_to_bezier_curves:
#         for point in bezier_curve:
#             if (point[0] < xmin):
#                 xmin = point[0]
#             if (point[0] > xmax):
#                 xmax = point[0]
#             if (point[1] < ymin):
#                 ymin = point[1]
#             if (point[1] > ymax):
#                 ymax = point[1]
    
#     extremities_list = [xmin, xmax, ymin, ymax]
#     return extremities_list

# listExtremities = extremities_of_path(paths_list[0])
# # for v in listExtremities:
# #     print(v)

# def seperate_components(paths_list):
#     # On donne comme argument la liste des courbes de Bézier représentant chacun des paths 
#     # Path_list = [Bezier_curves1, bezier_curves2, .... bezier_curvesX]
#     # Bezier_curves = [Bezier_curve1, Beziercurve2 ....]
#     # Bezier_curve = (c1,c2,c3,cend)
#     # controlPoint = (Réel, Imaginaire)
#     # Liste qui va contenir les index des paths selon l'ordre [Maille, CD, CG, CH, CB]
#     ordered_components = []
#     extremities_list_all_paths = []
#     max_length = 0
#     connectors_index = []
#     connectors_list = []
#     y_max = 0
#     x_max = 0
#     y_min = 0 
#     x_min = 0
#     for i in range(len(paths_list)):
#         if (path_length(paths[i]) > max_length):
#             max_length = path_length(paths[i]) 
#     #print(f"The maximum length in our shape is {max_length}, (which belongs to la maille)")
#     ordered_components.append(paths_length_list.index(max_length)) # paths_length_list has the length of each one of the components

#     # Create a list that have the extremities of all the paaths (Maille + Connectors)
#     for i in range(len(paths_list)):
#         extremities_list_all_paths.append(extremities_of_path(paths_list[i]))

#     # Create an intermediate list that has connectors indexes
#     for i in range(len(paths_list)):
#         if (i != paths_length_list.index(max_length)):
#             connectors_index.append(i)
   
#     # Create an intermediate list that has only the extremitie s of the connectors
#     connectors_list = [extremities_list_all_paths[i] for i in connectors_index]
    
#     min_values = [min(column) for column in zip(*connectors_list)] # min[xmin, xmax, ymin, ymax]
#     max_values = [max(column) for column in zip(*connectors_list)] # max[xmin, xmax, ymin, ymax]

#     for v in min_values:
#         x_min = min_values[0]
#         y_min = min_values[2]

#     for v in max_values:
#         x_max = max_values[1]
#         y_max = max_values[3]

#     # Transposing extremities_list_all_paths (to have rows of the values not the list)
#     tansposed_extremities = [list(row) for row in zip(*extremities_list_all_paths)]
#     ordered_components.append(tansposed_extremities[1].index(x_max))
#     ordered_components.append(tansposed_extremities[0].index(x_min))
#     ordered_components.append(tansposed_extremities[3].index(y_max))
#     ordered_components.append(tansposed_extremities[2].index(y_min))


#     return ordered_components

# separerated_compenents = seperate_components(paths_list)
# for i in range(len(separerated_compenents)):
#     if i==0:
#         print(f"The index of la maille is {separerated_compenents[i]}")
#     elif i==1:
#         print(f"The index of CD is {separerated_compenents[i]}")
#     elif i==2:
#         print(f"The index of CG is {separerated_compenents[i]}")
#     elif i==3:
#         print(f"The index of CH is {separerated_compenents[i]}")
#     else:
#         print(f"The index of CB is {separerated_compenents[i]}")

# #Search for intersection between the right connector and la maille
# # print(paths[1])
        
# def maille_conncetors_intersections(paths_non_nulle):
#     # The goal is to return a list of lists
#     # Each sub_list is the intersections between la maille and one of the connectors
#     # The result is the intersections with CD, CG, CH, CB respectively
#     intersections_list = []
#     for i in separerated_compenents:
#         if i!= 0:
#             intersections = []
#             for (T1, seg1, t1), (T2, seg2, t2) in paths_non_nulle[0].intersect(paths_non_nulle[i]):
#                 intersections.append(paths_non_nulle[i].point(T2))
#             intersections_list.append(intersections)
    
#     return intersections_list

# intersections_list = maille_conncetors_intersections(paths_non_nulle)
# # for i in range(len(intersections_list)):
# #     if i==0:
# #         print(f"The intersections with CD are {intersections_list[i]}")
# #     elif i==1:
# #         print(f"The intersections with CG are {intersections_list[i]}")
# #     elif i==2:
# #         print(f"The intersections with CH are {intersections_list[i]}")
# #     else:
# #         print(f"The intersections with CB are {intersections_list[i]}")


# def maille_conncetors_seg_intersections(paths_non_nulle):
#     seg_intersections = []
#     for i in separerated_compenents:
#         if i!= 0:
#             intersections = []
#             for (T1, seg1, t1), (T2, seg2, t2) in paths_non_nulle[0].intersect(paths_non_nulle[i]):
#                 intersections.append(seg1)
#             seg_intersections.append(intersections)
    
#     return seg_intersections

# def maille_conncetors_t_intersections(paths_non_nulle):
#     t_intersections = []
#     for i in separerated_compenents:
#         if i!= 0:
#             intersections = []
#             for (T1, seg1, t1), (T2, seg2, t2) in paths_non_nulle[0].intersect(paths_non_nulle[i]):
#                 intersections.append(t1)
#             t_intersections.append(intersections)
    
#     return t_intersections

# print(f"The segment intersection between la maille et CG is {maille_conncetors_seg_intersections(paths_non_nulle)[1]}")
# #print(f"The index of the longest path is {seperate_components(paths)}")

# seg1 = maille_conncetors_seg_intersections(paths_non_nulle)[0]
# p1 = maille_conncetors_intersections(paths_non_nulle)[0][0]

# segG = maille_conncetors_seg_intersections(paths_non_nulle)[1]
# pG = maille_conncetors_intersections(paths_non_nulle)[1][0]
# #Methode personalisée

# def my_equidistant_sampling(num_samples, segments_list):
#     # La distance qui sépare deux points consécutifs équidistants
#     uniformed_distance = maille_length / num_samples
#     sampled_points = []
#     accumulated_length = 0
#     # print(f"uniformed_distance= {uniformed_distance}")
#     i = 1
#     itG = 0
#     itD = 0
#     for j in range(len(segments_list)):
#         accumulated_length += segments_list[j].length()
#         #print("I AM HERE")
#         # print(f"We are in segment {j}")
#         if accumulated_length >= i*uniformed_distance:

#             for k in range(int(accumulated_length/uniformed_distance)-len(sampled_points)):

#                 if (segments_list[j].length()-accumulated_length+i*uniformed_distance <= segments_list[j].length()  ):
#                     t = svgpathtools.CubicBezier.ilength(segments_list[j], segments_list[j].length()-accumulated_length+i*uniformed_distance)
#                     # print(f"t = {t}")
#                     point = segments_list[j].poly()(t)
#                     if segments_list[j] == seg1[0] and itD == 0 and point.real < p1.real and point.imag < p1.imag:
#                         print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CD")
#                         sampled_points.append(p1)
#                         i+=1
#                         itD+=1
#                     if segments_list[j] == segG[0] and itG == 0 and point.real > pG.real :
#                         print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CG")
#                         sampled_points.append(pG)
#                         i+=1
#                         itG+=1
#                     else:
#                         sampled_points.append(point)
#                         i+=1
                    
                    
#                 # print(f"The value of i is {i}")

    
#     return sampled_points



# # Calculate the curvature at a specific point in curve

# def calculate_curvature_at_one_point(bezier_poly, t):
#     dp = bezier_poly.deriv()(t) # Premiere dérivée
#     dx, dy = np.real(dp), np.imag(dp)
#     denom = np.sqrt(dx**2+dy**2)**3 # le dénominateur de la courbure
    
#     d2p = bezier_poly.deriv().deriv()(t) # la deuxieme dérivée 
#     d2x, d2y = np.real(d2p), np.imag(d2p)
#     nom = np.abs(dx*d2y - dy*d2x) # le nominateur de la courbure
#     if not math.isnan(nom/denom):
#         return nom/denom
#     else :
#         print(bezier_poly)
#         return 0


# # Calculate the curvature of all the curve

# def calculate_curvature_of_curve(bezier_poly, num_points):
#     total_curvature = 0
#     for t in range(num_points+1):
#         t /= num_points
#         if not math.isnan(calculate_curvature_at_one_point(bezier_poly, t)):
#             curvature = calculate_curvature_at_one_point(bezier_poly, t)
#         #else:
#             #print(f"t:= {t}")
#             #print(f"The poly is: {bezier_poly}")
        
#         total_curvature += curvature
    
#     return total_curvature

# # define the max of the curvature

# def max_curvature(bezier_curves_to_poly, num_points):
#     max = 0
#     for poly in bezier_curves_to_poly:
#         curvature = calculate_curvature_of_curve(poly, num_points)
#         if calculate_curvature_of_curve(poly, num_points) > max:
#             max = curvature
    
#     return max

# # Define the min of the curvature
# def min_curvature(bezier_curves_to_poly, num_points):
#     min = max_curvature(bezier_curves_to_poly, num_points)
#     for poly in bezier_curves_to_poly:
#         curvature = calculate_curvature_of_curve(poly, num_points)
#         if calculate_curvature_of_curve(poly, num_points) < min:
#             min = curvature
    
#     return min


# curvatures_list = []

# for list in bezier_curves_to_poly_list:
#     curvature_list = []
#     for poly in list:
#         curvature_list.append(calculate_curvature_of_curve(poly, 50))
#     curvatures_list.append(curvature_list)

# # for i in range(len(curvatures_list)):
# #     print(curvatures_list[i])

# for list in curvatures_list:
#     print(list)

# total_curvature = 0
# for list in curvatures_list:
#     for curvature in list:
#         total_curvature += curvature

# #Min Max Normalization of curvatures
# def normalize_curvatures_list(curvatures_list):
#     curvatures_list_normalized = []
#     min = min_curvature(bezier_curves_to_poly, 100)
#     max = max_curvature(bezier_curves_to_poly, 100)
#     for curvature in curvatures_list:
#         curvatures_list_normalized.append(curvature/(max- min))
    
#     return curvatures_list_normalized

# curvatures_list_normalized = normalize_curvatures_list(curvatures_list)
# # for i in range(len(curvatures_list_normalized)):
# #     print(f"{curvatures_list_normalized[i]}")

# tD = maille_conncetors_t_intersections(paths_non_nulle)[0][0]
# tG = maille_conncetors_t_intersections(paths_non_nulle)[1][0]

# def curvature_based_sampling(i, bezier_curves_to_poly, total_points):
#     sampled_points_curv = []
#     itD = 0
#     itG = 0
#     t_intersection = 0
#     t_values_list = []
#     for j in range(len(bezier_curves_to_poly)):
#         num_samples = int((curvatures_list[i][j]/total_curvature)*total_points) 
#         # print(num_samples)
#         if num_samples == 0:
#             num_samples = 4
#         t_values = np.linspace(0, 1, num_samples)
        
#         # curve_poly_points = [bezier_curves_to_poly(t) for t in t_values]
#         if bezier_curves_to_poly[j] == seg1[0].poly() and itD == 0 :
#             print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CD")
#             t_values_list = t_values.tolist()
#             t_intersection = tD
#             position = next((k for k, v in enumerate(t_values_list) if v > t_intersection), len(t_values_list))
#             t_values_list.insert(position, t_intersection)
#             t_values = np.array(t_values_list)
#             itD+=1
#         if bezier_curves_to_poly[j] == segG[0].poly() and itG == 0:
#             print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CG")
#             t_intersection = tG
#             position = next((k for k, v in enumerate(t_values_list) if v > t_intersection), len(t_values_list))
#             t_values_list.insert(position, t_intersection)
#             t_values = np.array(t_values_list)
#             itG+=1
        
#         sampled_points_curv.extend(bezier_curves_to_poly[j](t) for t in t_values)
    
#     return sampled_points_curv

# # # print(f"Tha max curvature is {max_curvature(bezier_curves_to_poly, 100)}")
# # # print(f"Tha min curvature is {min_curvature(bezier_curves_to_poly, 100)}")



# # Sample points from the entire shape
# # equidistant_points = curvature_based_sampling(bezier_curves_to_poly, 800)
# #for i in range(len(segments_list)):
# for i in range(len(bezier_curves_to_poly_list)):
#     #equidistant_points = my_equidistant_sampling(600, segments_list[i])
#     #print(f"The first point in equidistant_points is {equidistant_points[0]}")
#     equidistant_points = curvature_based_sampling(i, bezier_curves_to_poly_list[i], 800)
#     x_coords = [point.real for point in equidistant_points]
#     y_coords = [-point.imag for point in equidistant_points]

#     if (i == separerated_compenents[1]): # Connector droit
#         for k in range(len(x_coords)):
#             print("I M HERE")
#             if  x_coords[k] <= intersections_list[0][0].real:
#                 x_coords[k] = intersections_list[0][0].real
#                 y_coords[k] = -intersections_list[0][0].imag

#     if (i == separerated_compenents[2]): # Connector gauche
#         for k in range(len(x_coords)):
#             print("I M HEEEEERE")
#             if  x_coords[k] >= intersections_list[1][0].real:
#                 x_coords[k] = intersections_list[1][0].real
#                 y_coords[k] = -intersections_list[1][0].imag


#     # Plot the sampled points
#     plt.plot(x_coords, y_coords, color='blue', marker='.')

# plt.axis('equal')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('Equidistant Sampled Points from Bézier Curves')
# plt.grid(True)
# plt.show()

