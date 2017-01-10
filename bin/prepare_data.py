
""" Prepare_data.py

Code to take all phoenix-aces fits files and create .dat files with wavelength
and flux.
Adds them to the data directory of eniric for convolutions etc.

This wastes alot of memory duplicating wavelemgth vector.

Jason Neal Janurary 2017
"""
from __future__ import division, print_function
import os
import sys
import pandas as pd
from astropy.io import fits
from eniric.IOmodule import pdwrite_2col

data_dir = "../data/PHOENIX-ACES_spectra/"
phoenix_dir = "../../../data/fullphoenix/"

wavelength_file = "WAVE_PHOENIX-ACES-AGSS-COND-2011.fits"

def main():
    wavelength = fits.getdata(data_dir + wavelength_file)  # Phoenix wavelength

    # get all phoenix fits files we want to convert
    for (path, dirs, files) in os.walk(phoenix_dir):
        # print(path)
        # print(dirs)
        phoenix_files = [f for f in files if
                         f.endswith("PHOENIX-ACES-AGSS-COND-2011-HiRes.fits")]

        for phoenix_file in phoenix_files:
            if int(phoenix_file[3:8]) > 4000:
                # Not doing temperatures over 4000 K.
                pass
            else:
                Z_folder = path.split("/")[-1]
                os.makedirs(os.path.join(data_dir, Z_folder), exist_ok=True)  # make folder if doesn't exit
                output_filename = os.path.join(data_dir, Z_folder,
                                               phoenix_file[:-5] + "_wave.dat")  # Name of .dat file

                spectra = fits.getdata(os.path.join(path, phoenix_file))

                # Need to add conversions pedro preformed to flux!

                if not pdwrite_2col(output_filename, wavelength, spectra,
                                header=["# Wavelength", "Flux"]):
                    print("Successfully wrote to ", output_filename)
                else:
                    print("Failed to write to ", output_filename)

    print("Done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
