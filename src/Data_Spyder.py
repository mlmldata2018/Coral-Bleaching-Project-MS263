# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:08:51 2018

@author: Steve
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs

from coral_project_functions import make_coral_map

# Reference for the data refered to as hughes in this code:

# Hughes, T. P. et al. Spatial and temporal patterns of mass bleaching of
# corals in the Anthropocene. Science 359, 80–83 (2018).

# Read data from the Hughes supplemental material.  The first
# sheet is a cut-and-paste from their document with obvious typos
# fixed by hand and a few columns added for easier data manipulation.
# The second sheet has been arranged for easier import.
filename = '../data/Hughes100Reefs.xlsx'
hughes = pd.read_excel(filename,header=0,sheet_name=1, na_values='-')

## Cell 2
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


## Cell 3
plt.figure(figsize=[12, 4])
ax = make_coral_map()
# Hughes reef areas can be large.  Make size proportional.  Conveniently, the marker
# size argument is in square units.  However, our map is in degree units and the areas
# are in kilometers.  This should be calculated carefully for map display, but for now
# just to a rough conversion.  The initial value relates to pixels per square degree.
conversion = 60*(1/111)**2

lon = hughes['Numeric Lon']
plt.scatter(lon-180*(np.sign(lon)-1), hughes['Numeric Lat'], marker='o',
            s=conversion*hughes.Size_km2.astype(float),
            label='Hughes Areas', transform=ccrs.PlateCarree())
# Mark our cells with small dots.
# scatter is broken so that the "," argument to plot pixels is ignored.
# use s=1 to make a very small dot.
lon = cells['Lon']
plt.scatter(lon-180*(np.sign(lon)-1), cells['Lat'], marker='.', s=1, label='Cell centers',
           transform=ccrs.PlateCarree())
plt.legend()
plt.text(110, 25, 'Caribbean')
plt.text(-60, -25, 'Australia')
plt.text(-152, 9, 'Red\nSea')
plt.text(20, 25, 'Hawaii')


## Cell 4
# Now try an indication of bleaching severity.
sss = hughes.Size_km2.astype(float)
sss = sss[~np.isnan(sss)]
print("Area size min/max/mean/median:", min(sss), max(sss), np.mean(sss), np.median(sss), 'km^2')

plt.figure(figsize=[12, 4])
ax = make_coral_map()
conversion = 60*(1/111)**2
lon = hughes['Numeric Lon']
severity = hughes['Severe count']
plt.scatter(lon-180*(np.sign(lon)-1), hughes['Numeric Lat'], marker='o',
            s=conversion*hughes.Size_km2.astype(float),
            label='Hughes Areas',
            c=severity,
            cmap="plasma",
            transform=ccrs.PlateCarree())

plt.title('Severe Bleaching Events, 1980-2016', fontsize=14)
plt.clim(0, 10)
plt.colorbar(pad=0.02)
plt.text(110, 25, 'Caribbean')
plt.text(-60, -25, 'Australia')
plt.text(-152, 9, 'Red\nSea')
plt.text(20, 25, 'Hawaii')


## Cell 5
# Look at Bleaching events from the numerical model, using the same scale as
# the previous plot of Hughes data.

mat_data = sio.loadmat('../data/HughesCompEvents_selV_rcp60E=1OA=1.mat')
# Put the bleaching counts into a data frame.
modelBleaching = pd.DataFrame(mat_data['events80_2016'])
modelBleaching.rename(columns={0: 'Events'}, inplace=True)
# Be we really want this in the cells dataframe
cells['Events'] = modelBleaching['Events']

# For later use, also load the un-summarized data which has the bleaching
# flags for each reef and year from 1980 to 2016.  Branching and massive coral
# are treated separately.
#modelDetail = pd.DataFrame(mat_data['events80_2016_detail'][:, :, 1])
massive_bleach = np.array(mat_data['events80_2016_detail'][:, :, 0])
branching_bleach = np.array(mat_data['events80_2016_detail'][:, :, 1])

del mat_data
del modelBleaching
plt.figure(figsize=[12, 4])
ax = make_coral_map()
conversion = 60*(1/111)**2

lon = cells['Lon']
plt.scatter(lon-180*(np.sign(lon)-1), cells['Lat'], c = cells['Events'],
            marker='.', s=1, label='Events', cmap="plasma",
            transform=ccrs.PlateCarree())
plt.title('Modeled Bleaching Events, 1980-2016')
plt.clim(0, 10)
plt.colorbar(pad=0.10)


## Cell 8 (6 and 7 are just "head"s)
# To make a fair comparison, we need to figure out which of our cells match Hughes reef areas.
# Each area has a center and an area, so we can use a circle of that area as a first-order guess.
# Unfortunately, it seems that the areas are quite warped, because some of the centers are far
# inland.

# Try scipy.spatial.cKDTree to find neighbors.
from scipy import spatial
# Build the tree (a binary trie) of our cells.
# NOTE: cells.as_matrix({'Lon', 'Lat'}) does not return the columns in a determinate order!
# explicitly stack the columns instead.
lonlat = np.column_stack((cells['Lon'], cells['Lat']))
tree = spatial.cKDTree(lonlat)

# For each of the 100 Hughes cells, get a list of our cells which are likely to overlap.
# I failed to find a way to add variable-length lists to a column, so the lists are stored
# separately.
hughes = hughes.assign(radius_km=hughes.Size_km2**0.5)
cell_lists = [[] for i in range(len(hughes))]
match_idx = np.zeros(len(hughes), dtype=np.bool)
for i in range(len(hughes)):
    # convert radius to degrees (ignoring change of size with latitude for now)
    # also, add 0.5 degrees as a rough allowance for our cell size
    # radius = 0.5 + hughes.radius_km[i] / 111
    # Experimentally, try a large radius to compare over larger areas even without overlap.
    # 0 gives 15 comparisons, 0.5 gives 76, 2.0 gives 93.  In all cases there's an
    # insignificant negative correlation in bleaching.
    radius = 0.5 + hughes.radius_km[i] / 111

    c = tree.query_ball_point([hughes['Numeric Lon'][i], hughes['Numeric Lat'][i]],
                              radius, n_jobs=2)
    # Convert zero-based indexes to 1-based cell numbers.
    cell_lists[i] = [x+1 for x in c]
    match_idx[i] = len(c) > 0

print(cell_lists)

# Hughes et al. assigns each reef area to a region.  Repeat the use of the tree with
# a large enough radius that each cell is matched to some hughes area, and store the
# area name in the cell dataframe.  This allows us to assign each cell to a region.
# To increase the odds of high quality matches, this will be run at a small radius
# first, which then increases.  Matches found at a small radius will not be overwritten
# by matches at a large radius.
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
        c = tree.query_ball_point([hughes['Numeric Lon'][i], hughes['Numeric Lat'][i]],
                                  radius, n_jobs=-1)
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
print('Search time = ', (t1-t0), ' sec.')

# Some special cases are easier to identify visually than with the approach above.
# South atlantic, off Brazil is initially id'd as Indian Ocean/ Middle East!
# Make a bounding box to specify these cells
box = [-40, -25, -26, -16]
cells.loc[(cells.Lat > box[2]) & (cells.Lat < box[3]) & (cells.Lon > box[0]) &
          (cells.Lon < box[1]), 'Region'] = "WAtl"
# Others off Brazil are labeled Pacific.
box = [-39, -34, -16, -8]
cells.loc[(cells.Lat > box[2]) & (cells.Lat < box[3]) & (cells.Lon > box[0]) &
          (cells.Lon < box[1]), 'Region'] = "WAtl"
# Some SW Caribbean cells are id'd as Pacific
box = [-83, -80,  12, 16]
cells.loc[(cells.Lat > box[2]) & (cells.Lat < box[3]) & (cells.Lon > box[0]) &
          (cells.Lon < box[1]), 'Region'] = "WAtl"
box = [-81, -76, 8.8, 11]
cells.loc[(cells.Lat > box[2]) & (cells.Lat < box[3]) & (cells.Lon > box[0]) &
          (cells.Lon < box[1]), 'Region'] = "WAtl"

print('Pacific:', sum(cells['Region'] == 'Pac'))
print('Indian Ocean - Middle East:', sum(cells['Region'] == 'IO-ME'))
print('Australasia:', sum(cells['Region'] == 'AuA'))
print('West Atlantic:', sum(cells['Region'] == 'WAtl'))
cells.to_pickle('../results/Logan_cells_events_region.pkl')
print(cells.head())


## SKIP MANY CELLS

## The new part 5/7, with cumulative sums
# massive_bleach
#idx = cells['Region'] == 'AuA'

# The annual bleaching count for the whole world, based on Logan et al. (2018)
cell_annual_b = np.sum(branching_bleach, 0)
cell_annual_m = np.sum(massive_bleach, 0)
cell_annual = np.sum(massive_bleach | branching_bleach, 0)

# Hughes severe events are flagged by the letter S in columns called 1980, 1981, etc.
hughes_annual = np.zeros(2016-1980+1)
for y in range(1980, 2017):
    hughes_annual[y-1980] = sum(hughes[y] == 'S')

hughes_annual = np.int32(hughes_annual)
print('Hughes:')
print(hughes_annual)
print('Branching and massive')
print(cell_annual_b)
print(cell_annual_m)
print('Either')
print(cell_annual)