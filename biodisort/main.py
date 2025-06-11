#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from biosnicar.drivers import get_albedo

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pathlib import Path
from biosnicar.utils.validate_inputs import validate_inputs
from biosnicar.rt_solvers.adding_doubling_solver import adding_doubling_solver
from biosnicar.optical_properties.column_OPs import get_layer_OPs, mix_in_impurities
from biosnicar.utils.display import display_out_data, plot_albedo
from biosnicar.drivers.setup_snicar import setup_snicar
from biosnicar.rt_solvers.toon_rt_solver import toon_solver
from biodisort.classes.optical_properties_for_disort import OpticalPropertiesForDisort
from biodisort.classes.model_config import DisortConfig
import disort


BIODISORT_SRC_PATH = Path(__file__).resolve().parent.parent
print("BIODISORT_SRC_PATH in setup_snicar.py: ", BIODISORT_SRC_PATH)
input_file = BIODISORT_SRC_PATH.joinpath("inputs.yaml").as_posix()

# first build the ice column and illumination conditions by instantiating the relevant classes from snicar
(
ice,
illumination,
rt_config,
snicar_config,
plot_config,
impurities,
) = setup_snicar("default")

# validate the inputs
validate_inputs(ice, illumination, impurities)

# now get the optical properties of the ice column
ssa_snw, g_snw, mac_snw = get_layer_OPs(ice, snicar_config)
tau, ssa, g, L_snw = mix_in_impurities(
    ssa_snw, g_snw, mac_snw, ice, impurities, snicar_config
)

# create an object to store the snicar column OPs
optical_properties = OpticalPropertiesForDisort(ssa, tau, g, L_snw) 
pf = np.zeros((128, ice.nbr_lyr)) # TODO update with real pmom calculation
disort_config = DisortConfig(input_file,snicar_config, ice, illumination, optical_properties, pf)

albedo_medium = np.zeros((5,))
diffuse_up_flux = np.zeros((disort_config.nbr_lyr))
diffuse_down_flux = np.zeros((disort_config.nbr_lyr))
direct_beam_flux = np.ones((disort_config.nbr_lyr,))
flux_divergence = np.zeros((disort_config.nbr_lyr,))
intensity = np.zeros((5, disort_config.nbr_lyr, 1))
mean_intensity = np.zeros((disort_config.nbr_lyr,))
transmissivity_medium = np.zeros((disort_config.nbr_lyr,))

brdf_type = 1
brdf_arg = np.array([1, 0.6, 0.06, 0.001, 0.0001, 0.00001])
empty_bemst = np.zeros((16,))
empty_emust = np.zeros((5,))
empty_rho_accurate = np.zeros((5, 1))
empty_rhou = np.zeros((disort_config.n_streams, disort_config.n_streams//2 + 1, disort_config.n_streams))
empty_rhoq = np.zeros((disort_config.n_streams//2, disort_config.n_streams//2 + 1, disort_config.n_streams))

# do brdf
rhoq, rhou, emust, bemst, rho_accurate = disort.disobrdf(disort_config.usr_ang, disort_config.umu, disort_config.fbeam, disort_config.umu0, disort_config.lambertian, disort_config.albedo, disort_config.onlyfl, empty_rhoq, empty_rhou, empty_emust,
empty_bemst, disort_config.debug, disort_config.azimuth_angle, disort_config.phi0, empty_rho_accurate, 1, brdf_arg, disort_config.nmug, disort_config.n_streams, numu=disort_config.n_polar, nphi=disort_config.n_azimuth)

# do disort and wrangtle an output to plot
alb =[]
for i in range(480):
    
    rfldir, rfldn, flup, dfdt, uavg, uu, albedo_medium, trnmed = disort.disort(disort_config.usr_ang, 
    disort_config.usr_tau, disort_config.boundary_conditions, disort_config.onlyfl, disort_config.prnt,
    disort_config.plank, disort_config.lambertian, disort_config.deltamplus, disort_config.do_pseudo_sphere, 
    disort_config.optical_depth[:,i], disort_config.ss_alb[:,i], disort_config.pmom, 
    disort_config.temperatures, disort_config.wavenumber_low, disort_config.wavenumber_high, 
    disort_config.utau, disort_config.umu0, disort_config.phi0, disort_config.umu, disort_config.azimuth_angle,
    disort_config.fbeam, disort_config.fisot, disort_config.albedo, disort_config.btemp, disort_config.ttemp, 
    disort_config.temis, disort_config.earth_radius, disort_config.lyr_height, empty_rhoq, empty_rhou, 
    empty_rho_accurate, empty_bemst, empty_emust, disort_config.accuracy, disort_config.header, 
    direct_beam_flux, diffuse_down_flux, diffuse_up_flux, flux_divergence, mean_intensity, intensity, 
    albedo_medium, transmissivity_medium, maxcmu=disort_config.n_streams, maxulv=disort_config.nbr_lyr, maxmom=127)

    # remember each output is an array over viewing angles - we need a suitable itnegration func, for now just grab idx 0
    # for each wavelength and bung it in an output array
    # albedo is total upwards flux divided by total downwards flux
    alb.append(flup[0]/(rfldir[0]+rfldn[0]))


plt.plot(snicar_config.wavelengths[0:200], alb[0:200])
plt.xlabel("wavelength (um)")
plt.ylabel("albedo")
plt.show()



