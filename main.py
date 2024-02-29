"""
This is the main file of the project. It will run the Ising model in parallel and plot the results.
@Author: Lucas BOISTAY
@Date: 2024-02-29
"""

from src.utils import create_gif, run_parallel_ising
from src.graphs import plot_data_from_file
from constants import t_min, t_max, iterations, N, M, number_of_simulations, number_of_pool_processes

import numpy as np
# Create N ising model and run the simulation to get the final energy and magnetization and plot it

final_energy = []
final_magnetization = []


if __name__ == "__main__":
    # Parameters

    temperatures = np.linspace(t_min, t_max, number_of_simulations)

    # Run the model once for a gif of the magnetization lattice

    create_gif(2.269, iterations)

    # Run the model in parallel

    #run_parallel_ising(number_of_simulations, number_of_pool_processes, temperatures)

    # Read the data from the file and plot it

    #plot_data_from_file('data/data.txt')
