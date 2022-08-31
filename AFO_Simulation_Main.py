import AFO0_Simulation
import AFO1_DesignParameter
import os
import AFO2_MBDModel
import AFO3_ParaTestSelect
import numpy as np
import AFO4_ResultsCollection
import AFO5_DoE
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import itertools
import tkinter
from tkinter import filedialog
import math
import AFO_Simulation_Optimization
import AFO9_MeshMechanics
import AFO10_OpenSimAPI


solution = [[101, 259],
                   [101, 259],
                   [19.02205431, 20.44985441],
                   [394, 190]]
# Display the MSK model based on the provided solution (design variables)
AFO_Simulation_Optimization.Main_model_demo (solution, 0)


"""
for num_strap4 in range (6, 8):
    solution = [[78.17011239, 100.73042733, 303.09510209, 304.48512362],
                    [345.75577512, 170.25159198, 186.60823527, 55.41003946],
                    [16.39262715, 19.74779624, 21.12849443, 21.76360147],
                    [26, 378, 193,  num_strap4]]
    # Run simulation and collect the results
    Angles_DL, Muscles_diff, strap_forces_diff, strap_pene_monitor=AFO_Simulation_Optimization.Main_Simulation(solution, 00)
    # print iteration history to txt file
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    with open (os.path.join(path_simulation, 'log_results_check.txt'), 'a') as f:
        print('The number of iteration: %d \n' %(35), file=f)
        print('The number of the strap 4:%d \n' %(num_strap4), file=f)
        print('Angles_DL=[Subtalar_DL_max_platform0, Subtalar_DL_max_platform45, Ankle_DL_max_platform0, Ankle_DL_max_platform45]:', file=f)
        print('%s' %(Angles_DL), file=f)
        print('Muscles_diff=[diff_average_musforce_total_walk_norm, diff_average_musforce_total_run_norm]:', file=f)
        print('%s' %(Muscles_diff), file=f)
        print('strap_forces_diff=[strap_forces_diff_DL_platform0, strap_forces_diff_DL_platform45, strap_forces_diff_Walk, strap_forces_diff_Run]:', file=f)
        print('%s' %(strap_forces_diff), file=f)
        print('#####################################################################################################', file=f)

for num_strap4 in range (7, 9):
    solution = [[77.90326426, 100.87050424, 304.09510209, 304.96437419],
                    [346.38245762, 170.01525895, 187.60823527, 56.20937242],
                    [16.38644684, 19.74200634, 21.02849443, 21.8],
                    [26, 378, 193,  num_strap4]]
    # Run simulation and collect the results
    Angles_DL, Muscles_diff, strap_forces_diff, strap_pene_monitor=AFO_Simulation_Optimization.Main_Simulation(solution, 00)
    # print iteration history to txt file
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    with open (os.path.join(path_simulation, 'log_results_check.txt'), 'a') as f:
        print('The number of iteration: %d \n' %(34), file=f)
        print('The number of the strap 4:%d \n' %(num_strap4), file=f)
        print('Angles_DL=[Subtalar_DL_max_platform0, Subtalar_DL_max_platform45, Ankle_DL_max_platform0, Ankle_DL_max_platform45]:', file=f)
        print('%s' %(Angles_DL), file=f)
        print('Muscles_diff=[diff_average_musforce_total_walk_norm, diff_average_musforce_total_run_norm]:', file=f)
        print('%s' %(Muscles_diff), file=f)
        print('strap_forces_diff=[strap_forces_diff_DL_platform0, strap_forces_diff_DL_platform45, strap_forces_diff_Walk, strap_forces_diff_Run]:', file=f)
        print('%s' %(strap_forces_diff), file=f)
        print('#####################################################################################################', file=f)
"""

"""
# Simulation of drop landing
folder_index=0
[AFO_bottom_location, AFO_top_location, theta_0_values, n_elements]=solution
AFO0_Simulation.Simulation(('AFODroplanding', 'simulation', solution, str(folder_index), [25, 0, 0]))
AFO0_Simulation.Simulation(('AFODroplanding', 'simulation', solution, str(folder_index), [0, -45, -25]))
Results_parameter_DL=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']   # The specified parameter to extract
platform0=[25,0,0]    # The platform orientation of 0 degree, inclination of 25 degree
platform45=[0,-45,-25]   # The platform orientation of 45 degree, inclination of 25 degree
results_directory_platform0=str(folder_index)+str(platform0[0])+str(platform0[1])+str(platform0[2])   # The folder for the simulation results for platform orientation of  0 degree
results_directory_platform45=str(folder_index)+str(platform45[0])+str(platform45[1])+str(platform45[2]) # The folder for simulation results for platform orienation of 45 degree
output_folder_DL_platform0='Simulation models\Drop landing'+str(folder_index)+'\DL simulation results\\'+results_directory_platform0     # The folder path for the simulation with platform orientation of 0 degree
output_folder_DL_platform45='Simulation models\Drop landing'+str(folder_index)+'\DL simulation results\\'+results_directory_platform45  # The folder path for the simulation with platform orientation of 45 degree
data_DL_platform0= AFO4_ResultsCollection.Simulationresultscollection(output_folder_DL_platform0, Results_parameter_DL, 'default_states_degrees.mot')  # put the specified results into a matrix for platform 0
data_DL_platform45= AFO4_ResultsCollection.Simulationresultscollection(output_folder_DL_platform45, Results_parameter_DL, 'default_states_degrees.mot')  # put the specified results into a matrix for platform 45
# The maximum subtalar angles for drop landing with two platfomr orientations (0 and 45 degrees)
Subtalar_DL_max_platform0=max(data_DL_platform0[:,1])  # The maximum subtalar angle for drop landing with platform 0 orientation
Subtalar_DL_max_platform45=max(data_DL_platform45[:,1])  # The maximum subtalar angle for drop landing with platform 45 orientation
# The maximum ankle angles for drop landing with two platform orientations (0 and 45 degrees)
Ankle_DL_max_platform0=max(data_DL_platform0[:,2])  # The maximum ankle angle for drop landing with platform 0 orientation
Ankle_DL_max_platform45=max(data_DL_platform45[:,2])  # The maximum ankle angle for drop landing with platform 45 orientation
#---------------------------------------------------------------------------------
# The drop landing model for calculating the strap_length_ini and fatigue length
osimModel_platform0='Simulation models\Drop landing'+str(folder_index)+'\Fullbodymodel_DL_platform0_AFO.osim'
osimModel_platform45='Simulation models\Drop landing'+str(folder_index)+'\Fullbodymodel_DL_platform45_AFO.osim'
# Calculate the initial strap length at default position of drop landing
[DL_strap_lengths_ini_platform0, DL_strap_forces_ini_platform0]=AFO10_OpenSimAPI.Liginitstates(osimModel_platform0)
[DL_strap_lengths_ini_platform45, DL_strap_forces_ini_platform45]=AFO10_OpenSimAPI.Liginitstates(osimModel_platform45)
#---------------------------------------------------------------------------------
# Collect the fatigue forces for the 4 straps from the AFO mechanics (AFO9_MeshMechanics) for drop landing
# Fatigue strap forces for drop landing of platform 0 degree
AFO_FL_platform0=AFO9_MeshMechanics.MeshMechanics(osimModel_platform0, theta_0_values, n_elements) # Get the force-length relationship for the four straps
FL_length_mesh_max_platfrom0=[max(AFO_FL_platform0[0][0]), max(AFO_FL_platform0[1][0]), max(AFO_FL_platform0[2][0]), max(AFO_FL_platform0[3][0])] # The maximum lengths (fatigue lengths) for the four straps from AFO9_MeshMechanics
FL_force_mesh_max_platform0=[max(AFO_FL_platform0[0][1]), max(AFO_FL_platform0[1][1]), max(AFO_FL_platform0[2][1]), max(AFO_FL_platform0[3][1])] # The maximum forces (fatigue forces) for the four straps from AFO9_MeshMechanics
#print('Max lengths from the AFO9_MeshMechanics: %s'  %(FL_length_mesh_max))
#print('Max forces from the AFO9_MeshMechanics: %s'  %(FL_force_mesh_max))
# Fatigue strap forces for drop landing of platform 45 degree
AFO_FL_platform45=AFO9_MeshMechanics.MeshMechanics(osimModel_platform45, theta_0_values, n_elements) # Get the force-length relationship for the four straps
FL_length_mesh_max_platform45=[max(AFO_FL_platform45[0][0]), max(AFO_FL_platform45[1][0]), max(AFO_FL_platform45[2][0]), max(AFO_FL_platform45[3][0])] # The maximum lengths (fatigue lengths) for the four straps from AFO9_MeshMechanics
FL_force_mesh_max_platform45=[max(AFO_FL_platform45[0][1]), max(AFO_FL_platform45[1][1]), max(AFO_FL_platform45[2][1]), max(AFO_FL_platform45[3][1])] # The maximum forces (fatigue forces) for the four straps from AFO9_MeshMechanics
#print('Max lengths from the AFO9_MeshMechanics: %s'  %(FL_length_mesh_max))
#print('Max forces from the AFO9_MeshMechanics: %s'  %(FL_force_mesh_max))
#---------------------------------------------------------------------------------
# Collect the maximum ligament (strap) length and force during the drop landing simulation
[DL_strap_lengths_realtime_platform0, DL_strap_forces_realtime_platform0, DL_strap_lengths_max_platform0, DL_strap_forces_max_platform0]=AFO10_OpenSimAPI.LigMechanicsMax (output_folder_DL_platform0, 'default_states_degrees.mot', osimModel_platform0)
[DL_strap_lengths_realtime_platform45, DL_strap_forces_realtime_platform45, DL_strap_lengths_max_platform45, DL_strap_forces_max_platform45]=AFO10_OpenSimAPI.LigMechanicsMax (output_folder_DL_platform45, 'default_states_degrees.mot', osimModel_platform45)
[DL_strap_lengths_grad_platform0, DL_strap_pene_monitor_platform0]=AFO10_OpenSimAPI.LigPeneMonitor(DL_strap_lengths_realtime_platform0, DL_strap_lengths_ini_platform0, 0.0045)
[DL_strap_lengths_grad_platform45, DL_strap_pene_monitor_platform45]=AFO10_OpenSimAPI.LigPeneMonitor(DL_strap_lengths_realtime_platform45, DL_strap_lengths_ini_platform45, 0.0045)
#print('The max strap lengths for DL: %s'  %(DL_strap_lengths_max))
#print('The max strap forces for DL: %s'  %(DL_strap_forces_max))
#---------------------------------------------------------------------------------
# Calculate the differences between the maximum real-time strap forces and the fatigure strap forces
strap_forces_diff_DL_platform0=np.array(DL_strap_forces_max_platform0)-np.array(FL_force_mesh_max_platform0)
strap_forces_diff_DL_platform45=np.array(DL_strap_forces_max_platform45)-np.array(FL_force_mesh_max_platform45)
print('The maximum subtalar angle for platform 0: %s' %(Subtalar_DL_max_platform0))
print('The maximum subtalar angle for platform 45: %s' %(Subtalar_DL_max_platform45))
print('The differences of strap forces for DL_platform 0: %s' %(strap_forces_diff_DL_platform0))
print('The differences of strap forces for DL_platform 45: %s' %(strap_forces_diff_DL_platform45))

# The plot of force-length relationship in four sub-figures
FL_matrix_lst=AFO_FL_platform0
DL_strap_lengths_realtime_platform0=np.array(DL_strap_lengths_realtime_platform0)
DL_strap_lengths_ini_platform0=np.array(DL_strap_lengths_ini_platform0).reshape(-1,1)
DL_FL_matrix=DL_strap_lengths_realtime_platform0/DL_strap_lengths_ini_platform0
plt.figure()
plt.subplot(2,2,1)
plt.plot(FL_matrix_lst[0][0], FL_matrix_lst[0][1], color='r', marker='.', label='FL for strap 1')
plt.plot(DL_FL_matrix[0], DL_strap_forces_realtime_platform0[0], color='b', marker='*', label='Realtime FL for strap 1')
plt.plot()
plt.subplot(2,2,2)
plt.plot(FL_matrix_lst[1][0], FL_matrix_lst[1][1], color='r', marker='.', label='FL for strap 2')
plt.plot(DL_FL_matrix[1], DL_strap_forces_realtime_platform0[1], color='b', marker='*', label='Realtime FL for strap 2')
plt.subplot(2,2,3)
plt.plot(FL_matrix_lst[2][0], FL_matrix_lst[2][1], color='r', marker='.', label='FL for strap 3')
plt.plot(DL_FL_matrix[2], DL_strap_forces_realtime_platform0[2], color='b', marker='*', label='Realtime FL for strap 3')
plt.subplot(2,2,4)
plt.plot(FL_matrix_lst[3][0], FL_matrix_lst[3][1], color='r', marker='.', label='FL for strap 4')
plt.plot(DL_FL_matrix[3], DL_strap_forces_realtime_platform0[3], color='b', marker='*', label='Realtime FL for strap 3')
plt.show()
"""





"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (Code 0): The normal whole process of wal and running simulation, including scaling, IK, RRA, CMC, FD
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
AFO0_Simulation.Simulation('walk', 'simulation', results_directory='')
AFO0_Simulation.Simulation('run', 'simulation', results_directory='')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (Code 1): The determination of ranges of the design variables and step size for each variable for optimization
#      The necessary inputs for batch simulation, results collection in codes (3), (4), (5), (6)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# The ranges for design variables
Var_range_FL_amplification=[range(3,4), range(1,2), range(1,2), range(1,2)]                                     # Range of design variables: force-length amplification (fl_am)
Var_rang_FL_shift=[range(1,2), range(1,2), range(1,2), range(1,2)]                                                     # Range of design variables: force-length shift (fl_shift)
Var_range_stripe_orientation=[range(0,1), range(0,1), range(0,1), range(0,1)]                                     # Range of design variables: stripe orientation (strip_ori)
Var_range_bottom_location=[range(0,1), range(0,1), range (0,1), range(0,1)]                                      # Range of design variables: bottom endpoint location (bottom_location)
# The step size for each design variable during optimization
FL_amplification_stepsize=6                                                                                                                # The step size for the design parameter: force-length amplification, can be changed to any number
FL_shift_stepsize=0.2                                                                                                                             # The step size for the design parameter: force-length shift, can be changed to any number
strip_orientation_stepsize=5                                                                                                                   # The step size for the design parameter: strap orientation, can be changed to any number
bottom_location_stepsize=5                                                                                                                   # The step size for the design parameter: bottom endpoint location, can be changed to any number
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (Code 2): The walk and running simulation for models without AFO. Before perform the simulation, make sure the scaling, IK and RRA have already been performed,
#       To perform scaling, IK, and RRA, use the whole process of walk and running simulation in code (0)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
AFO0_Simulation.Simulation('walk_withoutAFO', 'simulation', results_directory='')
AFO0_Simulation.Simulation('run_withoutAFO', 'simulation', results_directory='')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (Code 3): Batch simulation for the drop landing, walk and run
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product (*Var_range_FL_amplification):                                                                                               # Design variable: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(*Var_rang_FL_shift):                                                                                                   # Design variable: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product (*Var_range_stripe_orientation):                                                                      # Deisgn variable: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product (*Var_range_bottom_location):                # Design variable: bottom endpoint location (bottom_location)
                #------------------------------------------------------------------------------
                # The amplification (scaling) of the force-length relationship
                #FL_amplification_1=FL_amplification_2=FL_amplification_3=FL_amplification_4=FL_amplification_stepsize*math.pow(10, fl_am_1)

                FL_amplification_1=fl_am_1*FL_amplification_stepsize
                FL_amplification_2=fl_am_2*FL_amplification_stepsize
                FL_amplification_3=fl_am_3*FL_amplification_stepsize
                FL_amplification_4=fl_am_4*FL_amplification_stepsize
                #-----------------------------------------------------------------------------
                # The shift of the force-length relationship
                FL_shift_1=fl_shift_1*FL_shift_stepsize-0.2
                FL_shift_2=fl_shift_2*FL_shift_stepsize-0.2
                FL_shift_3=fl_shift_3*FL_shift_stepsize-0.2
                FL_shift_4=fl_shift_4*FL_shift_stepsize-0.2
                #-----------------------------------------------------------------------------
                # The orientation of AFO strip
                Strip_orientation=np.array([strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4])*strip_orientation_stepsize
                #-----------------------------------------------------------------------------
                # The location of the bottom endpoints of the AFO
                bottom_location_angle=np.array([bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4])*bottom_location_stepsize
                #-----------------------------------------------------------------------------
                # Change the design parameters in the AFO design text file
                AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_1, FL_shift_1, 'AFO_FLrelationship_one')
                AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_2, FL_shift_2, 'AFO_FLrelationship_two')
                AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_3, FL_shift_3, 'AFO_FLrelationship_three')
                AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_4, FL_shift_4, 'AFO_FLrelationship_four')
                AFO3_ParaTestSelect.AFOmaterialVariables(Strip_orientation,Strip_orientation,'AFO_stripe_orientations')
                AFO3_ParaTestSelect.AFOmaterialVariables(bottom_location_angle,bottom_location_angle,'AFO_bottom_location_angle')
                #-----------------------------------------------------------------------------
                # The batch of simulation
                ResultDirectory_parameter_str=(str(fl_am_1)+str(fl_am_2)+str(fl_am_3)+str(fl_am_4)+str(fl_shift_1)+str(fl_shift_2)+str(fl_shift_3)+str(fl_shift_4)       # The name of the result folder
                                                                    +str(strip_ori_1)+str(strip_ori_2)+str(strip_ori_3)+str(strip_ori_4)
                                                                    +str(bottom_location_1)+str(bottom_location_2)+str(bottom_location_3)+str(bottom_location_4))
                # The drop landing simulation DL
                #AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ('SimulationOutput_DL_'+ResultDirectory_parameter_str))
                # The walking simulation Walk
                AFO0_Simulation.Simulation('Walk_AFO', 'simulation', ('SimulationOutput_Walk_'+ResultDirectory_parameter_str))
                # The running simulation Run
                #AFO0_Simulation.Simulation('Run_AFO', 'simulation', ('SimulationOutput_Run_'+ResultDirectory_parameter_str))
                #-----------------------------------------------------------------------------
                # Resume the design parameters to origin value in the AFO design parameter files: copy a default text into the design text file
                # 1/FL_amplification_1, -FL_shift_1: invalid parameters, 'Resume design file': command for resuming the design parameter txt file
                AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_1, -FL_shift_1, 'Resume design file')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  (Code 4): Put the simulation results from the results folders to an excel documents_Drop landing
#                  For drop landing activity, collect the maximum subtalar angle and ankle angle
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
Subtalar_matrix_DL=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product (*Var_range_FL_amplification):                                                                                               # Design variable: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(*Var_rang_FL_shift):                                                                                                   # Design variable: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product (*Var_range_stripe_orientation):                                                                      # Deisgn variable: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product (*Var_range_bottom_location):                # Design variable: bottom endpoint location (bottom_location)
                simulationresults_parameter_str=(str(fl_am_1)+str(fl_am_2)+str(fl_am_3)+str(fl_am_4)+str(fl_shift_1)+str(fl_shift_2)+str(fl_shift_3)+str(fl_shift_4)      # The name of the result folder
                                                                        +str(strip_ori_1)+str(strip_ori_2)+str(strip_ori_3)+str(strip_ori_4)+str(bottom_location_1)+str(bottom_location_2)+str(bottom_location_3)+str(bottom_location_4))
                output_folder=os.path.join(SelectionPath, ('SimulationOutput_DL_'+simulationresults_parameter_str))
                data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')                                                  # put the specified results into a matrix
                if data.size==0:                                                                                                                                                                                                                               # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    # transform the variables to numbers
                    Var_to_num=(fl_am_1*pow(10,15)+fl_am_2*pow(10,14)+fl_am_3*pow(10,13)+fl_am_4*pow(10,12)+fl_shift_1*pow(10,11)+fl_shift_2*pow(10,10)+fl_shift_3*pow(10,9)+fl_shift_4*pow(10,8)+strip_ori_1*pow(10,7)
                                    +strip_ori_2*pow(10,6)+strip_ori_3*pow(10,5)+strip_ori_4*pow(10,4)+bottom_location_1*pow(10,3)+bottom_location_2*pow(10,2)+bottom_location_3*pow(10,1)+bottom_location_1)
                    Subtalar_matrix_DL.append(([Var_to_num, fl_am_1, fl_am_2, fl_am_3, fl_am_4, fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4, strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4, bottom_location_1,
                                                                   bottom_location_2, bottom_location_3, bottom_location_4, max(data[:,1]), max(data[:,2])]))                                    # Put the four variables and the subtalar angles into a list
Subtalar_matrix_DL=np.array(Subtalar_matrix_DL)                                                                                                                                                                                                      # Transform the list to the matrix
Excel_title=['Variables_in_num', 'fl_am_1','fl_am_2','fl_am_3','fl_am_4', 'fl_shift_1', 'fl_shift_2', 'fl_shift_3', 'fl_shift_4', 'strip_ori_1', 'strip_ori_2', 'strip_ori_3', 'strip_ori_4',
                   'bottom_location_1', 'bottom_location_2', 'bottom_location_3', 'bottom_location_4', 'Max subtalar angle', 'Max ankle angle']                                                                 # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel(SelectionPath, 'Results.xls', 'DL_Platform 25', Excel_title, Subtalar_matrix_DL)                                                                                  # Put the four variables and subtalar angles to an excel
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  (Code 5): Put the simulation results from the results folders to an excel documents_Walk
#                  For walk and running, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle
#                  inteplote the curve across the whole cycle into thousands of points anc calculate the differences of muscle forces for these points)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Results_parameter=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r',
                                  'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r',
                                  'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']                       # The specified parameter to extract
# The folder path of the walk and run
Activity='Gait simulation'
Activity_folder_name='Walk'
Activity_results_file='cmc_MuscleAnalysis_TendonForce.sto'
MuscleForces_diff_matrix_activity=[]                                                                             # Subtalar_matrix_activity=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
Activity_folder=SelectionPath+'\\4_CMC\SimulationOutput_'+Activity_folder_name+'_'
# The folder path for model without AFO
output_folder_data_withoutAFO=Activity_folder+'0000000000000000'
data_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_withoutAFO, Results_parameter, Activity_results_file)

# For walk and run, sum the differences of muscle forces over the whole cycle
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product (*Var_range_FL_amplification):                                                                                               # Design variable: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(*Var_rang_FL_shift):                                                                                                   # Design variable: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product (*Var_range_stripe_orientation):                                                                      # Deisgn variable: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product (*Var_range_bottom_location):                # Design variable: bottom endpoint location (bottom_location)
                output_folder_data_AFO=(Activity_folder+str(fl_am_1)+str(fl_am_2)+str(fl_am_3)+str(fl_am_4)+str(fl_shift_1)+str(fl_shift_2)+str(fl_shift_3)+str(fl_shift_4)
                                                            +str(strip_ori_1)+str(strip_ori_2)+str(strip_ori_3)+str(strip_ori_4)+str(bottom_location_1)+str(bottom_location_2)+str(bottom_location_3)+str(bottom_location_4))
                data_AFO= AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_AFO, Results_parameter, Activity_results_file)
                if data_AFO.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    diff_average_muscleforce_WholeMuscle=[]
                    for muscle_num in range (1, len(data_withoutAFO[0])):
                        [diff_total_muscleforce, diff_average_muscleforce, diff_max_muscleforce]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, muscle_num, len(data_withoutAFO))
                        diff_average_muscleforce_WholeMuscle.append(diff_average_muscleforce)
                    diff_average_muscleforce_WholeMuscle=np.array(diff_average_muscleforce_WholeMuscle)                   # The matrix include the absolute differences of muscle forces for each musch for each design case
                    diff_average_muscleforce_totalForce=np.sum(diff_average_muscleforce_WholeMuscle)                           # The total differences of muscle forces for all the muscle in the right legs for each design case
                    # transform the variables to numbers
                    Var_to_num=(fl_am_1*pow(10,15)+fl_am_2*pow(10,14)+fl_am_3*pow(10,13)+fl_am_4*pow(10,12)+fl_shift_1*pow(10,11)+fl_shift_2*pow(10,10)+fl_shift_3*pow(10,9)+fl_shift_4*pow(10,8)+strip_ori_1*pow(10,7)
                                            +strip_ori_2*pow(10,6)+strip_ori_3*pow(10,5)+strip_ori_4*pow(10,4)+bottom_location_1*pow(10,3)+bottom_location_2*pow(10,2)+bottom_location_3*pow(10,1)+bottom_location_1)
                    MuscleForces_diff_matrix_activity.append(([Var_to_num, fl_am_1, fl_am_2, fl_am_3, fl_am_4, fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4, strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4, bottom_location_1,
                               bottom_location_2, bottom_location_3, bottom_location_4, diff_average_muscleforce_totalForce]))                                                            # Put the four variables and the subtalar angles into a list
MuscleForces_diff_matrix_activity=np.array(MuscleForces_diff_matrix_activity)                                                                                                                                                                 # Transform the list to the matrix
Excel_title=['Variables_in_num', 'fl_am_1','fl_am_2','fl_am_3','fl_am_4', 'fl_shift_1', 'fl_shift_2', 'fl_shift_3', 'fl_shift_4', 'strip_ori_1', 'strip_ori_2', 'strip_ori_3', 'strip_ori_4',
                   'bottom_location_1', 'bottom_location_2', 'bottom_location_3', 'bottom_location_4', 'Average muscle forces differences']                   # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel(SelectionPath, 'Results.xls', Activity, Excel_title, MuscleForces_diff_matrix_activity)                     # Put the differences of muscle forces into excel file
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  (Code 6): Put the simulation results from the results folders to an excel documents_Running
#                  For walk and running, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle
#                 inteplote the curve across the whole cycle into thousands of points anc calculate the differences of muscle forces for these points)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Results_parameter=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r',
                                  'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r',
                                  'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']                       # The specified parameter to extract
# The folder path of the walk and run
Activity='Running simulation'
Activity_folder_name='Run'
Activity_results_file='cmc_MuscleAnalysis_TendonForce.sto'
MuscleForces_diff_matrix_activity=[]                                                                             # Subtalar_matrix_activity=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
Activity_folder=SelectionPath+'\\4_CMC\SimulationOutput_'+Activity_folder_name+'_'
# The folder path for model without AFO
output_folder_data_withoutAFO=Activity_folder+'0000000000000000'
data_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_withoutAFO, Results_parameter, Activity_results_file)

# For walk and run, sum the differences of muscle forces over the whole cycle
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product (*Var_range_FL_amplification):                                                                                         # Design variable: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(*Var_rang_FL_shift):                                                                                             # Design variable: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product (*Var_range_stripe_orientation):                                                                # Deisgn variable: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product (*Var_range_bottom_location):          # Design variable: bottom endpoint location (bottom_location)
                output_folder_data_AFO=(Activity_folder+str(fl_am_1)+str(fl_am_2)+str(fl_am_3)+str(fl_am_4)+str(fl_shift_1)+str(fl_shift_2)+str(fl_shift_3)+str(fl_shift_4)
                                                            +str(strip_ori_1)+str(strip_ori_2)+str(strip_ori_3)+str(strip_ori_4)+str(bottom_location_1)+str(bottom_location_2)+str(bottom_location_3)+str(bottom_location_4))
                data_AFO= AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_AFO, Results_parameter, Activity_results_file)
                if data_AFO.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    diff_average_muscleforce_WholeMuscle=[]
                    for muscle_num in range (1, len(data_withoutAFO[0])):
                        [diff_total_muscleforce, diff_average_muscleforce, diff_max_muscleforce]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, muscle_num, len(data_withoutAFO))
                        diff_average_muscleforce_WholeMuscle.append(diff_average_muscleforce)
                    diff_average_muscleforce_WholeMuscle=np.array(diff_average_muscleforce_WholeMuscle)                   # The matrix include the absolute differences of muscle forces for each musch for each design case
                    diff_average_muscleforce_totalForce=np.sum(diff_average_muscleforce_WholeMuscle)                           # The total differences of muscle forces for all the muscle in the right legs for each design case
                    # transform the variables to numbers
                    Var_to_num=(fl_am_1*pow(10,15)+fl_am_2*pow(10,14)+fl_am_3*pow(10,13)+fl_am_4*pow(10,12)+fl_shift_1*pow(10,11)+fl_shift_2*pow(10,10)+fl_shift_3*pow(10,9)+fl_shift_4*pow(10,8)+strip_ori_1*pow(10,7)
                                            +strip_ori_2*pow(10,6)+strip_ori_3*pow(10,5)+strip_ori_4*pow(10,4)+bottom_location_1*pow(10,3)+bottom_location_2*pow(10,2)+bottom_location_3*pow(10,1)+bottom_location_1)
                    MuscleForces_diff_matrix_activity.append(([Var_to_num, fl_am_1, fl_am_2, fl_am_3, fl_am_4, fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4, strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4, bottom_location_1,
                               bottom_location_2, bottom_location_3, bottom_location_4, diff_average_muscleforce_totalForce]))                                                            # Put the four variables and the subtalar angles into a list
MuscleForces_diff_matrix_activity=np.array(MuscleForces_diff_matrix_activity)                                                                                                                                                                 # Transform the list to the matrix
Excel_title=['Variables_in_num', 'fl_am_1','fl_am_2','fl_am_3','fl_am_4', 'fl_shift_1', 'fl_shift_2', 'fl_shift_3', 'fl_shift_4', 'strip_ori_1', 'strip_ori_2', 'strip_ori_3', 'strip_ori_4',
                   'bottom_location_1', 'bottom_location_2', 'bottom_location_3', 'bottom_location_4', 'Average muscle forces differences']                   # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel(SelectionPath, 'Results.xls', Activity, Excel_title, MuscleForces_diff_matrix_activity)                     # Put the differences of muscle forces into excel file
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
