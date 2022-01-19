# -*- coding: utf-8 -*-
import math
import AFO_Simulation_Optimization
import numpy as np
import copy
import multiprocessing

def objective(Subtalar_drop, MusDiff_walk, MusDiff_run, n_elements):
	# This is the cost function
	# to put the value of the cost function calculated for that simulation
	Func=abs(MusDiff_walk)+abs(MusDiff_run)+np.maximum(0, (Subtalar_drop-15))+n_elements/100
	return Func

# Module used to calculate the gradient for each design parameter for each strap, including run the simulation and calculate the bojective function due to small change, calculate the gradient
def Gradient_calculation(solution_smallchange, Objective_ini):
	# Run the simulation of drop landing, walk and running
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution_smallchange)
	# Calculate the objective function for the solution with small change     # np.sum(solution_smallchange[3]) is the total element numbers for all the straps
	Objective_SmallChange=objective(Subtablar_drop, MusDiff_walk, MusDiff_run, np.sum(solution_smallchange[3]))
	# Calculate the  gradient after the small change
	Gradient=Objective_SmallChange - Objective_ini
	return Gradient

# derivative of objective function
def derivative(solution):
	# Input a small increase for each design parameter
	# V_increment=[[0.5,0.5,0.5,0.5], [0.5,0.5,0.5,0.5],[1,1,1,1],[0.2,0.2,0.2,0.2]]
	V_increment=[1,1,1,5]                           # Small increment for AFO_bottom_location, AFO_strap_orientations, AFO_FL_amplification and AFO_FL_shift respectively
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Calculate cost function for initial solution
	[AFO_bottom_location, AFO_strap_orientation, theta_0_values, n_elements]=solution
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution)
	Objective_ini=objective(Subtablar_drop, MusDiff_walk, MusDiff_run, np.sum(solution[3]))
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Small change for the design variables
	# Small chaneg for the design variable_AFO_bottom_location for strap1, strap2, strap3 amd strap4
	solution_bottom_location_smallchange1, solution_bottom_location_smallchange2=copy.deepcopu(solution), copy.deepcopu(solution)
	solution_bottom_location_smallchange3, solution_bottom_location_smallchange4=copy.deepcopu(solution), copy.deepcopu(solution)
	solution_bottom_location_smallchange1[0][0]+=V_increment[0]; solution_bottom_location_smallchange2[0][1]+=V_increment[0]
	solution_bottom_location_smallchange3[0][2]+=V_increment[0]; solution_bottom_location_smallchange4[0][3]+=V_increment[0]
	# Small change for the design variable_AFO_strap_orientation for strap1, strap2, strap3 amd strap4
	solution_strap_orientation_smallchange1, solution_strap_orientation_smallchange2=copy.deepcopu(solution), copy.deepcopu(solution)
	solution_strap_orientation_smallchange3, solution_strap_orientation_smallchange4=copy.deepcopu(solution), copy.deepcopu(solution)
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

	solution_smallchange_list=[solution_bottom_location_smallchange1, solution_bottom_location_smallchange2, solution_bottom_location_smallchange3, solution_bottom_location_smallchange4,
	                                             solution_strap_orientation_smallchange1, solution_strap_orientation_smallchange2, solution_strap_orientation_smallchange3, solution_strap_orientation_smallchange4,
												 solution_theta_0_values_smallchange1, solution_theta_0_values_smallchange2, solution_theta_0_values_smallchange3, solution_theta_0_values_smallchange4,
												 solution_n_elements_smallchange1, solution_n_elements_smallchange2, solution_n_elements_smallchange3, solution_n_elements_smallchange4]
	Gradient=[]
	pool=Pool(processes=16)
	for solution_smallchange in solution_smallchange_list:
		gradient_temp=pool.apply_async(Gradient_calculation, (solution_smallchange, Objective_ini))
		Gradient.append(gradient_temp.get())
	pool.close()
	pool.join()
	return Gradient

	
	# AFO_bottom_location for strap 1
	# Cost function for small increased AFO_bottom_location for strap 1
	solution_bottom_location_smallchange1=copy.deepcopu(solution)
	solution_bottom_location_smallchange1[0][0]+=V_increment[0]
	# Call the module Gradient_calculation to calculate the gradient for AFO_bottom_location of strap 1
	p11=multiprocessing.Process(target=Gradient_calculation, args=(solution_bottom_location_smallchange1, Objective_ini))
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strap 2
	solution_bottom_location_smallchange2=copy.deepcopu(solution)
	solution_bottom_location_smallchange2[0][1]+=V_increment[0]
	p12=multiprocessing.Process(target=Gradient_calculation, args=(solution_bottom_location_smallchange2, Objective_ini))
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strap 3
	solution_bottom_location_smallchange3=copy.deepcopu(solution)
	solution_bottom_location_smallchange3[0][2]+=V_increment[0]
	p13=multiprocessing.Process(target=Gradient_calculation, args=(solution_bottom_location_smallchange3, Objective_ini))
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strap 4
	solution_bottom_location_smallchange4=copy.deepcopu(solution)
	solution_bottom_location_smallchange4[0][3]+=V_increment[0]
	p14=multiprocessing.Process(target=Gradient_calculation, args=(solution_bottom_location_smallchange4, Objective_ini))
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable AFO_strap_orientation
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 1
	# Cost function for small increased AFO_strap_orientation for strap 1
	solution_strap_orientation_smallchange1=copy.deepcopy(solution)
	solution_strap_orientation_smallchange1+=V_increment[1]
	# Call the module Gradient_calculation to calculate the gradient for AFO_strap_orientation of strap 1
	p21=multiprocessing.Process(target=Gradient_calculation, args=(solution_strap_orientation_smallchange1, Objective_ini))
	#--------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 2
	solution_strap_orientation_smallchange2=copy.deepcopy(solution)
	solution_strap_orientation_smallchange2+=V_increment[1]
	p22=multiprocessing.Process(target=Gradient_calculation, args=(solution_strap_orientation_smallchange2, Objective_ini))
	#--------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 3
	solution_strap_orientation_smallchange3=copy.deepcopy(solution)
	solution_strap_orientation_smallchange3+=V_increment[1]
	p23=multiprocessing.Process(target=Gradient_calculation, args=(solution_strap_orientation_smallchange3, Objective_ini))
	#--------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 4
	solution_strap_orientation_smallchange4=copy.deepcopy(solution)
	solution_strap_orientation_smallchange4+=V_increment[1]
	p24=multiprocessing.Process(target=Gradient_calculation, args=(solution_strap_orientation_smallchange4, Objective_ini))
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable theta_0_values
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# theta_0_values for strap 1
	# Cost function for small increased theta_0_values for strap 1
	solution_theta_0_values_smallchange1=copy.deepcopy(solution)
	solution_theta_0_values_smallchange1+=V_increment[2]
	# Call the module Gradient_calculation to calculate the gradient for theta_0_values of strap 1
	p31=multiprocessing.Process(target=Gradient_calculation, args=(solution_theta_0_values_smallchange1, Objective_ini))
	#--------------------------------------------------------------------------------------
	# theta_0_values for strap 2
	solution_theta_0_values_smallchange2=copy.deepcopy(solution)
	solution_theta_0_values_smallchange2+=V_increment[2]
	p32=multiprocessing.Process(target=Gradient_calculation, args=(solution_theta_0_values_smallchange2, Objective_ini))
	#--------------------------------------------------------------------------------------
	# theta_0_values for strap 3
	solution_theta_0_values_smallchange3=copy.deepcopy(solution)
	solution_theta_0_values_smallchange3+=V_increment[2]
	p33=multiprocessing.Process(target=Gradient_calculation, args=(solution_theta_0_values_smallchange3, Objective_ini))
	#--------------------------------------------------------------------------------------
	# theta_0_values for strap 4
	solution_theta_0_values_smallchange4=copy.deepcopy(solution)
	solution_theta_0_values_smallchange4+=V_increment[2]
	p34=multiprocessing.Process(target=Gradient_calculation, args=(solution_theta_0_values_smallchange4, Objective_ini))
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable n_elements
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# n_elements for strap 1
	# Cost function for small increased n_elements for strap 1
	solution_n_elements_smallchange1=copy.deepcopy(solution)
	solution_n_elements_smallchange1+=V_increment[3]
	# Call the module Gradient_calculation to calculate the gradient for n_elements of strap 1
	p41=multiprocessing.Process(target=Gradient_calculation, args=(solution_n_elements_smallchange1, Objective_ini))
	#--------------------------------------------------------------------------------------
	# n_elements for strap 2
	solution_n_elements_smallchange2=copy.deepcopy(solution)
	solution_n_elements_smallchange2+=V_increment[3]
	p42=multiprocessing.Process(target=Gradient_calculation, args=(solution_n_elements_smallchange2, Objective_ini))
	#--------------------------------------------------------------------------------------
	# n_elements for strap 3
	solution_n_elements_smallchange3=copy.deepcopy(solution)
	solution_n_elements_smallchange3+=V_increment[3]
	p43=multiprocessing.Process(target=Gradient_calculation, args=(solution_n_elements_smallchange3, Objective_ini))
	#--------------------------------------------------------------------------------------
	# n_elements for strap 4
	solution_n_elements_smallchange4=copy.deepcopy(solution)
	solution_n_elements_smallchange4+=V_increment[3]
	p44=multiprocessing.Process(target=Gradient_calculation, args=(solution_n_elements_smallchange4, Objective_ini))

	p11.start(); p12.start(); p13.start(); p14.start();  p21.start(); p22.start(); p23.start(); p24.start()
	p31.start(); p32.start(); p33.start(); p34.start();  p41.start(); p42.start(); p43.start(); p44.start()
	p11.join(); p12.join(); p13.join(); p14.join(); p21.join(); p22.join(); p23.join(); p24.join()
	p31.join(); p32.join(); p33.join(); p34.join(); p41.join(); p42.join(); p43.join(); p44.join()

	return [[Gradient_bottom_location_strap1, Gradient_bottom_location_strap2, Gradient_bottom_location_strap3, Gradient_bottom_location_strap4],
                [Gradient_strap_orientation_strap1, Gradient_strap_orientation_strap2, Gradient_strap_orientation_strap3, Gradient_strap_orientation_strap4],
			    [Gradient_theta_0_values_strap1, Gradient_theta_0_values_strap2, Gradient_theta_0_values_strap3, Gradient_theta_0_values_strap4],
			    [Gradient_n_elements_strap1, Gradient_n_elements_strap2, Gradient_n_elements_strap3, Gradient_n_elements_strap4]]
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
	solution = [[14, 101, 259, 346], [-40, 0, 0, 50], [20.34, 21.20, 13.18, 18.9], [30, 100, 100, 30]]
	bounds_upper=[[180, 180, 360, 360], [70, 70, 70, 70], [21.8, 21.8, 21.8, 21.8], [300,300,300,300]]
	bounds_low=[[0, 0, 180, 180], [-70, -70, -70, -70], [0,0,0,0], [0,0,0,0]]

    #it is just a starting point for the optimisation
    # run the gradient descent
	for i in range(n_iter):
		# calculate gradient
		solution=list(solution)
		#--------------------------------------------------------------------------
		# Compare the solution with the upper and low bounds
		cmp_boundslow=solution>bounds_low     # compare solution and bounds_low, if the values in solution bigger than bounds_low, then return true
		cmp_boundsupper=solution<bounds_upper
		# If solution exceeds the bounds_low or bounds_upper, then update the solution with bounds
		[bounds_low, solution, bounds_upper]=np.array([bounds_low, solution, bounds_upper])
		solution=np.maximum(bounds_low, solution) # if solution is lower than bounds_low, update the solution with bounds_low
		solution=np.minimum(solution, bounds_upper)
		# record whether the solution reach the bounds or not, if solution is within the bounds, retunr true, otherwise, return false
		cmp_marker=np.logical_and(bounds_low<solution, solution<bounds_upper)
		#--------------------------------------------------------------------------
		gradient = derivative(solution)
		# take a step
		solution = np.array(solution) - step_size * np.array(gradient)
		# evaluate candidate point
		"""
		[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution)
		# Calculate the objective function for the solution with small change
		Objective_eval=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
		# report progress
		print('>%d f(%s) = %.5f' % (i, solution, solution_eval))
		"""
		print('>%d f(%s) = %.5f' % (i, solution))
	# return [solution, solution_eval]
	return solution

# define the total iterations
n_iter = 2
# define the step size, this value is something you'll probably need to experiment with
step_size = 0.5
# perform the gradient descent search
#best, score = gradient_descent(objective, derivative, n_iter, step_size)
best= gradient_descent(objective, derivative, n_iter, step_size)
print('Done!')
#print('f(%s) = %f' % (best, score))
print('f(%s) = %f' % (best))
