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
# Batch simulation for the DL, walk and run
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(1,9), range(8,9), range(1,2), range(3,4)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(0,2), range(0,1), range(2,3), range(2,3)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):       # Deisgn parameters of stripe orientation
            # The scaling of force-length relationship
            FL_amplification_1=af_am_1*20
            FL_amplification_2=af_am_2*20
            FL_amplification_3=af_am_3*20
            FL_amplification_4=af_am_4*20
            # The shift of force-length relationship
            FL_shift_1=af_shift_1*0.2-0.2
            FL_shift_2=af_shift_2*0.2-0.2
            FL_shift_3=af_shift_3*0.2-0.2
            FL_shift_4=af_shift_4*0.2-0.2
            # The orientation of AFO strip
            Strip_orientation=np.array([strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4])
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Change the design parameters in the AFO design text file
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_1, FL_shift_1, 'AFO_FLrelationship_one')
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_2, FL_shift_2, 'AFO_FLrelationship_two')
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_3, FL_shift_3, 'AFO_FLrelationship_three')
            AFO3_ParaTestSelect.AFOmaterialVariables(FL_amplification_4, FL_shift_4, 'AFO_FLrelationship_four')
            AFO3_ParaTestSelect.AFOmaterialVariables(Strip_orientation,Strip_orientation,'AFO_stripe_orientations')
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # The batch of simulation
            # The drop landing simulation DL
            ResultDirectory_DL='SimulationOutput_DL_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory_DL)
            # The walking simulation Walk
            #ResultDirectory_Walk='SimulationOutput_Walk_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            #AFO0_Simulation.Simulation('Walk_AFO', 'simulation', ResultDirectory_Walk)
            # The running simulation Run
            #ResultDirectory_Run='SimulationOutput_Run_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            #AFO0_Simulation.Simulation('Run_AFO', 'simulation', ResultDirectory_Run)
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Resume the design parameters to origin value in the AFO design parameter files: copy a default text into the design text file
            # 1/FL_amplification_1, -FL_shift_1: invalid parameters, 'Resume design file': command for resuming the design parameter txt file
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_1, -FL_shift_1, 'Resume design file')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Put the simulation results from the results folders to an excel documents
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# For drop landing, pick up the maximum values
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
Subtalar_matrix_DL=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(1,4), range(4,9), range(1,4), range(2,7)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(0,3), range(0,3), range(0,3), range(0,3)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):
            # output_folder='Drop landing\DL simulation results\SimulationOutput_DL_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            simulationresults_folder='SimulationOutput_DL_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            output_folder=os.path.join(SelectionPath, simulationresults_folder)
            data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')                        # put the specified results into a matrix
            if data.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                continue
            else:
                # transform the variables to numbers
                Var_to_num=af_am_1*pow(10,7)+af_am_2*pow(10,6)+af_am_3*pow(10,5)+af_am_4*pow(10,4)+af_shift_1*pow(10,3)+af_shift_2*pow(10,2)+af_shift_3*pow(10,1)+af_shift_4
                Subtalar_matrix_DL.append([Var_to_num, af_am_1, af_am_2, af_am_3, af_am_4, af_shift_1*0.2-0.2, af_shift_2*0.2-0.2, af_shift_3*0.2-0.2, af_shift_4*0.2-0.2, max(data[:,1]), max(data[:,2])])       # Put the four variables and the subtalar angles into a list
Subtalar_matrix_DL=np.array(Subtalar_matrix_DL)                                                        # Transform the list to the matrix
Excel_title=['Variables in number', 'am_front_lateral','am_side_lateral','am_side_medial','am_front_lateral', 'shift_front_lateral', 'shift_side_lateral', 'shift_side_medial', 'shift_front_lateral', 'Max subtalar angle', 'Max ankle angle']              # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel(SelectionPath, 'Results.xls', 'DL_Platform 25', Excel_title, Subtalar_matrix_DL)          # Put the four variables and subtalar angles to an excel
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""


"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  Put the simulation results from the results folders to an excel documents
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# For walk and run, pick up the maximum values between the model with and without AFO
Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
# The folder path of the walk and run
Activity='Run simulation'
Activity_results_file='Walk_states_degrees.mot'
# Activity_folder=Activity+'\Model outputs\\5_ForwardDynamics_2nd\SimulationOutput_Walk_'
Subtalar_matrix_activity=[]
# Open and select the destination folder
root =tkinter.Tk()                                                      # Open the dialog of the file
root.withdraw()
SelectionPath=filedialog.askdirectory()                       # the path of the selected directory
Activity_folder=SelectionPath+'\SimulationOutput_Run_'

# The folder path for model without AFO
output_folder_data_withoutAFO=Activity_folder+'00000000'
data_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_withoutAFO, Results_parameter, Activity_results_file)

# For walk and run, sum the differences of ankle movements over the whole gait
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(1,4), range(4,9), range(1,4), range(2,7)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(0,3), range(0,3), range(0,3), range(0,3)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):
            output_folder_data_AFO=Activity_folder+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            data_AFO= AFO4_ResultsCollection.Simulationresultscollection(output_folder_data_AFO, Results_parameter, Activity_results_file)
            if data_AFO.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                continue
            else:
                # the third module parameter for the curvecomparison module is the i th parameters in the Results_parameter Matrix
                # e.g. Results_parameter_i=1: means subtalar angles,         Results_parameter_i=2: means the ankle angles
                #[diff_total_subtalar, diff_average_subtalar, diff_max_subtalar]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, 1, (min(len(data_withoutAFO), len(data_AFO))-2))
                [diff_total_subtalar, diff_average_subtalar, diff_max_subtalar]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, 1, len(data_withoutAFO))
                # [diff_total_ankle, diff_average_ankle, diff_max_ankle]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, 2, (min(len(data_withoutAFO), len(data_AFO))-2))
                [diff_total_ankle, diff_average_ankle, diff_max_ankle]=AFO4_ResultsCollection.curvecomparison(data_withoutAFO, data_AFO, 2, len(data_withoutAFO))
                # transform the variables to numbers
                Var_to_num=af_am_1*pow(10,7)+af_am_2*pow(10,6)+af_am_3*pow(10,5)+af_am_4*pow(10,4)+af_shift_1*pow(10,3)+af_shift_2*pow(10,2)+af_shift_3*pow(10,1)+af_shift_4
                Subtalar_matrix_activity.append([Var_to_num, af_am_1, af_am_2, af_am_3, af_am_4, af_shift_1*0.2-0.2, af_shift_2*0.2-0.2, af_shift_3*0.2-0.2, af_shift_4*0.2-0.2, diff_average_subtalar, diff_average_ankle])       # Put the four variables and the subtalar angles into a list

Subtalar_matrix_activity=np.array(Subtalar_matrix_activity)                                                        # Transform the list to the matrix
Excel_title=['Variables in number', 'am_front_lateral','am_side_lateral','am_side_medial','am_front_lateral', 'shift_front_lateral', 'shift_side_lateral', 'shift_side_medial', 'shift_front_lateral', 'Subtalar angle differences', 'Ankle angle differences']              # Define the title of the excel
AFO4_ResultsCollection.DLResultstoExcel(SelectionPath, 'Results.xls', Activity, Excel_title, Subtalar_matrix_activity)          # Put the four variables and subtalar angles to an excel
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""


"""
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  3D plot of the simulation results
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
AFO4_ResultsCollection.Excel3Dplot(sheet_name='Gait simulation plot', xs_variable='am_front_medial_value', ys_variable='shift_front_medial', zs_variable='Ankle angle differences')
AFO4_ResultsCollection.Excel3Dplot(sheet_name='Gait simulation plot', xs_variable='am_side_lateral_value', ys_variable='shift_side_lateral', zs_variable='Ankle angle differences')
AFO4_ResultsCollection.Excel3Dplot(sheet_name='Gait simulation plot', xs_variable='am_side_medial_value', ys_variable='shift_side_medial', zs_variable='Ankle angle differences')
AFO4_ResultsCollection.Excel3Dplot(sheet_name='Gait simulation plot', xs_variable='am_front_lateral_value', ys_variable='shift_front_lateral', zs_variable='Ankle angle differences')
"""
AFO4_ResultsCollection.Excel3Dplot(sheet_name='Sheet1', xs_variable='am_front_lateral_value', ys_variable='shift_front_lateral', zs_variable='Objective function2')


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  The objective function for the batch simulation
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ObjectiveFunction=abs(Gait_Subtalar difference)+abs(Gait_Ankle difference)+abs(Run_subtalar difference)+abs(Run_ankle difference)+exp(DL_sub-30)
#AFO4_ResultsCollection.ExcelObjectiveFunction('DL_Platform 25 plot', 'Gait simulation plot', 'Run simulation plot', 'Variables in number')
