# IS602 Week 11 Assignment
# Paul Garaud

import Tkinter, tkFileDialog
import pandas as pd
import numpy as np
import random as r
import matplotlib.pyplot as plt


def gauss_gen(n, mu, sigma):
    return [r.gauss(mu, sigma) for i in xrange(n)]


def gen_new_obs(start_val, pct_ch):
    out = start_val
    for pct in pct_ch:
        out *= 1 + pct
    return out


def main():

    root = Tkinter.Tk()
    root.withdraw()

    # load data
    file_loc = tkFileDialog.askopenfile()
    apple = pd.read_csv(file_loc, parse_dates=[0], na_values='XXXXX')
    apple.columns = [apple.columns[0], apple.columns[1], 'PctChange']

    # gaussian random number generator
    mu = apple.PctChange.mean()
    sigma = apple.PctChange.std()

    # monte carlo
    Day20Val = ()
    for i in xrange(10000):
        new20pct = gauss_gen(20, mu, sigma)
        Day20Val += (gen_new_obs(apple.Last.values[-1], new20pct), )

    # visualize
    plt.hist(Day20Val, bins=100, normed=1)
    plt.show()

    # sort & find lowest 1 percentile
    print('The value should be over %.2f 99%% of the time.'
          % np.percentile(Day20Val, 1))


if __name__ == '__main__':

    main()