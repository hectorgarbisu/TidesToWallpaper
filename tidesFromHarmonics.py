import matplotlib.pyplot as plt
import time, datetime
import math

def get_current_args_from_file(file, current_year):
    lines = [line.split() for line in file]
    current_year_column = current_year % 10
    current_year_row = (current_year-1970)/10
    rows = [8*x+current_year_row+1 for x in range(37)]
    args = [float(lines[row][current_year_column]) for row in rows]
    return args

def get_params():
    now = datetime.datetime.now()

    with open("data/casablanca-moroco_harmonics.txt") as file:
        amps, phases = zip(*[(float(x[1]), float(x[2])) for x in
                            [line.split() for line in file]])

    with open("data/speeds.txt") as file:
        speeds = [float(x[1]) for x in [line.split() for line in file]]

    with open("data/equilibrium.txt") as file:
        current_year_equilibrium_arguments = get_current_args_from_file(file, now.year)

    with open("data/node_factors.txt") as file:
        current_node_factor_arguments = get_current_args_from_file(file, now.year)

    return zip(amps, phases, speeds, current_year_equilibrium_arguments, current_node_factor_arguments)


def tide_point(t):
    params = get_params()
    return 0 + sum([amplitude*node_factor*math.cos((speed*t + equilibrium_argument - phase)/(2*math.pi))
                      for (amplitude, phase, speed, equilibrium_argument, node_factor) in params])

def get_current_day_forecast(number_of_10_minute_increments):
    now = datetime.datetime.now()
    CURRENT_HOUR_LAPSE = time.time()/(60*60)
    CURRENT_10_HOUR_LAPSE = CURRENT_HOUR_LAPSE/10 + 1
    last_midnight = CURRENT_10_HOUR_LAPSE - now.hour/10.  
    # 2.4 lapses of 10 hours a day
    # 144 10-minute increments for a day
    avg = 0.9
    waves = [avg + tide_point(last_midnight + (float(t/60.))) for t in range(number_of_10_minute_increments)]
    return waves

def get_now_index():
    now = datetime.datetime.now()
    now_index = int((now.hour*60 + now.minute)/10)
    return now_index

if __name__ == "__main__":
    # main part just for test

    now = datetime.datetime.now()
    CURRENT_HOUR_LAPSE = time.time()/(60*60)
    CURRENT_10_HOUR_LAPSE = CURRENT_HOUR_LAPSE/10 + 1
    last_midnight = CURRENT_HOUR_LAPSE - now.hour

    waves = get_current_day_forecast(150)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(len(waves)), waves)
    hourly = waves[::10]
    ax.plot(range(len(waves))[::10], hourly , 'd', linewidth=5, color='green')

    plt.show()
