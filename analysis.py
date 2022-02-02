#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 00:20:24 2020

@author: michel
"""

import numpy as np
import scipy as sc
import pixstem.api as ps
import hyperspy.api as hs
import pixstem.io_tools as it
import matplotlib.pylab as plt

# Load data using hyperspy and convert it to pixstem

data = hs.load("./Datos/11 SI data_20cm_CL1-2/Diffraction SI.dm4", lazy=True)
s = it.signal_to_pixelated_stem(data)

#Plot Position Averaged Convergent Electron Diffraction Pattern (PACBED)

s_PACBED = data.sum()
    
fig = plt.figure(figsize=(6,6))
plt.imshow(s_PACBED, cmap='plasma')
plt.xticks([])
plt.yticks([])
plt.show()

s_PACBED.save("./Datos/11 SI data_20cm_CL1-2/s_PACED.tif")