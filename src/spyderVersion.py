# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 14:55:02 2018

This is just a scratch pad!  Please see the Jupyter version.

@author: Steve
"""

#import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read data from the Hughes supplemental material.  The first
# sheet is a cut-and-paste from their document with obvious typos
# fixed by hand and a few columns added for easier data manipulation.
# The second sheet has been arranged for easier import.
filename = '../data/Hughes100Reefs.xlsx' 
hughes = pd.read_excel(filename,header=0,sheet_name=1)
# Missing size values are set to zero - be careful how they are used later!
hughes.Size_km2 = hughes.Size_km2.replace({"-": "0"})


# Now read our data for reef cell locations.
import scipy.io as sio

# A copy of the data is in the project.  The reference copy is in
# my Coral-Model-Data repository in the ProjectionsPaper directory.
mat_data = sio.loadmat('../data/ESM2M_SSTR_JD.mat')
# Put just the lat/lon columns into a data frame.  Note that they are stored
# with longitude first in the incoming data.
cells = pd.DataFrame(mat_data['ESM2M_reefs_JD'], columns=['Lon', 'Lat'])
del mat_data  # hope this gets garbage collected - it's big


plt.figure()
# Hughes reef areas can be large.  Make size proportional.  Conveniently, the marker
# size argument is in square units.
conversion = 40*(1/111)**2

plt.scatter(hughes['Numeric Lon'], hughes['Numeric Lat'], marker='o', s=conversion*hughes.Size_km2.astype(float))
# Mark our cells with small dots.
# scatter is broken so that the "," argument to plot pixels is ignored.
# use s=1 to make a very small dot.
plt.scatter(cells['Lon'], cells['Lat'], marker='.', s=1)