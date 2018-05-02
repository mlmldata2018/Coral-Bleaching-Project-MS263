# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 16:48:45 2018

@author: Steve
"""

# This code section is largely a duplicate of the data input in the
# Bleaching_Project_Data_Setup notebook, with fewer comments.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.io as sio
from mytools import principal_component as pc

# Now read our data for reef cell locations.
# A copy of the data is in this repository.  The reference copy is in
# my Coral-Model-Data repository in the ProjectionsPaper directory.
mat_data = sio.loadmat('../data/ESM2M_SSTR_JD.mat')
#print(mat_data)

# Put the lat/lon columns directly into a data frame.  Note that they are stored
# with longitude first in the incoming data.
cells = pd.DataFrame(mat_data['ESM2M_reefs_JD'], columns=['Lon', 'Lat'])
cells['abs_lat'] = abs(cells['Lat'])

# It makes more sense to have longitude have a break at 0 than at +-180, since the latter is in the midddle of a coral area.
cells['Lon'] = cells['Lon']-180*(np.sign(cells['Lon'])-1)

# Now add bleaching counts from a specific run.
bleach_data = sio.loadmat('../data/HughesCompEvents_selV_rcp60E=1OA=1.mat')
# Put the bleaching counts into a data frame.
modelBleaching = pd.DataFrame(bleach_data['events80_2016'])
modelBleaching.rename(columns={0: 'Events'}, inplace=True)
# Be we really want this in the cells dataframe
#cells['Events'] = modelBleaching['Events']
cells['Rand'] = np.random.uniform(low=-10, high=10, size=len(modelBleaching))
print(cells.head())

# Now get 1861-1950 SST mean and variance for each reef
sst = mat_data['SSTR_2M26_JD']
del mat_data  # this is big and not used again.
sst_mean = np.mean(sst, axis=1)
sst_var = np.var(sst, axis=1)
cells['SST'] = sst_mean
cells['variance'] = sst_var
print(cells.head())
all_names = list(cells)

print('PCA including signed and unsigned latitude:')
[eigenval, eigenvec, pct_acct, loadings, sorted_names] = pc.pca(np.asmatrix(cells),
     all_names, standardize=True, sort=True)
print('Names:\n', sorted_names)
print('Eigenvalues:\n', eigenval)
print('Eigenvectors:\n', eigenvec)
print('Variance accounted for by each component:\n', pct_acct)
print('Component loadings:\n', loadings)

print('PCA including only unsigned latitude:')
reduced_names = all_names
reduced_names.remove('Lat')
[eigenval, eigenvec, pct_acct, loadings, sorted_names] = pc.pca(np.asmatrix(cells[reduced_names]),
     reduced_names, standardize=True, sort=True)
print('Names:\n', sorted_names)
print('Eigenvalues:\n', eigenval)
print('Eigenvectors:\n', eigenvec)
print('Variance accounted for by each component:\n', pct_acct)
print('Component loadings:\n', loadings)

# Now look at factor loadings for the reduced list
# A = V (sqrt(Lambda))
# V = eigenvectors = eigenvec
# Lambda = eigenvalue matrix = eigenval
A = np.matmul(eigenvec, np.diag(eigenval)**0.5)
# A now contains the loadings for PC1 in the first row, and so on.
A
plt.figure()
plt.plot(A[:, 0], A[:, 1], 'o')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.xlabel('PC1 loading')
plt.ylabel('PC2 loading')
for i, txt in enumerate(sorted_names):
    plt.text(A[i,0]+0.05,A[i,1],txt)


# Now show all reefs transformed to PC1 and PC2
# Convert each observation (reef) to a point in PC1, PC2 coordinates.
# WARNING: data has not been sorted, eigen* have!
data = np.asarray(cells[reduced_names])
data_normalized = (data - np.mean(data, 0)) / np.std(data, 0, ddof=1)
print('Shapes before pc1 calculation:')
print(np.shape(data_normalized))
print(np.shape(eigenvec[0]))
print(np.shape(eigenval[0]))

pc1 = eigenval[0]*np.sum(data_normalized * eigenvec[0], 1)
print(np.shape(data_normalized))
print(np.shape(eigenvec[0]))
pc2 = eigenval[1]*np.sum(data_normalized * eigenvec[1], 1)
plt.figure()
plt.plot(pc1, pc2, ',')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Observations transformed to PC1 and PC2');