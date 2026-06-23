import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import gpytoolbox as gpy
from definitions import *
from matplotlib.collections import LineCollection

def plot_edges(vv,ee,color,verts=False):

    c = (color[0], color[1], color[2])
    ax = plt.gca()

    if ee.shape[0]<5000:
        x = []
        y = []
        completed = []
        ind = -1
        while len(completed)<ee.shape[0]:
            j = np.nonzero(ee[:,0]==ind)[0]
            j = np.setdiff1d(j,completed)
            if j.size>0:
                j = j[0]
                if ee[j,0]==ee[j,1]:
                    completed.append(j)
                    continue
                x[-1].append(vv[ee[j,1],0])
                y[-1].append(vv[ee[j,1],1])
                ind = ee[j,1]
                completed.append(j)
            else:
                j = np.setdiff1d(np.arange(ee.shape[0]),completed)
                if j.size==0:
                    assert False
                else:
                    j = j[0]
                if ee[j,0]==ee[j,1]:
                    completed.append(j)
                    continue
                x.append([])
                y.append([])
                x[-1].append(vv[ee[j,0],0])
                y[-1].append(vv[ee[j,0],1])
                x[-1].append(vv[ee[j,1],0])
                y[-1].append(vv[ee[j,1],1])
                # ax.plot([vv[ee[j,0],0],vv[ee[j,1],0]],
                #          [vv[ee[j,0],1],vv[ee[j,1],1]],
                #          'g',alpha=1)
                ind = ee[j,1]
                completed.append(j)
        assert np.all(np.sort(completed)==np.arange(ee.shape[0]))

        for i in range(len(x)):
            ax.plot(x[i],y[i],
                     linewidth=5,
                     solid_capstyle='round',
                     solid_joinstyle='miter',
                     color=c,alpha=1)
    else:
        # Too many line segments to do joining thing, just plot all.
        segs = np.zeros((ee.shape[0], 2, 2))
        segs[:,0,0] = vv[ee[:,0],0]
        segs[:,1,0] = vv[ee[:,1],0]
        segs[:,0,1] = vv[ee[:,0],1]
        segs[:,1,1] = vv[ee[:,1],1]
        line_segments = LineCollection(segs, linewidths=5,
            colors=c, linestyle='solid')
        ax.add_collection(line_segments)

    if verts:
        ax.scatter(vv[:,0],vv[:,1],color=c,
            s=60.)

def plot_spheres(vv,sdf):
    pc = (positive_sphere_color[0],positive_sphere_color[1],positive_sphere_color[2])
    nc = (negative_sphere_color[0],negative_sphere_color[1],negative_sphere_color[2])
    ax = plt.gca()
    f = sdf(vv)
    for i in range(vv.shape[0]):
        c = pc if f[i]>=0 else nc
        ax.add_patch(plt.Circle(vv[i,:], f[i], color=c, fill=False,alpha=0.1))