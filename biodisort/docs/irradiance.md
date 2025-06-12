# Irradiance in bioDISORT

DISORT (Discrete Ordinates Radiative Transfer) is a powerful model used to solve the radiative transfer equation in plane-parallel media, such as the Earth's atmosphere. One of the key outputs of DISORT is the surface irradiance, which is the amount of radiation reaching the Earth's surface. However, `biodisort` is primarily concerned with the radiative transfer in a column of ice sitting at the bottom of the atmosphere. This means we do not want all the calculations to begin with the solar constant - we want our unattenuated irradiance to be the bottom of atmosphere, or surface, irradiance. Therefore, we have to do a little adjusting of DISORT's config. We use the database of at-surface irradiance intensities from the `biosnicar` model (which themselves were precalculated using vanilla DISORT). We can prescribe a broad region (mid-latitude, polar) and season (summer, winter) and a solar zenith angle and then look up spectral at-surface irradiance intensities to pass to DISORT. This page will explain that process, clarify the variables used and the flow of information through `biodisort`.

Note that with the current set of irradiance flux files, it is strongly recommended to use EITHER direct (i.e. black sky/ direct only) or diffuse (i.e. white sky / diffuse only) and avoid adding a beam to a diffuse background. This is because the fluxes in the files assume this, and sum over wavelength to yield to ~700-800 W/m2 total broadband flux. Therefore, including both gives an unrealistic total flux (twice the expected surface flux, often exceeding the total TOA solar flux). There are several possible workarounds for this:

- use your own files for the diffuse and direct irradiance intensity derived from field measurements or atmospheric RT modelling
- use the `flx_frc_` variables in our irradiance files - these are the spectral *proportions* of the total flux contributed by each wavelength and multiply element-wise with a constant representing the total broadband diffuse and/or direct flux. This way you can have a sensible spectral distribution AND a sensible total broadband flux.

We haven't done much to support these workarounds yet - we will eventually - so there'll be some fiddlign required with the code (great first issues for someone!).

## Key Variables

### FBEAM
- **Definition**: `FBEAM` is the intensity of the direct beam.
- **Values**: The spectral irradiance intensity values are loaded in from an external file stored in the `biosnicar` database.
- **Role**: This flag toggles the model loading in a black-sky irradiance file as an irradiance component.

### FISOT
- **Definition**: `FISOT` represents the isotropic (diffuse) radiation flux at the surface. When `FISOT` is set, DISORT assumes that there is a uniform, diffuse radiation field incident from all directions above the atmosphere.
- **Values**: This is a scalar value representing the intensity of the isotropic radiation.
- **Role**: This variable sets the magnitude of the incoming diffuse radiation, which is then modulated by the optical properties of the atmosphere.

### UMU0 and PHI0
- **UMU0**: Cosine of the solar zenith angle, specifying the direction of the incoming solar beam.
- **PHI0**: Azimuth angle of the sun, measured from the positive x-axis (usually north).
- **Role**: These variables fully specify the direction and angle of the incoming solar radiation.

### SOLZEN
- **Definition**: `SOLZEN` is the solar zenith angle, in degrees.
- **Values**: 1-89. 0 is directly overhead, 90 is parallel with the horizon (both illegal values).
- **Role**: This is used to derive `UMU0`

### SEASON
- **Definition**: Season/region/solzen is used to determine at surface irradiance. Depending on the region/season/solzen combination a different irradiance file is loaded in and used to define `FISOT` and/or `FBEAM`.
- **Values**: "s", "w"
- **Role**: `SEASON` tells biodisort to grab files for summer or winter irradiance for a given region. These form the file stubs for reading in appropriate irradiance files.
  
### REGION
- **Definition**: Season/region/solzen is used to determine at surface irradiance. Depending on the region/season/solzen combinationa  different irradiance file is loaded in and used to configure `FISOT` and/or `FBEAM`.
- **Values**: "ml", "p" 
- **Role**: `REGION` tells biodisort to grab files for summer or winter irradiance for a given region. These form the file stubs for reading in appropriate irradiance files.


## Example: Isotropic Incident Radiation

When `FBEAM = 0` and the incident radiation is isotropic, the intensity arriving at the surface is uniform in all directions. The intensity \( I \) is given by:
\[ I = \frac{FISOT}{\pi} \]
where \( FISOT \) is the isotropic radiation flux.

### Discrete Ordinate Method with Isotropic Radiation

1. **Intensity at Each Angle**:
   - For isotropic radiation, the intensity \( I \) at the top of the atmosphere is uniform and given by:
     \[
     I = \frac{FISOT}{\pi}
     \]
   - This intensity is the same at every angle.

2. **Discrete Angles and Weights**:
   - `NSTREAMS` specifies the number of discrete angles (streams) used to represent the angular distribution of radiation in the downward direction.
   - These angles are chosen to cover the range from 0 to 1 (where 0 corresponds to the zenith and 1 corresponds to the horizon).
   - Each discrete angle \( \mu_i \) has an associated weight \( w_i \).

3. **Equal Intensity at Each Angle**:
   - Since the radiation is isotropic, the intensity at each discrete angle \( \mu_i \) is the same and equal to \( I \).

4. **Calculation of Downwelling Irradiance**:
   - The downwelling irradiance at any level in the atmosphere, including the surface, is approximated by summing the intensities at the discrete angles, weighted by their respective weights:
     \[
     F_{\text{down}} \approx \sum_{i=1}^{\text{NSTREAMS}} w_i I
     \]
   - Since \( I \) is the same for all angles, this simplifies to:
     \[
     F_{\text{down}} \approx I \sum_{i=1}^{\text{NSTREAMS}} w_i
     \]

### Example

Let's consider an example with `NSTREAMS = 4` and `FISOT = 10 W/m²`:

- The discrete angles \( \mu_i \) might be chosen as \( \mu_1 = 0.1, \mu_2 = 0.3, \mu_3 = 0.5, \mu_4 = 0.7 \).
- The associated weights \( w_i \) are determined to ensure accurate integration. For simplicity, let's assume the weights are \( w_1 = 0.1, w_2 = 0.3, w_3 = 0.3, w_4 = 0.3 \).

The intensity at each discrete angle is:
\[ I = \frac{10}{\pi} \approx 3.183 W/m²/sr \]

The downwelling irradiance is then approximated as:
\[ F_{\text{down}} \approx 3.183 \cdot (0.1 + 0.3 + 0.3 + 0.3) = 3.183 W/m² \]

## Role of NSTREAMS

`NSTREAMS` specifies the number of discrete angles (streams) used to represent the angular distribution of radiation in the downward direction. These streams are chosen to cover the range of angles from straight down (0 degrees) to nearly horizontal (around 80 degrees). The choice of `NSTREAMS` affects the angular resolution of the calculation:

- **Higher `NSTREAMS`**: Provides a more detailed and accurate representation of the angular distribution of radiation but increases computational cost.
- **Lower `NSTREAMS`**: Reduces computational cost but may sacrifice accuracy, especially in cases with complex angular dependencies.

## Total Downwelling Irradiance

When both `FISOT` and `FBEAM` are >0, the total downwelling irradiance at the surface is the sum of the isotropic and beam contributions:
\[ F_{\text{total}} = FISOT + FBEAM \cdot \mu_0 \]
where `FSOLAR` is the solar flux at the top of the atmosphere and `μ0 = UMU0` is the cosine of the solar zenith angle.

## Intuitive Explanation of Irradiance in DISORT

Imagine you're trying to figure out how much sunlight reaches the ground on a cloudy day. DISORT helps us do this by breaking down the problem into simpler parts.

1. **Isotropic Radiation (Cloudy Day)**: On a cloudy day, the sunlight is scattered in all directions by the clouds, so it comes from everywhere above you equally. This is what we call isotropic radiation. DISORT handles this by assuming the light comes in from all angles equally and then calculates how much of it reaches the ground.

2. **Beam Radiation (Sunny Day)**: On a sunny day, the sunlight comes directly from the sun, so it has a specific direction. DISORT can handle this too by considering a beam of light coming from a particular angle (defined by `UMU0` and `PHI0`).

3. **Discrete Angles**: To make the calculations manageable, DISORT doesn't consider every possible angle; it chooses a few key angles (defined by `NSTREAMS`) and calculates the light at those angles. Think of it like taking samples at specific points to estimate the whole.

4. **Weights**: Not all angles are equally important. Some angles might contribute more to the total light reaching the ground. The weights (`w_i`) help DISORT give more importance to these angles.

5. **Putting It Together**: Finally, DISORT adds up the light from all the chosen angles, taking into account their weights, to estimate the total amount of light that reaches the ground.

## Conclusion

DISORT handles surface irradiance by solving the radiative transfer equation for the specified incident radiation conditions. When `FBEAM = 0` and the irradiance is isotropic, the intensity at each of the `NSTREAMS` discrete angles is equal, representing the uniform distribution of radiation in all directions. The downwelling irradiance is then calculated by summing the intensities at these discrete angles, weighted by their respective weights, to approximate the integral of the intensity over the hemisphere. This approach ensures an accurate and efficient computation of the radiative transfer in the atmosphere.
