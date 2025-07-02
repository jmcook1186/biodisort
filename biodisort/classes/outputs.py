import numpy as np
from biodisort.classes.model_config import DisortConfig


class DisortOutputs:
    """Disort mdoel outputs.

    Attributes:

    """

    def __init__(self, model_config: DisortConfig):
        self.bba = 0.0
        self.intensities = np.zeros(
            shape=(
                model_config.nbr_wvl,
                len(model_config.emission_angles),
                model_config.nbr_lyr,
                1,
            )
        )
        self.spectral_albedo = np.zeros(shape=(model_config.nbr_wvl))
