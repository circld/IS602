# IS602 Week 6 Assignment
# Paul Garaud

import numpy as np
from timeit import timeit


np.random.seed(100)
x = tuple(np.random.randint(-1000, 1000, 100))

def sortwithloops(input):

    def select_pivot(elements):
        pivot_choices = [input[0], input[len(input) / 2], input[-1]]
        pivot_choices.remove(max(pivot_choices))
        pivot_choices.remove(min(pivot_choices))
        return pivot_choices[0]

    # base case
    if len(input) <= 1:
        return input

    # Pick an element to act as pivot
    pivot = select_pivot(input)

    #  Reorder the array s.t. smaller els come before pivot, larger after
    small_array = [sm for sm in input if sm < pivot]
    pivot_array = [piv for piv in input if piv == pivot]
    big_array = [bg for bg in input if bg > pivot]

    # Repeat recursively
    sorted_list = []
    if len(small_array) > 0:
        sorted_list.extend(sortwithloops(small_array))
    if len(pivot_array) > 0:
        sorted_list.extend(pivot_array)
    if len(big_array) > 0:
        sorted_list.extend(sortwithloops(big_array))
    return sorted_list


def sortwithoutloops(input):
    return sorted(input)


def sortwithnumpy(input):

    return np.sort(input)


def searchwithloops(input, value):
    return sum([i == value for i in input]) > 0


def searchwithoutloops(input, value):
    return value in input


def searchwithnumpy(input, value):
    return np.array(input == value).any()


def main():

    std_message = 'Avg execution time for %s (1000 loops):'

    for func in ('sortwithnumpy', 'sortwithloops', 'sortwithoutloops'):
        print std_message % func
        print '{:.4f} seconds'.format(timeit(stmt='%s(x)' % func,
                     setup='from __main__ import %s, x' % func,
                     number=1000))
    for func in ('searchwithnumpy', 'searchwithloops', 'searchwithoutloops'):
        print std_message % func
        print '{:.4f} seconds'.format(timeit(stmt='%s(x, 236)' % func,
                     setup='from __main__ import %s, x' % func,
                     number=1000))


if __name__ == '__main__':

    main()
