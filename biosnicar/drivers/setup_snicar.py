#!/usr/bin/python

import yaml
from pathlib import Path

from biosnicar.classes import (
    Ice,
    Impurity,
    ModelConfig,
)


def setup_snicar(input_file):
    """Builds impurity array and instances of all classes according to config in yaml file.

    Args:
        None

    Returns:
        ice: instance of Ice class
        model_config: instance of ModelConfig class


    """
    # define input file
    if input_file == "default":
        BIODISORT_SRC_PATH = Path(__file__).resolve().parent.parent
        input_file = BIODISORT_SRC_PATH.joinpath("../inputs.yaml").as_posix()

    else:
        input_file = input_file

    impurities = build_impurities_array(input_file)
    (
        ice,
        model_config,
    ) = build_classes(input_file)

    return (
        ice,
        model_config,
        impurities,
    )


def build_classes(input_file):
    """Instantiates classes according to config in yaml file.

    Args:
        None

    Returns:
        ice: instance of Ice class
        illumination: instance of Illumination class
        rt_config: instance of RTConfig class
        model_config: instance of ModelConfig class
        plot_config: instance of PlotConfig class
        display_config: instance of DisplayConfig class
    """

    ice = Ice(input_file)
    model_config = ModelConfig(input_file)

    return ice, model_config


def build_impurities_array(input_file):
    """Creates an array of instances of Impurity.

    creates an array of impurities - each one an instance of Impurity with
    properties defined in yaml file.

    Args:
        None

    Returns:
        impurities: array of instances of Impurity
    """

    with open(input_file, "r") as ymlfile:
        inputs = yaml.load(ymlfile, Loader=yaml.FullLoader)

    impurities = []

    for i, id in enumerate(inputs["IMPURITIES"]):
        name = inputs["IMPURITIES"][id]["NAME"]
        file = inputs["IMPURITIES"][id]["FILE"]
        coated = inputs["IMPURITIES"][id]["COATED"]
        unit = inputs["IMPURITIES"][id]["UNIT"]
        conc = inputs["IMPURITIES"][id]["CONC"]
        snicar_path = inputs["PATHS"]["SNICAR_BASE_PATH"]
        impurities.append(Impurity(file, coated, unit, name, conc, snicar_path))

    return impurities

    print("SETUP OK")


if __name__ == "__main__":
    pass
