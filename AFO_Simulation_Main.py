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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (0) The whole process of wal and running simulation
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#AFO0_Simulation.Simulation('walk', 'simulation', results_directory='')
#AFO0_Simulation.Simulation('run', 'simulation', results_directory='')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (0) The walk and running simulation for models without AFO
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#AFO0_Simulation.Simulation('walk_withoutAFO', 'simulation', results_directory='')
#AFO0_Simulation.Simulation('run_withoutAFO', 'simulation', results_directory='')

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# (1) Batch simulation for the DL, walk and run
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product(range(2,4), range(8,9), range(1,2), range(3,4)):                                                                                        # Design parameter: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):                                                                           # Design parameter: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(1,2), range(0,1), range(0,1)):                                                               # Deisgn parameter: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product(range(0,1), range(0,1), range (0,1), range(0,1)):      # Design parameter: bottom endpoint location (bottom_location)
                #------------------------------------------------------------------------------
                # The step size for each parameter during optimization
                FL_amplification_stepsize=1                                                                # The step size for the design parameter: force-length amplification, can be changed to any number
                FL_shift_stepsize=0.2                                                                             # The step size for the design parameter: force-length shift, can be changed to any number
                strip_orientation_stepsize=5                                                                  # The step size for the design parameter: strap orientation, can be changed to any number
                bottom_location_stepsize=5                                                                   # The step size for the design parameter: bottom endpoint location, can be changed to any number

                #------------------------------------------------------------------------------
                # The amplification (scaling) of the force-length relationship
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
                AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ('SimulationOutput_DL_'+ResultDirectory_parameter_str))
                # The walking simulation Walk
                AFO0_Simulation.Simulation('Walk_AFO', 'simulation', ('SimulationOutput_Walk_'+ResultDirectory_parameter_str))
                # The running simulation Run
                AFO0_Simulation.Simulation('Run_AFO', 'simulation', ('SimulationOutput_Run_'+ResultDirectory_parameter_str))
                #-----------------------------------------------------------------------------
                # Resume the design parameters to origin value in the AFO design parameter files: copy a default text into the design text file
                # 1/FL_amplification_1, -FL_shift_1: invalid parameters, 'Resume design file': command for resuming the design parameter txt file
                AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_1, -FL_shift_1, 'Resume design file')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  (2) Put the simulation results from the results folders to an excel documents_Drop landing
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# For drop landing, pick up the maximum values
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
Subtalar_matrix_DL=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product(range(2,4), range(8,9), range(1,2), range(3,4)):                                                                                         # Design parameter: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):                                                                            # Design parameter: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(1,2), range(0,1), range(0,1)):                                                                # Deisgn parameter: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product(range(0,1), range(0,1), range (0,1), range(0,1)):       # Design parameter: bottom endpoint location (bottom_location)
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
#  (3) Put the simulation results from the results folders to an excel documents_Walk
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# For walk, pick up the average differences of the subtalar angle and ankle angle between the models with and without AFO across the while gait
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
# The folder path of the walk simulation
Activity='Gait simulation'
Activity_folder_name='Walk'
Activity_results_file='Walk_states_degrees.mot'
Subtalar_matrix_activity=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
Activity_folder_1st=SelectionPath+'\\5_ForwardDynamics_1st\SimulationOutput_'+Activity_folder_name+'_'
Activity_folder_2nd=SelectionPath+'\\5_ForwardDynamics_2nd\SimulationOutput_'+Activity_folder_name+'_'

# The folder path for model without AFO
output_folder_data_withoutAFO_1st=Activity_folder_1st+'0000000000000000'
output_folder_data_withoutAFO_2nd=Activity_folder_2nd+'0000000000000000'
data_withoutAFO_1st=AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_withoutAFO_1st, Results_parameter, Activity_results_file)
data_withoutAFO_2nd=AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_withoutAFO_2nd, Results_parameter, Activity_results_file)

# For walk and run, sum the differences of ankle movements over the whole gait
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product(range(2,4), range(8,9), range(1,2), range(3,4)):                                                                                         # Design parameter: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):                                                                           # Design parameter: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(1,2), range(0,1), range(0,1)):                                                               # Deisgn parameter: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product(range(0,1), range(0,1), range (0,1), range(0,1)):      # Design parameter: bottom endpoint location (bottom_location)
                output_folder_data_AFO_1st=(Activity_folder_1st+str(fl_am_1)+str(fl_am_2)+str(fl_am_3)+str(fl_am_4)+str(fl_shift_1)+str(fl_shift_2)+str(fl_shift_3)+str(fl_shift_4)
                                                            +str(strip_ori_1)+str(strip_ori_2)+str(strip_ori_3)+str(strip_ori_4)+str(bottom_location_1)+str(bottom_location_2)+str(bottom_location_3)+str(bottom_location_4))
                output_folder_data_AFO_2nd=(Activity_folder_2nd+str(fl_am_1)+str(fl_am_2)+str(fl_am_3)+str(fl_am_4)+str(fl_shift_1)+str(fl_shift_2)+str(fl_shift_3)+str(fl_shift_4)
                                                            +str(strip_ori_1)+str(strip_ori_2)+str(strip_ori_3)+str(strip_ori_4)+str(bottom_location_1)+str(bottom_location_2)+str(bottom_location_3)+str(bottom_location_4))
                data_AFO_1st= AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_AFO_1st, Results_parameter, Activity_results_file)
                data_AFO_2nd= AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_AFO_2nd, Results_parameter, Activity_results_file)
                if data_AFO_1st.size==0:                                                                                   # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    # the third module parameter for the curvecomparison module is the i th parameters in the Results_parameter Matrix
                    # e.g. Results_parameter_i=1: means subtalar angles,         Results_parameter_i=2: means the ankle angles
                    [diff_total_subtalar1, diff_average_subtalar1, diff_max_subtalar1]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO_1st, data_AFO_1st, 1, len(data_withoutAFO_1st))
                    [diff_total_ankle1, diff_average_ankle1, diff_max_ankle1]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO_1st, data_AFO_1st, 2, len(data_withoutAFO_1st))
                if data_AFO_2nd.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    [diff_total_subtalar2, diff_average_subtalar2, diff_max_subtalar2]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO_2nd, data_AFO_2nd, 1, len(data_withoutAFO_2nd))
                    [diff_total_ankle2, diff_average_ankle2, diff_max_ankle2]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO_2nd, data_AFO_2nd, 2, len(data_withoutAFO_2nd))
                diff_average_subtalar=(diff_average_subtalar1+diff_average_subtalar2)/2
                diff_average_ankle=(diff_average_ankle1+diff_average_ankle2)/2
                # transform the variables to numbers
                Var_to_num=(fl_am_1*pow(10,15)+fl_am_2*pow(10,14)+fl_am_3*pow(10,13)+fl_am_4*pow(10,12)+fl_shift_1*pow(10,11)+fl_shift_2*pow(10,10)+fl_shift_3*pow(10,9)+fl_shift_4*pow(10,8)+strip_ori_1*pow(10,7)
                                       +strip_ori_2*pow(10,6)+strip_ori_3*pow(10,5)+strip_ori_4*pow(10,4)+bottom_location_1*pow(10,3)+bottom_location_2*pow(10,2)+bottom_location_3*pow(10,1)+bottom_location_1)
                Subtalar_matrix_activity.append(([Var_to_num, fl_am_1, fl_am_2, fl_am_3, fl_am_4, fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4, strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4, bottom_location_1,
                                               bottom_location_2, bottom_location_3, bottom_location_4, diff_average_subtalar, diff_average_ankle]))                                          # Put the four variables and the subtalar angles into a list
Subtalar_matrix_activity=np.array(Subtalar_matrix_activity)                                                        # Transform the list to the matrix
Excel_title=['Variables_in_num', 'fl_am_1','fl_am_2','fl_am_3','fl_am_4', 'fl_shift_1', 'fl_shift_2', 'fl_shift_3', 'fl_shift_4', 'strip_ori_1', 'strip_ori_2', 'strip_ori_3', 'strip_ori_4',
                   'bottom_location_1', 'bottom_location_2', 'bottom_location_3', 'bottom_location_4', 'Subtalar angle differences', 'Ankle angle differences']                   # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel(SelectionPath, 'Results.xls', Activity, Excel_title, Subtalar_matrix_activity)          # Put the four variables and subtalar angles to an excel
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""

"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  (4) Put the simulation results from the results folders to an excel documents_Running
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# For running, pick up the average differences of subtalar angle and ankle angle between the models with and without AFO across the whole cycle
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
# The folder path of the walk and run
Activity='Running simulation'
Activity_folder_name='Run'
Activity_results_file='Walk_states_degrees.mot'
Subtalar_matrix_activity=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
Activity_folder=SelectionPath+'\\5_ForwardDynamics\SimulationOutput_'+Activity_folder_name+'_'

# The folder path for model without AFO
output_folder_data_withoutAFO=Activity_folder+'0000000000000000'
data_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_withoutAFO, Results_parameter, Activity_results_file)

# For walk and run, sum the differences of ankle movements over the whole gait
for fl_am_1, fl_am_2, fl_am_3, fl_am_4 in itertools.product(range(2,4), range(8,9), range(1,2), range(3,4)):                                                                                         # Design parameter: force-length amplification (fl_am)
    for fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4 in itertools.product(range(1,2), range(0,1), range(2,3), range(2,3)):                                                                           # Design parameter: force-length shift (fl_shift)
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(1,2), range(0,1), range(0,1)):                                                               # Deisgn parameter: stripe orientation (strip_ori)
            for  bottom_location_1, bottom_location_2, bottom_location_3, bottom_location_4 in itertools.product(range(0,1), range(0,1), range (0,1), range(0,1)):      # Design parameter: bottom endpoint location (bottom_location)
                output_folder_data_AFO=(Activity_folder+str(fl_am_1)+str(fl_am_2)+str(fl_am_3)+str(fl_am_4)+str(fl_shift_1)+str(fl_shift_2)+str(fl_shift_3)+str(fl_shift_4)
                                                            +str(strip_ori_1)+str(strip_ori_2)+str(strip_ori_3)+str(strip_ori_4)+str(bottom_location_1)+str(bottom_location_2)+str(bottom_location_3)+str(bottom_location_4))
                data_AFO= AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_AFO, Results_parameter, Activity_results_file)
                if data_AFO.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                    continue
                else:
                    # the third module parameter for the curvecomparison module is the i th parameters in the Results_parameter Matrix
                    # e.g. Results_parameter_i=1: means subtalar angles,         Results_parameter_i=2: means the ankle angles
                    [diff_total_subtalar, diff_average_subtalar, diff_max_subtalar]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, 1, len(data_withoutAFO))
                    [diff_total_ankle, diff_average_ankle, diff_max_ankle]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, 2, len(data_withoutAFO))
                    # transform the variables to numbers
                    Var_to_num=(fl_am_1*pow(10,15)+fl_am_2*pow(10,14)+fl_am_3*pow(10,13)+fl_am_4*pow(10,12)+fl_shift_1*pow(10,11)+fl_shift_2*pow(10,10)+fl_shift_3*pow(10,9)+fl_shift_4*pow(10,8)+strip_ori_1*pow(10,7)
                                            +strip_ori_2*pow(10,6)+strip_ori_3*pow(10,5)+strip_ori_4*pow(10,4)+bottom_location_1*pow(10,3)+bottom_location_2*pow(10,2)+bottom_location_3*pow(10,1)+bottom_location_1)
                    Subtalar_matrix_activity.append(([Var_to_num, fl_am_1, fl_am_2, fl_am_3, fl_am_4, fl_shift_1, fl_shift_2, fl_shift_3, fl_shift_4, strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4, bottom_location_1,
                               bottom_location_2, bottom_location_3, bottom_location_4, diff_average_subtalar, diff_average_ankle]))                                                            # Put the four variables and the subtalar angles into a list
Subtalar_matrix_activity=np.array(Subtalar_matrix_activity)                                                                                                                                                                 # Transform the list to the matrix
Excel_title=['Variables_in_num', 'fl_am_1','fl_am_2','fl_am_3','fl_am_4', 'fl_shift_1', 'fl_shift_2', 'fl_shift_3', 'fl_shift_4', 'strip_ori_1', 'strip_ori_2', 'strip_ori_3', 'strip_ori_4',
                   'bottom_location_1', 'bottom_location_2', 'bottom_location_3', 'bottom_location_4', 'Subtalar angle differences', 'Ankle angle differences']                   # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel(SelectionPath, 'Results.xls', Activity, Excel_title, Subtalar_matrix_activity)          # Put the four variables and subtalar angles to an excel
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
