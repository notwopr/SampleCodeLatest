"""
Title: GRAPH FUNCS - ANIMATION - base
Date Started: Oct 27, 2020
Version: 1.0
Version Start: Oct 27, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Animate progression of price graph.

VERSIONS:
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
#   THIRD PARTY IMPORTS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.animation as animation
#   LOCAL APPLICATION IMPORTS
from pricehistorybot import grabsinglehistory
from fillgapbot import fill_gaps2
from FINALBAREMINCRUNCHER import oldbaremin_cruncher, baremax_cruncher
from statresearchbot import stat_profiler
from filelocations import readpkl, savetopkl


def datasnapshot(prices, stock):
    allprices = prices[stock].tolist()
    oldbareminrawpricelist = oldbaremin_cruncher(allprices)
    prices['oldbareminraw'] = np.array(oldbareminrawpricelist)
    baremaxrawpricelist = baremax_cruncher(allprices)
    prices['baremaxraw'] = np.array(baremaxrawpricelist)
    prices['trueline'] = ((prices['baremaxraw'] - prices['oldbareminraw']) / 2) + prices['oldbareminraw']
    return prices


# get snapshot of dropstats in dictionary
def getalldropsarr(prices, stock):
    dropdatasource = prices.copy()
    # calc drop stats
    alldropsarr = ((dropdatasource['oldbareminraw'] - dropdatasource[stock]) / dropdatasource[stock]).to_numpy()
    if len(alldropsarr) == 0:
        return
    else:
        alldropsarr = alldropsarr[alldropsarr < 0]
        if len(alldropsarr) == 0:
            return
        else:
            return alldropsarr


# get snapshot of dropstats in dictionary
def getdropstatsnapshot(alldropsarr):
    if len(alldropsarr) == 0:
        return
    else:
        statdict = stat_profiler(alldropsarr)

        # add std cushion
        statdict.update({
            'stat_mean-1.5std': statdict['stat_mean'] - (statdict['stat_std'] * 1.5),
            'stat_mean+1.5std': statdict['stat_mean'] + (statdict['stat_std'] * 1.5),
        })
        # remove std, sharpe
        del statdict['stat_std']
        del statdict['stat_sharpe']
        return statdict


def animate(i, axes, prices, stock, wintype, winwidth, margpct, savedir):
    #plt.cla()
    axes[0].clear()
    axes[1].clear()

    # slice prices
    snapshotprices = prices.iloc[0:i, :].copy()
    # set window vals
    if wintype == 'static':
        if winwidth == '':
            winwidth = len(prices)
        xmargval = winwidth * margpct
        ymargval = (prices[stock].max() - prices[stock].min()) * margpct
        plt.xlim(-xmargval, winwidth+xmargval)
        plt.ylim(-ymargval, prices[stock].max()+ymargval)
    elif wintype == 'rolling':
        if i > winwidth:
            winend = i
            winstart = winend - winwidth
            plt.xlim(winstart, winend)

    # gather graph data
    graphdata = datasnapshot(snapshotprices, stock)
    # open dropstats
    try:
        dropdfdata = readpkl('dropstats', savedir)
    except FileNotFoundError:
        dropdfdata = []
    # update and save dropdfdata
    alldropsarr = getalldropsarr(snapshotprices, stock)
    if alldropsarr is not None:
        # create alldropsdf
        alldropsdf = pd.DataFrame(data={'alldrops': alldropsarr})
        # get dropstats
        dropstatsnapshot = getdropstatsnapshot(alldropsarr)
        if dropstatsnapshot is not None:
            # save and add to dropstatdata if not empty
            dropdfdata.append(dropstatsnapshot)
            savetopkl('dropstats', savedir, dropdfdata)
            # create dropstatdf
            dropstatdf = pd.DataFrame(data=dropdfdata)
            # join alldropsdf to dropstatdf
            dropstatdf = dropstatdf.join(alldropsdf)
        else:
            dropstatdf = alldropsdf
        sns.lineplot(data=dropstatdf, ax=axes[1])
        axes[1].set(xlabel='Time', ylabel='Drop Amount')
    # plot data
    sns.lineplot(data=graphdata, ax=axes[0])
    axes[0].set(xlabel='Days', ylabel='Price')


def animateprices(stock, beg_date, end_date, margpct, wintype, winwidth, speed, saveanim, savefn, savedir):

    # clear dropdatafile
    if os.path.exists(savedir / "dropstats.pkl"):
        os.remove(savedir / "dropstats.pkl")
    # get overall pricedata
    prices = grabsinglehistory(stock)
    prices = fill_gaps2(prices, beg_date, end_date)

    # set out plot
    # fig = plt.figure()
    fig, (ax1, ax2) = plt.subplots(1, 2)

    fig.suptitle('Squeezegraph Over Time')

    # load writer
    writer = animation.FFMpegWriter(fps=speed, metadata=dict(artist='davidinvests'), bitrate=1800)

    # animate
    ani = animation.FuncAnimation(fig, animate, fargs=[(ax1, ax2), prices, stock, wintype, winwidth, margpct, savedir], repeat=False)
    plt.show()

    # save animation
    if saveanim == 'yes':
        # save
        ani.save(savedir / f'{savefn}.mp4', writer=writer)
