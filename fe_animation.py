from pathlib import Path
import mplcursors
from qtlib.types import OpenFilesType
from tweezers import api as tz, get_option
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

def feAnimation(dist, force, time, name, save):

    fig = plt.figure()
    ax = plt.axes()
    ax.set(xlabel = "distance (nm)", ylabel = "force (pN)", title = f"{name}.pkl")
    time_text = ax.text(0.95, 0.05,'',horizontalalignment='right', verticalalignment='bottom',
        transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='yellow'))
    # defined two lines, red line for first half, bule line for last half
    line1, = ax.plot([], [], lw=2, color = 'red')
    line2, = ax.plot([], [], lw=2, color = 'blue')
    # defined lists to save points on line
    x1data, y1data = [], []
    x2data, y2data = [], []
    print(len(dist))

    def init():
        line1.set_data([], [])
        line2.set_data([], [])
        time_text.set_text('Start')
        return line1, line2, time_text

    def animate(i):
        a = time[i]
        x = dist[i]
        y = force[i]
        if i <= len(dist) // 2 :
            x1data.append(x)
            y1data.append(y)
        else:
            x2data.append(x)
            y2data.append(y)
        
        line1.set_data(x1data, y1data)
        line2.set_data(x2data, y2data)
        
        ax.relim()
        ax.autoscale_view()
        
        time_text.set_text('Time: %.2fs' % a)
        return line1, line2, time_text

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(dist), interval=1, blit=False, repeat=False)
    # save animation
    if save:
        anim.save(f"{name}.mp4", writer="ffmpeg", fps=10, metadata={'title':'Animation of ploting ' + name +'.pkl'})
    else:
        plt.show()

def main(filePath: Path, *,
         save: bool = False):
    print("reading...", filePath)
    name = str(filePath)[:-4]
    tr = tz.trace(filePath).get_downsampled_to(10)
    dist = tr.dist.tolist()
    force = tr.force.tolist()
    time = tr.time.tolist()

    font = {'family':'sans-serif', 'size': 12}
    plt.rc('font', **font)
# creat animation for full trace or zoom in animation on NPS region
    feAnimation(dist, force, time, name, save)

if __name__ == "__main__":
    import defopt
    defopt.run(main)