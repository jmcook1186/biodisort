
def set_disort_params(ice, illumination, snicar_config):

    

    # general disort config
    n_streams = 32
    n_polar = 5
    n_azimuth = 1

    # disort specific params
    # illumination
    azimuth = 0

    # params common to snicar
    layer_thicknesses = np.array([0.01,0.1,0.1,0.1,0.1])
    n_layers = len(layer_thicknesses)
    solar_zenith_angle = 45 # aka phi0
    optical_depth = np.ones((layer_thicknesses.shape[0] - 1))
    ss_alb = np.ones((layer_thicknesses.shape[0] - 1))

    umu0 = 0.57 #cosine of solar zenith angle
    umu = [0.1, 0.2, 0.3, 0.4, 0.5] # cosine of emissions (viewing) angles 
    print(umu)

    # pmom is an array of phase function Legendre coefficients
    pmom = np.zeros((128, layer_thicknesses.shape[0]-1))
    pmom[0] = 1

    # Define output arrays

    albedo_medium = np.zeros((5,))
    diffuse_up_flux = np.zeros((n_layers,))
    diffuse_down_flux = np.zeros((n_layers,))
    direct_beam_flux = np.zeros((n_layers,))
    flux_divergence = np.zeros((n_layers,))
    intensity = np.zeros((5, n_layers, 1))
    mean_intensity = np.zeros((n_layers,))
    transmissivity_medium = np.zeros((5,))

    # Define miscellaneous variables
    user_od_output = [0, 0.05, 0.1, 0.2, 0.5]
    temper = np.zeros(n_layers)
    h_lyr = np.zeros(n_layers)

    # Make the surface
    brdf_arg = np.array([1, 0.06, 0.7, 0.26, 0.3, 1])
    empty_bemst = np.zeros((16,))
    empty_emust = np.zeros((5,))
    empty_rho_accurate = np.zeros((5, 1))
    empty_rhou = np.zeros((n_streams, n_streams//2 + 1, n_streams))
    empty_rhoq = np.zeros((n_streams//2, n_streams//2 + 1, n_streams))

    usr_ang = True
    usr_tau = True
    ibcnd = False
    onlyfl = False
    prnt= [True, True, True, False, False]
    plank= False
    lamber = True
    deltamplus= True
    do_pseudo_sphere= False
    wvnmlo = 1
    wvnhi = 1
    phi0 = 0
    fbeam = np.pi
    fisot = 0
    albedo = 0.1
    btemp = 0
    ttemp = 0
    temis = 1
    earth_radius= 3400000
    accur = 0
    header = ''
    dTau = 1
    debug = False
    brdf_type = 5
    nmug = 6


    return disort_params
