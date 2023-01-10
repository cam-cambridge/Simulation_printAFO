# Note: this code is developed based on the AFO8_Gradient Descent Optimization, it can output the separate term of strap 4 when calculating the gradient

# -*- coding: utf-8 -*-
import math
import AFO_Simulation_Optimization
import numpy as np
import copy
import multiprocessing
from multiprocessing import Pool
import os


def objective(Angles_DL, Muscles_diff, strap_forces_diff, n_elements):
    # This is the cost function
    # The terms in the cost function
    [Subtalar_DL_max_platform0, Ankle_DL_max_platform0] = Angles_DL  # The angles for drop landing
    # Muscle differences for walk and running for models with and without AFO
    [MusDiff_walk_norm, MusDiff_run_norm] = Muscles_diff
    # Differences of strap forces between simulation and fatigue values
    [strap_forces_diff_DL_platform0, strap_forces_diff_Walk, strap_forces_diff_Run] = strap_forces_diff
    n_elements = np.array(n_elements)
    strap1_forces_diff = np.array([strap_forces_diff_DL_platform0[0],
                                  strap_forces_diff_Walk[0], strap_forces_diff_Run[0]])
    strap2_forces_diff = np.array([strap_forces_diff_DL_platform0[1],
                                  strap_forces_diff_Walk[1], strap_forces_diff_Run[1]])
    Func = (MusDiff_walk_norm*10)**2+(MusDiff_run_norm)**2 + \
        (np.maximum(0, (Subtalar_DL_max_platform0-28)))**2*1e4 +\
        np.sum(strap_forces_diff_DL_platform0**2) + np.sum((np.maximum(
            [0, 0], strap_forces_diff_Walk))**2) + np.sum((np.maximum([0, 0], strap_forces_diff_Run))**2)+np.sum(n_elements)**2/50
    Func_term = [(MusDiff_walk_norm*10)**2+(MusDiff_run_norm)**2,
                 (np.maximum(0, (Subtalar_DL_max_platform0-28)))**2*1e4,
                 np.sum(strap_forces_diff_DL_platform0**2) + np.sum((np.maximum([0, 0], strap_forces_diff_Walk))**2) + np.sum((np.maximum([0, 0], strap_forces_diff_Run))**2), np.sum(n_elements)**2/50]
    return Func, Func_term
    # ----------------------------------------------------------------------
    #
# Module used to calculate the gradient for each design parameter for each strap, including run the simulation and calculate the bojective function due to small change, calculate the gradient


def Gradient_calculation(solution_smallchange_list):
    solution_smallchange = solution_smallchange_list[0]
    Objective_ini = solution_smallchange_list[1][0]
    Objective_ini_term = solution_smallchange_list[1][1]
    folder_index = solution_smallchange_list[2]
    # Run the simulation of drop landing, walk and running
    [Angles_DL, Muscles_diff, strap_forces_diff, strap_pene_monitor] = AFO_Simulation_Optimization.Main_Simulation(
        solution_smallchange, str(folder_index))
    # Calculate the objective function for the solution with small change     # np.sum(solution_smallchange[3]) is the total element numbers for all the straps
    [Objective_Smallchange, Objective_Smallchange_term] = objective(
        Angles_DL, Muscles_diff, strap_forces_diff, np.array(solution_smallchange[3]))
    # Calculate the  gradient after the small change
    Gradient = Objective_Smallchange - Objective_ini
    Gradient_term = list(np.array(Objective_Smallchange_term)-np.array(Objective_ini_term))
    return Gradient, Gradient_term
    #
# derivative of objective function


def derivative(solution, V_increment):
    # Input a small increase for each design parameter
    # V_increment=[[0.5,0.5,0.5,0.5], [0.5,0.5,0.5,0.5],[1,1,1,1],[0.2,0.2,0.2,0.2]]
    # V_increment=[0.5,0.5,0.1,1]                           # Small increment for AFO_bottom_location, AFO_stop_location, AFO_FL_amplification and AFO_FL_shift respectively
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Calculate cost function for initial solution
    [AFO_bottom_location, AFO_top_location, theta_0_values, n_elements] = solution
    [Angles_DL, Muscles_diff, strap_forces_diff,
        strap_pene_monitor] = AFO_Simulation_Optimization.Main_Simulation(solution, 0)
    [Objective_ini_total, Objective_ini_term] = objective(
        Angles_DL, Muscles_diff, strap_forces_diff, np.array(solution[3]))
    Objective_ini = [Objective_ini_total, Objective_ini_term]
    # Track the simulation results and objective function during iteration loops
    Simulation_results_tracker = [Angles_DL, Muscles_diff,
                                  strap_forces_diff, Objective_ini[0], Objective_ini[1]]
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The derivative for design variable
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Small change for the design variables
    # Small chaneg for the design variable_AFO_bottom_location for strap1, strap2, strap3 amd strap4
    solution_bottom_location_smallchange1, solution_bottom_location_smallchange2 = copy.deepcopy(
        solution), copy.deepcopy(solution)
    # solution_bottom_location_smallchange3, solution_bottom_location_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
    solution_bottom_location_smallchange1[0][0] += V_increment[0]
    solution_bottom_location_smallchange2[0][1] += V_increment[0]
    # solution_bottom_location_smallchange3[0][2]+=V_increment[0]; solution_bottom_location_smallchange4[0][3]+=V_increment[0]
    # Small change for the design variable_AFO_top_location for strap1, strap2, strap3 amd strap4
    solution_top_location_smallchange1, solution_top_location_smallchange2 = copy.deepcopy(
        solution), copy.deepcopy(solution)
    # solution_top_location_smallchange3, solution_top_location_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
    solution_top_location_smallchange1[1][0] += V_increment[1]
    solution_top_location_smallchange2[1][1] += V_increment[1]
    # solution_top_location_smallchange3[1][2]+=V_increment[1]; solution_top_location_smallchange4[1][3]+=V_increment[1]
    # Small change for the design variable_theta_0_values
    solution_theta_0_values_smallchange1, solution_theta_0_values_smallchange2 = copy.deepcopy(
        solution), copy.deepcopy(solution)
    # solution_theta_0_values_smallchange3, solution_theta_0_values_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
    solution_theta_0_values_smallchange1[2][0] += V_increment[2]
    solution_theta_0_values_smallchange2[2][1] += V_increment[2]
    # solution_theta_0_values_smallchange3[2][2]+=V_increment[2]; solution_theta_0_values_smallchange4[2][3]+=V_increment[2]
    # Small change for the design variable_n_elements
    solution_n_elements_smallchange1, solution_n_elements_smallchange2 = copy.deepcopy(
        solution), copy.deepcopy(solution)
    # solution_n_elements_smallchange3, solution_n_elements_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
    solution_n_elements_smallchange1[3][0] += V_increment[3]
    solution_n_elements_smallchange2[3][1] += V_increment[3]
    # solution_n_elements_smallchange3[3][2]+=V_increment[3]; solution_n_elements_smallchange4[3][3]+=V_increment[3]
    """
	solution_smallchange_list=[(solution_bottom_location_smallchange1, Objective_ini, 1), (solution_bottom_location_smallchange2, Objective_ini, 2),
	                                              (solution_bottom_location_smallchange3, Objective_ini,
	                                               3), (solution_bottom_location_smallchange4, Objective_ini, 4),
	                                              (solution_top_location_smallchange1, Objective_ini,
	                                               5), (solution_top_location_smallchange2, Objective_ini, 6),
												  (solution_top_location_smallchange3, Objective_ini,
												   7), (solution_top_location_smallchange4, Objective_ini, 8),
												  (solution_theta_0_values_smallchange1, Objective_ini,
												   9), (solution_theta_0_values_smallchange2, Objective_ini, 10),
												  (solution_theta_0_values_smallchange3, Objective_ini,
												   11), (solution_theta_0_values_smallchange4, Objective_ini, 12),
												  (solution_n_elements_smallchange1, Objective_ini,
												   13), (solution_n_elements_smallchange2, Objective_ini, 14),
												  (solution_n_elements_smallchange3, Objective_ini, 15), (solution_n_elements_smallchange4, Objective_ini, 16)]
	"""
    solution_smallchange_list = [(solution_bottom_location_smallchange1, Objective_ini, 1), (solution_bottom_location_smallchange2, Objective_ini, 2),
                                 (solution_top_location_smallchange1, Objective_ini,
                                  3), (solution_top_location_smallchange2, Objective_ini, 4),
                                 (solution_theta_0_values_smallchange1, Objective_ini,
                                  5), (solution_theta_0_values_smallchange2, Objective_ini, 6),
                                 (solution_n_elements_smallchange1, Objective_ini, 7), (solution_n_elements_smallchange2, Objective_ini, 8)]
    # The parallel simulation for 16 simulations of drop landing, walk and run
    pool = multiprocessing.Pool()
    Gradient = pool.map(Gradient_calculation, solution_smallchange_list)
    Gradient_total = [x[0] for x in Gradient]
    Gradient_term = [x[1] for x in Gradient]
    pool.close()
    pool.join()
    # Gradient=np.array(Gradient_total).reshape(4,4).tolist()
    Gradient = np.array(Gradient_total).reshape(4, 2).tolist()
    Gradient_term_strap4element = Gradient_term[0]
    return Gradient, Gradient_term_strap4element, Simulation_results_tracker, strap_pene_monitor
    #
# here you need to calculate the difference in the cost function caused by a small change in every design parameter
# So, for every design parameter (mesh stiffness, mesh strain when high stiffness occurs, mesh orientation etc)
# input a small increase while keeping the other design parameters constant
# and compare the outcome of the cost function that results. that difference in the cost function
# caused by the small change in design parameter is then the "gradient".
# What the best small change is is something you'll have to experiment with,
# but it can be different for each design parameter
# This defines the gradient descent algorithm


def gradient_descent(objective, derivative, n_iter, V_increment_initial):
    # generate an initial point
    # solution: This is any combination of design parameters. It doesn't matter what the combination is,
    # solution=[AFO_bottom_location, AFO_top_location, theta_0_values, n_elements]
    solution = [[73, 287],
                [108, 252],
                [21.8, 21.8],
                [240, 90]]
    bounds_low = [[45, 225], [0, 180], [0.1, 0.1], [1, 1]]
    bounds_upper = [[135, 315], [180, 360], [28, 28], [600, 600]]
# it is just a starting point for the optimisation
# run the gradient descent
    # round_index = 0                                 ############### need to change for restart based on the round_index value
    round_index = 0
    # Obj_r_index = 3                                 ############### need to change for restart based on the results in log file
    Obj_r_index = 3
    # Obj_r = [0, 1, 2, 3]                            ############### need to change for restart based on the results in log file
    Obj_r = [round_index, 1, 2, 3]
    # step_size = 2                                      ############### need to change for restart based on the round_index value
    step_size = 2
    # V_increment = V_increment_initial   ############## need to change for restart based on the round_index value
    V_increment = V_increment_initial

    for i in range(1, n_iter):  # need to change for restart
        # Using a varied increment during optimization
        if abs(Obj_r[Obj_r_index]-Obj_r[Obj_r_index-2])/Obj_r[Obj_r_index] < 0.005 and abs(Obj_r[Obj_r_index-1]-Obj_r[Obj_r_index-3])/Obj_r[Obj_r_index-1] < 0.005 or i > 50*(round_index+1):
            round_index += 1
            Obj_r_index = 3
            Obj_r = [round_index, 1, 2, 3]
            if round_index == 1:
                step_size = 1
                V_increment = V_increment_initial
            elif round_index == 2:
                step_size = 1
                V_increment = [i*0.5 for i in V_increment_initial]
            elif round_index == 3:
                step_size = 0.5
                V_increment = [i*0.5 for i in V_increment_initial]
            elif round_index == 4:
                if i < 100:
                    n_iter = 100
                else:
                    break
        # calculate gradient
        # Transfer the solution from other types into list type
        solution = list(solution)
        # --------------------------------------------------------------------------
        # Compare the solution with the upper and low bounds
        # compare solution and bounds_low, if the values in solution bigger than bounds_low, then return true
        cmp_boundslow = solution > bounds_low
        cmp_boundsupper = solution < bounds_upper
        # If solution exceeds the bounds_low or bounds_upper, then update the solution with bounds
        [bounds_low, solution, bounds_upper] = np.array([bounds_low, solution, bounds_upper])
        # if solution is lower than bounds_low, update the solution with bounds_low
        solution = np.maximum(bounds_low, solution)
        # if solution is larger than bounds_upper, update the solution with bounds_upper
        solution = np.minimum(solution, bounds_upper)
        # record whether the solution reach the bounds or not, if solution is within the bounds, retunr true, otherwise, return false
        cmp_marker = np.logical_and(bounds_low < solution, solution < bounds_upper)
        # --------------------------------------------------------------------------
        # Make sure the design variables n_element are integer type
        solution[3] = list(map(round, solution[3]))
        gradient, gradient_term_strap4element, simulation_results_tracker, strap_pene_monitor = derivative(
            solution, V_increment)
        # record the history of solution,simulation results, cost function
        Simulation_results_tracker_list = []
        Solution_tracker_list = []
        Strap_pene_monitor_list = []
        Simulation_results_tracker_list.append(simulation_results_tracker)
        Solution_tracker_list.append(solution)
        Strap_pene_monitor_list.append(strap_pene_monitor)
        # --------------------------------------------------------------------------
        # print iteration history to txt file
        # The full path for the python scrip folder: python script
        path_script = os.path.realpath(__file__)
        # The path of the folder including the python script: python simulation
        path_simulation = os.path.dirname(os.path.dirname(path_script))
        with open(os.path.join(path_simulation, 'log.txt'), 'a') as f:
            print('The number of iteration: %d \n' % (i), file=f)
            print('The solution track:', file=f)
            print('%s  # The position (central angle) of bottom endpoints for the two straps' %
                  (solution[0]), file=f)
            print('%s  # The position (central angle) of top endpoints for the two straps' %
                  (solution[1]), file=f)
            print('%s  # The start angles of the waves for the two straps' % (solution[2]), file=f)
            print('%s  # The element numbers for the two straps\n' % (solution[3]), file=f)
            print('The gradient track:', file=f)
            print('%s  # The derivative (gradient) of bottom endpoint position for the two straps' %
                  (gradient[0]), file=f)
            print('%s  # The derivative (gradient) of top endpoint position for the two straps' %
                  (gradient[1]), file=f)
            print('%s  # The derivative (gradient) of the start wave angles for the two straps' %
                  (gradient[2]), file=f)
            print('%s  # The derivative (gradient) of the element numbers for the two straps\n' %
                  (gradient[3]), file=f)
            # print('# The separate terms of cost function in gradient of strap 4:', file=f)
            # print('%s # abs(MusDiff_walk_norm), abs(MusDiff_run_norm), n_elements/100' %(gradient_term_strap4element[0:3]), file=f)
            # print('%s # np.maximum(0, (Subtalar_DL_max_platform0-15))*5, np.maximum(0, (Subtalar_DL_max_platform45-15))*5' %(gradient_term_strap4element[3:5]), file=f)
            # print('%s # np.sum(np.maximum([0, 0, 0, 0], strap_forces_diff_DL_platform0)) for drop landing with orientations of 0 and 45, walking and running\n' %(gradient_term_strap4element[5:9]), file=f)
            print('The simulation results track:', file=f)
            print('%s  # The subtalar angles and ankle angle for DL 0 degree' %
                  (simulation_results_tracker[0]), file=f)
            print('%s  # The muscle demand differences between models with and without AFO for walk and running' % (
                simulation_results_tracker[1]), file=f)
            print('# The strap force differences (max real-time strap forces - fatigue strap forces) for the two straps for DL_0 dgree, walk and running', file=f)
            print('%s # The strap force differences for DL_0 degree for the two straps' %
                  (simulation_results_tracker[2][0]), file=f)
            # print('%s # The strap force differences for DL_45 degree for the two straps' %(simulation_results_tracker[2][1]), file=f)
            print('%s # The strap force differences for walk for the two straps' %
                  (simulation_results_tracker[2][1]), file=f)
            print('%s # The strap force differences for running for the two straps\n' %
                  (simulation_results_tracker[2][2]), file=f)
            print('%s   # The individual term 1: the sum of square of the muscle differences for walk and running' % (
                simulation_results_tracker[4][0]), file=f)
            print('%s   # The individual term 2: the sum of square of the (subtalar -28) for DL0' %
                  (simulation_results_tracker[4][1]), file=f)
            print('%s   # The individual term 3: the sum of square of the strap force differences for DL, walk and running' % (
                simulation_results_tracker[4][2]), file=f)
            print('%s   # The individual term 4: the sum of the element numbers\n' %
                  (simulation_results_tracker[4][3]), file=f)
            print('The cost function track:  %s\n' % (simulation_results_tracker[3]), file=f)
            print('The strap penetration status: \n %s' % (strap_pene_monitor), file=f)
        # --------------------------------------------------------------------------
        # take a step
        if solution[3][1] > 1:
            gradient_norm = [[V_increment[0]/max(abs(np.array(gradient[0])))], [V_increment[1]/max(abs(np.array(gradient[1])))], [
                V_increment[2]/max(abs(np.array(gradient[2])))], [V_increment[3]/max(abs(np.array(gradient[3])))]]
        else:
            gradient_norm = [[V_increment[0]/max(abs(np.array(gradient[0])))], [V_increment[1]/max(abs(np.array(gradient[1])))], [
                V_increment[2]/max(abs(np.array(gradient[2])))], [V_increment[3]/(abs(np.array(gradient[3][0])))]]
        step_size_array = (np.array(gradient_norm)*step_size).reshape(-1, 1)
        solution = np.array(solution) - np.array(gradient)*step_size_array
        Obj_r.append(simulation_results_tracker[3])
        Obj_r_index += 1
        with open(os.path.join(path_simulation, 'log.txt'), 'a') as f:
            print('The updated solution (solution - gradient * step_size) track: \n %s' %
                  (solution), file=f)
            print('##################################################################################################### \n', file=f)
            print('The object record: %s\n' % (Obj_r), file=f)
            print('The object record restart: %s' % (Obj_r_index), file=f)
            print('##################################################################################################### \n', file=f)
    # evaluate final candidate point
    [Angles_DL, Muscles_diff, strap_forces_diff,
        strap_pene_monitor] = AFO_Simulation_Optimization.Main_Simulation(solution, 1000)
    # Calculate the final objective function
    Objective_final = objective(Angles_DL, Muscles_diff, strap_forces_diff, np.array(solution[3]))
    Simulation_results_tracker_list.append(
        [Angles_DL, Muscles_diff, strap_forces_diff, Objective_final])
    Solution_tracker_list.append(solution)
    Strap_pene_monitor_list.append(strap_pene_monitor)
    return Solution_tracker_list, Simulation_results_tracker_list, Strap_pene_monitor_list


if __name__ == '__main__':
    # define the total iterations
    # n_iter = 120
    n_iter = 200
    # define the step size, this value is something you'll probably need to experiment with
    # step_size = 0.5
    # The small change for the variables for calculating the gradient, the step size will be determined based on the V_increment
    V_increment_initial = [1, 1, 0.1, 2]
    # perform the gradient descent search
    # best, score = gradient_descent(objective, derivative, n_iter, step_size)
    solution_tracker, simulation_results_tracker, strap_pene_tracker = gradient_descent(
        objective, derivative, n_iter, V_increment_initial)
    print('Done!')
    # print('f(%s) = %f' % (best, score))
    # print('Solution history: \n %s' %(solution_tracker))
    # print('Simulation results and cost function history: \n %s' %(simulation_results_tracker))
