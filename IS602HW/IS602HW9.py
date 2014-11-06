# IS602 Week 9 Assignment
# Paul Garaud

import pandas as pd
from numpy import NaN
import Tkinter, tkFileDialog
import re


root = Tkinter.Tk()
root.withdraw()


def populate(dict_obj, **kwargs):
    for key, val in kwargs.items():
        dict_obj[key] = val
    return dict_obj


def main():

    # select data source
    options = dict()
    populate(options,
             filetypes=[('Text files', '.txt'), ('All files', '.*')],
             initialfile='epa-http.txt',
             title='Please select the text file containing the EPA-HTTP data.')
    fileloc = tkFileDialog.askopenfile(**options)

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

    # Which hostname or IP address made the most requests?
    print 'Most requests:'
    print data[['domain', 'request']].groupby(['domain']).count().sort('request', 0, False).ix[0]

    # Which hostname or IP address received the most bytes from the server?  How
    #   many bytes did it receive?
    print '\nMost bytes from server:'
    print data[['domain', 'bytes']].groupby(['domain']).sum().sort('bytes', 0, False).ix[0]

    # During what hour was the server the busiest in terms of requests?  (You can
    #   do this by grouping each hour period, e.g. 13:00 - 14:00. Then count the
    #   number of requests in each hour)
    p = pd.period_range(data.index.min(), pd.to_datetime('1995-08-31 00:00:00'), freq='H')
    print '\nBusiest hour:'
    busiest = data[['domain']].groupby(
        [data.index.map(lambda x: x.day),
         data.index.map(lambda y: y.hour)]
    ).count().sort('domain', 0, False).iloc[0]
    print '%i:00 - %i:00' % (busiest.name[1], busiest.name[1] + 1)


    # Which .gif image was downloaded the most during the day?
    print '\nMost downloaded .gif:'
    gifs = data.request.str.contains('.gif')
    data_by_gif = data[['domain', 'request']][gifs].groupby(['request'])
    most_gif = data_by_gif.count().sort('domain', 0, False).ix[0]
    print re.search(' .*?[.]gif', most_gif.name).group()

    # What HTTP reply codes were sent other than 200?
    print '\nHTTP reply codes (ex 200):'
    codes = pd.unique(data.reply)
    print sorted(codes[codes != 200])


if __name__ == '__main__':
    main()
