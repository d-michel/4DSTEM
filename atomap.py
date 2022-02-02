# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:30:35 2020

@author: Míchel
"""

import matplotlib.pyplot as plt
import atomap.api as am
import numpy as np
import hyperspy.api as hs

''' load the image '''
s = hs.load("/Michel/Datos/16/16.tif")
s.plot(colorbar = False)

''' finding the feature separation '''
s_peaks = am.get_feature_separation(s, separation_range = (15, 20))
s_peaks.plot()

''' generate the initial positions for the atomic columns '''
A_positions = am.get_atom_positions(s, separation = 15)

''' adding atoms using GUI '''
A_positions_new = am.add_atoms_with_gui(s, A_positions)

''' initialize a Sublattice '''
sublattice_A = am.Sublattice(A_positions_new, image = s.data, color = 'r')
sublattice_A.plot(markersize = 2)

''' refine the position of the atomic columns using center of mass and 2D Gaussian fit '''
sublattice_A.find_nearest_neighbors()
sublattice_A.refine_atom_positions_using_center_of_mass()
sublattice_A.get_position_history().plot()

''' define the atom_lattice object and save the atomic coordinates '''
atom_lattice = am.Atom_Lattice(image = s.data, name = 'test', sublattice_list = [sublattice_A])
atom_lattice.save("/Michel/Datos/16/16.hdf5", overwrite = True)
atom_lattice.plot(markersize = 2)

''' atom lattice analysis '''
i_points, i_record, p_record = atom_lattice.integrate_column_intensity(method = 'Voronoi')
i_record.plot(cmap = 'viridis')

# save image
i_record.change_dtype('float32')
i_record.save("/Michel/Datos/16/Voronoi.tif", overwrite = True)

''' atom lattice statistical analysis '''
models = am.quant.get_statistical_quant_criteria([sublattice_A], 10)

# insert number of differents atoms
atoms = 1
model = models[atoms-1] # 2nd model
atom_lattice_Q = am.quant.statistical_quant(s, sublattice_A, model, atoms)
