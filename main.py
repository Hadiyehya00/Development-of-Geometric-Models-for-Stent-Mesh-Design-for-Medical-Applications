from svgPathReader import SvgPathReader
from curvatureSampler import CurvatureSampler
from equidistantSampler import EquidistantSampler
from visualiser import Visualiser
from svgPathOperator import SvgPathOperator
from ui import InterfaceUtilisateur 
import tkinter as tk

# Charger le fichier SVG

root = tk.Tk()
Interface = InterfaceUtilisateur(root)
root.mainloop()
svg_file_path = Interface.get_file_path()

# Créer le lecteur de fichier svg
reader = SvgPathReader(svg_file_path)

# Créer l'opérateur de fichier svg
operator = SvgPathOperator(reader)

print(len(operator.svgPathReader.segments_list))

# Echantillonnage équidistant
equi_sampler = EquidistantSampler(operator)

# Echnatillonnage basé sur la courbure
curv_sampler = CurvatureSampler(operator)

# Visualiser l'échnatillonnage 
visualiser = Visualiser(equi_sampler)
visualiser.plot_shape(1000)
visualiser2 = Visualiser(curv_sampler)
visualiser2.plot_shape(800)