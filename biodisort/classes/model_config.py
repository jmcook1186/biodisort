import os
import numpy as np
import yaml
import biosnicar

class DisortConfig:
    """Model configuration.

    Attributes:


    """

    def __init__(self, input_file):
        with open(input_file, "r") as ymlfile:
            inputs = yaml.load(ymlfile, Loader=yaml.FullLoader)
