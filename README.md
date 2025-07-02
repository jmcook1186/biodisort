# biodisort

This is a *very early, draft, work-in-progress etc etc* implementation of a python interface to disort that is set up for ice surfaces and incorproates optical properties for a range of light absorbing particles found on glaciers and ice sheets. It extends the interface used by biosnicar but uses disort as the RT solver, enabling angular itensities to be returned as well as hemispheric albedo.

The disort model is provided as a binary file compiled from the FORTRAN code for DISORT v4 with bindings that allow the disort model to be imported intp python scripts and called as a Python function.

This project builds on two existing projects:

[biosnicar](https://github.com/jmcook1186/biosnicar-py)
[pydisort](https://github.com/mjwolff/pyDISORT)

You need to have `biosnicar` downloaded locally and the path to the top level biosnicar directory set in inputs.yaml (`SNICAR_BASE_PATH`). This enabled `biodisort` to grab optical property data for ice, water and impurities from the `biosnicar` database.


## setup

```
python setup.py
```

## configure

```
nano inputs.yaml
```

## run

```
python biodisort/drivers/main.py
```


# TODO
1) Check all array sizes and make sure they dynamically update correctly across snicar and disort params
2) Check brdf/surface generation and implement in the main flow
3) Create detailed input validation function that ensures internal consistency in all config
4) Synchronize snicar and disort illumination params *(done - but can be improved for cases where there are both diffuse and direct components)*
5) Implement output handling - we currently get viewing angle arrays at individual wavelengths - we want to have options to get angular intensities or hemispheric spectral values, and also broadband (done some basic output wrangling - need to add more control)
6) Remove unneccessary snicar code (*done a good amount of stripping - maybe some more still to find*)
7) Make sure default disort config is sensible for an ice column under combination direct/diffuse illumination
8) Docs!
9) Tests!
