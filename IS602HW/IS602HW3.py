# IS602 Week 3 Assignment
# Paul Garaud

import Tkinter, tkFileDialog
import re


root = Tkinter.Tk()
root.withdraw()


def load_data():
    """
    Load csv specified in pop-up dialog into memory
    :return: list of elements for each row in csv
    """
    file_path = tkFileDialog.askopenfilename()
    out = None
    if file_path != '':
        try:
            openfile = open(file_path, 'r')
            out = [line.strip().split(',') for line in openfile]
        except IOError:
            print 'File could not be loaded.'
        finally:
            openfile.close()
    return out


def create_data_structure(data, valid_dict, colnames=None):
    """
    Create hash of column name -> element i in each row in data; assigns numbers if colnames omitted
    :param data: list of lists
    :valid_dict: a dictionary mapping columns to tuple of valid values
    :param colnames: iterable with column names
    :return: dictionary
    """
    if colnames is None:
        colnames = range(len(data[0]))
    out = {colnames[i]: [] for i in xrange(len(colnames))}
    for line in data:
        for col in colnames:
            value = line[colnames.index(col)]
            check_value(col, value, valid_dict)
            out[col] += [value, ]
    return out


def check_value(col_name, value, valid_dict):
    """
    Validates data and throws error if invalid.
    :param col_name: column value appears in
    :param value: value to check
    :valid_dict: a dictionary mapping columns to tuple of valid values
    :return:
    """
    if value not in valid_dict[col_name]:
        raise ValueError("'{0}' is not a valid value in column '{1}'.".format(
            value, col_name
        ))

def check_keys(data, keys):
    """
    Validates data dict keys (ie columns); raises KeyError if invalid
    :param data: dict
    :param keys: str or iterable
    :return: None
    """
    if type(keys) is str:
        keys = [keys, ]
    for k in keys:
        if k not in data.keys():
            raise KeyError('{0} is not a valid column name.'.format(k))


def save_data(data, col_order=None):
    """
    Saves the data to a CSV file
    :param data: a dictionary object mapping column names -> lists of data
    :return: None
    """
    if type(data) is not dict:
        raise TypeError('Data must be a dictionary, not {0}'.format(type(data)))
    if col_order is None:
        cols = data.keys()
    else:
        check_keys(data, col_order)
        cols = col_order
    file_path = tkFileDialog.asksaveasfilename()
    if file_path == '':
        return None
    try:
        save_file = open(file_path, 'w')
        for row in xrange(len(data[cols[0]])):
            record = ''
            for col in cols:
                record += '{0},'.format(data[col][row])
            save_file.write(record + '\n')
    finally:
        save_file.close()


def sort_rows(data, sort_on, order='desc'):
    """
    Order rows in data on the sort_on column name ordered on order argument
    :param data: a dictionary object mapping column names -> lists of data
    :param sort_on: column name to sort on
    :param order: 'asc' or 'desc'
    :return: dict
    """

    val_map = {'vhigh': 3, 'high': 2, 'med': 1, 'low': 0,
                '5more': 5, 'more': 5,
                'big': 2, 'med': 1, 'small': 0}
    check_keys(data, sort_on)  # check column names for validity
    tmp_data = []
    i = 0
    for element in data[sort_on]:
        if re.match(r'^[0-9]$', element):
            value = int(element)
        else:
            value = val_map[element]
        tmp_data.append((value, i, element))
        i += 1
    tmp_data.sort(reverse=order == 'desc')
    index = [a[1] for a in tmp_data]
    sort_data = {}
    for col in data.keys():
        sort_data[col] = [data[col][ind] for ind in index]
    return sort_data


def find_rows(data, cols, regex=None):
    """
    Returns rows for specified columns matching regex expression
    nb regex must match for ALL columns in a record
    :param data: a dictionary object mapping column names -> lists of data
    :param cols: one (string) or more columns (iterable) to search within
    :param regex: regex pattern
    :return: dict
    """
    check_keys(data, cols)  # check column names for validity
    pattern = re.compile(regex)
    # if single col, make iterable
    if type(cols) is str:
        cols = [cols, ]
    rows = len(data[cols[0]])
    return_rows = []  # store row qualifying indices
    for i in xrange(rows):
        for col in cols:
            match = re.search(pattern, data[col][i])
            if not match:
                if i in return_rows:
                    return_rows.remove(i)
                break  # no need to check other columns--this row is out
            elif match and i not in return_rows:
                return_rows.append(i)
    return_data = {}
    for col in data.keys():
        return_data[col] = []
        for j in return_rows:
            return_data[col] += [data[col][j]]
    return return_data


def print_rows(data, col_order=None, nrows=None):
    """
    Prints rows of the data set passed in the data arg
    :param data: a dictionary object mapping column names -> lists of data
    :param col_order: a list of columns defining order in which to print
    :param nrows: limit output to first n rows; None -> print all
    :return: None
    """
    if col_order is None:
        columns = data.keys()
    else:
        check_keys(data, col_order)
        columns = col_order
    # ensure that the formatting of the output is aligned properly
    template = "{0}{1: >12}{2: >12}{3: >12}{4: >12}{5: >12}"
    print template.format(*tuple(columns))
    for i in xrange(len(data[columns[0]])):
        if nrows is not None and nrows <= i:
            break
        print template.format(*tuple([data[col][i] for col in columns]))


def select_rows(data, sort_on=None, which=None, num=5, order='desc',
                rcols=None, regex=None, col_order=None):
    """
    Calls sort_rows, find_rows (if necessary), & print_rows using args passed
    :param data: a dictionary object mapping column names -> lists of data
    :param which: return 'top' or 'bottom' num columns; else return all
    :param num: if which is specified, limits results to num records
    :param sort_on: column name to sort on
    :param order: 'asc' or 'desc'
    :param rcols: one (string) or more columns (iterable) to search within;
        if None, regex must match all columns to return record
    :param regex: regex pattern
    :param col_order: column order of printed output
    :returns: None
    """

    # find subset of columns (if rcols/regex specified)
    tmp_data = data
    if regex is not None:
        if rcols is not None:
            check_keys(data, rcols)
        else:
            rcols = data.keys()
        tmp_data = find_rows(data, rcols, regex)

    # sort
    if sort_on is not None:
        check_keys(data, sort_on)
        tmp_data = sort_rows(tmp_data, sort_on, order)

    # top/bottom
    if num < 1:
        which = None
    if which == 'top':
        tmp_data = {col: tmp_data[col][:num] for col in data.keys()}
    elif which == 'bottom':
        tmp_data = {col: tmp_data[col][-num:] for col in data.keys()}

    # print
    print_rows(tmp_data, col_order)

    return tmp_data

if __name__ == '__main__':

    raw_data = load_data()
    columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety']
    data_dict = {'buying': ('low', 'med', 'high', 'vhigh'),
                 'maint': ('low', 'med', 'high', 'vhigh'),
                 'doors': ('2', '3', '4', '5more'),
                 'persons': ('2', '4', 'more'),
                 'lug_boot': ('small', 'med', 'big'),
                 'safety': ('low', 'med', 'high')}

    cars = create_data_structure(raw_data, data_dict, colnames=columns)

    # a. Print to the console the top 10 rows of the data sorted by 'safety'
    #    in descending order
    select_rows(cars, sort_on='safety', order='desc', which='top', num=10,
                col_order=columns)

    # b. Print to the console the bottom 15 rows of the data sorted by 'maint'
    #    in ascending order
    select_rows(cars, sort_on='maint', order='asc', which='bottom', num=15,
                col_order=columns)

    # c. Print to the console all rows that are high or vhigh in fields
    #    'buying', 'maint', and 'safety', sorted by 'doors' in ascending order.
    select_rows(cars, sort_on='doors', order='asc',
                rcols=['buying', 'maint', 'safety'],
                regex=r'v?high',
                col_order=columns)

    # d. Save to a file all rows (in any order) that are: 'buying': vhigh,
    #    'maint': med, 'doors': 4, and 'persons': 4 or more.
    to_save = select_rows(cars, rcols='buying', regex='vhigh')
    to_save = select_rows(to_save, rcols='maint', regex='med')
    to_save = select_rows(to_save, rcols='doors', regex='4')
    to_save = select_rows(to_save, rcols='persons', regex='(4|more)')
    save_data(to_save, col_order=columns)
