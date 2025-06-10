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

import disort

(
ice,
illumination,
rt_config,
snicar_config,
plot_config,
impurities,
) = setup_snicar("default")

validate_inputs(ice, illumination, impurities)

# now get the optical properties of the ice column
ssa_snw, g_snw, mac_snw = get_layer_OPs(ice, snicar_config)
tau, ssa, g, L_snw = mix_in_impurities(
    ssa_snw, g_snw, mac_snw, ice, impurities, snicar_config
)

optical_properties = OpticalPropertiesForDisort(ssa, tau, g, L_snw) 

#TODO validate snicar and disort params are consistent

print(optical_properties.tau[0][0])


def set_disort_params(ice, illumination, snicar_config):

    # general disort config

    n_streams = 32
    n_polar = 5
    n_azimuth = 1

    # disort specific params
    # illumination
    azimuth = 0

    # params common to snicar
    layer_thicknesses = np.array([0.01,0.1,0.1,0.1,0.1])
    n_layers = len(layer_thicknesses)
    solar_zenith_angle = 45 # aka phi0
    optical_depth = np.ones((layer_thicknesses.shape[0] - 1))
    ss_alb = np.ones((layer_thicknesses.shape[0] - 1))

    umu0 = 0.57 #cosine of solar zenith angle
    umu = [0.1, 0.2, 0.3, 0.4, 0.5] # cosine of emissions (viewing) angles 
    print(umu)

    # pmom is an array of phase function Legendre coefficients
    pmom = np.zeros((128, layer_thicknesses.shape[0]-1))
    pmom[0] = 1

    # Define output arrays

    albedo_medium = np.zeros((5,))
    diffuse_up_flux = np.zeros((n_layers,))
    diffuse_down_flux = np.zeros((n_layers,))
    direct_beam_flux = np.zeros((n_layers,))
    flux_divergence = np.zeros((n_layers,))
    intensity = np.zeros((5, n_layers, 1))
    mean_intensity = np.zeros((n_layers,))
    transmissivity_medium = np.zeros((5,))

    # Define miscellaneous variables
    user_od_output = [0, 0.05, 0.1, 0.2, 0.5]
    temper = np.zeros(n_layers)
    h_lyr = np.zeros(n_layers)

    # Make the surface
    brdf_arg = np.array([1, 0.06, 0.7, 0.26, 0.3, 1])
    empty_bemst = np.zeros((16,))
    empty_emust = np.zeros((5,))
    empty_rho_accurate = np.zeros((5, 1))
    empty_rhou = np.zeros((n_streams, n_streams//2 + 1, n_streams))
    empty_rhoq = np.zeros((n_streams//2, n_streams//2 + 1, n_streams))

    usr_ang = True
    usr_tau = True
    ibcnd = False
    onlyfl = False
    prnt= [True, True, True, False, False]
    plank= False
    lamber = True
    deltamplus= True
    do_pseudo_sphere= False
    wvnmlo = 1
    wvnhi = 1
    phi0 = 0
    fbeam = np.pi
    fisot = 0
    albedo = 0.1
    btemp = 0
    ttemp = 0
    temis = 1
    earth_radius= 3400000
    accur = 0
    header = ''
    dTau = 1
    debug = False
    brdf_type = 5
    nmug = 6


    return disort_params



# now do disort
def construct_henyey_greenstein(gg, phi0):
    r"""Construct a Henyey-Greenstein phase function.

    Parameters
    ----------
    asymmetry_parameter: float
        The Henyey-Greenstein asymmetry parameter. Must be between -1 and 1.
    scattering_angles: ArrayLike
        1-dimensional array of scattering angles [degrees].

    Returns
    -------
    np.ndarray
        1-dimensiona phase function corresponding to each value in
        ``scattering_angles``.

    Notes
    -----
    The Henyey-Greenstein phase function (per solid angle) is defined as

    .. math::

       p(\theta) = \frac{1}{4\pi} \frac{1 - g^2}
                    {[1 + g^2 - 2g \cos(\theta)]^\frac{3}{2}}

    where :math:`p` is the phase function, :math:`\theta` is the scattering
    angle, and :math:`g` is the asymemtry parameter.

    .. warning::
       The normalization for the Henyey-Greenstein phase function is not the
       same as for a regular phase function. For this phase function,

       .. math::
          \int_{4\pi} p(\theta) = 1

       *not* 4 :math:`\pi`! To normalize it simply multiply the output by
       4 :math:`\pi`.

    Examples
    --------
    Construct a Henyey-Greenstein phase function.

    >>> import numpy as np
    >>> import pyrt
    >>> scattering_angles = np.arange(181)
    >>> g = 0.5
    >>> hg_pf = pyrt.construct_henyey_greenstein(g, scattering_angles)
    >>> hg_pf.shape
    (181,)

    """
    scattering_angles = np.asarray(phi0)
    asymmetry_parameter = np.asarray(gg)
    denominator = (1 + asymmetry_parameter ** 2 -
        2 * asymmetry_parameter *
        np.cos(np.radians(scattering_angles))) ** (3 / 2)
    return 1 / (4 * np.pi) * (1 - asymmetry_parameter ** 2) / denominator

# general disort config

n_streams = 32
n_polar = 5
n_azimuth = 1

# disort specific params
# illumination
azimuth = 0

# params common to snicar
layer_thicknesses = np.array([0.01,0.1,0.1,0.1,0.1])
n_layers = len(layer_thicknesses)
solar_zenith_angle = illumination.solzen # aka phi0
optical_depth = [tau[0][50],tau[0][50],tau[0][50],tau[0][50]]
ss_alb = [ssa[0][50],ssa[0][50],ssa[0][50],ssa[0][50]]

umu0 = 0.57 #cosine of solar zenith angle
umu = [0.1, 0.2, 0.3, 0.4, 0.5] # cosine of emissions (viewing) angles 
print(umu)

# pmom is an array of phase function Legendre coefficients
pmom = np.zeros((128, layer_thicknesses.shape[0]-1))
pmom[0] = 1

# Define output arrays

albedo_medium = np.zeros((5,))
diffuse_up_flux = np.zeros((n_layers,))
diffuse_down_flux = np.ones((n_layers,))
direct_beam_flux = np.ones((n_layers,))
flux_divergence = np.zeros((n_layers,))
intensity = np.zeros((5, n_layers, 1))
mean_intensity = np.zeros((n_layers,))
transmissivity_medium = np.zeros((5,))

# Define miscellaneous variables
user_od_output = [0, 0.05, 0.1, 0.2, 0.5]
temper = np.zeros(n_layers)
h_lyr = np.zeros(n_layers)

# Make the surface
brdf_arg = np.array([1, 0.06, 0.7, 0.26, 0.3, 1])
empty_bemst = np.zeros((16,))
empty_emust = np.zeros((5,))
empty_rho_accurate = np.zeros((5, 1))
empty_rhou = np.zeros((n_streams, n_streams//2 + 1, n_streams))
empty_rhoq = np.zeros((n_streams//2, n_streams//2 + 1, n_streams))

usr_ang = True
usr_tau = True
ibcnd = False
onlyfl = False
prnt= [False, False, False, False, False]
plank= False
lamber = True
deltamplus= True
do_pseudo_sphere= False
wvnmlo = 1
wvnhi = 1
phi0 = 0
fbeam = np.pi
fisot = 0
albedo = 0.1
btemp = 0
ttemp = 0
temis = 1
earth_radius= 3400000
accur = 0
header = ''
dTau = 1
debug = False
brdf_type = 5
nmug = 6

rhoq, rhou, emust, bemst, rho_accurate = disort.disobrdf(usr_ang, umu, fbeam, umu0, lamber, albedo, onlyfl, empty_rhoq, empty_rhou, empty_emust,
empty_bemst, debug, azimuth, phi0, empty_rho_accurate, brdf_type, brdf_arg, nmug, nstr=n_streams, numu=n_polar, nphi=n_azimuth)

pf = construct_henyey_greenstein([0.5,0.5,0.5,0.5,0.5],np.linspace(0, 180, num=5))*4*np.pi
print(pf)
# note optical depth is dtau

rfldir, rfldn, flup, dfdt, uavg, uu, albedo_medium, trnmed = disort.disort(usr_ang, usr_tau, ibcnd, onlyfl, prnt,
plank, lamber, deltamplus, do_pseudo_sphere, optical_depth, ss_alb, pmom, temper, wvnmlo, wvnhi, user_od_output, umu0, phi0,
umu, azimuth, np.pi, fisot, albedo, btemp, ttemp, temis, earth_radius, h_lyr, rhoq, rhou, rho_accurate, bemst, emust, accur, header, direct_beam_flux,
diffuse_down_flux, diffuse_up_flux, flux_divergence, mean_intensity, intensity, albedo_medium, transmissivity_medium, maxcmu=n_streams, maxulv=n_layers, maxmom=127)


plt.plot(rfldir)
plt.show()
