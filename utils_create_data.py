import os
import numpy as np


def clear_directory(location):
    os.chdir(location)
    current_files = [i for i in os.listdir(location)]
    for file in current_files:
        os.remove(file)


def clean_deg_data(deg_data):
    output_space = []
    for array in deg_data:
        if array[0].size > 0:
            if not array[0][0] == 0:
                output_space.append(array)
        else:
            pass
    collumn_1 = [i[0][0] for i in output_space]
    collumn_2 = [int(i[1]) for i in output_space]
    output_space = np.asarray([collumn_1, collumn_2]).T
    return output_space




