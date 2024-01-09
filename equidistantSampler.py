import svgpathtools
from svgPathReader import SvgPathReader
from svgPathOperator import SvgPathOperator
import math

class EquidistantSampler:
    def __init__(self, svgPathOperator):
        self.svgPathOperator = svgPathOperator
        self.svgPathOperator.set_maille_conncetors_intersections()
        self.svgPathOperator.set_maille_conncetors_seg_intersections()
        self.svgPathOperator.set_maille_conncetors_t_intersections()

    def my_equidistant_sampling(self, num_samples, segments_list):
    # La distance qui sépare deux points consécutifs équidistants
        uniformed_distance = self.svgPathOperator.svgPathReader.shape_length / num_samples
        sampled_points = []
        accumulated_length = 0
        segD = self.svgPathOperator.intersections_seg_list[0]
        segG = self.svgPathOperator.intersections_seg_list[1]
        segH = self.svgPathOperator.intersections_seg_list[2]
        segB = self.svgPathOperator.intersections_seg_list[3]
        pD = self.svgPathOperator.intersections_list[0][0]
        pG = self.svgPathOperator.intersections_list[1][0]
        pH = self.svgPathOperator.intersections_list[2][0] 
        pB = self.svgPathOperator.intersections_list[3][0] 
        tD = self.svgPathOperator.intersections_t_list[0][0]
        tG = self.svgPathOperator.intersections_t_list[1][0]
        tH = self.svgPathOperator.intersections_t_list[2][0]
        tB = self.svgPathOperator.intersections_t_list[3][0]
        # print(f"uniformed_distance= {uniformed_distance}")
        i = 1
        itG = 0
        itD = 0
        itH = 0
        itB = 0
        for j in range(len(segments_list)):
            accumulated_length += segments_list[j].length()
            #print("I AM HERE")
            # print(f"We are in segment {j}")
            if accumulated_length >= i*uniformed_distance:
                z = int(accumulated_length/uniformed_distance)-len(sampled_points)
                for k in range(int(accumulated_length/uniformed_distance)-len(sampled_points)):
                    if (segments_list[j].length()-accumulated_length+i*uniformed_distance <= segments_list[j].length()):
                        t = svgpathtools.CubicBezier.ilength(segments_list[j], segments_list[j].length()-accumulated_length+i*uniformed_distance)
                        # print(f"t = {t}")
                        point = segments_list[j].poly()(t)
                        if segments_list[j] == segD[0] and (tD<=t or k == z - 1) and itD == 0 :
                            print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CD")
                            sampled_points.append(pD)
                            i+=1
                            itD+=1
                            
                        elif segments_list[j] == segG[0] and (tG<=t or k == z - 1) and itG == 0:# and point.imag >= pG.imag:
                            print(f"The number of points in this segment is {int(accumulated_length/uniformed_distance)-len(sampled_points)}")
                            print("WE ARE IN THE SEGMENT WHERE THERE IS AN INTERSECTION CG")
                            print(f"k={k}, t = {t}")
                            print(f"tG= {tG}")
                            sampled_points.append(pG)
                            i+=1
                            itG+=1
                        
                        elif segments_list[j] == segH[0] and (tH<=t or k == z - 1) and itH ==0:
                            real_part = pB.real
                            imaginary_part = pH.imag
                            pHUpdated = complex(real_part, imaginary_part)
                            sampled_points.append(pHUpdated)
                            print(f"pH={pH}")
                            i+=1
                            itH+=1

                        elif segments_list[j] == segB[0] and (tB<=t or k == z - 1) and itB ==0:
                            # real_part = pH.real
                            # imaginary_part = pB.imag
                            # pBUpdated = complex(real_part, imaginary_part)
                            sampled_points.append(pB)
                            # print(f"pBUpdated={pBUpdated}")
                            print(f"pB = {pB}")
                            i+=1
                            itB+=1 

                        else:
                            sampled_points.append(point)
                            i+=1                   
                        
                    # print(f"The value of i is {i}")

        return sampled_points