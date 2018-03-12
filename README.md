### What I did

1. Read in data from a paper by Mumby et al. (reference below).
2. Read in reef locations from my current research with Cheryl Logan.
3. Plotted both on a simple lat/lon grid to show their relative locations.
4. Plotted the Mumby data colored by bleaching event count, as first step toward using the data.

### The questions

The first two questions are
1. How well does the model agree with the Hughes data?
2. Are the differences systematic, and how?  For example they may vary
    - by a simple scaling factor
    - by region
    - with increasing or decreasing date
    - randomly
    
### Background

Note: I described to you a fine grid of data using 0.04 degree resolution.  That is the approach in the Donner paper below.  Now it turns out that Cheryl would prefer a comparison with the newer Hughes paper, and Simon Donner agrees.


Bleaching is a key indicator of thermally stressed coral reefs because it almost always occurs under sufficiently high temperatures and because it is readily observed in the field.  Coral reef research has increased so rapidly that a "Since 2017" search for "coral reef" on Google Scholar gives 12,300 results.  Add the word "bleaching" and there are still 2,470 results.

Unfortunately, while there are many observations of corals bleaching there is little consistency in the data.  How severe was the bleaching?  How observed it?  Was the data biased by the fact that effort is focused where bleaching has already been observed or where it is convenient to travel?  Do we include citizen observations?  Some efforts to address that include

Donner, S. D., Rickbeil, G. J. M. & Heron, S. F. A new, high-resolution global mass coral bleaching database. PLoS One 12, e0175490 (2017).
Hughes, T. P. et al. Spatial and temporal patterns of mass bleaching of corals in the Anthropocene. Science 359, 80–83 (2018).

Computational results can be just as scattered.  Bleaching can be estimated by rules of thumb based on temperature variations above a baseline, or in mechanistic models.  It is currently impossible to build a really accurate mechanistic model, because fundamental parameters are still being determined.  Each model takes a different set of parameters into account, and must be calibrated with real world data.

Calibration is the goal of this project.  I plan to use data from Hughes et al. as a reference for calibrating and validating a model I have been working on with Cheryl Logan.  The first step, and perhaps the only step I will be able to complete for this class, is to find a useful way of comparing data between the two sources.  The Hughes data
are presented for 100 locations of widely varying size, giving simple none/moderate/severe categories for bleaching in each year, and is based on data from 349 references.  Hughes et al. attempt to represent the world's major reef areas, but not to include all reefs.  Our data attempt to cover essentially all reefs with cells about 1 by 0.5 degrees in size.  We know that each area contains coral reefs, but not how much area is included.  Bleaching is determined by population fluctuations in a simulation of reef growth and mortality.  In other words, the two data sets are different in size, coverage, and data definition.  Reconciling those things enough to make a useful comparison is the challenge.


    
