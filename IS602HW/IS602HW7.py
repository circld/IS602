"""
What we are doing here is very similar to homework 6, but now we'll look a
bit at scipy.

Do parts 1 and 2.  Part 3 is optional

Take what you did on homework 5 as a starting point (using any of the provided
datasets).  Replace the regression calculation using least squares with a curve
fitting approach (examples in the reading).  To start, just fit a linear
equation.  Output the equation to the console.  You don't need to graph
anything (we'll look at that in a couple more weeks).
Again, using timeit, compare the performance of your solution in homework 5 to
the scipy function.  Output the results to the console.

(Optional)  There are other models that can be fitted to the data we have.
Try to fit other equations, like Gaussian, to the data.  Output the equation
to the console.
"""
# IS602 Week 7 Assignment - SciPy
# Paul Garaud

import csv
from timeit import timeit
import numpy as np
from scipy.optimize import curve_fit


# Week 5 code
def dim(a):
    """
    Calculates the dimensions of array; raises error if not valid matrix
    :param a: vector or matrix
    :return: tuple of length 2 representing dimensions of a
    """
    nrows = len(a)
    try:
        ncols = [len(col) for col in a]
    except TypeError as e:
        ncols = 1
    ncols = set(ncols)

    if len(ncols) != 1:
        raise TypeError('Invalid matrix: must have same number of rows in each column.')
    ncols = ncols.pop()

    if nrows == 1 and ncols == 1:
        raise TypeError('Invalid matrix: this is a scalar.')

    return nrows, ncols


def mult(a, constant):

    if type(a) not in (tuple, list):
        return a * constant

    n, k = dim(a)
    out = ()
    for i in xrange(n):
        new_row = tuple([el * constant for el in a[i]])
        out += (new_row, )
    return out


def inner(a, b):
    """
    Calculate the inner product of two arrays
    :return: if conformable, return inner product (tuple)
    """
    # check if matrices are conformable
    if dim(a)[1] != dim(b)[0]:
        raise TypeError('These matrices %s %s and %s %s are not conformable.'
                        % ('a', dim(a), 'b', dim(b)))

    prod = ()
    for i in xrange(dim(a)[0]):
        new_row = ()
        for j in xrange(dim(b)[1]):
            b_col = [el[j] for el in b]
            new_row += (sum([e1 * e2 for e1, e2 in zip(a[i], b_col)]), )
        prod += (new_row, )

    return prod


def det(a):
    """
    Calculate determinant
    :param a: matrix (list/tuple)
    :return: matrix (tuple)
    """
    n, k = dim(a)

    if n != k:
        raise TypeError('det() requires a square matrix.')

    # base case: 2 x 2
    if n == 1:
        return a
    if n == 2:
        determinant = a[0][0] * a[1][1] - a[0][1] * a[1][0]
        return determinant

    # recursive call
    minors = minor(a)
    return sum([(-1)**(i % 2) * mult(det(minors[0][i]), a[0][i])
                for i in xrange(3)])


def minor(a, fun = None):
    n, k = dim(a)
    out = ()
    for i in xrange(n):
        new_row = ()
        for j in xrange(k):
            sub = [list(r) for r in a if r != a[i]]
            for r in sub:
                del r[j]
            if fun is not None and len(sub) > 1:
                new_row += (fun(sub), )
            elif len(sub) == 1:
                new_row += (sub[0][0], )
            else:
                new_row += (sub, )
        out += (new_row, )
    return(out)


def cofactor(a):
    """
    Generate the cofactor matrix for matrix a
    :param a: matrix (list/tuple)
    :return: matrix (tuple)
    """
    cof = minor(a, det)
    n, k = dim(cof)
    out = ()
    for row in xrange(n):
        out += (([(-1)**(row + col % 2) * cof[row][col]
                  for col in xrange(k)]), )
    return out


def trans(a):
    n, k = dim(a)
    out = ()
    if n == 1:
        for j in xrange(k):
            out += ((a[0][j], ), )
    elif k == 1:
        out += ([a[i][0] for i in xrange(n)], )
    else:
        for j in xrange(k):
            new_row = ()
            for i in xrange(n):
                new_row += (a[i][j], )
            out += (new_row, )
    return out


def invert(a):
    """
    Inverts a matrix
    :param a: matrix (list/tuple)
    :return: matrix (tuple)
    """
    n, k = dim(a)

    if n != k:
        raise TypeError('invert() requires a square matrix.')

    det_a = det(a)  # determinant
    cof = cofactor(a)  # matrix of cofactors
    adj = trans(cof)  # adjugate matrix
    return mult(adj, (1.0 / det_a))


def ls(y, x):
    """
    Perform least squares regression
    :param y: dependent variable (list/tuple)
    :param x: independent variable (list/tuple)
    :return: beta vector (tuple)
    (X'X)^-1 * X'y
    """
    x = tuple([(1, ) + row for row in x])
    cofactor(inner(trans(x), x))
    XX_inv = invert(inner(trans(x), x))
    Xy = inner(trans(x), y)
    return inner(XX_inv, Xy)


# Week 7 code
def linear(x, a, b):
    return a * x + b


def gaussian(x, a, mu, sigma):
    return a * np.exp(-(x - mu)**2 / (2 * sigma**2))


def main():

    # calculate least squares beta coefficient using ls()
    beta_old = ls(variables['body'], variables['brain'])

    # calculate least squares beta coefficient using curve_fit()
    # reshape to go from (65, 1) to (65,)
    beta_new, vcov = curve_fit(linear, abrain, abody)

    print('Week 5 model: bo = %.4f * br + %.4f' %
          (beta_old[1][0], beta_old[0][0]))

    print('SciPy model: bo = %.4f * br + %.4f\n' %
          (beta_new[0], beta_new[1]))

    imports = 'from __main__ import curve_fit, linear, abrain, abody, ' +  \
                'brain, body, ls, gaussian'
    times = 1000
    scipy_implementation = timeit('curve_fit(linear, abrain, abody)', setup=imports,
                      number=times)
    my_implementation = timeit('ls(body, brain)', setup=imports,
                   number=times)
    gaussian_implementation = timeit('curve_fit(gaussian, abrain, abody)', setup=imports,
                                    number=times)

    for result in ('my_implementation', 'scipy_implementation', 'gaussian_implementation'):
        print('Avg execution time for %s (%i reps):\n%s' %
              (result, times, eval(result)))

    print('\nGuassian:\nscaling var = %.4f\nmu = %.4f\nsigma = %.4f' %
          tuple(curve_fit(gaussian, abrain, abody)[0]))

# read in data
variables = {'animal': (), 'brain': (), 'body': ()}
with open('Animals2.csv') as f:
    csv_file = csv.reader(f, delimiter = ',')
    for line in csv_file:
        variables['animal'] += (line[0], )
        variables['body'] += (line[1], )
        variables['brain'] += (line[2], )

# remove header
for v in variables.keys():
    variables[v] = variables[v][1:]

# convert brain & body elements to float
for v in ('brain', 'body'):
    variables[v] = [(float(num), ) for num in variables[v]]

# timeit doesn't like dict variables
brain = variables['brain']
body = variables['body']

# np.array for curve_fit
abrain = np.array(variables['brain']).reshape(len(variables['brain']))
abody = np.array(variables['body']).reshape(len(variables['body']))


if __name__ == '__main__':

    main()

