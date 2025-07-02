from biodisort.classes.outputs import DisortOutputs
from biodisort.classes.model_config import DisortConfig
from biodisort.classes.brdf_config import BrdfConfig
import disort
import numpy as np

def run_disort(disort_config: DisortConfig, brdf_config: BrdfConfig)-> DisortOutputs:

    # set up empty arrays requires as disort inputs
    albedo_medium = np.zeros((disort_config.n_polar,))
    diffuse_up_flux = np.zeros((disort_config.nbr_lyr))
    diffuse_down_flux = np.zeros((disort_config.nbr_lyr))
    direct_beam_flux = np.ones((disort_config.nbr_lyr,))
    flux_divergence = np.zeros((disort_config.nbr_lyr,))
    intensity = np.zeros((disort_config.n_polar, disort_config.nbr_lyr, 1))
    mean_intensity = np.zeros((disort_config.nbr_lyr,))
    transmissivity_medium = np.zeros((disort_config.n_polar,))

    # create output object
    outputs = DisortOutputs(disort_config)

    for i in range(480):
        rfldir, rfldn, flup, dfdt, uavg, uu, albedo_medium, trnmed = disort.disort(
            disort_config.usr_ang,
            disort_config.usr_tau,
            disort_config.boundary_conditions,
            disort_config.onlyfl,
            disort_config.prnt,
            disort_config.plank,
            disort_config.lambertian,
            disort_config.deltamplus,
            disort_config.do_pseudo_sphere,
            disort_config.optical_depth[:, i],
            disort_config.ss_alb[:, i],
            disort_config.pmom,
            disort_config.temperatures,
            disort_config.wavenumber_low,
            disort_config.wavenumber_high,
            disort_config.utau,
            disort_config.umu0,
            disort_config.phi0,
            disort_config.umu,
            disort_config.azimuth_angle,
            disort_config.fbeam[i],
            disort_config.fisot[i],
            disort_config.albedo,
            disort_config.btemp,
            disort_config.ttemp,
            disort_config.temis,
            disort_config.earth_radius,
            disort_config.lyr_height,
            brdf_config.rhoq[i],
            brdf_config.rhou[i],
            brdf_config.rho_accurate[i],
            brdf_config.bemst[i],
            brdf_config.emust[i],
            disort_config.accuracy,
            disort_config.header,
            direct_beam_flux,
            diffuse_down_flux,
            diffuse_up_flux,
            flux_divergence,
            mean_intensity,
            intensity,
            albedo_medium,
            transmissivity_medium,
            maxcmu=disort_config.n_streams,
            maxulv=disort_config.nbr_lyr,
            maxmom=127,
        )

        # remember each output is an array over viewing angles - for now just take the mean over angle
        # for each wavelength and bung it in an output array
        # calculate hemispheric means
        flup_av = np.mean(flup)
        rfldir_av = np.mean(rfldir)
        rfldn_av = np.mean(rfldn)

        # albedo is total upwards flux divided by total downwards flux
        outputs.spectral_albedo[i] = flup_av / (rfldir_av + rfldn_av)
        # intensities come in the form intensities[wvl, emission-angle, lyr, value]
        outputs.intensities[i, :, :, :] = uu
    
    return outputs
