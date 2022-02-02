#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:06:32 2020

@author: michel
"""

import pixstem.dummy_data as dd
import pixstem.api as ps
import numpy as np
import dask.array as da
import hyperspy.api as hs
import pixstem.io_tools as it

def pixelated_STEM():
    
    s1 = dd.get_holz_simple_test_signal()
        # generating a test pixelated STEM dataset.
    s1.save("test_data.hdf5")
    
    s2 = ps.load_ps_signal("text_data.hdf5", lazy = True)
        # loading your own data.
        # here 'lazy = True' does not load all the data into memory, meaning very
            # large datasets can be processed.
    
    s1.plot()
    s2.plot()
        # plotting the data.


def from_NumPy_array_to_pixelatedSTEM_object():
    
    data = np.random.random((10, 15, 30, 35))
        # generating a random array with NumPy.
    s = ps.PixelatedSTEM(data) 
    print(s)
        # >>> <PixelatedSTEM, title: , dimensions: (15, 10|35, 30)>
        # dimensions 0/1 and 2/3 are lipped in the PixelatedSTEM signal and the
            # NumPy array. This is due to how HyperSpy handles the input data.


def from_Dask_array_to_LazyPixelatedSTEM_object():
    
    data = da.random.random((10, 7, 15, 32), chunks = ((2, 2, 2, 2)))
        # generating a random array with Dask.
    s = ps.LazyPixelatedSTEM(data)
    print(s)
        # >>> <LazyPixelatedSTEM, title: , dimensions: (7, 10|32, 15)>
        # dimensions are also lipped in the LazyPixelatedSTEM signal and the Dask
            # array.


def from_HyperSpy_signal_to_PixelatedSTEM():
    
    data = np.random.random((10, 15, 30, 35))
        # generating a random array with NumPy.
    s = hs.signals.Signal2D(data)
    s_new = it.signal_to_pixelated_stem(s)
    print(s)
        # >>> <Signal2D, title: , dimensions: (15, 10|35, 30)>
        # dimensions are also lipped in the PixelatedSTEM signal and the Numpy
            # array.


def differential_phase_contrast_beam_shift_data():
    
    s1 = dd.get_simple_dpc_signal()
        # generating a test DPC dataset.
    s1.save("test_dpc_data.hdf5")
    
    s2 = ps.load_dpc_signal("test_dpc_data.hdf5")
        # loading your own data.
    
    s1.plot()
    s1.get_color_signal().plot()
    
    s2.plot()
    s2.get_color_signal().plot()
        #plotting the data.


def from_NumPy_array_to_DPCSignal_objects():
    
    data1 = np.random.random((2, 21, 54))
        # generating a random array with NumPy.
    s1 = ps.DPCSignal2D(data1)
    print(s1)
        # <DPCSignal2D, title: , dimensions: (2|54, 21)>
        # dimensions are also lipped in the DPCSignal object and the Numpy array.
    
    data2 = np.random.random((2, 109))
    s2 = ps.DPCSignal1D(data2)
    print(s2)
        # <DPCSignal1D, title: , dimensions: (2|109)>
    
    data3 = np.random.random((2, ))
    s3 = ps.DPCBaseSignal(data3)
    print(s3)
        # <DPCBaseSignal, title: , dimensions: (|2)>