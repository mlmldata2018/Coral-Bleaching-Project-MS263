# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:08:51 2018

@author: Steve
"""
import numpy as np
import pandas as pd
from scipy import spatial


# Reference for the data refered to as hughes in this code:

# Hughes, T. P. et al. Spatial and temporal patterns of mass bleaching of
# corals in the Anthropocene. Science 359, 80–83 (2018).

# Read data from the Hughes supplemental material.  The first
# sheet is a cut-and-paste from their document with obvious typos
# fixed by hand and a few columns added for easier data manipulation.
# The second sheet has been arranged for easier import.
filename = '../data/Hughes100Reefs.xlsx'
hughes = pd.read_excel(filename, header=0, sheet_name=1, na_values='-')


# Now read our data for reef cell locations.
import scipy.io as sio

# Reference for all data for the 1,925 reef cell model.
# This has not been submitted to a journal yet, so all is subject to change:
#
# Logan, C. A., Dunne, J. P., Ryan, J. S., Baskett, M. L. & Donner, S. D. Can symbiont
# diversity and evolution allow corals to keep pace with global warming
# and ocean acidification? prep (2018).

# A copy of the data is in this repository.  The reference copy is in
# my Coral-Model-Data repository in the ProjectionsPaper directory.
mat_data = sio.loadmat('../data/ESM2M_SSTR_JD.mat')
# Put just the lat/lon columns into a data frame.  Note that they are stored
# with longitude first in the incoming data.
cells = pd.DataFrame(mat_data['ESM2M_reefs_JD'], columns=['Lon', 'Lat'])
del mat_data  # this gets garbage collected, saving around 200 MB.


# Look at Bleaching events from the numerical model, using the same scale as the previous plot of Hughes data.

mat_data = sio.loadmat('../data/HughesCompEvents_selV_rcp60E=1OA=1.mat')
# Put the bleaching counts into a data frame.
modelBleaching = pd.DataFrame(mat_data['events80_2016'])
modelBleaching.rename(columns={0: 'Events'}, inplace=True)
# Be we really want this in the cells dataframe
cells['Events'] = modelBleaching['Events']
del mat_data
del modelBleaching


# To make a fair comparison, we need to figure out which of our cells match Hughes reef areas.
# Each area has a center and an area, so we can use a circle of that area as a first-order guess.
# Unfortunately, it seems that the areas are quite warped, because some of the centers are far
# inland.

# Try scipy.spatial.cKDTree to find neighbors.
# Build the tree (a binary trie) of our cells.
lonlat = cells.as_matrix({'Lon', 'Lat'})

lon = cells['Lon']
lat = cells['Lat']
lonlat = np.column_stack((lon, lat))
print(lonlat)

exit

tree = spatial.cKDTree(lonlat)
print(tree)

# For each of the 100 Hughes cells, get a list of our cells which are likely to overlap.
# I failed to find a way to add variable-length lists to a column, so the lists are stored
# separately.
hughes = hughes.assign(radius_km=hughes.Size_km2**0.5)
cell_lists = [ [] for i in range(len(hughes)) ]
match_idx = np.zeros(len(hughes), dtype=np.bool)
for i in range(len(hughes)):
    # convert radius to degrees (ignoring change of size with latitude for now)
    # also, add 0.5 degrees as a rough allowance for our cell size
    # radius = 0.5 + hughes.radius_km[i] / 111
    # Experimentally, try a large radius to compare over larger areas even without overlap.
    # 0 gives 15 comparisons, 0.5 gives 76, 2.0 gives 93.  In all cases there's an
    # insignificant negative correlation in bleaching.
    radius = 0.5 + hughes.radius_km[i] / 111

    c = tree.query_ball_point([hughes['Numeric Lon'][i],hughes['Numeric Lat'][i]], radius, n_jobs=2)
    # Convert zero-based indexes to 1-based cell numbers.
    cell_lists[i] = [x+1 for x in c]
    match_idx[i] = len(c) > 0

print(cell_lists)

# Hughes et al. assigns each reef area to a region.  Repeat the use of the tree with a large enough radius that
# each cell is matched to some hughes area, and store the area name in the cell dataframe.  This allows us to
# assign each cell to a region.
# To increase the odds of high quality matches, this will be run at a small radius first,
# which then increases.  Matches found at a small radius will not be overwritten by matches at a large radius.
cells = cells.assign(Region='none')
cells_assigned = 0
r = 0.5
import time
t0 = time.time()
while cells_assigned < 1925:
    for i in range(len(hughes)):
        # 0 gives 15 comparisons, 0.5 gives 76, 2.0 gives 93.  In all cases there's an
        # insignificant negative correlation in bleaching.
        radius = r + hughes.radius_km[i] / 111
        c = tree.query_ball_point([hughes['Numeric Lon'][i],hughes['Numeric Lat'][i]], radius, n_jobs=-1)
        # Convert zero-based indexes to 1-based cell numbers.
        region = hughes.Region[i]
        #print('Reef', i, 'region', region, 'found ', c)
        for x in c:
            if cells.loc[x, 'Region'] == 'none':
                cells.loc[x, 'Region'] = region
                cells_assigned = cells_assigned + 1
    print('After r =', r, ',', cells_assigned, 'are assigned.')
    r = r * 2
t1 = time.time()
print('elapsed:', (t1-t0))
