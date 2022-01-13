# -*- coding: utf-8 -*-
import math
import AFO_Simulation_Optimization
import numpy as np

def objective(Subtalar_drop, MusDiff_walk, MusDiff_run, n_elements):
	# This is the cost function
	# to put the value of the cost function calculated for that simulation
	Func=abs(MusDiff_walk)+abs(MusDiff_run)+math.exp(Subtalar_drop)+e_elements/100
	return Func

# derivative of objective function
def derivative(solution, cmp_marker):
	# Module used to calculate the gradient for each design parameter for each strap, including run the simulation and calculate the bojective function due to small change, calculate the gradient
	def Gradient_calculation(solution, Objective_ini):
		# Run the simulation of drop landing, walk and running
		[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution)
		# Calculate the objective function for the solution with small change
		Objective_SmallChange=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
		# Calculate the  gradient after the small change
		Gradient=Objective_SmallChange - Objective_ini
		return Gradient

	# Input a small increase for each design parameter
	# V_increment=[[0.5,0.5,0.5,0.5], [0.5,0.5,0.5,0.5],[1,1,1,1],[0.2,0.2,0.2,0.2]]
	V_increment=[1,1,1,0.2]                           # Small increment for AFO_bottom_location, AFO_strap_orientations, AFO_FL_amplification and AFO_FL_shift respectively
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# Calculate cost function for initial solution
	[AFO_bottom_location, AFO_strap_orientation, theta_0_values, n_elements]=solution
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(solution)
	Objective_ini=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable AFO_bottom_location
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# AFO_bottom_location for strap 1
	# Cost function for small increased AFO_bottom_location for strap 1
	if cmp_marker[0][0]=='False':
		Gradient_bottom_location_strap1=0
	else:
		AFO_bottom_location[0]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strap 1
		# Call the module Gradient_calculation to calculate the gradient for AFO_bottom_location of strap 1
		Gradient_bottom_location_strap1=Gradient_calculation(solution, Objective_ini)
		AFO_bottom_location[0]-=V_increment[0]                                                                 # recover the data to original solution  for design variable AFO_bottom_location for strap 1
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strap 2
	if cmp_marker[0][1]=='False':
		Gradient_bottom_location_strap2=0
	else:
		AFO_bottom_location[1]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strap 2
		Gradient_bottom_location_strap2=Gradient_calculation(solution, Objective_ini)
		AFO_bottom_location[1]-=V_increment[0]                                                                 # recover the data to original solution  for design variable AFO_bottom_location for strap 2
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strap 3
	if cmp_marker[0][2]=='False':
		Gradient_bottom_location_strap3=0
	else:
		AFO_bottom_location[2]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strap 3
		Gradient_bottom_location_strap3=Gradient_calculation(solution, Objective_ini)
		AFO_bottom_location[2]-=V_increment[0]                                                                 # recover the data to original solution  for design variable AFO_bottom_location for strap 3
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strap 4
	if cmp_marker[0][3]=='False':
		Gradient_bottom_location_strap4=0
	else:
		AFO_bottom_location[3]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strap 4
		Gradient_bottom_location_strap4=Gradient_calculation(solution, Objective_ini)
		AFO_bottom_location[3]-=V_increment[0]                                                                 # recover the data to original solution  for design variable AFO_bottom_location for strap 4
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable AFO_strap_orientation
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 1
	# Cost function for small increased AFO_strap_orientation for strap 1
	if cmp_marker[1][0]=='False':
		Gradient_strap_orientation_strap1=0
	else:
		AFO_strap_orientation[0]+=V_increment[1]                                                                 # small incremen for design variable strap_orientation for strap 1
		# Call the module Gradient_calculation to calculate the gradient for AFO_strap_orientation of strap 1
		Gradient_strap_orientation_strap1=Gradient_calculation(solution, Objective_ini)
		AFO_strap_orientation[0]-=V_increment[1]                                                                 # recover the data to original solution  for design variable strap_orientation for strap 1
	#--------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 2
	if cmp_marker[1][1]=='False':
		Gradient_strap_orientation_strap2=0
	else:
		AFO_strap_orientation[1]+=V_increment[1]                                                                 # small incremen for design variable strap_orientation for strap 2
		Gradient_strap_orientation_strap2=Gradient_calculation(solution, Objective_ini)
		AFO_strap_orientation[1]-=V_increment[1]                                                                 # recover the data to original solution  for design variable strap_orientation for strap 2
	#--------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 3
	if cmp_marker[1][2]=='False':
		Gradient_strap_orientation_strap3=0
	else:
		AFO_strap_orientation[2]+=V_increment[1]                                                                 # small incremen for design variable strap_orientation for strap 3
		Gradient_strap_orientation_strap3=Gradient_calculation(solution, Objective_ini)
		AFO_strap_orientation[2]-=V_increment[1]                                                                 # recover the data to original solution  for design variable strap_orientation for strap 3
	#--------------------------------------------------------------------------------------
	# AFO_strap_orientation for strap 4
	if cmp_marker[1][3]=='False':
		Gradient_strap_orientation_strap4=0
	else:
		AFO_strap_orientation[3]+=V_increment[1]                                                                 # small incremen for design variable strap_orientation for strap 4
		Gradient_strap_orientation_strap4=Gradient_calculation(solution, Objective_ini)
		AFO_strap_orientation[3]-=V_increment[1]                                                                 # recover the data to original solution  for design variable strap_orientation for strap 4
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable AFO_FL_mplification
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# AFO_FL_amplification for strap 1
	# Cost function for small increased AFO_FL_amplification for strap 1
	if cmp_marker[2][0]=='False':
		Gradient_theta_0_values_strap1=0
	else:
		theta_0_values[0]+=V_increment[2]                                                                 # small incremen for design variable AFO_FL_amplification for strap 1
		# Call the module Gradient_calculation to calculate the gradient for AFO_FL_mplification of strap 1
		Gradient_theta_0_values_strap1=Gradient_calculation(solution, Objective_ini)
		theta_0_values[0]-=V_increment[2]                                                                 # recover the data to original solution  for design variable AFO_FL_amplification for strap 1
	#--------------------------------------------------------------------------------------
	# AFO_FL_amplification for strap 2
	if cmp_marker[2][1]=='False':
		Gradient_theta_0_values_strap2=0
	else:
		theta_0_values[1]+=V_increment[2]                                                                 # small incremen for design variable AFO_FL_amplification for strap 2
		Gradient_theta_0_values_strap2=Gradient_calculation(solution, Objective_ini)
		theta_0_values[1]-=V_increment[2]                                                                 # recover the data to original solution  for design variable AFO_FL_amplification for strap 2
	#--------------------------------------------------------------------------------------
	# AFO_FL_amplification for strap 3
	if cmp_marker[2][2]=='False':
		Gradient_theta_0_values_strap3=0
	else:
		theta_0_values[2]+=V_increment[2]                                                                 # small incremen for design variable AFO_FL_amplification for strap 3
		Gradient_theta_0_values_strap3=Gradient_calculation(solution, Objective_ini)
		theta_0_values[2]-=V_increment[2]
	#--------------------------------------------------------------------------------------
	# AFO_FL_amplification for strap 4
	if cmp_marker[2][3]=='False':
		Gradient_theta_0_values_strap4=0
	else:
		theta_0_values[3]+=V_increment[2]                                                                 # small incremen for design variable AFO_FL_amplification for strap 3
		Gradient_theta_0_values_strap4=Gradient_calculation(solution, Objective_ini)
		theta_0_values[3]-=V_increment[2]
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable AFO_FL_shift
	#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	# AFO_FL_shift for strap 1
	# Cost function for small increased AFO_FL_shift for strap 1
	if cmp_marker[3][0]=='False':
		Gradient_n_elements_strap1=0
	else:
		n_elements[0]+=V_increment[3]                                                                 # small incremen for design variable AFO_FL_shift for strap 1
		# Call the module Gradient_calculation to calculate the gradient for AFO_FL_shift of strap 1
		Gradient_n_elements_strap1=Gradient_calculation(solution, Objective_ini)
		n_elements[0]-=V_increment[3]                                                                 # recover the data to original solution  for design variable AFO_FL_shift for strap 1
	#--------------------------------------------------------------------------------------
	# AFO_FL_shift for strap 2
	if cmp_marker[3][1]=='False':
		Gradient_n_elements_strap2=0
	else:
		n_elements[1]+=V_increment[3]                                                                 # small incremen for design variable AFO_FL_shift for strap 2
		Gradient_n_elements_strap2=Gradient_calculation(solution, Objective_ini)
		n_elements[1]-=V_increment[3]                                                                 # recover the data to original solution  for design variable AFO_FL_shift for strap 2
	#--------------------------------------------------------------------------------------
	# AFO_FL_shift for strap 3
	if cmp_marker[3][2]=='False':
		Gradient_n_elements_strap3=0
	else:
		n_elements[2]+=V_increment[3]                                                                 # small incremen for design variable AFO_FL_shift for strap 3
		Gradient_n_elements_strap3=Gradient_calculation(solution, Objective_ini)
		n_elements[2]-=V_increment[3]                                                                 # recover the data to original solution  for design variable AFO_FL_shift for strap 3
	#--------------------------------------------------------------------------------------
	# AFO_FL_shift for strap 4
	if cmp_marker[3][3]=='False':
		Gradient_n_elements_strap4=0
	else:
		n_elements[3]+=V_increment[3]                                                                 # small incremen for design variable AFO_FL_shift for strap 4
		Gradient_n_elements_strap4=Gradient_calculation(solution, Objective_ini)
		n_elements[3]-=V_increment[3]                                                                 # recover the data to original solution  for design variable AFO_FL_shift for strap 4
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
		# Check whether the solution reaches the bounds, if so, derivative remain the one in the last step, and new derivative will not calculate
		gradient = derivative(solution, cmp_marker)
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
best, score = gradient_descent(objective, derivative, n_iter, step_size)
print('Done!')
print('f(%s) = %f' % (best, score))
