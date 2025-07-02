import numpy as np
import yaml
from biodisort.classes.optical_properties_for_disort import OpticalPropertiesForDisort
from biodisort.classes.model_config import DisortConfig
class BrdfConfig:
    """Disort mdoel outputs.

    Attributes:

    """

    def __init__(self, input_file, disort_config: DisortConfig, optical_properties: OpticalPropertiesForDisort):
        
        with open(input_file, "r") as ymlfile:
            inputs = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.brdf_type= inputs["DISORT"]["BRDF"]["BRDF_TYPE"]
        self.brdf_arg_b0 = inputs["DISORT"]["BRDF"]["B0"]
        self.brdf_arg_h = inputs["DISORT"]["BRDF"]["H"]
        self.brdf_arg_w = optical_properties.ssa[0]
        self.brdf_arg_asym = optical_properties.g[0]
        self.brdf_arg_frac = inputs["DISORT"]["BRDF"]["FRAC"]
        self.brdf_arg_roughness = inputs["DISORT"]["BRDF"]["ROUGHNESS"]

        self.bemst = np.zeros((disort_config.nbr_wvl,16,))
        self.emust = np.zeros((disort_config.nbr_wvl,disort_config.n_polar,))
        self.rho_accurate = np.zeros((disort_config.nbr_wvl,disort_config.n_polar, 1))
        self.rhou = np.zeros((disort_config.nbr_wvl,disort_config.n_streams, disort_config.n_streams//2 + 1, disort_config.n_streams))
        self.rhoq = np.zeros((disort_config.nbr_wvl,disort_config.n_streams//2, disort_config.n_streams//2 + 1, disort_config.n_streams))

        

        def zero_arrays(self):
            """
            Sets arrays for brdf functions back to zero.
            Calling this ensures zero arrays are passed to disort brdf functions
            """
            self.bemst = np.zeros(disort_config.nbr_wvl,(16,))
            self.emust = np.zeros((disort_config.nbr_wvl,disort_config.n_polar,))
            self.rho_accurate = np.zeros((disort_config.nbr_wvl,disort_config.n_polar, 1))
            self.rhou = np.zeros((disort_config.nbr_wvl,disort_config.n_streams, disort_config.n_streams//2 + 1, disort_config.n_streams))
            self.rhoq = np.zeros((disort_config.nbr_wvl,disort_config.n_streams//2, disort_config.n_streams//2 + 1, disort_config.n_streams))
            
            return
