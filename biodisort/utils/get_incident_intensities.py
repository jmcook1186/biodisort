#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from biodisort.classes.model_config import DisortConfig
import xarray as xr
import numpy as np



def get_intensity_of_direct_beam(disort_config: DisortConfig):
    """
    gets the intensity of the direct beam from precalculated files
    returns values by wavelength
    """
    if disort_config.direct:
        solzen = disort_config.solar_zenith_angle
        cloud_stub = "_clr_"       
        coszen_stub = str("SZA" + str(solzen).rjust(2, "0"))
        incoming_file = xr.open_dataset(
            str("/home/joe/Code/biosnicar-py/Data/OP_data/480band/fsds/swnb_480bnd_"
                + disort_config.region
                + disort_config.season
                + cloud_stub
                + coszen_stub
                + ".nc"
            )
        )

        flx_slr = incoming_file["flx_dwn_sfc"].values
        flx_slr[flx_slr <= 0] = 1e-30
    else:
        flx_slr = np.zeros(480)*1e-30
    return flx_slr


def get_diffuse_intensity(disort_config: DisortConfig):
    """
    gets the intensity of the direct beam from precalculated files
    returns values by wavelength
    """
    if disort_config.diffuse:
        solzen = disort_config.solar_zenith_angle
        cloud_stub = "_cld"
        incoming_file = xr.open_dataset(
            str("/home/joe/Code/biosnicar-py/Data/OP_data/480band/fsds/swnb_480bnd_"
                + disort_config.region
                + disort_config.season                
                + cloud_stub
                + ".nc"
            )
        )

        flx_slr = incoming_file["flx_dwn_sfc"].values
        flx_slr[flx_slr <= 0] = 1e-30
    else:
        flx_slr = np.zeros(480)*1e-30

    return flx_slr
