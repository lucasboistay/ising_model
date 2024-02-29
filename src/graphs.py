"""
To plot the different graphs of the Ising model

@Author: Lucas BOISTAY
@Date: 2024-02-29
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.utils import find_critical_temperature
from src.utils import Onsager
from constants import N, M, iterations, t_min, t_max


def plot_critical_temperature(filename: str, temperature: np.ndarray, magnetization: np.ndarray,
                              smoothed_magnetization: np.ndarray, derivative_magnetization: np.ndarray,
                              critical_temperature: float) -> None:
    """
    Plot the critical temperature graph
    :param filename: (str) Filename
    :param temperature: (np.ndarray) Temperature
    :param magnetization: (np.ndarray) Magnetization
    :param smoothed_magnetization: (np.ndarray) Smoothed magnetization
    :param derivative_magnetization: (np.ndarray) Derivative of magnetization
    :param critical_temperature: (float) Critical temperature
    :return: None
    """
    plt.figure(figsize=(14, 10))

    plt.plot(temperature, derivative_magnetization, label="Derivative of magnetization")
    plt.plot(temperature, magnetization, label="Magnetization")
    plt.plot(temperature, smoothed_magnetization, label="Smoothed magnetization")
    # plot the critical temperature line
    plt.axvline(x=critical_temperature, color='red', linestyle='--',
                label=r'Computated $T_c$')
    plt.legend()
    plt.xlabel(rf"Temperature /J")
    plt.ylabel(rf"Magnetisation /µ")
    plt.title(f'Critical temperature computation\nCritical temperature = {critical_temperature:.2f}')
    plt.savefig(f"data/{filename}.png", dpi=300)
    plt.show()
    plt.close()


def plot_data_from_file(filename: str) -> None:
    """
    Read the data from the file and plot it
    :param filename: (str) Filename
    :return: None
    """
    data = pd.read_csv('data/data.txt', sep='\t')
    temperatures = data['Temperature']
    final_energy = data['Energy']
    final_magnetization = data['Magnetization']

    # Find the critical temperature

    critical_temperature, smoothed_magnetization, derivative_magnetization = find_critical_temperature(temperatures,
                                                                                                       final_magnetization)
    plot_critical_temperature("critical_temperature", temperatures, final_magnetization, smoothed_magnetization,
                              derivative_magnetization, critical_temperature)

    # Plot the final energy and magnetization

    onsager = [Onsager(2.269, T) for T in temperatures]

    plt.figure(figsize=(14, 10))
    plt.plot(temperatures, final_magnetization, 'bo', label=rf"Simulation data (Monte Carlo)")
    plt.plot(temperatures, onsager, 'g--', label=rf"Onsager solution (Analytical)")
    # plot the critical temperature line
    plt.axvline(x=2.269, color='green', linestyle='-', label=r"Analitical $T_c = 2.269$")
    plt.axvline(x=critical_temperature, color='blue', linestyle='-',
                label=rf"Computated $T_c = {critical_temperature:.2f}$")
    plt.xlabel(rf"Temperature /J")
    plt.ylabel(rf"Magnetisation /µ")
    plt.legend()
    plt.axhline(c="k", linewidth=1)
    plt.axvline(c="k", linewidth=1)
    plt.title(f'Magnetisation vs Temperature\n(Lattice : {N}x{M}, {iterations} iterations)')
    plt.savefig(f"data/magnetization.png", dpi=300)
    plt.show()
