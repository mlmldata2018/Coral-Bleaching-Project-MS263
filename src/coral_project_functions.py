# -*- coding: utf-8 -*-
"""
Utility functions specific to a class project comparing two sets of coral reef
bleaching data.
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from scipy import stats


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
    print('In function, extent = ', extent)
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
    plt.figure()
    plt.plot(df['Severe count'], df['cell_bleach'], 'o')
    plt.xlabel('Bleaching Counted by Hughes et al.')
    plt.ylabel('Average Bleaching in Adjacent Logan et al. Cells')
    plt.title('Logan et al. vs. Hughes et al. Bleaching events' + set_name)

    # Straight from the scipy docs...
    slope, intercept, r_value, p_value, std_err = stats.linregress(
            df['Severe count'], df['cell_bleach'])
    plt.plot(df['Severe count'], intercept + slope*df['Severe count'],
             'r', label='fitted line')
    print("r-squared:", r_value**2)
