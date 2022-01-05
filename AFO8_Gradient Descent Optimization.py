# -*- coding: utf-8 -*-
import math
import AFO_Simulation_Optimization
import numpy as np

def objective(Subtablar_drop, MusDiff_walk, MusDiff_run):
	# This is the cost function
	# to put the value of the cost function calculated for that simulation
	Func=abs(MusDiff_walk)+abs(MusDiff_run)+math.exp(Subtalar_drop)
	return Func

# derivative of objective function
def derivative(solution):
	# Input a small increase for each design parameter
	# V_increment=[[0.5,0.5,0.5,0.5], [0.5,0.5,0.5,0.5],[1,1,1,1],[0.2,0.2,0.2,0.2]]
	V_increment=[0.5,0.5,1,0.2]
	#----------------------------------------------------------------------------------------------------------------------------
	# Cost function for initial solution
	[AFO_bottom_location, Stripe_orientation, AFO_FL_amplification, AFO_FL_shift]=solution
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(AFO_bottom_location, Stripe_orientation, AFO_FL_amplification, AFO_FL_shift)
	Objective_ini=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
	#----------------------------------------------------------------------------------------------------------------------------
	# The derivative for design variable AFO_bottom_location
	#----------------------------------------------------------------------------------------------------------------------------
	# AFO_bottom_location for strip 1
	# Cost function for small increased AFO_bottom_location for strip 1
	AFO_bottom_location[0]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strip 1
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(AFO_bottom_location, Stripe_orientation, AFO_FL_amplification, AFO_FL_shift)
	Objective_bottom_location_strip1=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
	# Calculate the  partitial derivative for AFO_bottom_location for strip 1
	Gradient_bottom_location_strip1=Objective_bottom_location_strip1- Objective_ini
	AFO_bottom_location[0]-=V_increment[0]
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strip 2
	# Cost function for small increased AFO_bottom_location for strip 2
	AFO_bottom_location[1]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strip 2
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(AFO_bottom_location, Stripe_orientation, AFO_FL_amplification, AFO_FL_shift)
	Objective_bottom_location_strip2=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
	# Calculate the  partitial derivative for AFO_bottom_location for strip 2
	Gradient_bottom_location_strip2=Objective_bottom_location_strip2- Objective_ini
	AFO_bottom_location[1]-=V_increment[1]
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strip 3
	# Cost function for small increased AFO_bottom_location for strip 3
	AFO_bottom_location[2]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strip 2
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(AFO_bottom_location, Stripe_orientation, AFO_FL_amplification, AFO_FL_shift)
	Objective_bottom_location_strip3=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
	# Calculate the  partitial derivative for AFO_bottom_location for strip 3
	Gradient_bottom_location_strip3=Objective_bottom_location_strip3- Objective_ini
	AFO_bottom_location[2]-=V_increment[2]
	#--------------------------------------------------------------------------------------
	# AFO_bottom_location for strip 4
	# Cost function for small increased AFO_bottom_location for strip 4
	AFO_bottom_location[3]+=V_increment[0]                                                                 # small incremen for design variable AFO_bottom_location for strip 2
	[Subtablar_drop, MusDiff_walk, MusDiff_run]=AFO_Simulation_Optimization.Main_Simulation(AFO_bottom_location, Stripe_orientation, AFO_FL_amplification, AFO_FL_shift)
	Objective_bottom_location_strip4=objective(Subtablar_drop, MusDiff_walk, MusDiff_run)
	# Calculate the  partitial derivative for AFO_bottom_location for strip 4
	Gradient_bottom_location_strip4=Objective_bottom_location_strip4- Objective_ini
	AFO_bottom_location[3]-=V_increment[3]
		


	return #here you need to calculate the difference in the cost function caused by a small change in every design parameter
#So, for every design parameter (mesh stiffness, mesh strain when high stiffness occurs, mesh orientation etc)
#input a small increase while keeping the other design parameters constant
#and compare the outcome of the cost function that results. that difference in the cost function
# caused by the small change in design parameter is then the "gradient".
#What the best small change is is something you'll have to experiment with,
#but it can be different for each design parameter

# This defines the gradient descent algorithm
def gradient_descent(objective, derivative, bounds, n_iter, step_size):
	# generate an initial point
	# solution: This is any combination of design parameters. It doesn't matter what the combination is,
	# solution=(AFO_bottom_location, AFO_stripe_orientations, AFO_FL_amplification, AFO_FL_shift)
	solution = [[14, 101, 259, 346], [-40, 0, 0, 50], [10,10,10,10], [2,2,2,2]]

    #it is just a starting point for the optimisation
    # run the gradient descent
	for i in range(n_iter):
		# calculate gradient
		gradient = derivative(solution)
		# take a step
		solution = solution - step_size * gradient
		# evaluate candidate point
		solution_eval = objective(solution)
		# report progress
		print('>%d f(%s) = %.5f' % (i, solution, solution_eval))
	return [solution, solution_eval]

# define the total iterations
n_iter = 30
# define the step size, this value is something you'll probably need to experiment with
step_size = 0.1
# perform the gradient descent search
best, score = gradient_descent(objective, derivative, bounds, n_iter, step_size)
print('Done!')
print('f(%s) = %f' % (best, score))
