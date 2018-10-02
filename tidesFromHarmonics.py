import math
import matplotlib.pyplot as plt
import time, datetime


def get_current_args_from_file(file, current_year):
    lines = [line.split() for line in file]
    current_year_column = current_year % 10
    current_year_row = (current_year-1970)/10
    rows = [8*x+current_year_row+1 for x in range(37)]
    args = [float(lines[row][current_year_column]) for row in rows]
    return args

avg = 0

def tide_point(t):
    return avg + sum([amplitude*node_factor*math.cos((speed*t + equilibrium_argument - phase)/(2*math.pi))
                      for (amplitude, phase, speed, equilibrium_argument, node_factor) in
                      zip(amps, phases, speeds, current_year_equilibrium_arguments, current_node_factor_arguments)])

def get_current_day_forecast():
    return 0

if __name__ == "__main__":
    now = datetime.datetime.now()
    CURRENT_HOUR_LAPSE = time.time()/(60*60)
    CURRENT_10_HOUR_LAPSE = CURRENT_HOUR_LAPSE/10 + 1
    last_midnight = CURRENT_HOUR_LAPSE - now.hour

    with open("./casablanca-moroco_harmonics.txt") as file:
        amps, phases = zip(*[(float(x[1]), float(x[2])) for x in
                            [line.split() for line in file]])

    with open("speeds.txt") as file:
        speeds = [float(x[1]) for x in [line.split() for line in file]]

    with open("equilibrium.txt") as file:
        current_year_equilibrium_arguments = get_current_args_from_file(file, now.year)

    with open("node_factors.txt") as file:
        current_node_factor_arguments = get_current_args_from_file(file, now.year)
        
    DAYS = 1
    # 2.4 LAPSES OF 10HOURS FOR A DAY
    waves = [tide_point(CURRENT_10_HOUR_LAPSE + (float(t)/100.)) for t in range(240*DAYS)]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(len(waves)), waves)
    hourly = waves[::10]
    ax.plot(range(len(waves))[::10], hourly , 'd', linewidth=5, color='green')

    plt.show()
