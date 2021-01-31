from utils_create_data import clear_directory
from coupons_and_fatigue_files import ExtractDataFileNames
from create_data import VariousCouponsTogether

"""
note: change saving_location to dataX\BC_n and coupons = ['L1_S11_F' , ...]
"""
colab = 0
conidition = 'loaded'

location_of_NASA_composite_files = r'C:\...\data'

if conidition == 'loaded':
    saving_location_dframes = r'C:\...'
    saving_location = r'C:\...'
    bc = ['Loaded', 'loaded', 'Loaded ', 'loaded ', ' loaded'] 
    # add all variants of boundary condition name due to dissimilarities in Excel data


if __name__ == '__main__':

    # =======================================SelectData======================================================== #

    coupons = ['L1_S11_F', 'L1_S12_F', 'L1_S18_F', 'L1_S19_F']
    
    # =====================================ExtractDataFileNames================================================ #

    create_names = ExtractDataFileNames(saving_location_dframes, location_of_NASA_composite_files, coupons, bc)
    fatigue_stage_files = create_names.collect_all()
    create_names.store_frames()

    # ==================================LoadAndStoreData======================================================= #

    clear_directory(saving_location)
    Various_coupons = VariousCouponsTogether(location_of_NASA_composite_files, saving_location, coupons, fatigue_stage_files)
    Various_coupons.obtain_data_and_store()
