from biodisort.classes.optical_properties_for_disort import OpticalPropertiesForDisort
from biosnicar.optical_properties.column_OPs import get_layer_OPs, mix_in_impurities
from biosnicar.drivers.setup_snicar import setup_snicar

def get_column_ops()-> OpticalPropertiesForDisort:
    # first build the ice column and illumination conditions by instantiating the relevant classes from snicar
    (
        ice,
        snicar_config,
        impurities,
    ) = setup_snicar("default")

    # now get the optical properties of the ice column
    ssa_snw, g_snw, mac_snw = get_layer_OPs(ice, snicar_config)
    tau, ssa, g, L_snw = mix_in_impurities(
        ssa_snw, g_snw, mac_snw, ice, impurities, snicar_config
    )

    # create an object to store the snicar column OPs
    optical_properties = OpticalPropertiesForDisort(ssa, tau, g, L_snw)
    return optical_properties, snicar_config, ice
