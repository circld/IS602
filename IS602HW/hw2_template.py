# 1. fill in this class
#   it will need to provide for what happens below in the
#	main, so you will at least need a constructor that takes the values as (Brand, Price, Safety Rating),
# 	a function called showEvaluation, and an attribute carCount

class CarEvaluation:
    'A simple class that represents a car evaluation'
    # Wasn't sure if you wanted us to define getters and setters, so used
    # introspection instead for extra practice.
    carCount = 0

    def __init__(self, make, price, safety):
        self.make, self.price, self.safety = make, price, safety
        CarEvaluation.carCount += 1

    def showEvaluation(self):
        """
        Prints a string communicating the attributes of the vehicle
        :return: None
        """
        print('The %s has a %s price and its safety is rated a %s' %
              (self.make, self.price, self.safety))


#2. fill in this function
#   it takes a list of CarEvaluation objects for input and either "asc" or "des"
#   if it gets "asc" return a list of car names order by ascending price
# 	otherwise by descending price
def sortbyprice(items, order='asc'):
    """
    :param items: array of CarEvaluation objects
    :param order: sort order ('asc' or 'des')
    :return: returns array of CarEvaluation sorted by price
    """

    def convert_levels(level):
        """
        Converts 'High', 'Med', 'Low' to 3, 2, 1 for sorting purposes
        :param level: 'High', 'Med', or 'Low'
        :return: integer reflecting level
        """
        if level == 'High':
            return 3
        elif level == 'Med':
            return 2
        else:
            return 1

    car_data = [(convert_levels(getattr(i, 'price')), getattr(i, 'make'))
                for i in items
                if hasattr(i, 'price') and hasattr(i, 'make')]
    car_data.sort(reverse=order == 'des')
    car_names = [val[1] for val in car_data]
    return car_names


#3. fill in this function
#   it takes a list for input of CarEvaluation objects and a value to search for
#	it returns true if the value is in the safety  attribute of an entry on the list,
#   otherwise false
def searchforsafety(items, safety):
    safety_vals = [getattr(i, 'safety') for i in items
                   if hasattr(i, 'safety')]
    return safety in safety_vals


# This is the main of the program.  Expected outputs are in comments after the function calls.
if __name__ == "__main__":
    car_methods = {}
    # I am not sure if I understood the optional portion of the exercise
    # but took a stab at it. Would be good to see exactly what you had in
    # mind next class
    for method in dir(CarEvaluation):
        car_methods[method] = getattr(CarEvaluation, method)

    eval1 = CarEvaluation("Ford", "High", 2)
    eval2 = CarEvaluation("GMC", "Med", 4)
    eval3 = CarEvaluation("Toyota", "Low", 3)

    print "Car Count = %d" % getattr(CarEvaluation, 'carCount')  # Car Count = 3

    car_methods['showEvaluation'](eval1)  # The Ford has a High price and it's safety is rated a 2
    car_methods['showEvaluation'](eval2)  # The GMC has a Med price and it's safety is rated a 4
    car_methods['showEvaluation'](eval3)  # The Toyota has a Low price and it's safety is rated a 3

    L = [eval1, eval2, eval3]

    print sortbyprice(L, "asc")  # [Toyota, GMC, Ford]
    print sortbyprice(L, "des")  # [Ford, GMC, Toyota]
    print searchforsafety(L, 2)  # true
    print searchforsafety(L, 1)  # false