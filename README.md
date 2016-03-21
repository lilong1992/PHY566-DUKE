# PHY566-DUKE
**PHY566: Computational Physics -- Group Assignment #1**

Team #2:

  * Christopher Flower   (cjf21@duke.edu)

  * Long Li              (ll199@duke.edu)

  * Shen Yan             (sy123@duke.edu)

  * Wenzhe Yu            (wy29@duke.edu)

Instruction:

This repo contains Python codes for the first group assignment of the course Computational Physics, taught by Prof. Steffen A. Bass at Duke University.

The source codes can be found in the src directory:

1_randomwalk.py simulates a random walker in two dimensional.

2_diffusion.py solves the diffusion equation by finite difference method.

3_gasmixing_v*.py simulates the mixing of two gases in a two dimensional rectangular enclosure.

v0: pick a grid point randomly; choose a direction randomly; move one step if allowed.

v1: pick a point from the occupied sites; choose a direction randomly; move one step if allowed. Faster than v0.

v2: pick a point from a dynamically updated region; choose a direction randomly from allowed directions; move one step if allowed. Faster than v1.

v3: pick a point from the occupied sites; choose a direction randomly; move several steps if allowed. Faster than v2.

3_gasmixing_average.py: average the linear population densities of gases over a large number of trials.

3_plot_average.py: read, average, and plot the density files written by 3_gasmixing_average.py.

For details, please refer to the documentation in the doc directory.

2016, Duke University. All rights reserved.
