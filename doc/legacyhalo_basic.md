# Basic Tutorial About Using `legacyhalo`

## Environment setup

- Define the project: e.g., `project=manga`
- `legacypipe`:
    - `LEGACYPIPE_CODE_DIR`: Location of the `legacypipe`. Don't need to touch.
    - `PYTHONPATH`: Python path.

- `legacyhalo` and input/output:
    - `LEGACYHALOS_DIR`: `legacyhalo` location, need to go to the `project` folder.
    - Output data location: `LEGACYHALOS_DATA_DIR=/global/cscratch1/sd/ioannis/$project-data`
    - Output HTML location: `LEGACYHALOS_HTML_DIR=/global/cfs/cdirs/cosmo/www/temp/ioannis/$project-html` 

- `legacyhalo` code:
    - `LEGACYHALOS_CODE_DIR`, `PATH`, and `PYTHONPATH`

- Legacy survey data:
    - e.g. `LEGACY_SURVEY_DIR=/global/cfs/cdirs/cosmo/work/legacysurvey/dr9k`
    - And there are other data directories that don't need to change.

- `export PYTHONNOUSERSITE = 1` # Don't add ~/.local/ to Python's sys.path

- Calculate the necessary memory:
    - `ncores = 8`
    - `maxmem = 134217728 # Cori/Haswell = 128 GB`
    - `grep -q "Xeon Phi" /proc/cpuinfo && maxmem=100663296 # Cori/KNL = 98 GB`
    - `let usemem=${maxmem}*${ncores}/32`

- All the project specific environment parameters can be defined here too:
    - Such as `HSC_DIR`, `HSC_DATA_DIR`.

## Shifter or Docker configuration

- `legacysurvey` and `legacyhalos` docker:
    `SHIFTER=docker:legacysurvey/legacyhalos:v0.0.4`

- Load the shifter: 
    - `shifterimg pull $SHIFTER`
    - `shifter --image $SHIFTER bash`

## Project specific module: `project.py`

- Need to be in the `legacyhalo` Python folder.
    - **TODO**: Only way? Do I have to upgrade `legacyhalo`?
    - Using `manga.py` and `hsc.py` as examples

- Define some constants
    - `RACOLUMN`, `DECCOLUMN`, `ZCOLUMN`, `GALAXYCOLUMN`
    - `GALAXYCOLUMN`: e.g. ID
    - `RADIUS_CLUSTER_KPC`, `RADIUSFACTOR`

- `mpi_args()` function to organize all the arguments:
    - `nproc`, `mpi`
    - `first`, `last`
    - Different procedures: `coadds`, `custom-coadds`, `ellipse`, `integrate`, `htmlplots`.
    - `--count`, `--debug`, `--verbose`, `--clobber`

- `missing_files()` function:
    - Take the `sample` as input. Also deals with different `filetype`.
    - Need to get `galaxy` and `galaxydir`. Can be from a different function.
    - Define file suffix and file names for different `filetype`: `coadds`, `pipeline-coadds`, `ellipse`, `htmlplots`, `htmlindex`, `html`
    - Basically figure out how many galaxies are left to deal with.

- `get_galaxy_galaxydir()`, retrieve the galaxy name and the (nested) directory:
    - Take the `cat` as input; also take `datadir` and `htmldir`
    - Get galaxy ID and/or name, coordinates
        - If there are too many galaxies, can get their Healpix pixel number and use the `pixnum` to group galaxies.
        - Get the folder names for the galaxy output data and html: `galaxydir` and `htmlgalaxydir`.
        - Return the galaxy IDs and folder names.

- Project specific locations:
    - `hsc_dir`, based on `$HSC_DIR`
    - `hsc_data_dir`, based on `$HSC_DATA_DIR`
    - `hsc_html_dir`, based on `$HSC_HTML_DIR`

- `read_sample()`:
    - Organize the data from the catalog into a `sample`.
    - Has a `first` and `last` options, so don't need to read the whole catalog. 
    - Basically just read the catalog using `astropy` and rename some columns.

- `make_html()`: Make the HTML pages
    - Take `sample`, `datadir`, `htmldir`.
    - `refband="r"`, `pixscale=0.262`.
    - Better not change this one...

## MPI wrapper for the project: A Python script

- There is a `main` function as the top-level wrapper
    - All the arguments are available in this wrapper.
    - One can run this script or submit it using `slurm`.

- Project specific module
    - Need to have a `legacyhalo/$project.py` module.
    - Need to import the `project` module and get the `args`: `legacyhalos.manga.mpi_args()`.
    - **TODO**: Ask about whether this is the only way.

- Procedures:
    - Need to read and broadcast the sample.
        - Can define a `read_sample` function in the project specific module.
        - Broadcast: `comm = MPI.COMM_WORLD` and `sample = comm.bcast(sample, root=0)`
    - Building the web-page and integrating the ellipse-fitting results work on the full sample, so do that here and then return.   
        - Define a `make_html` function in `project.py`

## Wrapper to run the script or submit the job

-

-----

## Brief Note by Enia Xhakaj

- How to use/install legacy_halos
    - `manga-env` — script that creates an environment 
        - Specify the project and then you have 3 vars: 
            1. specified directory: `LEGACYHALOS_DIR` 
            2. data directory 
            3. html directory
    - `manga-shifter`: 
        - This is a container. This will keep other things like the `scikit-images` without having to reload them 
    - `manga-mpi`: 
        - Builds the custom code, sky subtraction, ellipse fitting and makes webpages
        - This needs to be written for our project 
    - `manga.py`: 
        - (check the readme file) 