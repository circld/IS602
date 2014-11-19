# IS602 Week 8 Assignment
# Paul Garaud

import Tkinter, tkFileDialog
import glob
from scipy.misc import imread, imsave
from scipy import ndimage
import numpy as np
from matplotlib import pyplot as plt


root = Tkinter.Tk()
root.withdraw()

def threshold(img, cutoff):
    return np.where(img > cutoff, 255., 0.)


def count_obj(img):
    return ndimage.measurements.label(img)


def find_center(img, labs, index):
    return ndimage.measurements.center_of_mass(img, labs, index)


def plot_and_show(labs, centers):
    plt.imshow(labs)
    # images represented as (y, x)
    plt.scatter([i[1] for i in centers], [i[0] for i in centers],
                color='darkgray')
    plt.show()

def main():

    # prompt user to select directory with images to process
    img_dir = tkFileDialog.askdirectory(title='Select directory of '
                                              'images to process.')
    images = glob.glob1(img_dir, '*.png')
    img_np = [imread(img_dir + '/' + img).astype(np.float32) for img in images]

    cutoff = 127.5
    kern_sd = 5

    for image in img_np:

        # smooth
        sm_image = ndimage.gaussian_filter(image, kern_sd)

        # threshold
        thresh = threshold(sm_image, cutoff)

        # count objs
        labelled, num_obj = count_obj(thresh)
        print '\nThis image appears to have %i objects' % num_obj

        # find centers
        centers = find_center(thresh, labelled, range(1, num_obj + 1))
        print centers

        # plot
        plot_and_show(labelled, centers)

        raw_input('\nPress any key to continue.')

    root.destroy()


if __name__ == '__main__':

    main()
