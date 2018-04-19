# -*- coding: utf-8 -*-
"""
This function uses Tom Connolly's idea of setting up a map in a function,
but it is customized to default to a world map of the tropics centered on
the coral triangle.

"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


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

    Based on
    http://scitools.org.uk/cartopy/docs/v0.15/examples/tick_labels.html
    License: Open Government License, 
    https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/

    Example code:

    import cartopy.crs as ccrs
    plt.figure()
    ax = make_map(projection=ccrs.Mercator())
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

    # Reefs are most abundant in the western pacific and between +- 30 latitude.
    # It is important to specify the crs argument to set_extent, or the extent
    # may be partially ignored. 
    # The more important thing seems to be to call this AFTER the other actions
    # on the axis.
    print('In function, extent = ', extent)
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    return ax
