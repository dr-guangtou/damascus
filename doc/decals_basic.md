# Basic Information about LegacySurvey/DECaLS 

---- 

## DESI Imaging Survey Requirements:

- Imaging will be in three optical bands to a depth of at least **g=24.0, r=23.4 and z=22.5 ** (5-σ galaxy detection) in extinction-corrected magnitudes
- The fill factor will be at least 90% to full depth, will be at least 95% at 0.3 mag shallower than full depth, and 98% at 0.6 mag shallower.
- $z$-band image quality will be smaller than 1.3 arcsec FWHM in at least one pass.
- The systematic errors in astrometry will be less than 30 mas RMS. The random errors in astrometry will be less than 95 mas RMS.
- The systematic errors in the photometric system will be less than 1% RMS for g-band and r-band, and less than 2% RMS for z-band.

## Data Directory:

- `DR8`: https://portal.nersc.gov/project/cosmo/data/legacysurvey/dr8/
- `DR9-SV`: https://portal.nersc.gov/project/cosmo/data/legacysurvey/dr9sv/

### Summary file:

#### `survey-bricks.fits.gz`

- `BRICKNAME`, `BRICKID`, `BRICKROW`, `BRICKCOL`
- `BRICKQ`: Priority factor for processing
- RA, Dec of the center, and the lower & upper boundaries.

#### `survey-bricks-<dr>-south.fits.gz`

- Number of exposure, objects of different types.
- PSF sizes; 5-sigma PSF detection depth; 5-sigma galaxy (0.45" round exp) detection depth
- Milky way dust extinction information. 

#### `survey-ccds-decam-dr8.fits.gz`

- This file contains information regarding the photometric and astrometric zero points for each CCD of every image that is part of the DR8 data release
- Per CCD sky background information: `skyrms`, `ccdskysb`, `ccdskycounts`

### `Tractor` Catalog: `tractor-<brick>.fits`

- Stored at `<camera>/tractor/<AAA>/tractor-<brick>.fits`

#### Useful columns:

- ID: `objid`, `brickid`, `brickname`, `brick_primary`, `ra`, `dec`
- "Bright object mask": `brightblob`; and other mask `maskbits`
- Object type: `type`
- Gaia astrometry information: `pmra`, `pmdec`, `parallax` and `_ivar`, `gaia_pointsource`, `gaia_phot_g_mean_mag` etc.
- Flux: `flux_[g/r/z/W1/W2/W3/W4]` and `flux_ivar_[g/r/z/W1/W2/W3/W4]`.
- Fiberflux: `fiberflux_[g/r/z]` and `fibertotflux_[g/r/z]` (Predicted r-band flux within a fiber from all sources at this location in 1 arcsec Gaussian seeing). 
- Aperture flux: `apflux_[g/r/z]` in apertures of radius [0.5, 0.75, 1.0, 1.5, 2.0, 3.5, 5.0, 7.0] arcsec. And `apflux_ivar_[g/r/z]`.
- Number of observations in each band: `nobs_[g/r/z/W1/W2/W3/W4]`.
- PSF size and depth: `psfsize_[g/r/z/]` and `psfdepth_[g/r/z/W1/W2/W3/W4]`. Also for galaxy: `galdepth_[g/r/z]` (for a galaxy (0.45" exp, round)
- Morphology: `fracdev` and `fracdev_ivar`; `shape[exp/dev]_r`, `shape[exp/dev]_e1`, `shape[exp/dev]_e2`; and their `_ivar`.
	- $|e|=\sqrt{e_1^{2} + e_2^{2}}$; $\frac{b}{a}=\frac{1-|e|}{1+ |e|}$; $\phi=\frac{1}{2}\arctan\frac{e_2}{e_1}$
- Deblender information: 
	- `fracflux_[g/r/z/W1/W2/W3/W4]`: Profile-weighted fraction of the flux from other sources divided by the total flux
	- `fracmasked_[g/r/z]`: Profile-weighted fraction of pixels masked from all observations of this object
- Goodness-of-fit: `rchisq_[g/r/z/W1/W2/W3/W4]`: Profile-weighted χ² of model fit normalized by the number of pixels.
	- This 5-element vector contains the χ² difference between the best-fit point source (type="PSF"), round exponential galaxy model ("REX"), de Vaucouleurs model ("DEV"), exponential model ("EXP"), and a composite model ("COMP"), in that order.
	- The rchisq values are interpreted as the reduced χ² pixel-weighted by the model fit.

### Sweep catalog: `sweep-<brickmin>-<brickmax>.fits`

- The sweeps are light-weight FITS binary tables (containing a subset of the most commonly used Tractor measurements) of all the Tractor catalogs for which `BRICK_PRIMARY==T` in rectangles of RA, Dec.
- Flux, Object type; Reduced chi^2 of the model; Number of observations; Deblender information; Masks; PSF size and depth; Gaia information.


----

## DR8

- [DR8 description](http://legacysurvey.org/dr8/description/)
	- Sixth relase of DECaLS data; include WISE fluxes.
	- DR8 also includes DECam data from a range of non-DECaLS surveys.
	- **13161** $\rm deg^2$ with all three-band and at least three passes.
	- `southern` sources are from DECam surveys.	

### `Brick`: 

- $0.25 \times 0.25\ \rm deg^2$; defined in box of (RA, Dec).
- The image stacks use a simple tangent-plane (WCS TAN) projection around the brick center.
- **Image stack**: overlap adjacent images by approximately 130 pixels in each direction. These are tangent projections centered at each brick center, North up, with dimensions of 3600×3600
- Pixel size: 0.262 arcsec/pix for DECaLS; 2.75 arcsec/pix for WISE

### Cutout API (Only for DECaLS):

- JPEG (DECaLS): http://legacysurvey.org/viewer/jpeg-cutout?ra=190.1086&dec=1.2005&layer=dr8-south&pixscale=0.27&bands=grz
- FITS (DECaLS): http://legacysurvey.org/viewer/fits-cutout?ra=190.1086&dec=1.2005&layer=dr8-south&pixscale=0.27&bands=grz
- There are model and residual layers: `dr8-south-model` and `dr8-south-resid`.
- The maximum size for cutouts (in number of pixels) is currently 512.
- It is possible to retrieve multiple cutouts from the command line using standard utilites such as wget.

### Algorithms:

- Using `LegacyPipe dr8v3.2` and `Tractor dr8.1`. Also use the community pipeline with `SourceExtractor 2.25.0` and `PSFEx 3.21.1`.
- The source detection uses a PSF- and SED-matched-filter detection on the stacked images, with a 6σ detection limit.
- Many foreground sources, like bright star, GCs, bright galaxies are extracted separately. The foreground objects consist of pre-defined geometrical masks (which are elliptical for galaxies) that are fixed at their expected positions. The reasoning behind treating bright foreground sources as special cases is that many of them have large halos or include diffuse light that is not included in the Tractor model choices.

- See the `BRIGHTBLOB` and `MASKBITS`: http://legacysurvey.org/dr8/bitmasks/
- Spatially-varying PSF models are from `SExtractor` and `PSFex`.
- `Tractor` morphologies: 
	- `PSF`: point sources, 
	- `REX`: round exponential galaxies with a variable radius
	- `DEV`: de Vaucouleurs profiles (elliptical galaxies)
	- `EXP`: exponential profiles (spiral galaxies)
	- `COMP`: composite profiles that are deVaucouleurs + exponential (with the same source center). 
	- `DUP`: set for Gaia sources that are coincident with, and so have been fit by, an extended source.
	- Any extended source classifications have to be at least 5.8σ detections and that composite profiles must be at least 6.5σ detections.

- The fluxes are not constrained to be positive-valued. This allows the fitting of very low signal-to-noise sources without introducing biases at the faint end.
- `Tractor`: The current core routine uses the sparse least squares solver from the `SciPy` package, or the open source `Ceres` solver, originally developed by Google. 
	- `EXP` and `DEV` profiles are using MoG approximation. PSF convolvement is done using a new Fourier-space method (Lang, in prep).

### Photometry:
	
- An AB system reports the same flux in any band for a source whose spectrum is constant in units of erg/cm²/Hz. A source with a spectrum of $f=10^{−(48.6+22.5)/2.5}$ erg/cm²/Hz would be reported to have an integrated flux of 1 nanomaggie in any filter.
- Photometric calibration is done by comparing with Pan-STARRS1 (PS1) PSF photometry
	- $g_{\rm DECam} = g_{\rm PS}+0.00062+0.03604(g−i)+0.01028(g−i)^2−0.00613(g−i)^3$
	- $r_{\rm DECam} = r_{\rm PS}+0.00495−0.08435(g−i)+0.03222(g−i)^2−0.01140(g−i)^3$
	- $z_{\rm DECam} = z_{\rm PS}+0.02583−0.07690(g−i)+0.02824(g−i)^2−0.00898(g−i)^3$
- The brightnesses of objects are all stored as linear fluxes in units of nanomaggies. The conversion from linear fluxes to magnitudes is $m=22.5−2.5\log_{10}(\rm flux)$.
- The WISE Level 1 images and the unWISE image stacks are on a Vega system. We have converted these to an AB system

### Astrometry:

- Tied to Gaia Data Release 2. Astrometric residuals are typically smaller than ±0.03″.
- Astrometric calibration of all optical Legacy Survey data is conducted using Gaia astrometric positions of stars matched to Pan-STARRS1 (PS1).

### Photometric Redshift

- The Photometric Redshifts for the Legacy Surveys (PRLS), see [Zhou et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020arXiv200106018Z/abstract) 
	- Using random forest method. 
	- As a rule of thumb, objects brighter than **z-band magnitude of 21** are mostly reliable, whereas fainter objects are increasingly unreliable with large systematic offsets.
	- The photo-z catalogs do not provide information on star-galaxy separation.
- `z_phot_mean`, `z_phot_median`, `z_phot_std`, `z_spec` (if available), `survey` (for spec-z).


### Image Stacks files: `<region>/coadd/`

- Image stacks are on tangent-plane (WCS TAN) projections, 3600 × 3600 pixels, at 0.262 arcseconds per pixel

- Useful files:
	- `legacysurvey-<brick>-ccds.fits`: FITS binary table with the list of CCD images that were used in this brick.
	- `legacysurvey-<brick>-image-<filter>.fits.fz`: Stacked image centered on a brick
		- The primary HDU contains the coadded image (inverse-variance weighted coadd), in units of nanomaggies per pixel.
		- **NOTE**: These are not the images used by Tractor, which operates on the single-epoch images. These images are resampled using **Lanczos-3** resampling.
	- `legacysurvey-<brick>-invvar-<filter>.fits.fz`: Corresponding stacked inverse variance image based on the sum of the inverse-variances of the individual input images in units of 1/(nanomaggies)² per pixel.
	- `legacysurvey-<brick>-maskbits.fits.fz`: Bitmask of possible problems with pixels in this brick. 
		- `HDU1`: The optical bitmasks,
		- `HDU2/3`: The WISE W1/W2 bitmasks.
	- `legacysurvey-<brick>-model-<filter>.fits.fz`: Stacked model image centered on a brick location
	- `legacysurvey-<brick>-[image/model/resid].jpg`: JPEG image of the calibrated image using the g,r,z filters as the colors.

### Splinesky Files: `calib/<camera>/splinesky-merged/<EXPOS>/<camera>-<EXPOSURE>.fits`

- This file contains all of the sky models for a given exposure number, as a single FITS binary table with 60 rows, one per CCD. Each row is the sky model for a single CCD.
- 2-D sky is modeled using [`scipy` `RectBivariateSpline`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RectBivariateSpline.html#scipy.interpolate.RectBivariateSpline) function.
- The spline grid cells for DR8 are ~256 pixels in size.


### Known Issues:

- Patching Morphological Models: The upshot of this issue is that when REX is better than PSF, but not by a sufficiently large margin, then the EXP or DEV model would be chosen instead of the PSF model. Patched files can be identified by the header card: PATCHED (= integer number of sources patched).
- The brightest stars are missing from models and catalogs: Due to saturation and negative model flux. Will be fixed in DR9.
- Bricks that didn't finish processing: Mostly caused by large galaxies or large star clusters, or bright stars.

### DR8 Bitmask

- See [here](http://legacysurvey.org/dr8/bitmasks/) for details

- `BRIGHTBLOB`. 0: `BRIGHT`, 1: `MEDIUM`, 2: `CLUSTER`, 3: `GALAXY`.
- `MASKBITS`:
	- `Legacypipe` bitmask definitions can be found [here](https://github.com/legacysurvey/legacypipe/blob/master/py/legacypipe/bits.py)
	- Non-primary region of the brick; saturation; bright object mask, bailout blob.
	- `ALLMASK_<X>`: a source that touches a bad pixel in all of a set of overlapping X-band images: including bad pixel, saturation, interpolation, cosmic-ray, bleeding trail, edge pixel, multi-exposure transient.
	- `ANYMASK_<X>` denotes a source that touches a bad pixel in any of a set of overlapping X-band images.
	- `WISEMASK_[W1/W2]`: including diffraction spike; optical ghost; first & second latent image; AllWISE-like circular halo; bright star.