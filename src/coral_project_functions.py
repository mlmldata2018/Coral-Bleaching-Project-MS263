# -*- coding: utf-8 -*-
"""
Utility functions specific to a class project comparing two sets of coral reef
bleaching data.
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from scipy import stats
import numpy as np
import math


def make_coral_map(projection=ccrs.Miller(central_longitude=180),
                   extent=[10, 330, -35, 35], xticks=[60, 120, 180, 240, 300],
                   yticks=[-30, -15, 0, 15, 30], subspec=None):
    '''
    Return axis object for cartopy coral area map with labeled gridlines.

    Input: projection: Cartopy projection, default = cartopy.crs.Miller()
           extent: Region to cover, with longitude measured east from Greenwich,
               default = [10, 330, -35, 35]
           xticks: Longitude labels, default = [60, 120, 180, 240, 300]
           yticks: Latitude labels, default = [-30, -15, 0, 15, 30]
    Output: Cartopy axis object

    Based on Tom Connolly's example from MS 263, which is in turn
    Based on
    http://scitools.org.uk/cartopy/docs/v0.15/examples/tick_labels.html
    License: Open Government License,
    https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/

    Example code:

    import cartopy.crs as ccrs
    plt.figure()
    ax = make_coral_map(projection=ccrs.Mercator())
    '''
    if subspec is None:
        ax = plt.axes(projection=projection)
    else:
        ax = plt.subplot(subspec, projection=projection)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    ax.coastlines()
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.ylim(extent[2:4])

    # Reefs are most abundant in the western pacific and between +- 30 latitude.
    # It is important to specify the crs argument to set_extent, or the extent
    # may be partially ignored.
    # The more important thing seems to be to call this AFTER the other actions
    # on the axis.
    ax.set_extent(extent, crs=ccrs.PlateCarree())

    return ax


def bleach_scatter(df, set_name):
    """
    Scatter plot two bleaching measures against each other with a trendline.

    Input: df: a dataframe, which must include columns named "Severe count"
           and "cell_bleach"
           set_name: a name appended to the plot title
    Output: none
    """
    # Don't call figure() here, so outside code can display this as a figure
    # or in subplots.
    #plt.figure()
    plt.plot(df['Severe count'], df['cell_bleach'], 'o')
    plt.xlabel('Hughes Bleaching')
    plt.ylabel('Logan Bleaching')
    plt.title('Bleaching events, ' + set_name)

    # Straight from the scipy docs...
    slope, intercept, r_value, p_value, std_err = stats.linregress(
            df['Severe count'], df['cell_bleach'])
    plt.plot(df['Severe count'], intercept + slope*df['Severe count'],
             'r', label='fitted line')
    print(set_name, "r-squared:", r_value**2)


def scatter_all(df, marker_size=1):
    names = list(df)
    var_count = len(names)
    # there a "n choose 2" plots
    p_count = math.factorial(var_count)/2/math.factorial(var_count-2)
    rows = np.ceil(p_count/2)
    print('Plotting', var_count, 'variables in', p_count, 'plots and', rows, 'rows.')
    print('There are', len(df), 'rows of data.')
    count = 1;
    for i, namex in enumerate(names):
        for j, namey in enumerate(names[i+1:]):
            plt.subplot(rows, 2, count)
            plt.scatter(df[namex], df[namey], marker='.', s=marker_size)
            plt.xlabel(namex)
            plt.ylabel(namey)
            count = count + 1
    plt.subplots_adjust(hspace=1.2, wspace=0.3)


def bleach_annual_plot(bb, mb, hb, title, cumulative=False):
    # The annual bleaching count for the whole world, based on Logan et al. (2018)

    cell_annual = np.sum(mb | bb, 0)

    # Hughes severe events are flagged by the letter S in columns called 1980, 1981, etc.
    hughes_annual = np.zeros(2016-1980+1)
    for y in range(1980, 2017):
        hughes_annual[y-1980] = sum(hb[y] == 'S')

    hughes_annual = np.int32(hughes_annual)

    if cumulative:
        hughes_annual = cumulativesum(hughes_annual)
        cell_annual = cumulativesum(cell_annual)
        hughes_norm = hughes_annual
        cell_norm = hughes_annual[-1]*cell_annual/cell_annual[-1]
    else:
        hughes_norm = np.mean(hughes_annual)*hughes_annual/sum(hughes_annual)
        cell_norm = np.mean(hughes_annual)*cell_annual/sum(cell_annual)

    # Plot global cumulative total by year for both approaches.
    #plt.figure()
    plt.plot(range(1980, 2017), hughes_norm, label='Hughes')
    plt.plot(range(1980, 2017), cell_norm, label='Logan')
    plt.xlabel('Year')
    plt.ylabel('Normalized bleaching count')
    plt.legend()
    plt.title(title)

    #plt.figure()
    #shiftYear = -1.5
    #plt.plot(range(1980, 2017), hughes_norm, label='Hughes')
    #plt.plot(shiftYear+np.array(range(1980, 2017)), cell_norm, label='Logan')
    #plt.legend()

def cumulativesum(data):
    '''Return the seqential sums of values in the argument.

       Accepts an array or list and returns a numpy.array of
       the same length and data type.  The nth value in the
       output array is the sum of the first n values in the input.
    '''

    # Initialize the output to zeros, which should be faster
    # than append.  'zeros_like' attempts to match the data type.
    cum_array = np.zeros_like(data)
    cumsum = 0
    # Go through all the input values, using their index i to
    # place the cumulative sum into the output array.
    for i, val in enumerate(data):
        cumsum = cumsum + val
        cum_array[i] = cumsum

    return cum_array


if __name__ == '__main__':
    import pandas as pd

    print('Begin standalone diagnostics')
    df = pd.DataFrame(np.random.randint(0, high=10, size=(100, 37)),
        columns=range(1980, 2017))




    bleach_annual_plot(np.random.randint(0, high=10, size=(1925, 37)),
                       np.random.randint(0, high=10, size=(1925, 37)),
                       df)
