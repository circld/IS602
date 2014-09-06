

#1. fill in this function
#   it takes a list for input and return a sorted version
#   do this with a loop, don't use the built in list functions
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

#2. fill in this function
#   it takes a list for input and return a sorted version
#   do this with the built in list functions, don't us a loop
def sortwithoutloops(input):
    return sorted(input)


#3. fill in this function
#   it takes a list for input and a value to search for
#	it returns true if the value is in the list, otherwise false
#   do this with a loop, don't use the built in list functions
def searchwithloops(input, value):
    return sum([i == value for i in input]) > 0


#4. fill in this function
#   it takes a list for input and a value to search for
#	it returns true if the value is in the list, otherwise false
#   do this with the built in list functions, don't use a loop
def searchwithoutloops(input, value):
    return value in input

if __name__ == "__main__":	
    L = [5,3,6,3,13,5,6]
    print sortwithloops(L)  # [3, 3, 5, 5, 6, 6, 13]
    print sortwithoutloops(L)  # [3, 3, 5, 5, 6, 6, 13]
    print searchwithloops(L, 5)  # true
    print searchwithloops(L, 11)  # false
    print searchwithoutloops(L, 5)  # true
    print searchwithoutloops(L, 11)  # false
