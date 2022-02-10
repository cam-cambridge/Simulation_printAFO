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

# Display the MSK model based on the provided solution (design variables)
solution = [[14, 101, 259, 346], [-40, 0, 0, 50], [20.34, 21.20, 13.18, 18.9], [30, 100, 100, 30]]
AFO_Simulation_Optimization.Main_model_demo (solution, 0)

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
