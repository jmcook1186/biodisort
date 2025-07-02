import numpy as np
import yaml

class BrdfConfig:
    """Disort mdoel outputs.

    Attributes:

    """

    def __init__(self,input_file, disort_config):
        with open(input_file, "r") as ymlfile:
            inputs = yaml.load(ymlfile, Loader=yaml.FullLoader)
        
        self.brdf_type= inputs["DISORT"]["BRDF"]["BRDF_TYPE"]
        self.brdf_arg = inputs["DISORT"]["BRDF"]["BRDF_ARG"]
        self.bemst = np.zeros((16,))
        self.emust = np.zeros((disort_config.n_polar,))
        self.rho_accurate = np.zeros((disort_config.n_polar, 1))
        self.rhou = np.zeros((disort_config.n_streams, disort_config.n_streams//2 + 1, disort_config.n_streams))
        self.rhoq = np.zeros((disort_config.n_streams//2, disort_config.n_streams//2 + 1, disort_config.n_streams))
