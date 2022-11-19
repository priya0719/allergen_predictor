import numpy as np

def represent_as_E_descriptors(sequence):
    allergens_E_descriptors = []
    for base in sequence:
        # adding all the 5 E Descriptors for each base and generating our E Descriptor sequence
        allergens_E_descriptors.extend(E_descriptors[base])

    return allergens_E_descriptors


# this function takes the E Descriptor sequence for each sequence and converts E descriptors sequence as a 2-D array,
# one row corresponding each type of descriptor, for each sequence and returns the same as a 2-D array named as E.
# this function is called for one sequence at a time
def convert_to_2D(descriptors):
    E1 = []
    E2 = []
    E3 = []
    E4 = []
    E5 = []
    for i in range(0, len(descriptors), 5):
        E1.append(descriptors[i])
        E2.append(descriptors[i + 1])
        E3.append(descriptors[i + 2])
        E4.append(descriptors[i + 3])
        E5.append(descriptors[i + 4])

    E = [E1, E2, E3, E4, E5]
    E = np.array(E)
    return E


# this function takes j_list, lag, n, and E as input
# returns a dictionary of auto covariance values
# this funstion is called for one sequence at a time
def calculate_auto_covariance(j_list, lag, n, E):
    auto_covariance = []
    for j in j_list:
        for l in lag:
            sum = 0
            for i in range(0, n - l):
                sum += (E[j, i] * E[j, i + l]) / (n - l)
            auto_covariance.append(sum)
    # print(auto_covariance)
    return auto_covariance


# this function takes j_list, k_list, lag, n, and E as input
# returns a dictionary of cross covariance values
# this funstion is called for one sequence at a time
def calculate_cross_covariance(j_list, k_list, lag, n, E):
    cross_covariance = []
    for j in j_list:
        for k in k_list:
            if j == k:
                continue
            else:
                for l in lag:
                    sum = 0
                    for i in range(0, n - l):
                        sum += (E[j, i] * E[k, i + l]) / (n - l)

                    cross_covariance.append(sum)
    # print(cross_covariance)
    return cross_covariance


# this main function takes the input file which can be either the .csv file for allergens or non allergens
def main(sequence, j_list, k_list, lag):
    aa_set = ['A','R','N','D','C','Q','E','G','H','I','L','K','M','F','P','S','T','W','Y','V','O','U']
    for aa in sequence:
        if aa not in aa_set:
            return 'Entered sequence has undefined character'

    allergens_E_descriptors = represent_as_E_descriptors(sequence)

    descriptors = allergens_E_descriptors
    E = convert_to_2D(descriptors)  # calling convert_to_2D function
    n = len(descriptors) // 5
    auto_covariance = calculate_auto_covariance(j_list, lag, n, E)  # calling calculate_auto_covariance fucntion

    cross_covariance = calculate_cross_covariance(j_list, k_list, lag, n,
                                                  E)  # calling calculate_auto_covariance fucntion

    final_sequence = auto_covariance + cross_covariance

    return final_sequence


###########################################################################################

# j_list is 0 to 4 because we have 5 E Descriptors
j_list = [0, 1, 2, 3, 4]

# lag is set to 5, as the in our data the length of shortest sequence is 5
lag = [1, 2, 3, 4, 5]

# we need this, exclusively for calculating cross covariance
k_list = [0, 1, 2, 3, 4]

E_descriptors = {'A': [0.008, 0.134, -0.475, -0.039, 0.181],
                 'R': [0.171, -0.361, 0.107, -0.258, -0.364],
                 'N': [0.255, 0.038, 0.117, 0.118, -0.055],
                 'D': [0.303, -0.057, -0.014, 0.225, 0.156],
                 'C': [-0.132, 0.174, 0.07, 0.565, -0.374],
                 'Q': [0.149, -0.184, 0.03, 0.035, -0.112],
                 'E': [0.221, -0.280, -0.315, 0.157, 0.303],
                 'G': [0.218, 0.562, -0.024, 0.018, 0.106],
                 'H': [0.023, -0.177, 0.041, 0.28, -0.021],
                 'I': [-0.353, 0.071, -0.088, -0.195, -0.107],
                 'L': [-0.267, 0.018, -0.265, -0.274, 0.206],
                 'K': [0.243, -0.339, -0.044, -0.325, -0.027],
                 'M': [-0.239, -0.141, -0.155, 0.321, 0.077],
                 'F': [-0.329, -0.023, 0.072, -0.002, 0.208],
                 'P': [0.173, 0.286, 0.407, -0.215, 0.384],
                 'S': [0.199, 0.238, -0.015, -0.068, -0.196],
                 'T': [0.068, 0.147, -0.015, -0.132, -0.274],
                 'W': [-0.296, -0.186, 0.389, 0.083, 0.297],
                 'Y': [-0.141, -0.057, 0.425, -0.096, -0.091],
                 'V': [-0.274, 0.136, -0.187, -0.196, -0.299]}

#sequence = "ATGACG"
# calling main function
#converted_sequence = main(sequence, j_list, k_list, lag)
# print(converted_sequence)
