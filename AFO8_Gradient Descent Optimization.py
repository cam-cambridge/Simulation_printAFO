# -*- coding: utf-8 -*-

def objective(MusDiff_walk, MusDiff_walk, Subtablar_drop):
	# This is the cost function
	# to put the value of the cost function calculated for that simulation
	import math
	Func=abs(MusDiff_walk)+abs(MusDiff_walk)+math.exp(Subtalar_drop)
	return Func

# derivative of objective function
def derivative(x):
	
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
	solution = #This is any combination of design parameters. It doesn't matter what the combination is,
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
