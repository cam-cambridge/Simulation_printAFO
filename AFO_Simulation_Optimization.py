import AFO0_Simulation
import AFO1_DesignParameter
import os
import AFO2_MBDModel
import AFO3_ParaTestSelect
import numpy as np
import AFO4_ResultsCollection
import pandas as pd
import itertools
import math
import multiprocessing
from multiprocessing import Pool
import AFO9_MeshMechanics
import AFO10_OpenSimAPI

def Main_Simulation (DesignVariables, folder_index):
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Simulations of drop landing, walk and Running
    #-----------------------------------------------------------------------------
    # The drop landing simulation DL
    #AFO0_Simulation.Simulation('AFODroplanding', 'simulation', DesignVariables, 'SimulationOutput_DL_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('AFODroplanding', 'simulation', DesignVariables, str(folder_index)))
    # The walking simulation Walk
    #AFO0_Simulation.Simulation('Walk_AFO', 'simulation', DesignVariables, 'SimulationOutput_Walk_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('Walk_AFO', 'simulation', DesignVariables, str(folder_index)))
    # The running simulation Run
    #AFO0_Simulation.Simulation('Run_AFO', 'simulation', DesignVariables, 'SimulationOutput_Run_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('Run_AFO', 'simulation', DesignVariables, str(folder_index)))

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Collect the simulation results for drop landing, walk and running
    #-----------------------------------------------------------------------------
    #****************************************************
    # For drop landing activity, collect the maximum subtalar angle and ankle angle
    Results_parameter_DL=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/ankle_r/ankle_angle_r/value']                                          # The specified parameter to extract
    output_folder_DL='Simulation models\Drop landing'+str(folder_index)+'\DL simulation results\\'+str(folder_index)
    data_DL= AFO4_ResultsCollection.Simulationresultscollection(output_folder_DL, Results_parameter_DL, 'default_states_degrees.mot')      # put the specified results into a matrix
    Subtalar_DL_max=max(data_DL[:,1])                                                                                                                                                                    # The maximum subtalar angle during drop landing
    #-----------------------------------------------------------------------------
    # Collect the maximum ligament (strap) length and force during the drop landing simulation
    osimModel='Simulation models\Drop landing'+str(folder_index)+'\Fullbodymodel_droplanding_AFO.osim'
    [DL_strap_lengths_max, DL_strap_forces_max]=AFO10_OpenSimAPI.LigMechanicsMax (output_folder_DL, 'default_states_degrees.mot', osimModel)

    #-----------------------------------------------------------------------------
    #  For walk, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle
    #****************************************************
    #  inteplote the curve across the whole cycle into lots of points (equal to the time instances for model without AFO) and calculate the differences of muscle forces for these points
    # The parameters collected from the simulation results of walk_the muscle forces for all the muscles in the right leg
    Results_parameter_walk=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r',
                                      'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r',
                                      'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']
    # The folder that includes the results of walking simulation without AFO
    output_folder_walk_withoutAFO='Simulation models\Gait simulation'+str(folder_index)+'\Model outputs\\4_CMC\SimulationOutput_walk_withoutAFO'
    # The total muscle force for all the muscles in the right leg
    data_walk_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_walk_withoutAFO, Results_parameter_walk, 'cmc_MuscleAnalysis_TendonForce.sto')
    # The folder that includes the results of walking simulation with AFO
    output_folder_walk_AFO='Simulation models\Gait simulation'+str(folder_index)+'\Model outputs\\4_CMC\\'+str(folder_index)
    # The total muscle force for all the muscles in the right leg
    data_walk_AFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_walk_AFO, Results_parameter_walk, 'cmc_MuscleAnalysis_TendonForce.sto')
    diff_average_musforce_WholeMuscle_walk=[]
    for muscle_num in range (1, len(data_walk_withoutAFO[0])):
        [diff_total_musforce_walk, diff_average_musforce_walk, diff_max_musforce_walk]=AFO4_ResultsCollection.curvecomparison(data_walk_withoutAFO, data_walk_AFO, muscle_num, len(data_walk_withoutAFO))
        diff_average_musforce_WholeMuscle_walk.append(diff_average_musforce_walk)                                # The matrix include the absolute differences of muscle forces for each musch for each design case
        diff_average_musforce_total_walk=np.sum(diff_average_musforce_WholeMuscle_walk)                     # The total differences of muscle forces for all the muscle in the right legs for each design case
        diff_average_musforce_total_walk_norm=diff_average_musforce_total_walk/85.0668
    #-----------------------------------------------------------------------------
    # Collect the maximum ligament (strap) force during the walk simulation
    osimModel='Simulation models\Gait simulation'+str(folder_index)+'\Model outputs\\3_RRA\Fullbodymodel_Walk_RRA_final_AFO.osim'
    [Walk_strap_lengths_max, Walk_strap_forces_max]=AFO10_OpenSimAPI.LigMechanicsMax (output_folder_walk_AFO, 'cmc_states.sto', osimModel)

    #-----------------------------------------------------------------------------
    #  For running, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle
    #****************************************************
    #  inteplote the curve across the whole cycle into lots of points (equal to the time instances for model without AFO) and calculate the differences of muscle forces for these points
    # The parameters collected from the simulation results of running_the muscle forces for all the muscles in the right leg
    Results_parameter_run=['time', 'addbrev_r', 'addlong_r', 'addmagDist_r', 'addmagIsch_r', 'addmagMid_r', 'addmagProx_r', 'bflh_r', 'bfsh_r', 'edl_r', 'ehl_r', 'fdl_r', 'fhl_r', 'gaslat_r',
                                      'gasmed_r', 'glmax1_r', 'glmax2_r', 'glmax3_r', 'glmed1_r', 'glmed2_r', 'glmed3_r', 'glmin1_r', 'glmin2_r', 'glmin3_r', 'grac_r', 'iliacus_r', 'perbrev_r',
                                      'perlong_r', 'piri_r', 'psoas_r', 'recfem_r', 'sart_r', 'semimem_r', 'semiten_r', 'soleus_r', 'tfl_r', 'tibant_r', 'tibpost_r', 'vasint_r', 'vaslat_r', 'vasmed_r']
    # The folder that includes the results of running simulation without AFO
    output_folder_run_withoutAFO='Simulation models\Running simulation'+str(folder_index)+'\Model outputs\\4_CMC\SimulationOutput_Run_withoutAFO'
    # The total muscle force for all the muscles in the right leg
    data_run_withoutAFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_run_withoutAFO, Results_parameter_run, 'cmc_MuscleAnalysis_TendonForce.sto')
    # The folder that includes the results of running simulation with AFO
    output_folder_run_AFO='Simulation models\Running simulation'+str(folder_index)+'\Model outputs\\4_CMC\\'+str(folder_index)
    # The total muscle force for all the muscles in the right leg
    data_run_AFO=AFO4_ResultsCollection.Simulationresultscollection(output_folder_run_AFO, Results_parameter_run, 'cmc_MuscleAnalysis_TendonForce.sto')
    diff_average_musforce_WholeMuscle_run=[]
    for muscle_num_r in range (1, len(data_run_withoutAFO[0])):
        [diff_total_musforce_run, diff_average_musforce_run, diff_max_musforce_run]=AFO4_ResultsCollection.curvecomparison(data_run_withoutAFO, data_run_AFO, muscle_num_r, len(data_run_withoutAFO))
        diff_average_musforce_WholeMuscle_run.append(diff_average_musforce_run)                                # The matrix include the absolute differences of muscle forces for each musch for each design case
        diff_average_musforce_total_run=np.sum(diff_average_musforce_WholeMuscle_run)                     # The total differences of muscle forces for all the muscle in the right legs for each design case
        diff_average_musforce_total_run_norm=diff_average_musforce_total_run/72.840
    #-----------------------------------------------------------------------------
    # Collect the maximum ligament (strap) force during the runsimulation
    osimModel='Simulation models\Running simulation'+str(folder_index)+'\Model outputs\\3_RRA\Fullbodymodel_Run_RRA_final_AFO.osim'
    [Run_strap_lengths_max, Run_strap_forces_max]=AFO10_OpenSimAPI.LigMechanicsMax (output_folder_run_AFO, 'cmc_states.sto', osimModel)

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Collect the strap lengths and forces during simulation and compare to the fatigue force in AFO mechanics (AFO9_MeshMechanics)
    #-----------------------------------------------------------------------------
    # Collect the maximum ligament (strap) lengths or forces during the DL, walk and run
    strap_lengths=np.vstack((DL_strap_lengths_max, Walk_strap_lengths_max, Run_strap_lengths_max)) # Combine the three max strap lengths for three activities
    strap_forces=np.vstack((DL_strap_forces_max, Walk_strap_forces_max, Run_strap_forces_max)) # Combine the three max strap forces for three activities
    strap_lengths_sim_max=np.max(strap_lengths, axis=0) # The maxim strap lengths for the three activities
    strap_forces_sim_max=np.max(strap_forces, axis=0) # The maxim strap forces for the three activities
    #-----------------------------------------------------------------------------
    # Collect the maximum force in the AFO mechanics (AFO9_MeshMechanics)
    [AFO_bottom_location, AFO_strap_orientations, theta_0_values, n_elements]=DesignVariables  # Design variables
    AFO_FL=AFO9_MeshMechanics.MeshMechanics(AFO_strap_orientations, theta_0_values, n_elements)
    FL_length_mesh_max=[max(AFO_FL[0][0]), max(AFO_FL[1][0]), max(AFO_FL[2][0]), max(AFO_FL[3][0])]
    FL_force_mesh_max=[max(AFO_FL[0][1]), max(AFO_FL[1][1]), max(AFO_FL[2][1]), max(AFO_FL[3][1])]
    #-----------------------------------------------------------------------------
    # Calculate the differences between max strap forces and the fatigue forces
    strap_force_diff=np.array(strap_forces_sim_max)-np.array(FL_force_mesh_max)
    return Subtalar_DL_max, diff_average_musforce_total_walk_norm, diff_average_musforce_total_run_norm, strap_forces_diff
    #
def Main_model_demo (DesignVariables, folder_index):
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Simulations of drop landing, walk and Running
    # The drop landing simulation DL
    #AFO0_Simulation.Simulation('AFODroplanding', 'simulation', DesignVariables, 'SimulationOutput_DL_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('AFODroplanding', 'model', DesignVariables, str(folder_index)))
    # The walking simulation Walk
    #AFO0_Simulation.Simulation('Walk_AFO', 'simulation', DesignVariables, 'SimulationOutput_Walk_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('Walk_AFO', 'model', DesignVariables, str(folder_index)))
    # The running simulation Run
    #AFO0_Simulation.Simulation('Run_AFO', 'simulation', DesignVariables, 'SimulationOutput_Run_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('Run_AFO', 'model', DesignVariables, str(folder_index)))
