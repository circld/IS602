# Perform a Monte Carlo simulation to calculate Value at Risk (VaR) for the
# Apple stock price using the file attached to this lesson. There exist a
# number of ways to do this type of analysis, but you can follow this basic
# procedure (refer to this PDF (mc.pdf) for a more rigorous mathematical
# overview):

# 1. The file (apple.2011.csv) has 3 columns: date, price, and percent change.
#    The information you are really interested in is the percent change.  This
#    value is the percent change in the price from the previous date to the date
#    on the corresponding row.
# 2. Use the percent change values to create a Gaussian random number generator.
#   This generator will create Gaussian-distributed randoms to use as
#   hypothetical percent changes on the day to day price of Apple stock.
# 3. With that generator, create 20 random numbers.  With these randoms, you can
#   find a potential price change over 20 days.
# 4. Start with the price from the last row and the random numbers to determine
#   a hypothetical price after 20 days.  To do this, take that last price,
#   apply a percent change and get a new price.  Then take that new price, and
#   apply the next percent change.  Do this for the 20 randoms, and get a final
#   price.
# 5. Store the final price after 20 days (you can discard the intermediate price
#   values).
# 6. Repeat steps 3-5 a very large number of times.  Something like 10000.  Each
#   run will yield a different result.
# 7. Take all of the stored prices (10000 or so), sort them, and find the 1%
#   lowest percentile.  This value is the final result, and represents the VaR
#   with 99% confidence.  This means that the price will be above this result
#   after 20 days with a confidence level of 99%.

# The other requirement for this assignment is to use an IPython Notebook.
# Include in the notebook all the code, the results, and any other
# information you feel is needed (charts, graphs, plots, etc).  Rather than
# submitting .py files, give me the .ipynb file for your notebook.

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