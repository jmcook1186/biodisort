import numpy as np
import yaml

class BrdfConfig:
    """Disort mdoel outputs.

    Attributes:

    """

    def __init__(self,input_file):
        with open(input_file, "r") as ymlfile:
            inputs = yaml.load(ymlfile, Loader=yaml.FullLoader)
        
        self.brdf_type= inputs["DISORT"]["BRDF"]["BRDF_TYPE"]
