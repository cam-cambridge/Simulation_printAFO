import numpy as np
import math
import matplotlib.pyplot as plt

def MeshMechanics (strap_orientations, theta_0_values, n_elements):
    def output_mechprops(strap_orientation, theta_0, n_elements):
        strap_orientation  = math.radians(strap_orientation) # convert from degrees to radians
        theta_0 = math.radians(theta_0) # convert from degrees to radians

        #calculated parameters
        strap_length = AFO_height / math.cos(strap_orientation) # in mm
        wave_length = strap_length / n_waves # in mm
        wave_height = (wave_length / 2) * math.tan(theta_0) # in mm
        wave_hypotenuse = wave_height / math.sin(theta_0) # in mm
        CSA_total = CSA_element * n_elements # in mm^2
        E_effective = np.around((2135.6 - (2732.2 * (theta_0))), decimals=1) # in MPa, effective Youngs as defined by relationship to theta_0

        # populate decreasing array of theta based on starting value
        percentage = 0.9 # determines step change in theta values
        values = 1000 # determines number of values in theta array
        theta_array = theta_0 * np.full(values,percentage).cumprod()
        theta_array = np.insert(theta_array,0,theta_0)

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

            if Force > force_limit * n_elements:
                break
            else:
                Force_array.append(Force)
                extension_array.append(extension_total)
                length_array.append(length_factor)


        #convert lsts to arrays
        Force_array = np.array(Force_array)
        extension_array = np.array(extension_array)
        length_array = np.array(length_array)

        return Force_array,extension_array,length_array
    # fixed parameters
    # those based on the cylinder surface in the simulation
    #AFO_cylinder_radius = 36.5 # in mm, based on radius of ankle girth for height (1.829m) and BMI (25.4) of Walk model  in Table 5 of Yu, C[2009]. Applied Ergonomics
    AFO_height = 100 #in mm, based ~50mm above baseline of avg antropometric distance from lateral malleous height to ankle girth height in Table 4 of Tu, H.[2014]. Int. J. Indust. Ergonomics
    n_waves = 20 # fixed to be able to divide height into wave length that is printable (~5mm)

    # those based on experimental results
    K_element = 0.781 # bending stiffness, in N*mm
    CSA_element = 0.0557332 # average CSA for fibres printed with 0.25mm nozzle and 0.2mm layer height, in mm^2
    force_limit = 2 # # Max force per element, in N, based on fatigue results for h = 1mm

    FL_matrix_lst = []


    for i, theta_0 in enumerate(theta_0_values):
        strap_orientation = strap_orientations[i]
        n_elements_values = n_elements[i]
        #label = labels[i]
        Force_array,extension_array,length_array = output_mechprops(strap_orientation, theta_0, n_elements_values)

        # combine arrays into Force-Length matrix for OpenSim
        #FL_matrix = np.vstack((Force_array,length_array))
        FL_matrix = np.vstack((length_array, Force_array))
        # add matrix to list
        FL_matrix_lst.append(FL_matrix)
    return FL_matrix_lst
#
