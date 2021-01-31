# guided_wave_shm_data_loading_and_storing_hdf5
This code organises the guided wave data from: https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/ for pyhon use. Originally, the data is given in .mat files. It was not very compatible with python. This tool allows for the selection of boundary conditions (BC) of individual or multiple coupons. The data of each coupon & the selected BC is stored into HDF5 files. Additional files are generated for the dataframes.

The execute_data_create.py file is the run file and is designed in a user friendly way.
