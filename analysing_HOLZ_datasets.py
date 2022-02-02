#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 01:49:03 2020

@author: michel
"""

import pixstem.api as ps

def loading_dataset():
    
    s1 = ps.dummy_data.get_holz_heterostructure_test_signal()
        # using a test dataset, containing disk and a ring.
        # the disk represents the STEM bright field disk, while the ring
            # represents the HOLZ ring.
            
    s2 = ps.load_ps_signal('yourfilename')
        # loaging your own data
    

def visualizing_the_data(s):
    
    print(s)
        # <PixelatedSTEM, title: , dimensions: (40, 40|80, 80)>
    s.plot()


def removing_dead_pixels(s):
    
    s_dif = s.mean(axis = (0, 1))
    s_dead_pixels = s_dif.find_dead_pixels(lazy_result = False, show_progressbar = False)
    s.plot()
    
    s = s.correct_bad_pixels(s_dead_pixels)
    
    
def finding_the_centre_position(s):
    
    s_com = s.center_of_mass(threshold = 2, show_progressbar = False)
    print(s_com)
        # <DPCSignal2D, title: , dimensions: (2|40, 40)>
    s_com.plot()