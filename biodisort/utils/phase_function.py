import numpy as np
import matplotlib.pyplot as plt

def hg_legendre_coefficients(g, n_coeffs):
    """
    Compute Legendre expansion coefficients for Henyey-Greenstein phase function.
    
    Parameters:
    -----------
    g : float
        Asymmetry parameter (-1 <= g <= 1)
        g > 0: forward scattering
        g = 0: isotropic scattering
        g < 0: backward scattering
    n_coeffs : int
        Number of Legendre coefficients to compute
    
    Returns:
    --------
    omega : numpy array
        Legendre coefficients [ω₀, ω₁, ω₂, ..., ω_{n-1}]
    
    Notes:
    ------
    For the Henyey-Greenstein phase function:
    ωₙ = (2n + 1) * g^n
    """
    if not -1 <= g <= 1:
        raise ValueError(f"Asymmetry parameter g must be in [-1, 1], got {g}")
    
    if n_coeffs < 1:
        raise ValueError(f"Number of coefficients must be >= 1, got {n_coeffs}")
    
    # Create array of coefficient indices
    n = np.arange(n_coeffs)
    
    # Analytical formula for HG Legendre coefficients
    # NOTE DISORT 4.0 expects to receive the legendre expansion g**n NOT (2n+1)g**n as it was in DISORT <4.0
    omega = np.power(g, n)

    return omega
