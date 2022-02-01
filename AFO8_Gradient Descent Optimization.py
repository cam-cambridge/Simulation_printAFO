# -*- coding: utf-8 -*-
import math
import AFO_Simulation_Optimization
import numpy as np
import copy
import multiprocessing
from multiprocessing import Pool
import os

def objective(subtalar_drop, MusDiff_walk, MusDiff_run, n_elements):
	# This is the cost function
	# to put the value of the cost function calculated for that simulation
	Func=abs(MusDiff_walk)+abs(MusDiff_run)+np.maximum(0, (subtalar_drop-15))+n_elements/100
	return Func
	#
# Module used to calculate the gradient for each design parameter for each strap, including run the simulation and calculate the bojective function due to small change, calculate the gradient
def Gradient_calculation(solution_smallchange_list):
	solution_smallchange=solution_smallchange_list[0]
	Objective_ini=solution_smallchange_list[1]
	folder_index=solution_smallchange_list[2]
	# Run the simulation of drop landing, walk and running
	[subtalar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution_smallchange, str(folder_index))
	# Calculate the objective function for the solution with small change     # np.sum(solution_smallchange[3]) is the total element numbers for all the straps
	Objective_SmallChange=objective(subtalar_drop, MusDiff_walk, MusDiff_run, np.sum(solution_smallchange[3]))
	# Calculate the  gradient after the small change
	Gradient=Objective_SmallChange - Objective_ini
	return Gradient
	#
# derivative of objective function
def derivative(solution):
	# Input a small increase for each design parameter
	# V_increment=[[0.5,0.5,0.5,0.5], [0.5,0.5,0.5,0.5],[1,1,1,1],[0.2,0.2,0.2,0.2]]
	V_increment=[1,1,1,5]                           # Small increment for AFO_bottom_location, AFO_strap_orientations, AFO_FL_amplification and AFO_FL_shift respectively
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Calculate cost function for initial solution
	[AFO_bottom_location, AFO_strap_orientation, theta_0_values, n_elements]=solution
	[subtalar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution, 0)
	Objective_ini=objective(subtalar_drop, MusDiff_walk, MusDiff_run, np.sum(solution[3]))
	# Track the simulation results and objective function during iteration loops
	Simulation_results_tracker=[subtalar_drop, MusDiff_walk, MusDiff_run, Objective_ini]
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Small change for the design variables
	# Small chaneg for the design variable_AFO_bottom_location for strap1, strap2, strap3 amd strap4
	solution_bottom_location_smallchange1, solution_bottom_location_smallchange2=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_bottom_location_smallchange3, solution_bottom_location_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_bottom_location_smallchange1[0][0]+=V_increment[0]; solution_bottom_location_smallchange2[0][1]+=V_increment[0]
	solution_bottom_location_smallchange3[0][2]+=V_increment[0]; solution_bottom_location_smallchange4[0][3]+=V_increment[0]
	# Small change for the design variable_AFO_strap_orientation for strap1, strap2, strap3 amd strap4
	solution_strap_orientation_smallchange1, solution_strap_orientation_smallchange2=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_strap_orientation_smallchange3, solution_strap_orientation_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_strap_orientation_smallchange1[1][0]+=V_increment[1]; solution_strap_orientation_smallchange2[1][1]+=V_increment[1]
	solution_strap_orientation_smallchange3[1][2]+=V_increment[1]; solution_strap_orientation_smallchange4[1][3]+=V_increment[1]
	# Small change for the design variable_theta_0_values
	solution_theta_0_values_smallchange1, solution_theta_0_values_smallchange2=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_theta_0_values_smallchange3, solution_theta_0_values_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_theta_0_values_smallchange1[2][0]+=V_increment[2]; solution_theta_0_values_smallchange2[2][1]+=V_increment[2]
	solution_theta_0_values_smallchange3[2][2]+=V_increment[2]; solution_theta_0_values_smallchange4[2][3]+=V_increment[2]
	# Small change for the design variable_n_elements
	solution_n_elements_smallchange1, solution_n_elements_smallchange2=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_n_elements_smallchange3, solution_n_elements_smallchange4=copy.deepcopy(solution), copy.deepcopy(solution)
	solution_n_elements_smallchange1[3][0]+=V_increment[3]; solution_n_elements_smallchange2[3][1]+=V_increment[3]
	solution_n_elements_smallchange3[3][2]+=V_increment[3]; solution_n_elements_smallchange4[3][3]+=V_increment[3]
	solution_smallchange_list=[(solution_bottom_location_smallchange1, Objective_ini, 1), (solution_bottom_location_smallchange2, Objective_ini, 2),
	                                              (solution_bottom_location_smallchange3, Objective_ini, 3), (solution_bottom_location_smallchange4, Objective_ini, 4),
	                                              (solution_strap_orientation_smallchange1, Objective_ini, 5), (solution_strap_orientation_smallchange2, Objective_ini, 6),
												  (solution_strap_orientation_smallchange3, Objective_ini, 7), (solution_strap_orientation_smallchange4, Objective_ini, 8),
												  (solution_theta_0_values_smallchange1, Objective_ini, 9), (solution_theta_0_values_smallchange2, Objective_ini, 10),
												  (solution_theta_0_values_smallchange3, Objective_ini, 11), (solution_theta_0_values_smallchange4, Objective_ini, 12),
												  (solution_n_elements_smallchange1, Objective_ini, 13), (solution_n_elements_smallchange2, Objective_ini, 14),
												  (solution_n_elements_smallchange3, Objective_ini, 15), (solution_n_elements_smallchange4, Objective_ini, 16)]
    # The parallel simulation for 16 simulations of drop landing, walk and run
	pool=multiprocessing.Pool()
	Gradient=pool.map(Gradient_calculation, solution_smallchange_list)
	Gradient=np.array(Gradient).reshape(4,4).tolist()
	return Gradient, Simulation_results_tracker

#here you need to calculate the difference in the cost function caused by a small change in every design parameter
#So, for every design parameter (mesh stiffness, mesh strain when high stiffness occurs, mesh orientation etc)
#input a small increase while keeping the other design parameters constant
#and compare the outcome of the cost function that results. that difference in the cost function
# caused by the small change in design parameter is then the "gradient".
#What the best small change is is something you'll have to experiment with,
#but it can be different for each design parameter

# This defines the gradient descent algorithm
def gradient_descent(objective, derivative, n_iter, step_size):
	# generate an initial point
	# solution: This is any combination of design parameters. It doesn't matter what the combination is,
	# solution=[AFO_bottom_location, AFO_strap_orientations, theta_0_values, n_elements]
	solution = [[14, 101, 259, 346], [-20, 0, 0, 20], [20.34, 21.20, 13.18, 18.9], [30, 100, 100, 30]]
	bounds_upper=[[180, 180, 360, 360], [70, 70, 70, 70], [21.8, 21.8, 21.8, 21.8], [300,300,300,300]]
	bounds_low=[[0, 0, 180, 180], [-70, -70, -70, -70], [0.1,0.1,0.1,0.1], [0,0,0,0]]

    #it is just a starting point for the optimisation
    # run the gradient descent
	for i in range(n_iter):
		# calculate gradient
		solution=list(solution)                  # Transfer the solution from other types into list type
		#--------------------------------------------------------------------------
		# Compare the solution with the upper and low bounds
		cmp_boundslow=solution>bounds_low     # compare solution and bounds_low, if the values in solution bigger than bounds_low, then return true
		cmp_boundsupper=solution<bounds_upper
		# If solution exceeds the bounds_low or bounds_upper, then update the solution with bounds
		[bounds_low, solution, bounds_upper]=np.array([bounds_low, solution, bounds_upper])
		solution=np.maximum(bounds_low, solution) # if solution is lower than bounds_low, update the solution with bounds_low
		solution=np.minimum(solution, bounds_upper) # if solution is larger than bounds_upper, update the solution with bounds_upper
		# record whether the solution reach the bounds or not, if solution is within the bounds, retunr true, otherwise, return false
		cmp_marker=np.logical_and(bounds_low<solution, solution<bounds_upper)
		#--------------------------------------------------------------------------
		solution[3]=list(map(int, solution[3]))      # Make sure the design variables n_element are integer type
		gradient, simulation_results_tracker = derivative(solution)
		# record the history of solution,simulation results, cost function
		Simulation_results_tracker_list=[]
		Solution_tracker_list=[]
		Simulation_results_tracker_list.append(simulation_results_tracker)
		Solution_tracker_list.append(solution)
		#--------------------------------------------------------------------------
		# print iteration history to txt file
		path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
        path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
		with open (os.path.join(path_simulation, 'log.txt'), 'a') as f:
			print('The number of iteration: %d \n' %(i), file=f)
			print('The solution track: \n %s\n' %(solution), file=f)
			print('The gradient track: \n %s\n' %(gradient), file=f)
			print('The simulation results track: \n %s' %(simulation_results_tracker), file=f)
		#--------------------------------------------------------------------------
		# take a step
		solution = np.array(solution) - step_size * np.array(gradient)
		with open(os.path.join(path_simulation, 'log.txt'), 'a') as f:
			print('The updated solution: \n %s' % (solution), file=f)
			print('#####################################################################################################', file=f)
	# evaluate final candidate point
	[subtalar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution, 1000)
	# Calculate the final objective function
	Objective_final=objective(subtalar_drop, MusDiff_walk, MusDiff_run, np.sum(solution[3]))
	Simulation_results_tracker_list.append([subtalar_drop, MusDiff_walk, MusDiff_run, Objective_final])
	Solution_tracker_list.append(solution)
	return Solution_tracker_list, Simulation_results_tracker_list

if __name__ == '__main__':
	# define the total iterations
	n_iter = 10
	# define the step size, this value is something you'll probably need to experiment with
	step_size = 0.01
	# perform the gradient descent search
	#best, score = gradient_descent(objective, derivative, n_iter, step_size)
	solution_tracker, simulation_results_tracker= gradient_descent(objective, derivative, n_iter, step_size)
	print('Done!')
	#print('f(%s) = %f' % (best, score))
	print('Solution history: \n %s' %(solution_tracker))
	print('Simulation results and cost function history: \n %s' %(simulation_results_tracker))
