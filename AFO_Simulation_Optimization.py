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
    #*****************************************************************************************************************
    # Simulations of drop landing, walk and Running
    #****************************************************************************************************************
    # The drop landing simulation DL
    #AFO0_Simulation.Simulation('AFODroplanding', 'simulation', DesignVariables, 'SimulationOutput_DL_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('AFODroplanding', 'simulation', DesignVariables, str(folder_index), [25, 0, 0]))
    AFO0_Simulation.Simulation(('AFODroplanding', 'simulation', DesignVariables, str(folder_index), [0, -45, -25]))
    # The walking simulation Walk
    #AFO0_Simulation.Simulation('Walk_AFO', 'simulation', DesignVariables, 'SimulationOutput_Walk_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('Walk_AFO', 'simulation', DesignVariables, str(folder_index)))
    # The running simulation Run
    #AFO0_Simulation.Simulation('Run_AFO', 'simulation', DesignVariables, 'SimulationOutput_Run_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('Run_AFO', 'simulation', DesignVariables, str(folder_index)))

    #*****************************************************************************************************************
    # Collect the simulation results for drop landing, walk and running
    #*****************************************************************************************************************
    [AFO_bottom_location, AFO_top_location, theta_0_values, n_elements]=DesignVariables    # Design variables
    #*****************************************************************************
    # For drop landing, collect the maximum subtalar angle and ankle angle, and maximum strap forces, and fatigue strap forces
    #*****************************************************************************
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
    # FL_length_mesh_max_platfrom0=[max(AFO_FL_platform0[0][0]), max(AFO_FL_platform0[1][0]), max(AFO_FL_platform0[2][0]), max(AFO_FL_platform0[3][0])] # The maximum lengths (fatigue lengths) for the four straps from AFO9_MeshMechanics
    FL_length_mesh_max_platfrom0=[max(AFO_FL_platform0[0][0]), max(AFO_FL_platform0[1][0])] # The maximum lengths (fatigue lengths) for the two straps from AFO9_MeshMechanics
    # FL_force_mesh_max_platform0=[max(AFO_FL_platform0[0][1]), max(AFO_FL_platform0[1][1]), max(AFO_FL_platform0[2][1]), max(AFO_FL_platform0[3][1])] # The maximum forces (fatigue forces) for the four straps from AFO9_MeshMechanics
    FL_force_mesh_max_platform0=[max(AFO_FL_platform0[0][1]), max(AFO_FL_platform0[1][1])] # The maximum forces (fatigue forces) for the two straps from AFO9_MeshMechanics
    #print('Max lengths from the AFO9_MeshMechanics: %s'  %(FL_length_mesh_max))
    #print('Max forces from the AFO9_MeshMechanics: %s'  %(FL_force_mesh_max))
    # Fatigue strap forces for drop landing of platform 45 degree
    AFO_FL_platform45=AFO9_MeshMechanics.MeshMechanics(osimModel_platform45, theta_0_values, n_elements) # Get the force-length relationship for the four straps
    # FL_length_mesh_max_platform45=[max(AFO_FL_platform45[0][0]), max(AFO_FL_platform45[1][0]), max(AFO_FL_platform45[2][0]), max(AFO_FL_platform45[3][0])] # The maximum lengths (fatigue lengths) for the four straps from AFO9_MeshMechanics
    FL_length_mesh_max_platform45=[max(AFO_FL_platform45[0][0]), max(AFO_FL_platform45[1][0])] # The maximum lengths (fatigue lengths) for the two straps from AFO9_MeshMechanics
    # FL_force_mesh_max_platform45=[max(AFO_FL_platform45[0][1]), max(AFO_FL_platform45[1][1]), max(AFO_FL_platform45[2][1]), max(AFO_FL_platform45[3][1])] # The maximum forces (fatigue forces) for the four straps from AFO9_MeshMechanics
    FL_force_mesh_max_platform45=[max(AFO_FL_platform45[0][1]), max(AFO_FL_platform45[1][1])] # The maximum forces (fatigue forces) for the two straps from AFO9_MeshMechanics
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
    #print('The differences of strap forces for DL: %s' %(strap_forces_diff_DL))

    #*****************************************************************************
    # For walk, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle, and strap forces for the 4 straps
    #*****************************************************************************
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
    #---------------------------------------------------------------------------------
    # The walk model for calculating the strap_length_ini and fatigue length
    osimModel_walk='Simulation models\Gait simulation'+str(folder_index)+'\Model outputs\\3_RRA\Fullbodymodel_Walk_RRA_final_AFO.osim'
    # Calculate the initial strap length at default postion of walk
    [walk_strap_lengths_ini, walk_strap_forces_ini]=AFO10_OpenSimAPI.Liginitstates(osimModel_walk)
    #---------------------------------------------------------------------------------
    # Collect the fatigue forces for the 4 straps from the AFO mechanics (AFO9_MeshMechanics) for walk
    # Fatigue strap forces for walk
    AFO_FL_walk=AFO9_MeshMechanics.MeshMechanics(osimModel_walk, theta_0_values, n_elements) # Get the force-length relationship for the four straps
    # FL_length_mesh_max_walk=[max(AFO_FL_walk[0][0]), max(AFO_FL_walk[1][0]), max(AFO_FL_walk[2][0]), max(AFO_FL_walk[3][0])] # The maximum lengths (fatigue lengths) for the four straps from AFO9_MeshMechanics
    FL_length_mesh_max_walk=[max(AFO_FL_walk[0][0]), max(AFO_FL_walk[1][0])] # The maximum lengths (fatigue lengths) for the two straps from AFO9_MeshMechanics
    # FL_force_mesh_max_walk=[max(AFO_FL_walk[0][1]), max(AFO_FL_walk[1][1]), max(AFO_FL_walk[2][1]), max(AFO_FL_walk[3][1])] # The maximum forces (fatigue forces) for the four straps from AFO9_MeshMechanics
    FL_force_mesh_max_walk=[max(AFO_FL_walk[0][1]), max(AFO_FL_walk[1][1])] # The maximum forces (fatigue forces) for the two straps from AFO9_MeshMechanics
    #print('Max lengths from the AFO9_MeshMechanics: %s'  %(FL_length_mesh_max))
    #print('Max forces from the AFO9_MeshMechanics: %s'  %(FL_force_mesh_max))
    #---------------------------------------------------------------------------------
    # Collect the maximum ligament (strap) force during the walk simulation
    [Walk_strap_lengths_realtime, Walk_strap_forces_realtime, Walk_strap_lengths_max, Walk_strap_forces_max]=AFO10_OpenSimAPI.LigMechanicsMax (output_folder_walk_AFO, 'cmc_Kinematics_q.sto', osimModel_walk)
    [Walk_strap_lengths_grad, Walk_strap_pene_monitor]=AFO10_OpenSimAPI.LigPeneMonitor(Walk_strap_lengths_realtime, walk_strap_lengths_ini, 0.0045)
    #print('The max strap lengths for Walk: %s' %(Walk_strap_lengths_max))
    #print('The max strap forces for Walk: %s' %(Walk_strap_forces_max))
    #---------------------------------------------------------------------------------
    # Calculate the differences between the maximum real-time strap forces and the fatigure strap forces
    strap_forces_diff_Walk=np.array(Walk_strap_forces_max)-np.array(FL_force_mesh_max_walk)
    #print('The differences of strap forces for DL: %s' %(strap_forces_diff_Walk))


    #*****************************************************************************
    # For running, collect the average differences of muscle forces between the models with and without AFO cross the whole cyecle, and strap forces for the 4 straps
    #*****************************************************************************
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
    #---------------------------------------------------------------------------------
    # The running model for calculating the strap_length_ini and fatigue length
    osimModel_run='Simulation models\Running simulation'+str(folder_index)+'\Model outputs\\3_RRA\Fullbodymodel_Run_RRA_final_AFO.osim'
    # Calculate the initial strap length at default postion of running
    [run_strap_lengths_ini, run_strap_forces_ini]=AFO10_OpenSimAPI.Liginitstates(osimModel_run)
    #---------------------------------------------------------------------------------
    # Collect the fatigue forces for the 4 straps from the AFO mechanics (AFO9_MeshMechanics) for running
    # Fatigue strap forces for running
    AFO_FL_run=AFO9_MeshMechanics.MeshMechanics(osimModel_run, theta_0_values, n_elements) # Get the force-length relationship for the four straps
    # FL_length_mesh_max_run=[max(AFO_FL_run[0][0]), max(AFO_FL_run[1][0]), max(AFO_FL_run[2][0]), max(AFO_FL_run[3][0])] # The maximum lengths (fatigue lengths) for the four straps from AFO9_MeshMechanics
    FL_length_mesh_max_run=[max(AFO_FL_run[0][0]), max(AFO_FL_run[1][0])] # The maximum lengths (fatigue lengths) for the two straps from AFO9_MeshMechanics
    # FL_force_mesh_max_run=[max(AFO_FL_run[0][1]), max(AFO_FL_run[1][1]), max(AFO_FL_run[2][1]), max(AFO_FL_run[3][1])] # The maximum forces (fatigue forces) for the four straps from AFO9_MeshMechanics
    FL_force_mesh_max_run=[max(AFO_FL_run[0][1]), max(AFO_FL_run[1][1])] # The maximum forces (fatigue forces) for the two straps from AFO9_MeshMechanics
    #print('Max lengths from the AFO9_MeshMechanics: %s'  %(FL_length_mesh_max))
    #print('Max forces from the AFO9_MeshMechanics: %s'  %(FL_force_mesh_max))
    #---------------------------------------------------------------------------------
    # Collect the maximum ligament (strap) force during the run simulation
    [Run_strap_lengths_realtime, DL_strap_forces_realtime, Run_strap_lengths_max, Run_strap_forces_max]=AFO10_OpenSimAPI.LigMechanicsMax (output_folder_run_AFO, 'cmc_Kinematics_q.sto', osimModel_run)
    [Run_strap_lengths_grad, Run_strap_pene_monitor]=AFO10_OpenSimAPI.LigPeneMonitor(Run_strap_lengths_realtime, run_strap_lengths_ini, 0.0045)
    #print('The max strap lengths for Run: %s' %(Run_strap_lengths_max))
    #print('The max strap forces for Run: %s' %(Run_strap_forces_max))
    #---------------------------------------------------------------------------------
    # Calculate the differences between the maximum real-time strap forces and the fatigure strap forces
    strap_forces_diff_Run=np.array(Run_strap_forces_max)-np.array(FL_force_mesh_max_run)
    #print('The differences of strap forces for DL: %s' %(strap_forces_diff_Run))

    #---------------------------------------------------------------------------------
    # Put the subtalar and angles angle, muscle differences and strap forces into three matrixes
    # The subtalar and ankle angles for drop landing with different platform orientations (0 and 45 degrees)
    Angles_DL=[Subtalar_DL_max_platform0, Subtalar_DL_max_platform45, Ankle_DL_max_platform0, Ankle_DL_max_platform45]
    # The normalized muscle forces differences for walk and running
    Muscles_diff=[diff_average_musforce_total_walk_norm, diff_average_musforce_total_run_norm]
    # The differences of strap forces between simulation and fatigue values
    strap_forces_diff=[strap_forces_diff_DL_platform0, strap_forces_diff_DL_platform45, strap_forces_diff_Walk, strap_forces_diff_Run]
    # The penetration status of the strap during simulation
    strap_pene_monitor=[DL_strap_pene_monitor_platform0, DL_strap_pene_monitor_platform45, Walk_strap_pene_monitor, Run_strap_pene_monitor]
    return Angles_DL, Muscles_diff, strap_forces_diff, strap_pene_monitor
    #
def Main_model_demo (DesignVariables, folder_index):
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Simulations of drop landing, walk and Running
    # The drop landing simulation DL
    #AFO0_Simulation.Simulation('AFODroplanding', 'simulation', DesignVariables, 'SimulationOutput_DL_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('AFODroplanding', 'model', DesignVariables, str(folder_index), [25, 0, 0]))
    AFO0_Simulation.Simulation(('AFODroplanding', 'model', DesignVariables, str(folder_index), [0, -45, -25]))
    # The walking simulation Walk
    #AFO0_Simulation.Simulation('Walk_AFO', 'simulation', DesignVariables, 'SimulationOutput_Walk_AFO'+str(folder_index))
    AFO0_Simulation.Simulation(('Walk_AFO', 'model', DesignVariables, str(folder_index)))
    # The running simulation Run
    AFO0_Simulation.Simulation(('Run_AFO', 'model', DesignVariables, str(folder_index)))
