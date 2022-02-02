#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py4DSTEM package functions

Created on Tue Dec  1 12:48:13 2020

@author: michel
"""

import numpy as np
import matplotlib.pyplot as plt
import py4DSTEM

filepath_input = "/home/michel/Escritorio/Apuntes/Físicas/'4. Cuarto'/Investigación/data.dm3"
filepath_output = "/home/michel/Escritorio/Apuntes/Físicas/'4. Cuarto'/Investigación/data.h5"

""" Load the data"""
# Load a .dm3 file
datacube = py4DSTEM.io.read(filepath_input)

# This file's metadata didn't contain the shape of the beam raster, so the data is reshaped to set that here
datacube.set_scan_shape(10, 10)

# The data is shaped like
# (x_R, y_R, x_K, y_K), where R/K are real/diffraction space
datacube.data.shape

# Cropping and binning
# Note that for large datasets, binning can also be performed during loading, for some fileformats

# See the docstring for io.read
datacube.crop_data_real(2, 10, 2, 10)
datacube.crop_data_diffraction(2)

# Maximum diffraction pattern
# This is a computational fast and visually information rich way to slice into a 4D-STEM dataset

# Bragg scattering inmediately pops out. Here we can also clearly see the presence of diffection shifts in the shape of the bright central region
max_dp = np.max(datacube.data, axis = (0, 1))
py4DSTEM.visualize.show(max_dp, 0, 2)

# Position a bright-field detector
x0, y0 = 121, 136
R = 25
py4DSTEM.visualize.show_circ(max_dp, 0, 2, center = (x0, y0), R = R, alpha = 0.25)

# Show the bright-field image
BF_image = py4DSTEM.process.virtualimage.get_virtualimage_circ(datacube, x0, y0, R)
py4DSTEM.visualize.show(BF_image, contrast = 'minmax')

# Visualize a single diffraction pattern
rx, ry = 2, 5
py4DSTEM.visualize.show_points(BF_image, rx, ry, contrast = 'minmax', figsize = (6, 6))
py4DSTEM.visualize.show(datacube.data[rx,ry,:,:], 0, 2, figsize = (6, 6))

# Visualize a grid of diffraction patterns
x0, y0 = 3, 1
xL, yL = 3, 3

py4DSTEM.visualize.show_grid_overlay(BF_image, x0, y0, xL, yL, contrast = 'minmax', color = 'k', linewidth = 5, figsize = (8, 8))
py4DSTEM.visualize.show_DP_grid(datacube, x0, y0, xL, yL, min = 0, max = 2, bordercolor = 'k', borderwidth = 5, axsize = (4, 4))

""" Bragg disk detection """
# Construct an image of the vacuum probe, to use as a template for finding the other Bragg disks
# This step can look very different for different datasets - see TKTK probe_template_generation.ipynb
# The best practice is to always record a vacuum probe of every camera length / convergence angle combo
# you use in a day of experiments!
probe = py4DSTEM.process.diskdetection.get_probe_from_vacuum_4Dscan(datacube)
py4DSTEM.visualize.show(probe,0,10)

# Preprocessing for the template matching step - see TKTK probe_template_generation.ipynb
probe_kernel = py4DSTEM.process.diskdetection.get_probe_kernel_subtrgaussian(probe,sigma_probe_scale=2)
py4DSTEM.visualize.show_kernel(probe_kernel,R=100,L=200,W=5)

# Select a few diffraction patterns to test parameters on
# In most cases, (1) running disk detection on the full dataset will be slow, and (2) it can be helpful to 
# manually tune some the parameters for this algorithm. Here we're picking a few DP to tune on.
rxs = 3,3,3
rys = 0,4,7
colors=['r','b','g']

dp1 = datacube.data[rxs[0],rys[0],:,:]
dp2 = datacube.data[rxs[1],rys[1],:,:]
dp3 = datacube.data[rxs[2],rys[2],:,:]

py4DSTEM.visualize.show_points(BF_image,contrast='minmax',x=rxs,y=rys,point_color=colors)
py4DSTEM.visualize.show_image_grid(lambda i:[dp1,dp2,dp3][i],1,3,min=0.5,max=2,axsize=(5,5),get_bc=lambda i:colors[i])

# Run the disk detection on the selected DPs.  For more on disk detection, see TKTK disk_detection.ipynb
corrPower=1
sigma=2
edgeBoundary=20
minRelativeIntensity=0.005
relativeToPeak=0
minPeakSpacing=60
maxNumPeaks=70
subpixel='multicorr'
upsample_factor=16

disks_selected = py4DSTEM.process.diskdetection.find_Bragg_disks_selected(datacube,probe_kernel,rxs,rys,
                        corrPower=corrPower,sigma=sigma,edgeBoundary=edgeBoundary,
                        minRelativeIntensity=minRelativeIntensity,relativeToPeak=relativeToPeak,
                        minPeakSpacing=minPeakSpacing,maxNumPeaks=maxNumPeaks,
                        subpixel=subpixel,upsample_factor=upsample_factor)

# TKTK should I say something about the lambda functions???
py4DSTEM.visualize.show_image_grid(lambda i:[dp1,dp2,dp3][i],1,3,min=0.5,max=2,axsize=(5,5),           # Show DPs
                                   get_bc=lambda i:colors[i],
                                   get_x=lambda i:disks_selected[i].data['qx'],
                                   get_y=lambda i:disks_selected[i].data['qy'],
                                   #get_s=lambda i:disks_selected[i].data['intensity'],
                                   get_pointcolors=lambda i:colors[i])

# Run disk detection on the entire dataset
disks = py4DSTEM.process.diskdetection.find_Bragg_disks(datacube,probe_kernel,
                        corrPower=corrPower,sigma=sigma,edgeBoundary=edgeBoundary,
                        minRelativeIntensity=minRelativeIntensity,relativeToPeak=relativeToPeak,
                        minPeakSpacing=minPeakSpacing,maxNumPeaks=maxNumPeaks,
                        subpixel=subpixel,upsample_factor=upsample_factor)

# Compute and show the Bragg vector map.  See TKTK [what should I point to here?]
braggvectormap = py4DSTEM.process.diskdetection.get_bragg_vector_map(disks,datacube.Q_Nx,datacube.Q_Ny)
py4DSTEM.visualize.show(braggvectormap,0,2,cmap='viridis')

""" Save and load """
# py4DSTEM saves data as DataObjects - there's six of them, and they are:
# DataCubes, CountedDataCubes, DiffractionSlices, RealSlices, PointList, PointListArray
max_dp_DiffSlice = py4DSTEM.io.DiffractionSlice(data=max_dp, name='max_dp')
BF_image_RealSlice = py4DSTEM.io.RealSlice(data=BF_image, name='BF_image')
three_dps = py4DSTEM.io.DiffractionSlice(data=np.dstack([dp1,dp2,dp3]),
                                                         slicelabels=['dp1','dp2','dp3'],
                                                         name='three_dps')
dp3_disks = disks_selected[2]
dp3_disks.name = 'some_bragg_disks'
disks.name = 'braggpeaks'
datacube.name = '4ddatacube'

data = [max_dp_DiffSlice,BF_image_RealSlice,three_dps,dp3_disks,disks,datacube]
py4DSTEM.io.save(filepath_output,data,overwrite=True)

# See TKTK io.ipynb for more on the fileformat and read/write functionality
# For demo purposes, here we'll just open the file we just saved
# When passed a native py4DSTEM file, the io.read function prints a list of the file contents
py4DSTEM.io.read(filepath_output)

# Load the data
max_dp_h5 = py4DSTEM.io.read(filepath_output,data_id='max_dp')
max_dp_h5 = max_dp_h5.data

datacube_h5 = py4DSTEM.io.read(filepath_output,data_id='4ddatacube')

# Oh look! Its the same data.  How nice.
np.sum(max_dp_h5-max_dp)

np.sum(datacube_h5.data - datacube.data)