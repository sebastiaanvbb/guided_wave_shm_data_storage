from utils_create_data import clear_directory
from coupons_and_fatigue_files import ExtractDataFileNames
from create_data import VariousCouponsTogether

"""
self note: change saving_location to dataX\BC_n and coupons = ['L1_S11_F' , ...]
"""
colab = 0
conidition = 'loaded'
if colab == 0:
    location_of_NASA_composite_files = r'C:\Users\Sebastiaan\PycharmProjects\ML_for_SHM\data'
    if conidition == 'clamped':
        saving_location_dframes = r'C:\Users\Sebastiaan\PycharmProjects\ML_for_SHM\data\data_all_sets_together\dataX' \
                                  r'\data_frames_clamped'
        saving_location = r'C:\Users\Sebastiaan\PycharmProjects\ML_for_SHM\data\data_all_sets_together\dataX\BC_clamped'
        # type all name variants in the string below as the excels sheets which
        # are scanned for data extraction are not typed up consistently
        bc = ['Clamped', 'clamped', 'Clamped ', 'clamped ', 'Clamped ']
    elif conidition == 'traction free':
        saving_location_dframes = r'C:\Users\Sebastiaan\PycharmProjects\ML_for_SHM\data\data_all_sets_together\dataX' \
                                  r'\data_frames_free'
        saving_location = r'C:\Users\Sebastiaan\PycharmProjects\ML_for_SHM\data\data_all_sets_together\dataX\\BC_traction_free'
        bc = ['Traction Free', 'traction free', 'Traction free', 'traction Free', 'Traction Free ']
    elif conidition == 'loaded':
        saving_location_dframes = r'C:\Users\Sebastiaan\PycharmProjects\ML_for_SHM\data\data_all_sets_together\dataX' \
                                  r'\data_frames_loaded'
        saving_location = r'C:\Users\Sebastiaan\PycharmProjects\ML_for_SHM\data\data_all_sets_together\dataX\BC_loaded'
        bc = ['Loaded', 'loaded', 'Loaded ', 'loaded ', ' loaded']
else:
    location_of_NASA_composite_files = r'/content/gdrive/My Drive/composites'
    saving_location_dframes = r'/content/gdrive/My Drive/data_sets_comps/data_frames/data_frames'
    saving_location = r'/content/gdrive/My Drive/data_sets_comps/dataX'

if __name__ == '__main__':

    # =======================================SelectData======================================================== #

    # coupons = ['L2_S11_F', 'L2_S17_F', 'L2_S18_F', 'L2_S20_F']
    coupons = ['L1_S11_F', 'L1_S12_F', 'L1_S18_F', 'L1_S19_F']
    # coupons = ['L3_S11_F', 'L3_S13_F', 'L3_S18_F', 'L3_S20_F']  # L3S14_0_0 is incomplete and not used
    # =====================================ExtractDataFileNames================================================ #

    create_names = ExtractDataFileNames(saving_location_dframes, location_of_NASA_composite_files, coupons, bc)
    fatigue_stage_files = create_names.collect_all()
    create_names.store_frames()

    # ==================================LoadAndStoreData======================================================= #

    clear_directory(saving_location)
    Various_coupons = VariousCouponsTogether(location_of_NASA_composite_files, saving_location, coupons, fatigue_stage_files)
    Various_coupons.obtain_data_and_store()
