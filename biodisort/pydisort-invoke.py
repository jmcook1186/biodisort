import disort
import numpy as np
from pathlib import Path
import sys
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from biosnicar.drivers import setup_snicar
from biodisort.brdf.phase_function import construct_henyey_greenstein


# general disort config

n_streams = 32
n_polar = 5
n_azimuth = 1

# disort specific params
# illumination
azimuth_angle = 0

# params common to snicar
layer_thicknesses = np.array([0.01,0.1,0.1,0.1,0.1])
nbr_lyr = len(layer_thicknesses)
solar_zenith_angle = 45 # aka phi0
optical_depth = np.ones((layer_thicknesses.shape[0] - 1))
ss_alb = np.ones((layer_thicknesses.shape[0] - 1))

umu0 = np.cos(np.radians(solar_zenith_angle))
umu = np.cos(np.radians([80, 70, 60, 50, 40])) # cosine of emissions (viewing) angles 
print("umu", umu)

# pmom is an array of phase function Legendre coefficients
pmom = np.zeros((128, layer_thicknesses.shape[0]-1))
pmom[0] = 1

# Define output arrays

albedo_medium = np.zeros((5,))
diffuse_up_flux = np.zeros((nbr_lyr))
diffuse_down_flux = np.zeros((nbr_lyr))
direct_beam_flux = np.ones((nbr_lyr,))
flux_divergence = np.zeros((nbr_lyr,))
intensity = np.zeros((5, nbr_lyr, 1))
mean_intensity = np.zeros((nbr_lyr,))
transmissivity_medium = np.zeros((5,))

# Define miscellaneous variables
utau = np.cumsum(layer_thicknesses) # USRTAU: USeR TAU. Denote whether radiant quantities should be returned at user-specified optical depths
temperatures = [273.15, 273.15, 273.15, 273.15, 273.15]
lyr_height = np.zeros(nbr_lyr)

# Make the surface
brdf_type = 1
brdf_arg = np.array([1, 0.6, 0.06, 0.001, 0.0001, 0.00001])
empty_bemst = np.zeros((16,))
empty_emust = np.zeros((5,))
empty_rho_accurate = np.zeros((5, 1))
empty_rhou = np.zeros((n_streams, n_streams//2 + 1, n_streams))
empty_rhoq = np.zeros((n_streams//2, n_streams//2 + 1, n_streams))

usr_ang = True
usr_tau = True
ibcnd = False
onlyfl = False
prnt= [True, True, True, True, True]
plank= False
lamber = True
deltamplus= True
do_pseudo_sphere= False
wvnmlo = 0.002
wvnhi = 0.002
phi0 = 0 # azimuth angle of incident beam
fbeam = 1 # beam flux at the top boundary
fisot = 1 # isotropic flux at the top boundary
albedo = 0.8
btemp = 273.15
ttemp = 273.15
temis = 1
earth_radius= 3400000
accur = 0.001
header = ''
debug = True
nmug = 6

rhoq, rhou, emust, bemst, rho_accurate = disort.disobrdf(usr_ang, umu, fbeam, umu0, lamber, albedo, onlyfl, empty_rhoq, empty_rhou, empty_emust,
empty_bemst, debug, azimuth_angle, phi0, empty_rho_accurate, brdf_type, brdf_arg, nmug, nstr=n_streams, numu=n_polar, nphi=n_azimuth)

pf = construct_henyey_greenstein([0.5,0.5,0.5,0.5,0.5],np.linspace(0, 180, num=5))*4*np.pi
print(pf)

# note optical depth is dtau
rfldir, rfldn, flup, dfdt, uavg, uu, albedo_medium, trnmed = disort.disort(usr_ang, usr_tau, ibcnd, onlyfl, prnt,
plank, lamber, deltamplus, do_pseudo_sphere, optical_depth, ss_alb, pmom, temperatures, wvnmlo, wvnhi, utau, umu0, phi0,
umu, azimuth_angle, fbeam, fisot, albedo, btemp, ttemp, temis, earth_radius, lyr_height, rhoq, rhou, rho_accurate, bemst, 
emust, accur, header, direct_beam_flux, diffuse_down_flux, diffuse_up_flux, flux_divergence, mean_intensity, intensity, 
albedo_medium, transmissivity_medium, maxcmu=n_streams, maxulv=nbr_lyr, maxmom=127)


print(uu)
