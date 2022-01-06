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
    Results_parameter_DL=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
    output_folder_DL='Drop landing\DL simulation results\SimulationOutput_DL_AFO'
    data_DL= AFO4_ResultsCollection.Simulationresultscollection(output_folder_DL, Results_parameter_DL, 'default_states_degrees.mot')      # put the specified results into a matrix
    Subtalar_DL_max=max(data_DL[:,1])                                                                                                                                                                    # The maximum subtalar angle during drop landing

    #-----------------------------------------------------------------------------
    #  For walk, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle
    #  inteplote the curve across the whole cycle into lots of points (equal to the time instances for model without AFO) and calculate the differences of muscle forces for these points
    # The parameters collected from the simulation results of walk_the muscle forces for all the muscles in the right leg
    Results_parameter_walk=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r',
                                      'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r',
                                      'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']
    # The folder that includes the results of walking simulation without AFO
    output_folder_walk_withoutAFO='Gait simulation\Model outputs\\4_CMC\SimulationOutput_walk_withoutAFO'
    # The total muscle force for all the muscles in the right leg
    data_walk_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_walk_withoutAFO, Results_parameter_walk, 'cmc_MuscleAnalysis_TendonForce.sto')
    # The folder that includes the results of walking simulation with AFO
    output_folder_walk_AFO='Gait simulation\Model outputs\\4_CMC\SimulationOutput_walk_AFO'
    # The total muscle force for all the muscles in the right leg
    data_walk_AFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_walk_AFO, Results_parameter_walk, 'cmc_MuscleAnalysis_TendonForce.sto')
    diff_average_musforce_WholeMuscle_walk=[]
    for muscle_num in range (0, len(data_walk_withoutAFO[0])):
        [diff_total_musforce_walk, diff_average_musforce_walk, diff_max_musforce_walk]=AFO4_ResultsCollection.curvecomparison(data_walk_withoutAFO, data_walk_AFO, muscle_num, len(data_walk_withoutAFO))
        diff_average_musforce_WholeMuscle_walk.append(diff_average_musforce_walk)                                # The matrix include the absolute differences of muscle forces for each musch for each design case
        diff_average_musforce_total_walk=np.sum(diff_average_musforce_WholeMuscle_walk)                     # The total differences of muscle forces for all the muscle in the right legs for each design case

    #-----------------------------------------------------------------------------
    #  For running, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle
    #  inteplote the curve across the whole cycle into lots of points (equal to the time instances for model without AFO) and calculate the differences of muscle forces for these points
    # The parameters collected from the simulation results of running_the muscle forces for all the muscles in the right leg
    Results_parameter_run=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r',
                                      'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r',
                                      'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']
    # The folder that includes the results of running simulation without AFO
    output_folder_run_withoutAFO='Running simulation\Model outputs\\4_CMC\SimulationOutput_Run_withoutAFO'
    # The total muscle force for all the muscles in the right leg
    data_run_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_run_withoutAFO, Results_parameter_run, 'cmc_MuscleAnalysis_TendonForce.sto')
    # The folder that includes the results of running simulation with AFO
    output_folder_run_AFO='Running simulation\Model outputs\\4_CMC\SimulationOutput_Run_AFO'
    # The total muscle force for all the muscles in the right leg
    data_run_AFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_run_AFO, Results_parameter_run, 'cmc_MuscleAnalysis_TendonForce.sto')
    diff_average_musforce_WholeMuscle_run=[]
    for muscle_num_r in range (0, len(data_run_withoutAFO[0])):
        [diff_total_musforce_run, diff_average_musforce_run, diff_max_musforce_run]=AFO4_ResultsCollection.curvecomparison(data_run_withoutAFO, data_run_AFO, muscle_num_r, len(data_run_withoutAFO))
        diff_average_musforce_WholeMuscle_run.append(diff_average_musforce_run)                                # The matrix include the absolute differences of muscle forces for each musch for each design case
        diff_average_musforce_total_run=np.sum(diff_average_musforce_WholeMuscle_run)                     # The total differences of muscle forces for all the muscle in the right legs for each design case
    return Subtalar_DL_max, diff_average_musforce_total_walk, diff_average_musforce_total_run
