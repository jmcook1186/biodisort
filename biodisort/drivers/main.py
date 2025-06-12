#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
import numpy as np
import matplotlib.pyplot as plt
from biosnicar.utils.validate_inputs import validate_inputs
from biosnicar.optical_properties.column_OPs import get_layer_OPs, mix_in_impurities
from biosnicar.drivers.setup_snicar import setup_snicar
from biodisort.classes.optical_properties_for_disort import OpticalPropertiesForDisort
from biodisort.classes.model_config import DisortConfig
from biodisort.utils.get_incident_intensities import get_intensity_of_direct_beam, get_diffuse_intensity
import disort

BIODISORT_SRC_PATH = Path(__file__).resolve().parent.parent.parent
print("BIODISORT_SRC_PATH in setup_snicar.py: ", BIODISORT_SRC_PATH)
input_file = BIODISORT_SRC_PATH.joinpath("inputs.yaml").as_posix()

# first build the ice column and illumination conditions by instantiating the relevant classes from snicar
(
ice,
snicar_config,
impurities,
) = setup_snicar("default")

# validate the inputs
# validate_inputs(ice, impurities)

# now get the optical properties of the ice column
ssa_snw, g_snw, mac_snw = get_layer_OPs(ice, snicar_config)
tau, ssa, g, L_snw = mix_in_impurities(
    ssa_snw, g_snw, mac_snw, ice, impurities, snicar_config
)

# create an object to store the snicar column OPs
optical_properties = OpticalPropertiesForDisort(ssa, tau, g, L_snw) 
pf = np.zeros((128, 5)) # TODO update with real pmom calculation
disort_config = DisortConfig(input_file,snicar_config, ice, optical_properties, pf)

# set incident intensities 
disort_config.fbeam = get_intensity_of_direct_beam(disort_config) # set direct radiation
disort_config.fisot = get_diffuse_intensity(disort_config) # set diffuse radiation

# plt.plot(disort_config.fbeam)
# plt.plot(disort_config.fisot)
# plt.plot(disort_config.fbeam+disort_config.fisot)
# print(np.sum(disort_config.fbeam+disort_config.fisot))
# plt.show()


albedo_medium = np.zeros((disort_config.n_polar,))
diffuse_up_flux = np.zeros((disort_config.nbr_lyr))
diffuse_down_flux = np.zeros((disort_config.nbr_lyr))
direct_beam_flux = np.ones((disort_config.nbr_lyr,))
flux_divergence = np.zeros((disort_config.nbr_lyr,))
intensity = np.zeros((disort_config.n_polar, disort_config.nbr_lyr, 1))
mean_intensity = np.zeros((disort_config.nbr_lyr,))
transmissivity_medium = np.zeros((disort_config.n_polar,))

brdf_type = 1
brdf_arg = np.array([1, 0.6, 0.06, 0.001, 0.0001, 0.00001])
empty_bemst = np.zeros((16,))
empty_emust = np.zeros((disort_config.n_polar,))
empty_rho_accurate = np.zeros((disort_config.n_polar, 1))
empty_rhou = np.zeros((disort_config.n_streams, disort_config.n_streams//2 + 1, disort_config.n_streams))
empty_rhoq = np.zeros((disort_config.n_streams//2, disort_config.n_streams//2 + 1, disort_config.n_streams))

# do brdf
rhoq, rhou, emust, bemst, rho_accurate = disort.disobrdf(disort_config.usr_ang, disort_config.umu, disort_config.fbeam, disort_config.umu0, disort_config.lambertian, disort_config.albedo, disort_config.onlyfl, empty_rhoq, empty_rhou, empty_emust,
empty_bemst, disort_config.debug, disort_config.azimuth_angle, disort_config.phi0, empty_rho_accurate, 1, brdf_arg, disort_config.nmug, disort_config.n_streams, numu=disort_config.n_polar, nphi=disort_config.n_azimuth)

# do disort and wrangtle an output to plot
alb =[]
intensities = np.zeros(shape=(480,17,5,1))

for i in range(480):
    print("WL = ", snicar_config.wavelengths[i])
    rfldir, rfldn, flup, dfdt, uavg, uu, albedo_medium, trnmed = disort.disort(disort_config.usr_ang, 
    disort_config.usr_tau, disort_config.boundary_conditions, disort_config.onlyfl, disort_config.prnt,
    disort_config.plank, disort_config.lambertian, disort_config.deltamplus, disort_config.do_pseudo_sphere, 
    disort_config.optical_depth[:,i], disort_config.ss_alb[:,i], disort_config.pmom, 
    disort_config.temperatures, disort_config.wavenumber_low, disort_config.wavenumber_high, 
    disort_config.utau, disort_config.umu0, disort_config.phi0, disort_config.umu, disort_config.azimuth_angle,
    disort_config.fbeam[i], disort_config.fisot[i], disort_config.albedo, disort_config.btemp, disort_config.ttemp, 
    disort_config.temis, disort_config.earth_radius, disort_config.lyr_height, empty_rhoq, empty_rhou, 
    empty_rho_accurate, empty_bemst, empty_emust, disort_config.accuracy, disort_config.header, 
    direct_beam_flux, diffuse_down_flux, diffuse_up_flux, flux_divergence, mean_intensity, intensity, 
    albedo_medium, transmissivity_medium, maxcmu=disort_config.n_streams, maxulv=disort_config.nbr_lyr, maxmom=127)

    # remember each output is an array over viewing angles - for now just take the mean over angle
    # for each wavelength and bung it in an output array
    # albedo is total upwards flux divided by total downwards flux
    flup_av = np.mean(flup)
    rfldir_av= np.mean(rfldir)
    rfldn_av = np.mean(rfldn) 
    alb.append(flup_av/(rfldir_av+rfldn_av))

    intensities[i,:,:,:] = uu

for i in range(17):
    plt.plot(intensities[0:100,i,0,0], label = f"polar angle {i+1}")
plt.xlabel("wavelength")
plt.ylabel("intensity (Wm-2)")
plt.legend()
plt.show()

# plt.plot(alb)
# plt.xlabel("wavelength (um)")
# plt.ylabel("albedo")
# plt.show()
