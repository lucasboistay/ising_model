"""
This file contains the different function to run the Ising model in parallel or even to create a gif of the lattice
magnetization. It also contains the function to find the critical temperature and the Onsager solution for the
magnetization.

@Author: Lucas BOISTAY
@Date: 2024-02-28
"""

from src.isingModel import IsingModel
from constants import N, M, iterations, t_min, t_max

import numpy as np
import pandas as pd
from multiprocessing import Pool
import time
from scipy.signal import savgol_filter


def find_critical_temperature(temperature: np.ndarray, magnetization: np.ndarray) -> -(float, np.ndarray, np.ndarray):
    """
    Find the critical temperature
    :param temperature: (np.ndarray) Temperature array
    :param magnetization: (np.ndarray) Magnetization array
    :return: (float) Critical temperature
    """
    # Find the critical temperature by finding the temperature where the magnetization is the most changing by derivate
    smooth_magnetization = savgol_filter(magnetization, 20, 3)  # Smooth the magnetization
    derivative = abs(np.gradient(smooth_magnetization, temperature))
    max_derivative_index = np.argmax(derivative)
    critical_temperature = temperature[max_derivative_index]

    return critical_temperature, smooth_magnetization, derivative


def Onsager(Tc: float, T: float) -> float:
    """
    Onsager solution for the magnetization
    :param Tc: (float) Critical temperature
    :param T: (np.ndarray) Temperature array
    :return: (np.ndarray) Onsager solution
    """
    if T < Tc:
        return (1 - 1 / (np.sinh(2 / T) ** 4)) ** (1 / 8)
    else:
        return 0


def run_model(N: int, M: int, temperature: float, iterations: int) -> (float, float):
    """
    Run one Ising model
    :param N: (int) Number of rows
    :param M: (int) Number of columns
    :param temperature: (int) temperature
    :param iterations: (int) number of iterations
    :return: (float, float) final energy and magnetization
    """
    # Create an Ising model
    ising = IsingModel(N, M, temperature, iterations)

    ising.initialize_lattice(1)  # To get a lattice with all 1's

    # information about the lattice
    starting_lattice = np.copy(ising.get_lattice())

    ising.run_monte_carlo()

    ending_lattice = np.copy(ising.get_lattice())

    return ising.get_total_energy(), ising.magnetization()


def create_gif(temperature: float, iterations: int) -> None:
    """
    Create a gif of the lattice magnetization for a given temperature
    :param temperature: (float) temperature for the ising model
    :param iterations: (int) number of iterations for the ising model
    :return: None
    """
    print(f"------ Creating gif for T={temperature}... ------")
    ising = IsingModel(N, M, temperature, iterations)
    ising.initialize_lattice("random")  # To get a lattice with all 1's
    ising.run_monte_carlo(save_image=True)
    print("Gif created and saved as ising.gif")


def run_parallel_ising(N_simulation: int, N_pool_processes: int, temperatures: np.ndarray) -> None:
    """
    Run the Ising model in parallel
    :param N_simulation: (int) Number of simulations
    :param N_pool_processes: (int) Number of pool processes (number of cores of your CPU)
    :param temperatures: (np.ndarray) Temperatures array
    :return: None
    """

    print("------ Running the model in parallel... ------")
    print(f"Number of simulations: {N_simulation}")

    with Pool(N_pool_processes) as p:  # Run the model in parallel with a pool of processes, if not understood, it's ok
        # v Run the model for each temperature v
        print("Pool of processes created")
        start_time = time.time()
        results = p.starmap(run_model, [(N, M, temperature, iterations) for temperature in temperatures])
        final_energy, final_magnetization = zip(*results)  # Unzip the results
        end_time = time.time()
        p.close()  # Close the pool
        print("Pool of processes closed")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        p.join()  # Join the pool

    # Normalisation
    final_energy = np.array(final_energy) / (N * M)  # Normalise the final energy
    final_magnetization = np.array(final_magnetization) / (N * M)  # Normalise the final magnetization

    # Save the data in a txt file as a table

    data = pd.DataFrame({'Temperature': temperatures, 'Energy': final_energy, 'Magnetization': final_magnetization})
    # data.to_csv('data/data.txt', index=False, sep='\t')

    print("Data saved in data/data.txt")
