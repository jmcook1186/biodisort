from biodisort.classes.model_config import DisortConfig
from biodisort.classes.brdf_config import BrdfConfig
import disort


def get_brdf(disort_config: DisortConfig, brdf_config: BrdfConfig):
    
    rhoq = []
    rhou = []
    emust =[]
    bemst =[]
    rho_accurate = []

    for i in range(disort_config.nbr_wvl-1):
        brdf_arg = [brdf_config.brdf_arg_b0, brdf_config.brdf_arg_h, brdf_config.brdf_arg_w[0], brdf_config.brdf_arg_asym[0],brdf_config.brdf_arg_frac, brdf_config.brdf_arg_roughness]

        rhoq_i, rhou_i, emust_i, bemst_i, rho_accurate_i = disort.disobrdf(
            disort_config.usr_ang,
            disort_config.umu,
            disort_config.fbeam,
            disort_config.umu0,
            disort_config.lambertian,
            disort_config.albedo,
            disort_config.onlyfl,
            brdf_config.rhoq[i],
            brdf_config.rhou[i],
            brdf_config.emust[i],
            brdf_config.bemst[i],
            disort_config.debug,
            disort_config.azimuth_angle,
            disort_config.phi0,
            brdf_config.rho_accurate[i],
            brdf_config.brdf_type,
            brdf_arg,
            disort_config.nmug,
            disort_config.n_streams,
            numu=disort_config.n_polar,
            nphi=disort_config.n_azimuth,
        )

        brdf_config.rhoq[i] = rhoq_i
        brdf_config.rhou[i] =rhou_i
        brdf_config.emust[i] = emust_i
        brdf_config.bemst[i] = bemst_i
        brdf_config.rho_accurate[i] = rho_accurate_i

    return brdf_config

if __name__ == "__main__":
    pass
