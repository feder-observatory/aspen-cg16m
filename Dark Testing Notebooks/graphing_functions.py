from matplotlib import pyplot as plt
import numpy as np

__all__ = ['plot_linearity', 'plot_dark_current']

def plot_linearity(all_darks, bad_locs, exposures, pix_max=0, pix_min=0, legend=True, plot_fraction=1.0):
    max_exposure = np.max(exposures)
    plt.figure(figsize=(10, 10))
    badnesses = []
    longest_exp = all_darks[:, :, -1]
    #print('outside loop', bad_locs.shape, flush=True)
    for i, j in zip(bad_locs[:, 0], bad_locs[:, 1]):
        #print('inside loop')
        actual_values = all_darks[i, j, :]/longest_exp[i, j]
        badness = np.sqrt(((actual_values - exposures/max_exposure)**2).mean())
        badnesses.append(badness)
        wid = 4 if badness > 0.07 else 1
        if np.random.rand() < plot_fraction:
            plt.plot(exposures, actual_values, label='{}, {}; {:.3f}'.format(i,j, badness), linewidth=wid)
    plt.plot([0, max_exposure], [0,1], color='black', linewidth=4, linestyle='dashed', label='Linear')
    if legend:
        plt.legend(bbox_to_anchor=(1.5, 0.6), ncol=3)
    plt.ylim(-0.1, 1.1)
    plt.xlabel('Exposure time (sec)', size=20)
    plt.ylabel('pixel value as fraction of value in 120sec frame', size=20)
    plt.title('Linearity of master darks ({} pixels '
              'between {}$\sigma$ and {}$\sigma$)'.format(bad_locs.shape[0], pix_min, pix_max),
              size=15)
    return badnesses


def plot_dark_current(all_darks, bad_locs, badnesses, exposures, gain=1.5, legend=False, plot_fraction=1.0):
    plt.figure(figsize=(10, 10))
    linestyles = ['dashed', 'solid', 'dotted']
    for i, j, badness in zip(bad_locs[:, 0], bad_locs[:, 1], badnesses):
        actual_values = gain * all_darks[i, j, :] / exposures
        width = 4 if badness > 0.07 else 1
        wid = 4 if badness > 0.07 else 1
        if np.random.rand() < plot_fraction:
            plt.plot(exposures, actual_values, label='{}, {}; {:.3f}'.format(i,j, badness), linewidth=wid)
        #plt.plot(exposures, actual_values, label='{}, {}'.format(i,j), 
                 #linestyle=np.random.choice(linestyles), linewidth=width)
        

    plt.xlabel('Exposure time (sec)', size=20)
    plt.ylabel('Dark current (e$^-$/sec/pixel', size=20)
    if legend:
        plt.legend()
        