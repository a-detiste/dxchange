#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the Australian Synchrotron Facility
data as original tiff.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    fname = 'data_dir/'

    proj_start = 0
    proj_end = 1801
    flat_start = 0
    flat_end = 10
    dark_start = 0
    dark_end = 10

    ind_tomo = range(proj_start, proj_end)
    ind_flat = range(flat_start, flat_end)
    ind_dark = range(dark_start, dark_end)

    # Select the sinogram range to reconstruct.
    start = 290
    end = 294

    # Read the Australian Synchrotron Facility data
    proj, flat, dark = dxchange.read_aus_microct(fname, ind_tomo, ind_flat, ind_dark, sino=(start, end))

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0])

    # Flat-field correction of raw data.
    proj = tomopy.normalize(proj, flat, dark)

    # Find rotation center.
    rot_center = tomopy.find_center(proj, theta, init=1024, ind=0, tol=0.5)
    print("Center of rotation: ", rot_center)

    proj = tomopy.minus_log(proj)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/aus_')
