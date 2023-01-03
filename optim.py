# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging as log
import math
import matplotlib.pyplot as plt
from openpyxl import Workbook
from pathlib import Path
import random
import statistics
import sys

"""
Evolutionary algorithms

Differential evolution for: 
* 1st DeJong function
* 2nd DeJong function
* Schwefel function
* Rastrigin function

@author: Filip Findura
"""

# Requested dimensions, max energy function calls and iterations:
D = [10, 30]
FES = 5000
ITERATIONS = 30

# Differential evolution:
DE_NP = 50   # Population size
DE_F = 0.5   # Mutation constant
DE_CR = 0.9  # Crossbreeding threshold

# Logging root handler:
logger = log.getLogger()
# Logging level:
LOG_LVL = 'INFO'

# Output Excel workbook:
wb = Workbook(write_only=True)

# All results of optimization:
FUNCTIONS = ['de_jong_1', 'de_jong_2', 'schwefel', 'rastrigin']
RESULTS = dict()


##################################################
# Energy Functions
##################################################
def de_jong_1(inputs: list):
    # http://profesores.elo.utfsm.cl/~tarredondo/info/soft-comp/functions/node2.html
    return sum([x**2 for x in inputs])


def de_jong_2(x: list):
    # http://profesores.elo.utfsm.cl/~tarredondo/info/soft-comp/functions/node5.html
    d = len(x)
    result = 0

    for i in range(d - 1):
        result += 100 * (x[i]**2 - x[i+1]) ** 2 + (1 - x[i]) ** 2

    return result


def schwefel(x: list):
    # https://www.sfu.ca/~ssurjano/schwef.html
    d = len(x)
    result = 0
    alpha = 418.982887

    for i in range(d):
        result -= x[i] * math.sin(math.sqrt(math.fabs(x[i])))

    return result + alpha * d


def rastrigin(x: list):
    # http://www.sfu.ca/~ssurjano/rastr.html
    d = len(x)
    result = 0

    for i in range(d):
        result += x[i]**2 - 10 * math.cos(2 * math.pi * x[i])

    return 10 * d + result


##################################################
# Algorithms
##################################################
def differential_evolution(it: int, fn, dim: int, constr_min: float, constr_max: float,
                           enable_plots: bool = False):
    logger.info(f"Starting simulated annealing for D{dim} {fn.__name__}...")
    ws = wb.create_sheet()
    ws.title = f"Differential evolution {fn.__name__.replace('_', ' ').title()} D{dim}"
    ws.append(["Iteration", "Minimum", "Inputs"])
    if enable_plots:
        plt.figure(3+dim)

    # TODO

    if enable_plots:
        plt.xlabel('Cost Function Evaluations')
        plt.ylabel('Results')
        plt.title(f"All iterations of differential evolution for {fn.__name__.replace('_', ' ').title()}, D{dim}")

        splt = plt.subplot()
        box = splt.get_position()
        splt.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        splt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        plt.show()
        plt.clf()


##################################################
# Helpers
##################################################
def set_logging(l_name: str, level: str):
    """Set up attributes of the root logger

    :param l_name: string name of the logger
    :param level: string name of base log level
    """
    global logger

    log_format = "%(asctime)s | %(levelname)-5s | %(message)s"
    if level == "DEBUG":
        log_format += " | %(filename)s@ln%(lineno)d"
    formatter = log.Formatter(log_format)

    logger = log.getLogger(l_name)
    logger.setLevel(level)
    handler = log.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_results(it: int, enable_plots: bool = False):
    for d in D:
        RESULTS[d] = {
            'differential_evolution': dict(),
        }
        differential_evolution(it, de_jong_1, d, -5.0, 5.0, enable_plots)
        differential_evolution(it, de_jong_2, d, -5.0, 5.0, enable_plots)
        differential_evolution(it, schwefel, d, -500, 500, enable_plots)
        differential_evolution(it, rastrigin, d, -500, 500, enable_plots)

        if enable_plots:
            for idx, f in enumerate(FUNCTIONS):
                avg_x = dict()
                med_x = dict()
                max_x = dict()
                min_x = dict()
                graph_y = dict()

                for ndx, k in enumerate(RESULTS[d].keys()):
                    plt.figure(d + idx * 4 + ndx + 100)
                    avg_x[k] = list()
                    med_x[k] = list()
                    max_x[k] = list()
                    min_x[k] = list()
                    graph_y[k] = list()

                    steps = FES
                    for x in range(steps):
                        x_total = list()
                        y_total = 0
                        try:
                            for i in range(it):
                                x_total.append(RESULTS[d][k][f][i][x][1])
                                if RESULTS[d][k][f][i][x][0] > y_total:
                                    y_total = RESULTS[d][k][f][i][x][0]
                        except IndexError:
                            logger.error(f"Alg: {k}; fn: {f}; step: {x}/{steps}")
                            sys.exit(1)
                        avg_x[k].append(statistics.mean(x_total))
                        med_x[k].append(statistics.median(x_total))
                        max_x[k].append(max(x_total))
                        min_x[k].append(min(x_total))
                        graph_y[k].append(y_total)

                    # I mixed up x and y, so graph_y is axis x and foo_x is on axis y...
                    plt.plot(graph_y[k], avg_x[k], label="Average")
                    plt.plot(graph_y[k], med_x[k], label="Median")
                    plt.plot(graph_y[k], max_x[k], label="Max")
                    plt.plot(graph_y[k], min_x[k], label="Min")

                    plt.xlabel('Cost Function Evaluations')
                    plt.ylabel('Results')
                    plt.title(f"Statistics for {k.replace('_', ' ')} for {f.replace('_', ' ').title()}, D{d}")

                    splt = plt.subplot()
                    box = splt.get_position()
                    splt.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                    splt.legend(loc='upper left', bbox_to_anchor=(1, 1))

                    plt.show()

                plt.figure(idx + 333 + d)
                for k in RESULTS[d].keys():
                    plt.plot(graph_y[k], avg_x[k], label=k.replace('_', ' ').title())

                plt.xlabel('Cost Function Evaluations')
                plt.ylabel('Results')
                plt.title(f"Algorithm comparison for {f.replace('_', ' ').title()}, D{d}")

                splt = plt.subplot()
                box = splt.get_position()
                splt.set_position([box.x0, box.y0, box.width * 0.8, box.height])
                splt.legend(loc='upper left', bbox_to_anchor=(1, 1))

                plt.show()

    wb.save(Path("./raw_output.xlsx"))
    wb.close()


if __name__ == "__main__":
    time_start = datetime.datetime.now()

    name = "ak9ev"
    set_logging(name, LOG_LVL)
    plots = "-p" in sys.argv or "--enable-plots" in sys.argv
    get_results(ITERATIONS, plots)

    time_stop = datetime.datetime.now()
    time_elapsed = time_stop - time_start
    logger.info(f"Done {ITERATIONS} iterations over {len(FUNCTIONS)} functions in {time_elapsed.total_seconds():.3f} "
                f"seconds ({time_elapsed.total_seconds() / 60:.3f} minutes).")
