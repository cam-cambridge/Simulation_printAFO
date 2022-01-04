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

def Main_Simulation (AFO_bottom_location, Stripe_orientation, AFO_FL_amplification, AFO_FL_shift):
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Change the design parameters in the AFO design text file
    AFO3_ParaTestSelect.AFOmaterialVariables(AFO_FL_amplification[0], AFO_FL_shift[0], 'AFO_FLrelationship_one')
    AFO3_ParaTestSelect.AFOmaterialVariables(AFO_FL_amplification[1], AFO_FL_shift[1], 'AFO_FLrelationship_two')
    AFO3_ParaTestSelect.AFOmaterialVariables(AFO_FL_amplification[2], AFO_FL_shift[2], 'AFO_FLrelationship_three')
    AFO3_ParaTestSelect.AFOmaterialVariables(AFO_FL_amplification[3], AFO_FL_shift[3], 'AFO_FLrelationship_four')
    AFO3_ParaTestSelect.AFOmaterialVariables(Strip_orientation,Strip_orientation,'AFO_stripe_orientations')
    AFO3_ParaTestSelect.AFOmaterialVariables(bottom_location_angle,bottom_location_angle,'AFO_bottom_location_angle')
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Simulations of drop landing, walk and Running
    # The drop landing simulation DL
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation', 'SimulationOutput_DL_AFO')
    # The walking simulation Walk
    AFO0_Simulation.Simulation('Walk_AFO', 'simulation', 'SimulationOutput_Walk_AFO')
    # The running simulation Run
    AFO0_Simulation.Simulation('Run_AFO', 'simulation', 'SimulationOutput_Run_AFO')
    #-----------------------------------------------------------------------------
    # Resume the design parameters to origin value in the AFO design parameter files: copy a default text into the design text file
    # 1/FL_amplification_1, -FL_shift_1: invalid parameters, 'Resume design file': command for resuming the design parameter txt file
    AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_1, -FL_shift_1, 'Resume design file')
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Collect the simulation results for drop landing, walk and running
    #-----------------------------------------------------------------------------
    # For drop landing activity, collect the maximum subtalar angle and ankle angle
    Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
    Subtalar_matrix_DL=[]

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

    return MusDiff_walk, MusDiff_run, Subtalar_drop
