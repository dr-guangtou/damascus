# DAMASCUS - **D**ec**A**ls **MAS**sive **C**lusters **U**sing central galaxie**S**

- This repo includes the codes, scripts, and `Jupyter` notebooks that help study massive galaxies in the DECaLS survey footprint with the help of the DESI spectroscopic data.
  - Most of the actual analysis will be done on NERSC's `Cori` supercomputer with the help of the `legacyhalos` package developed by John Moustakas. It will also make heavy use the `legacypipe` and `tractor` photometric engine developed by Dustin Lang. 
  - Here the codes are mainly for preparing the sample and post-processing the `legacyhalos` outputs for scientific analysis. 
  - The `legacyhalos` pipeline will also provide us the cutout images of galaxies. `Damascus` will try to include codes to perform other photometric analysis on them.

- Right now, this repo also includes codes and notebooks for carrying out DESi service tasks for:
    1. The Bright Galaxies (BGS) working group.
    2. The Cluster, Cross-Correlation, and Small-Scale Clustering (C3) working group.

- This repo will also try to include photometric comparison of galaxies between HSC and LegacySurvey images.
  - Jia-Xuan Li (李嘉轩; Princeton) has worked extensively on this and has summarized the results in [this paper](https://ui.adsabs.harvard.edu/abs/2021arXiv211103557L/abstract). His [`Kuaizi`](https://github.com/AstroJacobLi/kuaizi) repo includes all the codes and scripts for the analysis. There will be some overlap.


## Useful links:

- [DECaLS (The Dark Energy Camera Legacy Survey)](http://legacysurvey.org/decamls/)
- DECaLS is a component of the [DESI Legacy Imaging Surveys](http://legacysurvey.org/)
  - [Overview of the DESI Legacy Imaging Surveys](https://arxiv.org/pdf/1804.08657.pdf)
  
- [`legacyhalos` - Code and papers for a multi-faceted study of the baryonic content of dark matter halos in Legacy Survey imaging by John Moustakas](https://github.com/moustakas/legacyhalos)
- [`legacypipe` - Image reduction pipeline for the DESI Legacy Imaging Surveys, using the Tractor framework](https://github.com/legacysurvey/legacypipe)
- [`obiwan` - Inject artificial sources and rerun the pipeline to understand systematics](https://github.com/legacysurvey/obiwan)
