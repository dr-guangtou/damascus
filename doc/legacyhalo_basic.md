# Basic Tutorial About Using `legacyhalo`

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