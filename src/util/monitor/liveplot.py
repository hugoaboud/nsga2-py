import sys
sys.path.append('.')

import random 
import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import asyncio
import pickle
import numpy as np

from src.util.monitor.server import MonitorClient
from src.util.log import Log
from multiprocessing import Process, Queue

if __name__ == '__main__':

    Log.setup(level='INFO')

    server_ip = '127.0.0.1'
    queue = Queue()
    Process(target=MonitorClient.process, args=(server_ip, queue)).start()

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    lines = []
    data = []
    for _ in range(2):
        data.append(([],[])) 
        line, = ax1.plot([],[])
        lines.append(line)

    plt.xlabel('Epochs')
    plt.ylabel('Fitness')
    plt.title('Live Graph')

    def animate(frame):
        try:
            pfitnesses = queue.get_nowait()
        except:
            return line
        fitnesses = pickle.loads(pfitnesses) 
        dims = len(list(fitnesses.values())[0])
        fits = [[f[d] for f in fitnesses.values()] for d in range(dims)]
        max_fits = [np.max(fit_d) for fit_d in fits]
        avg_fits = [np.average(fit_d) for fit_d in fits]

        p = [avg_fits[0], max_fits[0]]
        if (math.isinf(p[0]) or math.isinf(p[1])):
            return lines

        for i in range(2):
            data[i][0].append(frame) 
            data[i][1].append(p[i]) 
            lines[i].set_xdata(data[i][0])
            lines[i].set_ydata(data[i][1])

        min_x = min([min(d[0]) for d in data])
        max_x = max([max(d[0]) for d in data])
        min_y = min([min(d[1]) for d in data])
        max_y = max([max(d[1]) for d in data])

        # print(xs)
        # print(ys)
        ax1.set_xlim(min_x-1, max_x+1)
        ax1.set_ylim(min_y-0.05, max_y+0.05)
        ax1.set_xticks(list(range(min_x, max_x+1)))
        return lines

    ani = animation.FuncAnimation(fig, animate, interval=100) 
    plt.show()
