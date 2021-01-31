import pandas as pd
import pickle

"""
The following code is simply used to select the desired files for conversion into hpf5
BC selector may select slight alteraions per BC
"""


class ExtractDataFileNames:

    def __init__(self, saving_location_dframes,  file_location, coupons, bc):

        self.saving_location_dframes = saving_location_dframes
        self.file_location = file_location
        self.coupons = [[i] for i in coupons]
        self.file_extensions = ['{}/{}'.format(i[:], i[0:2]+i[3:6]) for i in coupons]
        self.bc = bc
        self.data_frames = None

    @staticmethod
    def bc_selector(bc, frame):
        select_collumn = frame['Boundary Conditions']
        satisfied_indices = (select_collumn == bc[0]) | (select_collumn == bc[1]) | (select_collumn == bc[2]) | \
                            (select_collumn == bc[3]) | (select_collumn == bc[4])
        new_indices = satisfied_indices
        extracted_frame = frame[new_indices]

        single_dataset_per_cycle_num = 0
        if single_dataset_per_cycle_num == 1:
            cycle_collumn = extracted_frame['Cycles']
            delete_doubles = cycle_collumn.drop_duplicates()
            delete_doubles[:] = True
            new_indices[:] = False
            for i in delete_doubles.index.values:
                new_indices[i] = True
            extracted_frame = frame[new_indices]
        else:
            pass

        rel_files_with_comma = extracted_frame['Data File Name'].to_list()
        nu_rel_files = len(rel_files_with_comma)
        rel_files = [rel_files_with_comma[j][1:-1] for j in range(nu_rel_files)]
        return extracted_frame, rel_files

    def enter_all_selected_files(self, i):
        """
        13 total coupons. of 3 different layups. Each layup is considered independently
        """
        frame_1 = pd.read_excel(r'{}/{}.xlsx'.format(self.file_location, self.file_extensions[i]))
        extracted_frame_, health_stage_files_ = ExtractDataFileNames.bc_selector(self.bc, frame_1)

        return extracted_frame_, health_stage_files_

    def collect_all(self):
        num_coupons = len(self.coupons)
        self.data_frames = []
        fatigue_stage_files = []
        for i in range(num_coupons):
            extracted_frame1, health_stage_files1 = ExtractDataFileNames.enter_all_selected_files(self, i)
            self.data_frames.append(extracted_frame1)
            fatigue_stage_files.append(health_stage_files1)
        return fatigue_stage_files

    def store_frames(self):
        with open(self.saving_location_dframes, "wb") as fp:  # Pickling
            pickle.dump(self.data_frames, fp)
            pickle.dump(self.coupons, fp)

        return
