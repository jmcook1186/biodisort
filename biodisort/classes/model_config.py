import os
import numpy as np
import yaml
import biosnicar

class DisortConfig:
    """Model configuration.

    Attributes:


    """

    def __init__(self, input_file, ice, illumination, optical_properties_for_disort, phase_function):
        with open(input_file, "r") as ymlfile:
            inputs = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.n_streams = inputs["DISORT"]["CONFIG"]["N_STREAMS"]
        self.n_polar = inputs["DISORT"]["CONFIG"]["N_POLAR"]
        self.n_azimuth = inputs["DISORT"]["CONFIG"]["N_AZIMUTH"]
        self.azimuth_angle = inputs["DISORT"]["ORIENTATION"]["AZIMUTH_ANGLE"]
        self.emission_angles = inputs["DISORT"]["ORIENTATION"]["EMISSION_ANGLES"]
        self.layer_thicknesses = ice.layer_thicknesses
        self.nbr_lyr= ice.nbr_lyr
        self.solar_zenith_angle = illumination.solzen
        self.optical_depth = optical_properties_for_disort.tau
        self.ss_alb= optical_properties_for_disort.ssa
        self.umu0 = np.cos(np.radians(self.solar_zenith_angle))
        self.umu = np.cos(np.radians(self.emission_angles))
        self.pmom = phase_function
        self.temperatures = inputs["DISORT"]["ICE"]["TEMPERATURES"] # array of temperatures, in K, for each ice layer - default to melting point
        self.lyr_height = np.zeros(self.nbr_lyr)  # array of layer heights (m absl) - we assume plane parallel setup so set to zero
        self.umu = inputs["DISORT"]["CONFIG"]["VIEWING_ANGLES"] #  the cosines must be in descending order
        self.n_umu = len(self.umu)
        self.pmom = phase_function
        self.utau = np.cumsum(self.layer_thicknesses)
        self.boundary_conditions = inputs["DISORT"]["CONFIG"]["BOUNDARY_CONDITIONS"]
        self.phi0 = inputs["DISORT"]["CONFIG"]["PHI0"] # azimuth angle of incident beam
        self.wavenumber_high = np.array(10 ** 4 / snicar_config.wavelengths[-1])
        self.wavenumber_low = np.array(10 ** 4 / snicar_config.wavelengths[0])
