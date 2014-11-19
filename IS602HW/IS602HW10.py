# IS602 Week 10 Assignment
# Paul Garaud

import Tkinter, tkFileDialog
import os
import pandas as pd
from numpy import NaN
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


root = Tkinter.Tk()
root.withdraw()


def is_empty_quit(filename):
    if filename is None:
        print 'You did not select a file.'
        os._exit(0)


def populate(dict_obj, **kwargs):
    for key, val in kwargs.items():
        dict_obj[key] = val
    return dict_obj


def plot_cars():

    car_file = tkFileDialog.askopenfile(title='Please select cars.data.csv',
                                        filetypes=[('CSV files', '.csv')])
    is_empty_quit(car_file)
    cars = pd.read_csv(car_file, names=('buying', 'maint', 'doors', 'persons',
                                       'lug_boot', 'safety', 'dropme'),
                       header=None)
    cars = cars[cars.columns[:-1]]  # don't even remember what last col represents

    # getting data into numerical datatypes
    # next line works bc these columns are already sorted in desc order
    for val, num in zip(cars.buying.unique(), xrange(4, 0, -1)):
        cars[['buying', 'maint']] = cars[['buying', 'maint']].replace(val, num)

    # next line works bc this column is already sorted in asc order
    for val, num in zip(cars.safety.unique(), xrange(1, 4)):
        cars['safety'] = cars['safety'].replace(val, num)

    # doors not numeric
    cars['doors'] = cars['doors'].replace('5more', 5).astype('int64')

    cols = ('buying', 'maint', 'safety', 'doors')
    fig, ((p0, p1), (p2, p3)) = plt.subplots(2, 2)
    plots = {c: p for c, p in zip(cols, (p0, p1, p2, p3))}
    for col in cols:
        plots[col].hist(list(cars[col]), bins=len(cars[col].unique()),
                        histtype='stepfilled')
        plots[col].set_title(col)
    plt.show()


def plot_regression():
    animals_file = tkFileDialog.askopenfile(title='Please select Animals2.csv',
                                            filetypes=[('CSV files', '.csv')])
    is_empty_quit(animals_file)
    animals = pd.read_csv(animals_file, names=('animal', 'body', 'brain'),
                          skiprows=1)
    beta, vcov = curve_fit(lambda x, a, b: a * x + b, animals.body, animals.brain)

    plt.plot(animals.body, animals.brain, 'ko')
    plt.plot(animals.body, animals.body * beta[0] + beta[1])
    plt.xlabel('Body weight (kg)')
    plt.ylabel('Brain weight (g)')
    plt.text(10000, 1000, 'Body = %.4f * Brain + %.4f' % (beta[0], beta[1]))
    plt.title('The Relationship Between Brain Weight and Body Weight in Animals')
    plt.show()


def plot_centroids():
    image_file = tkFileDialog.askopenfilename(title='Please select Animals2.csv',
                                            filetypes=[('Image files',
                                                        ('.png', '.jpg', '.bnp'))])
    is_empty_quit(image_file)
    image = plt.imread(image_file)

    # centers (hard-coded)
    centers = [(73.979210290158534, 508.5656595871971, 1.0),
               (159.66453323580507, 181.65497851330346, 1.0),
               (148.95829596412557, 410.29439461883408, 1.0),
               (371.22474010344649, 418.99231832846829, 1.0),
               (281.88297872340428, 259.5, 1.0),
               (299.5, 136.5, 1.0),
               (326.50460405156537, 186.53738489871085, 1.0),
               (399.38095238095241, 94.238095238095241, 1.0),
               (437.19278510473237, 170.32816136539952, 1.0)]
    cent_y = [i[0] for i in centers]
    cent_x = [i[1] for i in centers]

    # display
    plt.imshow(image)
    plt.scatter(cent_x, cent_y, color='red')
    plt.show()


def plot_intervals():
    options = dict()
    populate(options,
             filetypes=[('Text files', '.txt'), ('All files', '.*')],
             initialfile='epa-http.txt',
             title='Please select the text file containing the EPA-HTTP data.')
    fileloc = tkFileDialog.askopenfile(**options)
    is_empty_quit(fileloc)

    # read into Pandas
    read_options = dict()
    populate(read_options,
             names=('domain', 'time', 'request', 'reply', 'bytes'),
             sep=' ',
             na_values={'bytes': ['-']})
    data = pd.read_table(fileloc, **read_options)

    # update time col to datetime object
    data.time.replace('[\[\]]', '', regex=True, inplace=True)
    subset = data.time < '30:00:00:00'
    data.time[subset] = '8-29-1995 ' + data.time[subset].astype(str)
    data.time[-subset] = '8-30-1995 ' + data.time[-subset].astype(str)
    data.time.replace(' \d{2}:', ' ', regex=True, inplace=True)
    data.time = pd.to_datetime(data.time, format='%m-%d-%Y %H:%M:%S')

    # reindex on time
    data.index = data.time
    data.drop('time', 1, inplace=True)

    # dealing with bastion.fdic.gov (munging reply column)
    okay = data.reply.str.contains('[0-9]{3}')
    data.request[-okay] = data.request[-okay] + data.reply[-okay]
    data.reply[-okay] = data.bytes[-okay]
    data.bytes[-okay] = NaN
    data.reply = data.reply.astype('int32')

    # plot data
    p = pd.period_range(data.index.min(), pd.to_datetime('1995-08-30 23:59:00'), freq='H')
    x = p.unique() - 224927
    y = data.groupby([data.index.map(lambda y: y.day),
                      data.index.map(lambda x : x.hour)]).count().request
    plt.plot(x, y)
    plt.xlabel('Time in hours (0 = 23:00 8/30/1995)')
    plt.ylabel('Number of requests')
    plt.title('Requests per hour (23:53 8/29/1995 to 23:07 8/30/1995)))))')
    plt.show()


def main():

    # Cars
    plot_cars()

    # Regression
    plot_regression()

    # Center points
    plot_centroids()

    # HTTP requests
    plot_intervals()


if __name__ == '__main__':

    main()