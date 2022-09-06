import numpy as np
import math
import matplotlib.pyplot as plt
import AFO10_OpenSimAPI

# fixed parameters
# those based on the cylinder surface in the simulation
#AFO_cylinder_radius = 36.5 # in mm, based on radius of ankle girth for height (1.829m) and BMI (25.4) of Walk model  in Table 5 of Yu, C[2009]. Applied Ergonomics
#AFO_height = 100 #in mm, based ~50mm above baseline of avg antropometric distance from lateral malleous height to ankle girth height in Table 4 of Tu, H.[2014]. Int. J. Indust. Ergonomics
n_waves = 1 # for the Vectra brace, the number of wave is 1
wave_length_ini = 0.04   # The length of wave
# those parameters are based on experimental results
K_element = 0.36# bending stiffness, in N*mm
CSA_element = 0.0294 # average CSA for fibres printed with 0.25mm nozzle and 0.2mm layer height, in mm^2
force_limit = 1 # # Max force per element, in N, based on fatigue results for Vectra brace
slippage=0.12

def MeshMechanics (osimModel, theta_0_values, n_elements):
    def output_mechprops(strap_length, theta_0, n_elements):
        theta_0 = math.radians(theta_0) # convert from degrees to radians, starting angle of the wave
        #calculated parameters
        #wave_length = strap_length*1000 / n_waves  # strap_length in mm, wave_length in mm
        wave_length=wave_length_ini * 1000       # wave length in mm
        strap_length=strap_length * 1000        # strap length in mm
        wave_height = (wave_length / 2) * math.tan(theta_0) # in mm
        wave_hypotenuse = wave_height / math.sin(theta_0) # in mm
        CSA_total = CSA_element * n_elements # in mm^2
        # E_effective = np.around((2135.6 - (2732.2 * (theta_0))), decimals=1) # in MPa, effective Youngs as defined by relationship to theta_0
        E_effective=np.around((7505.3-(17474*(theta_0))), decimals=1) # in MPa, effective Youngs as defined by relationship to theta_0
        # populate decreasing array of theta based on starting value
        percentage = 0.9 # determines step change in theta values
        values = 1000 # determines number of values in theta array
        theta_array = theta_0 * np.full(values, percentage).cumprod()
        theta_array = np.insert(theta_array, 0, theta_0)
        # create empty lsts
        Force_array = []
        extension_array = []
        length_array = []
        for i, theta in enumerate(theta_array):
            # calculate extension due to bending to angle theta
            extension_bending = 2 * n_waves * wave_hypotenuse * (math.cos(theta) - math.cos(theta_0))
            strain_bending = extension_bending / strap_length
            # calculate force required to achieve bending based on balance of moments
            cotcsc_theta = (1 / math.tan(theta)) + (1 / math.sin(theta))
            cotcsc_theta_0 = (1 / math.tan(theta_0)) + (1 / math.sin(theta_0))
            Force = (K_element * n_elements / wave_hypotenuse) * (np.log(cotcsc_theta)-np.log(cotcsc_theta_0))
            # calculate extension due to stretching under load based on Young's modulus
            stress_stretching = Force / CSA_total
            strain_stretching = stress_stretching / E_effective
            extension_stretching = strain_stretching * strap_length
            # sum extension due to both processes
            extension_total = extension_bending + extension_stretching
            strain_total = strain_bending + strain_stretching
            #calculate OpenSim length factor
            length_factor =  1 + strain_total
            if Force > force_limit * n_elements+1:           # provide some spaces for the Force, e.g. if Force > 240 N, it will not include 240 N
                break
            else:
                Force_array.append(Force)
                extension_array.append(extension_total)
                length_array.append(length_factor)
        #convert lists to arrays
        Force_array = np.array(Force_array)
        extension_array = np.array(extension_array)
        length_array = np.array(length_array)
        return Force_array, extension_array, length_array
    FL_matrix_lst = []
    [strap_lengths, strap_forces]=AFO10_OpenSimAPI.Liginitstates(osimModel)   # The original strap length of brace calculated from the MSK model
    for i, theta_0 in enumerate(theta_0_values):
        strap_length=strap_lengths[i]
        n_elements_values = n_elements[i]
        #label = labels[i]
        Force_array, extension_array, length_array = output_mechprops(strap_length, theta_0, n_elements_values)
        # combine arrays into Force-Length matrix for OpenSim
        FL_matrix = np.vstack((length_array, Force_array))

        # Add skin movements and slippage to the Force-Length curve
        FL_matrix[0] = FL_matrix[0] + slippage    # Add skin movements and slippage values to the horizontal axis of Force-Length curve
        FL_firstelement=[1, 0]                                # The first element added to the Force-Length curve due to skin movements and slippage
        FL_matrix=[[FL_firstelement[0]]+list(FL_matrix[0]), [FL_firstelement[1]]+list(FL_matrix[1])]    # Add the first element [1, 0] to the Force-length curve after skin movements and slippage
        FL_matrix=[np.array(FL_matrix[0]), np.array(FL_matrix[1])]         # Transfer the Force-Length curve matrix from list to array
        # Combine the Force-Length curve for two braces
        FL_matrix_lst.append(FL_matrix)
        print(FL_matrix_lst)
    return FL_matrix_lst
    #
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    # The inputs for the module - AFO9_MeshMechanics
    osimModel='C:/Users/xh308/Desktop/Drop landing0/SimulationComparisonwithExperiment_20220823/Fullbodymodel_DL_platform0_AFO_comparewithexperiment_withVectra_weight60_CoordinateLimiteForce_20220825 - Copy.osim'
    theta_0_values=[20.8, 20.8]
    n_elements=[240, 50]
    # The force-length relationship of the straps
    FL_matrix_lst=MeshMechanics(osimModel, theta_0_values, n_elements)
    # The plot of force-length relationship in four sub-figures
    plt.figure()
    plt.subplot(2,1,1)
    plt.plot(FL_matrix_lst[0][0], FL_matrix_lst[0][1], marker='o', label='FL for strap 1')
    plt.subplot(2,1,2)
    plt.plot(FL_matrix_lst[1][0], FL_matrix_lst[1][1], marker='o', label='FL for strap 2')
    plt.show()
    # The plot of the force-length relationship in one figure
    plt.figure()
    plt.plot(FL_matrix_lst[0][0], FL_matrix_lst[0][1], marker='o', label='FL for strap 1')
    plt.plot(FL_matrix_lst[1][0], FL_matrix_lst[1][1], marker='o', label='FL for strap 2')
    plt.show()
    # Save results to an excel files
    """
    exe_file='D:\GitHub_xj-hua\Simulation_printAFO_CAMG\Simulation models\Drop landing0\DL simulation results\Results_20220210.xlsx'
    sheet_name='Sheet1'
    strap_length_forces=FL_matrix_lst[1].T
    data_pd=pd.DataFrame(strap_length_forces)
    data_writer=pd.ExcelWriter(exe_file)
    data_pd.to_excel(data_writer, sheet_name)
    data_writer.save()
    data_writer.close()
    """
