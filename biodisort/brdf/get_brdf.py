from biodisort.classes.model_config import DisortConfig
from biodisort.classes.brdf_config import BrdfConfig
import disort


def get_brdf(disort_config: DisortConfig, brdf_config: BrdfConfig):

    rhoq, rhou, emust, bemst, rho_accurate = disort.disobrdf(
        disort_config.usr_ang,
        disort_config.umu,
        disort_config.fbeam,
        disort_config.umu0,
        disort_config.lambertian,
        disort_config.albedo,
        disort_config.onlyfl,
        brdf_config.empty_rhoq,
        brdf_config.empty_rhou,
        brdf_config.empty_emust,
        brdf_config.empty_bemst,
        disort_config.debug,
        disort_config.azimuth_angle,
        disort_config.phi0,
        brdf_config.empty_rho_accurate,
        brdf_config.brdf_type,
        brdf_config.brdf_arg,
        disort_config.nmug,
        disort_config.n_streams,
        numu=disort_config.n_polar,
        nphi=disort_config.n_azimuth,
    )

    return rhoq, rhou, emust, bemst, rho_accurate

if __name__ == "__main__":
    pass
