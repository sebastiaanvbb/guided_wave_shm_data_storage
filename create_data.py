import numpy as np
import h5py
import scipy.io
from utils_create_data import clean_deg_data


class LoadAndStoreData:

    """
    Load all required data and store it for a SINGLE COUPON
    """
    number_of_paths = 252
    signal_length = 2000

    def __init__(self, location_of_nasa_composite_files, saving_location_, test_coupon_, health_stage_files_):

        """
        :param saving_location_: location of files where h5 is to b saved
        :param test_coupon_: name of the coupon under fatigue test in file name format e.g. 'L1_S11_F'
        :param health_stage_files_: list containing all .mat file names
        from different SHM stages selected for experiment
        """
        self.location_of_nasa_composite_files = location_of_nasa_composite_files
        self.saving_location = saving_location_
        self.test_coupon = test_coupon_
        self.health_stage_files = health_stage_files_
        """
        :param sensor_data_flattened_:  
        """
        self.sensor_data_flattened_ = None
        self.sensor_data_original_shape_ = None
        self.residual_flattened = None
        self.residual = None
        self.deg_data = None
        self.path_data = None
        self.data_of_hm_cycle = None

        """
        useful later on
        """
        self.num_of_hm_stages = None

    def load_required_data_and_create_labels(self):

        """
        collect data and store in correct formats. 2 formats are used:
        1) stacked format:
         [signal number in health monitoring stage (252*number of health stages selected), length of signal (2000), 1]
        2) original format:
         [health monitorinc cycle, signal number (252 for all signals), length of signal (2000), 1]
        """
        stiffness_deg_data = []
        path_data = []

        sensor_result_stacked_format = []
        sensor_results_space_orig_format = []

        num_files = len(self.health_stage_files)  # all files satisfyng boundary coniditions from coupons_and_fatigue_files.py

        for i in range(num_files):
            selected_file = self.health_stage_files[i]
            print('---currently at file---')
            print(selected_file)

            # ==== load data of current cycle ==== #
            current_path = r'{}/{}/PZT-data/'.format(self.location_of_nasa_composite_files, self.test_coupon)
            data_of_hm_cycle = scipy.io.loadmat(current_path + selected_file)

            # ==== load stiffness loss from gages ==== #
            stiffness_loss_data = data_of_hm_cycle['coupon']['straingage_data'][0][0][0][0][1][0]
            stiffness_deg_data.append((stiffness_loss_data, self.health_stage_files[i].split('_')[1]))

            # ==== load sound bytes and their corresponding paths ==== #
            for j in range(self.number_of_paths):
                sensor_result = data_of_hm_cycle['coupon']['path_data'][0][0][0][j][6][:]
                sensor_result_stacked_format.append(sensor_result)

                sensor = data_of_hm_cycle['coupon']['path_data'][0][0][0][j][0][0][0]
                actuator = data_of_hm_cycle['coupon']['path_data'][0][0][0][j][1][0][0]
                path = [sensor, actuator]
                path_data.append(path)

            store_as_numpy = np.array(sensor_result_stacked_format)
            take_last_252 = store_as_numpy[-self.number_of_paths:, :, :]
            sensor_results_space_orig_format.append(take_last_252)

        self.sensor_data_flattened_ = np.array(sensor_result_stacked_format)
        self.sensor_data_original_shape_ = np.asarray(sensor_results_space_orig_format)

        print('---all files of {} are processed---'.format(self.test_coupon))

        self.num_of_hm_stages = self.sensor_data_original_shape_.shape[0]
        self.deg_data = clean_deg_data(stiffness_deg_data)
        self.path_data = np.asarray(path_data)
        self.data_of_hm_cycle = data_of_hm_cycle
        return

    def gain_standardization(self):
        """
        standardized gains if selected (not necesarry for running code).
        It was found that some paths have different gains applied to them. This is done in a
        consistent fashion throughout SHM cycles. Here these factors are all normalised to 1 by diving the signals by their corresponding
        gain. This may improve the later applied NN normalisation
        """
        """
        load all gain factors from any hm stage (gains are identical for all SHM stages)
        """
        gain_factors = []
        for i in range(self.number_of_paths):
            value = self.data_of_hm_cycle['coupon']['path_data'][0][0][0][i][4][0][0]
            gain_factors.append(value)
        gain_factors = np.array(gain_factors)
        gains_factor_new_dim = gain_factors[np.newaxis, ...]
        matrix_gains_2d = np.repeat(gains_factor_new_dim, self.signal_length, axis=0).T
        matrix_of_gains = matrix_gains_2d[:, :, np.newaxis]

        """
        divide all signals by the gain factors such that all gains are standardized to one
        """
        for i in range(self.num_of_hm_stages):
            entries = i*self.number_of_paths
            hm_cycle_set = self.sensor_data_flattened_[entries : entries + self.number_of_paths]
            divided_data = np.divide(hm_cycle_set, matrix_of_gains)
            self.sensor_data_flattened_[entries : entries + self.number_of_paths] = divided_data
            self.sensor_data_original_shape_[i, :, :, :] = divided_data

        return

    def residual_sensor_data(self):
        """
        residual sensor data (subtract the initial health stage from all signals of all stages to obtain the remained.
        This form of processing removes a large amount of the stochastic deviations present due to eg. imperfections.
        By using this data, the assumption is taken that the initial health stage carries no damage (Only 0 cycles).
        """
        residual = []
        data_0_damage = self.sensor_data_original_shape_[0, :, :, :]

        for i in range(self.num_of_hm_stages):
            subtract_vector = self.sensor_data_original_shape_[i, :, :, :] - data_0_damage
            residual.append(subtract_vector)

        self.residual = np.asarray(residual)
        self.residual_flattened = self.residual.reshape(-1, self.signal_length, 1)

        return

    def store_all_data_as_hdf5(self):

        with h5py.File(r'{}/data_{}.h5'.format(self.saving_location, self.test_coupon), 'w') as hdf:
            hdf.create_dataset('sensor_data_stacked_format',    data=self.sensor_data_flattened_)
            hdf.create_dataset('sensor_data_original_format',   data=self.sensor_data_original_shape_)
            hdf.create_dataset('residual_data_stacked_format',  data=self.residual_flattened)
            hdf.create_dataset('residual_data_original_format', data=self.residual)
            hdf.create_dataset('deg_data',                      data=self.deg_data)
            hdf.create_dataset('path_data',                     data=self.path_data)
        return


class VariousCouponsTogether(LoadAndStoreData):
    """
    class for evaluation and storage of various hp5 files of different coupons. This function depends on:
    Coupons_and_fatigue_files
    """
    def __init__(self, location_of_nasa_composite_files, saving_location_, coupon_list, health_stage_list):
        super().__init__(location_of_nasa_composite_files, saving_location_, None, None)
        self.coupon_list = coupon_list
        self.health_stage_list = health_stage_list

    def obtain_data_and_store(self):

        for coupon in enumerate(self.coupon_list):
            load_and_store = LoadAndStoreData(self.location_of_nasa_composite_files,
                                              self.saving_location, coupon[1],
                                              self.health_stage_list[coupon[0]])
            load_and_store.load_required_data_and_create_labels()
            # load_and_store.gain_standardization()
            load_and_store.residual_sensor_data()
            load_and_store.store_all_data_as_hdf5()
