#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 01:20:25 2020

@author: michel
"""

def visualizing_the_data(s):
    
    s.plot()
        # if you have a small dataset, s.plot can be used directly.
        # using s.plot() on a lazy signal makes the library calculate a 
            # navigation image, which can be time consuming (lazy = True).
    
    s.plot(navigator = 'slider')
    
    s_adf = s.virtual_annular_dark_field(25, 25, 5, 20, show_progressbar = False)
    s.plot(navigator = s_adf)
    s_bf = s.virtual_bright_field(25, 25, 5, show_progressbar = False)
    s.plot(navigator = s_bf)
        # using another signal as navigator


def center_of_mass(s):
    
    s_com = s.center_of_mass(threshold = 2, show_progressbar = False)
    s_com.plot()


def radial_average(s):
    
    s.axes_manager.signal_axes[0].offset = -25
    s.axes_manager.signal_axes[1].offset = -25
    
    s_r = s.radial_average(show_progressbar = False)
    s_r.plot()


def rotating_the_diffraction_pattern(s):
    
    s_rot = s.rotate_diffraction(30, show_progressbar=False)
    s_rot.plot()


def finding_and_removing_bad_pixels(s):
    
    s_dead_pixels = s.find_dead_pixels(show_progressbar=False, lazy_result=True)
    s_corr = s.correct_bad_pixels(s_dead_pixels)
        # removing dead pixels.
    
    s_hot_pixels = s.find_hot_pixels(show_progressbar=False, lazy_result=True)
    s_corr = s.correct_bad_pixels(s_hot_pixels)
        # removing hot pixels or single-pixel cosmic rays.
        # both corrections can be made at the same time.


def template_matching_with_a_disk_or_ring(s):
    
    s_template = s.template_match_disk(disk_r=5, lazy_result=False, show_progressbar=False)
    s_template.plot()
        # doing template matching over the signal (diffraction) dimensions
            # with a disk.
        # useful for preprocessing for finding the position of the diffraction
            # disks in convergent beam electron diffraction data.
            
    s_template = s.template_match_ring(r_inner=3, r_outer=5, lazy_result=False, show_progressbar=False)
    s_template.plot()


def template_matching_with_any_binary_image(s):
    
    s_template = s.template_match_with_binary_image(binary_image, show_progressbar=False, lazy_result=False)
    s_template.plot()
        # any shape input image can be used for the template matching.


def peak_finding(s):
    
    peak_array = s.find_peaks(lazy_result=False, show_progressbar=False)
    peaks11 = peak_array[1, 1]
        # use scikit-image’s Difference of Gaussian (DoG) function to find 
            # features in the signal dimensions.
    
    s.add_peak_array_as_markers(peak_array, color='purple', size=18)
    s.plot()
        # to visualize this, the peaks can be added to a signal as HyperSpy 
            # markers.
    
    s_template = s.template_match_disk(disk_r=5, show_progressbar=False)
    peak_array = s_template.find_peaks(show_progressbar=False)
    peak_array_computed = peak_array.compute()
        # for some data types, especially convergent beam electron 
            # diffraction, using template matching can improve the peak 
            # finding.
        # note: this might add extra peaks at the edges of the images.