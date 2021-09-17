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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# New AFO design in the musculoskeletal model with stripe orientations
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#AFO0_Simulation.Simulation('AFODroplanding', 'model', 'Simulationoutput')
#AFO0_Simulation.Simulation('Walk_AFO', 'model', 'Gait results collection')
#AFO0_Simulation.Simulation('RRA_run', 'model', 'Gait results collection')
#AFO0_Simulation.Simulation('Run_AFO', 'model', 'Model outputs')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Batch simulation for the DL, walk and run
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for af_am_1, af_am_2, af_am_3, af_am_4 in itertools.product(range(11,12), range(17,18), range(6,7), range(6,7)):     # Design parameters of force-length amplification
    for af_shift_1, af_shift_2, af_shift_3, af_shift_4 in itertools.product(range(5,6), range(5,6), range(5,6), range(5,6)):   # Design parameters of force-length shift
        for strip_ori_1, strip_ori_2, strip_ori_3, strip_ori_4 in itertools.product(range(0,1), range(0,1), range(0,1), range(0,1)):       # Deisgn parameters of stripe orientation
            # The scaling of force-length relationship
            FL_amplification_1=af_am_1*5
            FL_amplification_2=af_am_2*5
            FL_amplification_3=af_am_3*5
            FL_amplification_4=af_am_4*5
            # The shift of force-length relationship
            FL_shift_1=af_shift_1*0.04-0.2
            FL_shift_2=af_shift_2*0.04-0.2
            FL_shift_3=af_shift_3*0.04-0.2
            FL_shift_4=af_shift_4*0.04-0.2
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
            #ResultDirectory_DL='SimulationOutput_DL_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            #AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory_DL)
            # The walking simulation Walk
            ResultDirectory_Walk='SimulationOutput_Walk_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            AFO0_Simulation.Simulation('Walk_AFO', 'model', ResultDirectory_Walk)
            # The running simulation Run
            #ResultDirectory_Run='SimulationOutput_Run_'+str(af_am_1)+str(af_am_2)+str(af_am_3)+str(af_am_4)+str(af_shift_1)+str(af_shift_2)+str(af_shift_3)+str(af_shift_4)
            #AFO0_Simulation.Simulation('Run_AFO', 'simulation', ResultDirectory_Run)
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Resume the design parameters to origin value in the AFO design parameter files
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_1, -FL_shift_1, 'AFO_FLrelationship_one')
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_2, -FL_shift_2, 'AFO_FLrelationship_two')
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_3, -FL_shift_3, 'AFO_FLrelationship_three')
            AFO3_ParaTestSelect.AFOmaterialVariables(1/FL_amplification_4, -FL_shift_4, 'AFO_FLrelationship_four')
            AFO3_ParaTestSelect.AFOmaterialVariables(-Strip_orientation,-Strip_orientation,'AFO_stripe_orientations')
            #-------------------------------------------------------------------------------------------------------------------------------------------------------------------

            """
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            #  Put the simulation results from the results folders to an excel documents
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
            Subtalar_matrix=[]
            for asi in range (4,13):                                        # The number of the amplification variables for side FL relationship
                for afj in range (4,13):                                    # The number of the amplification variables for front FL relationship
                    for ssm in range (0,10):                              # The number of the shift variables for side FL relationship
                        for sfn in range (0,10):                           # The number of the shift variables for front FL relationship
                            output_folder=ResultDirectory='Drop landing_platform30\SimulationOutput_DL_'+str(asi)+str(afj)+str(ssm)+str(sfn)                # The folder of the FD results
                            data= AFO4_ResultsCollection.Simulationresultscollection(output_folder, Results_parameter, 'default_states_degrees.mot')                        # put the specified results into a matrix
                            if data.size==0:                                # If the folder does not exit, skip the current loop to the next one.
                                continue
                            else:
                                Subtalar_matrix.append([asi*10, afj*10, ssm*0.04-0.2, sfn*0.04-0.2, max(data[:,1]), max(data[:,2])])           # Put the four variables and the subtalar angles into a list
            Subtalar_matrix=np.array(Subtalar_matrix)                                                        # Transform the list to the matrix
            Excel_title=['Side_amplification','Front_amplification','Side_shift','Front_shift','Max subtalar angle', 'Max ankle angle']              # Define the title of the excel
            AFO4_ResultsCollection.DLResultstoExcel('Drop landing_platform30', 'DL Results.xls', 'Platform 30', Excel_title, Subtalar_matrix)          # Put the four variables and subtalar angles to an excel
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            """
