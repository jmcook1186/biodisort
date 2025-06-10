import numpy as np

def construct_henyey_greenstein(g, scattering_angles):
    r"""Construct a Henyey-Greenstein phase function.

    Parameters
    ----------
    asymmetry_parameter: float
        The Henyey-Greenstein asymmetry parameter. Must be between -1 and 1.
    scattering_angles: ArrayLike
        1-dimensional array of scattering angles [degrees].

    Returns
    -------
    np.ndarray
        1-dimensiona phase function corresponding to each value in
        ``scattering_angles``.

    Notes
    -----
    The Henyey-Greenstein phase function (per solid angle) is defined as

    .. math::

       p(\theta) = \frac{1}{4\pi} \frac{1 - g^2}
                    {[1 + g^2 - 2g \cos(\theta)]^\frac{3}{2}}

    where :math:`p` is the phase function, :math:`\theta` is the scattering
    angle, and :math:`g` is the asymemtry parameter.

    .. warning::
       The normalization for the Henyey-Greenstein phase function is not the
       same as for a regular phase function. For this phase function,

       .. math::
          \int_{4\pi} p(\theta) = 1

       *not* 4 :math:`\pi`! To normalize it simply multiply the output by
       4 :math:`\pi`.

    Examples
    --------
    Construct a Henyey-Greenstein phase function.

    """
    scattering_angles = np.asarray(scattering_angles)
    asymmetry_parameter = np.asarray(g)
    denominator = (1 + asymmetry_parameter ** 2 -
        2 * asymmetry_parameter *
        np.cos(np.radians(scattering_angles))) ** (3 / 2)
    return 1 / (4 * np.pi) * (1 - asymmetry_parameter ** 2) / denominator
