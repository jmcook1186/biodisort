import os
import numpy as np
import yaml
import biosnicar

class DisortConfig:
    """Model configuration.

    Attributes:


    """

    def __init__(self, input_file, snicar_config, ice, optical_properties_for_disort, phase_function):
        with open(input_file, "r") as ymlfile:
            inputs = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.n_streams = inputs["DISORT"]["CONFIG"]["N_STREAMS"]
        self.n_azimuth = inputs["DISORT"]["CONFIG"]["N_AZIMUTH"]
        self.azimuth_angle = inputs["DISORT"]["ORIENTATION"]["AZIMUTH_ANGLE"]
        self.emission_angles = inputs["DISORT"]["ORIENTATION"]["EMISSION_ANGLES"]
        self.n_polar = len(self.emission_angles)
        self.direct = inputs["ILLUMINATION"]["DIRECT"]
        self.diffuse = inputs["ILLUMINATION"]["DIFFUSE"]
        self.season = inputs["ILLUMINATION"]["SEASON"]
        self.region = inputs["ILLUMINATION"]["REGION"]
        self.layer_thicknesses = ice.dz
        self.nbr_wvl = snicar_config.nbr_wvl
        self.nbr_lyr= ice.nbr_lyr
        self.solar_zenith_angle = inputs["ILLUMINATION"]["SOLZEN"]
        self.optical_depth = optical_properties_for_disort.tau
        self.ss_alb= optical_properties_for_disort.ssa
        self.umu0 = np.cos(np.radians(self.solar_zenith_angle))
        self.umu = np.cos(np.radians(self.emission_angles))
        self.pmom = phase_function
        self.temperatures = inputs["DISORT"]["ICE"]["TEMPERATURES"] # array of temperatures, in K, for each ice layer - default to melting point
        self.lyr_height = np.zeros(self.nbr_lyr+1)  # array of layer heights (m absl) - we assume plane parallel setup so set to zero
        self.umu = np.cos(np.radians(self.emission_angles)) #  the cosines must be in descending order
        self.n_umu = len(self.umu)
        self.pmom = phase_function
        self.utau = np.cumsum(self.layer_thicknesses)
        self.boundary_conditions = inputs["DISORT"]["CONFIG"]["BOUNDARY_CONDITIONS"] # IBCND
        self.phi0 = inputs["DISORT"]["CONFIG"]["PHI0"] # azimuth angle of incident beam
        self.wavenumber_high = 0.0004
        self.wavenumber_low = 0.004878
        self.usr_ang = inputs["DISORT"]["CONFIG"]["USR_ANG"]
        self.usr_tau = inputs["DISORT"]["CONFIG"]["USR_TAU"]
        self.onlyfl = inputs["DISORT"]["CONFIG"]["ONLYFL"]
        self.prnt = inputs["DISORT"]["CONFIG"]["PRNT"]
        self.plank = inputs["DISORT"]["CONFIG"]["PLANK"]
        self.lambertian = inputs["DISORT"]["CONFIG"]["LAMBERTIAN"]
        self.deltamplus = inputs["DISORT"]["CONFIG"]["DELTAMPLUS"]
        self.do_pseudo_sphere = inputs["DISORT"]["CONFIG"]["DO_PSEUDO_SPHERE"]
        self.fisot = inputs["DISORT"]["CONFIG"]["FISOT"] # Intensity of top-boundary isotropic illumination.
        self.fbeam = inputs["DISORT"]["CONFIG"]["FBEAM"]
        self.albedo = inputs["DISORT"]["CONFIG"]["ALBEDO"] # albedo of bottom surface
        self.btemp = inputs["DISORT"]["CONFIG"]["BTEMP"]
        self.ttemp = inputs["DISORT"]["CONFIG"]["TTEMP"]
        self.temis = inputs["DISORT"]["CONFIG"]["TEMIS"]
        self.earth_radius = inputs["DISORT"]["CONFIG"]["EARTH_RADIUS"]
        self.accuracy = inputs["DISORT"]["CONFIG"]["ACCURACY"]
        self.header = inputs["DISORT"]["CONFIG"]["HEADER"]
        self.debug = inputs["DISORT"]["CONFIG"]["DEBUG"]
        self.nmug = inputs["DISORT"]["CONFIG"]["NMUG"]
        self.rhoq = inputs["DISORT"]["CONFIG"]["RHOQ"]
        self.rhou = inputs["DISORT"]["CONFIG"]["RHOU"]
        self.emust = inputs["DISORT"]["CONFIG"]["EMUST"]
        self.bemst = inputs["DISORT"]["CONFIG"]["BEMST"]
        self.rho_accurate = inputs["DISORT"]["CONFIG"]["RHO_ACCURATE"]
