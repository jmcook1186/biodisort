# Irradiance in bioDISORT

DISORT (Discrete Ordinates Radiative Transfer) is a powerful model used to solve the radiative transfer equation in plane-parallel media, such as the Earth's atmosphere. One of the key outputs of DISORT is the surface irradiance, which is the amount of radiation reaching the Earth's surface. However, `biodisort` is primarily concerned with the radiative transfer in a column of ice sitting at the bottom of the atmosphere. This means we do not want all the calculations to begin with the solar constant - we want our unattenuated irradiance to be the bottom of atmosphere, or surface, irradiance. Therefore, we have to do a little adjusting of DISORT's config. We use the database of at-surface irradiance intensities from the `biosnicar` model (which themselves were precalculated using vanilla DISORT). We can prescribe a broad region (mid-latitude, polar) and season (summer, winter) and a solar zenith angle and then look up spectral at-surface irradiance intensities to pass to DISORT. This page will explain that process, clarify the variables used and the flow of information through `biodisort`.

## Key Variables

### FBEAM
- **Definition**: `FBEAM` is a flag that indicates whether beam radiation (direct solar radiation) is included in the calculation.
- **Values**: `FBEAM = 0` means no beam radiation (only diffuse radiation), and `FBEAM = 1` means beam radiation is included.
- **Role**: This flag determines whether the model will account for direct solar radiation coming from a specific direction.

### FISOT
- **Definition**: `FISOT` represents the isotropic (diffuse) radiation flux at the top of the atmosphere. When `FISOT` is set, DISORT assumes that there is a uniform, diffuse radiation field incident from all directions above the atmosphere.
- **Values**: This is a scalar value representing the intensity of the isotropic radiation.
- **Role**: This variable sets the magnitude of the incoming diffuse radiation, which is then modulated by the optical properties of the atmosphere.

### UMU0 and PHI0
- **UMU0**: Cosine of the solar zenith angle, specifying the direction of the incoming solar beam.
- **PHI0**: Azimuth angle of the sun, measured from the positive x-axis (usually north).
- **Role**: These variables, along with `FBEAM`, fully specify the direction and angle of the incoming solar radiation.

### SOLZEN
- **Definition**: `SOLZEN` is the solar zenith angle, in degrees.
- **Values**: 0-90
- **Role**: This is used to derive `UMU0`

### SEASON
- **Definition**: Season/region/solzen is used to determine at surface irradiance. Depending on the region/season/solzen combination a different irradiance file is loaded in and used to define `FISOT`.
- **Values**: "s", "w"
- **Role**: `SEASON` tells biodisort to grab files for summer or winter irradiance for a given region. These form the file stubs for reading in appropriate irradiance files.
  
### REGION
- **Definition**: Season/region/solzen is used to determine at surface irradiance. Depending on the region/season/solzen combinationa  different irradiance file is loaded in and used to configure `FISOT`.
- **Values**: "ml", "p" 
- **Role**: `REGION` tells biodisort to grab files for summer or winter irradiance for a given region. These form the file stubs for reading in appropriate irradiance files.


## Isotropic Incident Radiation

When `FBEAM = 0` and the incident radiation is isotropic, the intensity at the top of the atmosphere is uniform in all directions. The intensity \( I \) is given by:
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

When both `FISOT` and `FBEAM` are set to 1, the total downwelling irradiance at the top of the atmosphere is the sum of the isotropic and beam contributions:
\[ F_{\text{total}} = FISOT + FSOLAR \cdot \mu_0 \]
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
