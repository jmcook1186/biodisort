#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
import numpy as np
import matplotlib.pyplot as plt
from biodisort.utils.get_column_ops import get_column_ops
from biodisort.classes.optical_properties_for_disort import OpticalPropertiesForDisort
from biodisort.classes.model_config import DisortConfig
from biodisort.classes.outputs import DisortOutputs
from biodisort.classes.brdf_config import BrdfConfig
from biodisort.utils.get_incident_intensities import (
    get_intensity_of_direct_beam,
    get_diffuse_intensity,
)
from biodisort.brdf.get_brdf import get_brdf
from biodisort.drivers.run_disort import run_disort
import disort

## Set paths
BIODISORT_SRC_PATH = Path(__file__).resolve().parent.parent.parent
input_file = BIODISORT_SRC_PATH.joinpath("inputs.yaml").as_posix()

optical_properties, snicar_config, ice = get_column_ops()

disort_config = DisortConfig(input_file, snicar_config, ice, optical_properties)
brdf_config = BrdfConfig(input_file, disort_config, optical_properties)
# set incident intensities
disort_config.fbeam = get_intensity_of_direct_beam(
    disort_config
)  # set direct radiation
disort_config.fisot = get_diffuse_intensity(disort_config)  # set diffuse radiation


# get brdf
brdf_config = get_brdf(disort_config, brdf_config)


from biodisort.utils.phase_function import hg_legendre_coefficients

def get_pmom(disort_config: DisortConfig, optical_properties: OpticalPropertiesForDisort):
    pmom = np.zeros((disort_config.nbr_wvl, disort_config.nmom, disort_config.nbr_lyr))
    for i in np.arange(0,disort_config.nbr_wvl,1):
        for j in np.arange(disort_config.nbr_lyr):
            g = optical_properties.g[j,i]
            pmom[i, :, j] = hg_legendre_coefficients(g, disort_config.nmom)
    return pmom


disort_config.pmom = get_pmom(disort_config, optical_properties)

outputs = run_disort(disort_config, brdf_config)


for i in range(9):
    plt.plot(
        outputs.intensities[0:100, i, 0, 0],
        label=f"emission ang {disort_config.emission_angles[i]} deg",
    )
plt.xlabel("wavelength")
plt.ylabel("intensity (Wm-2)")
plt.legend()
plt.show()

plt.plot(outputs.spectral_albedo)
plt.xlabel("wavelength (um)")
plt.ylabel("albedo")
plt.show()

print("BBA: ", sum(outputs.spectral_albedo))
