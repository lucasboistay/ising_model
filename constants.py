# Description: This file contains the constants used in the simulated annealing algorithm.

# General model constants

N = 100 # Number of rows
M = 100 # Number of columns
iterations = 100000 # Number of iterations

# Parallel processing constants

number_of_simulations = 100 # Number of simulations for the critical temperature computation
number_of_pool_processes = 10  # Number of pool processes, do not set it to more than the number of cores of your CPU

# Temperature constants

t_min = 0.1 # Minimum temperature for the critical temperature computation
t_max = 4 # Maximum temperature for the critical temperature computation
