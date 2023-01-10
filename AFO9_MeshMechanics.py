import numpy as np
import os
import math
import matplotlib.pyplot as plt
import AFO10_OpenSimAPI
from scipy import integrate
from scipy.integrate import quad
from scipy.interpolate import interp1d
from math import sqrt
# Angle in radians for using numpy sin and cos calculation
from numpy import arcsin, arctan, sin, cos, pi
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

# fixed parameters
# those based on the cylinder surface in the simulation
# AFO_cylinder_radius = 36.5 # in mm, based on radius of ankle girth for height (1.829m) and BMI (25.4) of Walk model  in Table 5 of Yu, C[2009]. Applied Ergonomics
# AFO_height = 100 #in mm, based ~50mm above baseline of avg antropometric distance from lateral malleous height to ankle girth height in Table 4 of Tu, H.[2014]. Int. J. Indust. Ergonomics
# n_waves = 1 # for the Vectra brace, the number of wave is 1
# wave_length_ini = 0.04   # The length of wave
n_periods = 1   # the number of wave period
period_length = 40   # in mm
# those parameters are based on experimental results
K_element = 0.267   # bending stiffness, in N*mm
CSA_element = 0.0294  # average CSA for fibres printed with 0.25mm nozzle and 0.2mm layer height, in mm^2
force_limit = 1   # 1 # # Max force per element, in N, based on fatigue results for Vectra brace
#slippage = 0.0125
slippage = 0.0123


def integrand(x, wave_height, wave_period_length):
    w = (2*pi/wave_period_length)
    return sqrt((-1*wave_height*w*sin(w*x))**2+1)


def output_mechprops(strap_length, theta_0, n_elements):
    theta_0_deg = theta_0       # starting angle in degrees
    # convert from degrees to radians, starting angle of the wave
    theta_0_rad = math.radians(theta_0)
    # calculated parameters
    wave_length = period_length/2           # wave length in mm
    # wave height in mm, theta_o_rad in radians
    wave_height = (wave_length/2)*math.tan(theta_0_rad)
    strap_length = strap_length * 1000     # convert strap_length from m to mm

    I = quad(integrand, 0, period_length, args=(wave_height, period_length))
    L1 = I[0]
    wave_height_new = 0.25*sqrt(L1**2 - period_length**2)
    wave_height_new = round(wave_height_new, 2)

    theta_0_new = math.atan((2*wave_height_new)/wave_length)
    deg_new = math.degrees(theta_0_new)
    wave_hypotenuse_new = wave_height_new / math.sin(theta_0_new)    # in mm
    wave_hypotenuse = wave_height / math.sin(theta_0_rad)   # in mm
    CSA_total = CSA_element * n_elements  # in mm^2
    # The angle used in E_effectivness equation is deg_new which is new theta_0 based on sine wave approximation and in degs (unit)
    # in MPa, effective Youngs as defined by relationship to theta_0
    E_effective = np.around((5404.8 - (128.92 * (theta_0_deg))), decimals=1)
    # populate decreasing array of theta based on starting value
    percentage = 0.95  # determines step change in theta values
    values = 10000  # determines number of values in theta array
    theta_array_new = theta_0_new * np.full(values, percentage).cumprod()
    theta_array_new = np.insert(theta_array_new, 0, theta_0_new)

    theta_array = theta_0_rad * np.full(values, percentage).cumprod()
    theta_array = np.insert(theta_array, 0, theta_0_rad)

    # create empty lsts
    Force_array = []
    extension_array = []
    length_array = []

    for i, (theta_new, theta) in enumerate(zip(theta_array_new, theta_array)):
        # calculate extension due to bending to angle theta
        extension_bending = 4 * n_periods * wave_hypotenuse_new * \
            (math.cos(theta_new) - math.cos(theta_0_new))
        strain_bending = extension_bending / strap_length
        # calculate force required to achieve bending based on balance of moments
        cotcsc_theta = (1 / math.tan(theta)) + (1 / math.sin(theta))
        cotcsc_theta_0 = (1 / math.tan(theta_0_rad)) + (1 / math.sin(theta_0_rad))
        Force = (K_element * n_elements / wave_hypotenuse) * \
            (np.log(cotcsc_theta)-np.log(cotcsc_theta_0))
        # calculate extension due to stretching under load based on Young's modulus
        stress_stretching = Force / CSA_total
        strain_stretching = stress_stretching / E_effective
        extension_stretching = strain_stretching * strap_length
        # sum extension due to both processes
        extension_total = extension_bending + extension_stretching
        strain_total = strain_bending + strain_stretching
        # calculate OpenSim length factor
        length_factor = 1 + strain_total
        # provide some spaces for the Force, e.g. if Force > 240 N, it will not include 240 N
        if Force > force_limit * n_elements:
            break
        else:
            Force_array.append(Force)
            extension_array.append(extension_total)
            length_array.append(length_factor)
    # convert lists to arrays
    Force_array = np.array(Force_array)
    extension_array = np.array(extension_array)
    length_array = np.array(length_array)
    return Force_array, extension_array, length_array


def MeshMechanics(osimModel, theta_0_values, n_elements):
    FL_matrix_lst = []
    # The original strap length of brace calculated from the MSK model
    [strap_lengths, strap_forces] = AFO10_OpenSimAPI.Liginitstates(osimModel)
    for i, theta_0 in enumerate(theta_0_values):
        strap_length = strap_lengths[i]
        n_elements_values = n_elements[i]
        #label = labels[i]
        Force_array, extension_array, length_array = output_mechprops(
            strap_length, theta_0, n_elements_values)
        # combine arrays into Force-Length matrix for OpenSim
        FL_matrix = np.vstack((length_array, Force_array))

        # Add skin movements and slippage to the Force-Length curve
        # Convert the slippage displacement to strain
        slippage_strain = slippage / strap_length
        # Add skin movements and slippage strain to the horizontal axis of Force-Length curve
        FL_matrix[0] = FL_matrix[0] + slippage_strain
        # The first element added to the Force-Length curve due to skin movements and slippage
        FL_firstelement = [[1, 1+slippage_strain/2], [0, 0]]
        # Add the first element [1, 0] to the Force-length curve after skin movements and slippage
        FL_matrix = [FL_firstelement[0]+list(FL_matrix[0]), FL_firstelement[1]+list(FL_matrix[1])]
        # Transfer the Force-Length curve matrix from list to array
        FL_matrix = [np.array(FL_matrix[0]), np.array(FL_matrix[1])]

        """
        # Add fatigue length: Extend the Force-Length curve: when the extension is larger than the fatigue length, the force will turn to 0
        # After the fatigue length, the force will turn to 0
        FL_fatigue = [[max(FL_matrix[0]), 1.5], [0, 0]]
        FL_matrix = [list(FL_matrix[0])+FL_fatigue[0], list(FL_matrix[1]) +
                     FL_fatigue[1]]  # Add FL_fatigue to the end of the FL curve
        # Transfer the Force-Length curve matrix from list to array
        FL_matrix = [np.array(FL_matrix[0]), np.array(FL_matrix[1])]
        """

        # Combine the Force-Length curve for two braces
        FL_matrix_lst.append(FL_matrix)
        # print(FL_matrix_lst)
    return FL_matrix_lst
    #


# Xijin' main code: output were force-length (extension rate) curves for OpenSim model
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    # The inputs for the module - AFO9_MeshMechanics
    osimModel = 'D:/XijinHua/GitHub_xj-hua/Simulation_printAFO_CAMG_20221010/Simulation models/Drop landing0/Fullbodymodel_DL_platform0_AFO.osim'
    theta_0_values = [21.8, 21.8]
    n_elements = [240, 90]
    # The force-length relationship of the straps
    FL_matrix_lst = MeshMechanics(osimModel, theta_0_values, n_elements)
    # The plot of force-length relationship in four sub-figures
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(FL_matrix_lst[0][0], FL_matrix_lst[0][1], marker='o', label='FL for strap 1')
    plt.subplot(2, 1, 2)
    plt.plot(FL_matrix_lst[1][0], FL_matrix_lst[1][1], marker='o', label='FL for strap 2')
    plt.show()
    # The plot of the force-length relationship in one figure
    plt.figure()
    plt.plot(FL_matrix_lst[0][0], FL_matrix_lst[0][1], marker='o', label='FL for strap 1')
    plt.plot(FL_matrix_lst[1][0], FL_matrix_lst[1][1], marker='o', label='FL for strap 2')
    plt.show()
    # Save results to an excel files
    exe_file = 'C:/Users/xh308/Desktop/Drop landing0/SimulationComparisonwithExperiment_20220908/Results.xlsx'
    sheet_name = 'Sheet1'
    strap_length_forces = np.array(FL_matrix_lst[0]).T
    data_pd = pd.DataFrame(strap_length_forces)
    data_writer = pd.ExcelWriter(exe_file)
    data_pd.to_excel(data_writer, sheet_name)
    data_writer.save()
    data_writer.close()

"""
# Zehao's main code: output were force-extension curves
# Note: in order to run the main code, it requires to disable the parameters in the hearder part, as these have been included in the main code
if __name__ == "__main__":
    # in degrees, wave starting angle, function of sine wave amplitude and period
    theta_0_values = [16.7, 21.80, 26.57]
    n_elements_values = [16, 16, 16]  # number of elements in the mesh

    # fixed parameters
    # those based on the cylinder surface in the simulation
    # AFO_cylinder_radius = 36.5 # in mm, based on radius of ankle girth for height (1.829m) and BMI (25.4) of Walk model  in Table 5 of Yu, C[2009]. Applied Ergonomics
    # AFO_height = 100 #in mm, based on avg antropometric distance from lateral malleous height to ankle girth height in Table 4 of Tu, H.[2014]. Int. J. Indust. Ergonomics
    n_periods_lst = [1, 1, 1]  # number of half periods
    # those based on experimental results
    K_element_lst = [0.267, 0.267, 0.267]  # bending stiffness, in N*mm
    #E_effective_lst = [1951, 783.8]
    # average CSA for fibres printed with 0.25mm nozzle and 0.2mm layer height, in mm^2
    CSA_element_lst = [0.0294, 0.0294, 0.0294]
    force_limit_lst = [1, 1, 1]  # Max force per element, in N, based on fatigue results for h = 1mm
    FL_matrix_lst = []

    # create figure container
    figB, axB = plt.subplots()
    Force_array_lst = []
    Extension_array_lst = []
    for i, theta_0 in enumerate(theta_0_values):
        #n_elements = n_elements_values[i]
        K_element = K_element_lst[i]
        #E_effective = E_effective_lst[i]
        CSA_element = CSA_element_lst[i]
        force_limit = force_limit_lst[i]
        n_periods = n_periods_lst[i]
        n_elements = n_elements_values[i]
        strap_length = 0.102450645276
        period_length = 40
        label = str(theta_0_values[i])

        Force_array, extension_array, length_array = output_mechprops(
            strap_length, theta_0, n_elements)
        Force_perElement = Force_array / n_elements
        axB.plot(extension_array, Force_perElement, label='{}'.format(label))
        Force_array_lst.append(Force_array)
        Extension_array_lst.append(extension_array)

        dict = {'Force': Force_array, 'Extension': extension_array}
        df = pd.DataFrame(dict)
        df.to_csv("D:\\Xijin Hua_Cambridge project\\Project meeting\\Zehao Ji\\MeshMechanicsCode\\MechanicalModelOutput.csv".format(
            theta_0, K_element))

    axB.set_xlabel('Distance [mm]')
    axB.set_ylabel('Force per element [N]')
    axB.legend()
    plt.show()
"""
