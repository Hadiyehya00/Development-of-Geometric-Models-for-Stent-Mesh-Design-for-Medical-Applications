from curvatureSampler import CurvatureSampler
from equidistantSampler import EquidistantSampler
import matplotlib.pyplot as plt
from typing import Union
import csv

class Visualiser:
    def __init__(self, sampler: Union[EquidistantSampler, CurvatureSampler]):
        self.sampler = sampler

    # Sample points from the entire shape
    def correct_shape(self, i, x_coords, y_coords):
        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[0]): # Connector droit
            for k in range(len(x_coords)):
                if  k == len(x_coords) -1 :
                    x_coords.append(x_coords[0])
                    y_coords.append(y_coords[0])

        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[1]): # Connector droit
            for k in range(len(x_coords)):
                if  x_coords[k] <= self.sampler.svgPathOperator.intersections_list[0][0].real:
                    print("Correcting the CD")
                    x_coords[k] = self.sampler.svgPathOperator.intersections_list[0][0].real
                    y_coords[k] = -self.sampler.svgPathOperator.intersections_list[0][0].imag

        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[2]): # Connector gauche
            for k in range(len(x_coords)):
                if  x_coords[k] >= self.sampler.svgPathOperator.intersections_list[1][0].real:
                    print("Correcting the CG")
                    x_coords[k] = self.sampler.svgPathOperator.intersections_list[1][0].real
                    y_coords[k] = -self.sampler.svgPathOperator.intersections_list[1][0].imag
        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[3]): # Connector Haut
            for k in range(len(x_coords)):
                # if  y_coords[k] <= -self.sampler.svgPathOperator.intersections_list[2][0].imag:
                #     print("Correcting the CH")
                    x_coords[k] = self.sampler.svgPathOperator.intersections_list[3][0].real
                    y_coords[k] = -self.sampler.svgPathOperator.intersections_list[2][0].imag
        if (i == self.sampler.svgPathOperator.svgPathReader.seperated_components[4]): # Connector Bas
            for k in range(len(x_coords)):
                # if  y_coords[k] >= -self.sampler.svgPathOperator.intersections_list[3][0].imag:
                #     print("Correcting the CB")
                    x_coords[k] = self.sampler.svgPathOperator.intersections_list[3][0].real
                    y_coords[k] = -self.sampler.svgPathOperator.intersections_list[3][0].imag
                    
    
    def points_in_csv_file(self, i, x_coords, y_coords):
        csv_file = f'path{i}_data.csv'
        with open(csv_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['X', 'Y'])       
            for j in range (len(x_coords)):
                csv_writer.writerow([x_coords[j],y_coords[j]])


    def plot_shape(self, sampled_points):
        if isinstance(self.sampler, EquidistantSampler):           
            for i in range(len(self.sampler.svgPathOperator.svgPathReader.segments_list)):
                equidistant_points = self.sampler.my_equidistant_sampling(sampled_points, self.sampler.svgPathOperator.svgPathReader.segments_list[i])
                x_coords = [point.real for point in equidistant_points]
                y_coords = [-point.imag for point in equidistant_points]
                self.correct_shape(i, x_coords, y_coords)
                # Plot the sampled points
                self.points_in_csv_file(i, x_coords, y_coords)
                plt.plot(x_coords, y_coords, color='blue', marker='.')
                
        if isinstance(self.sampler, CurvatureSampler): 
            for i in range(len(self.sampler.svgPathOperator.svgPathReader.bezier_curves_to_poly_list)):
                curvature_sampled_points = self.sampler.curvature_based_sampling(i, self.sampler.svgPathOperator.svgPathReader.bezier_curves_to_poly_list[i], sampled_points)
                x_coords = [point.real for point in curvature_sampled_points]
                y_coords = [-point.imag for point in curvature_sampled_points]
                self.correct_shape(i, x_coords, y_coords)
                plt.plot(x_coords, y_coords, color='blue', marker='.')

        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Sampled Points from Bézier Curves')
        plt.grid(True)
        plt.show()


