import math
from PIL import Image, ImageFilter, ImageChops
import operator
import os


# https://stackoverflow.com/questions/1927660/compare-two-images-the-python-linux-way
def rmsdiff(ha, hb):
    h1 = ha.histogram()
    h2 = hb.histogram()

    return math.sqrt(reduce(operator.add,
                           map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))


def complexity_score(image):
    return rmsdiff(image,image.filter(ImageFilter.FIND_EDGES))


def process_image_set(filenames, images, type):
    imin=-1
    imax=0

    for i in range(0,len(filenames)):
        score = complexity_score(images[i])
        print '%s, %s, %s' % (type, filenames[i], score)

        if imin is -1:
            imin = score

        if imin > score:
            imin = score

        if imax < score:
            imax = score

    print 'min: %s, max: %s, range: %s' % (imin, imax, imax-imin)

if __name__ == "__main__":
    interesting_filenames = os.listdir("test_images/interesting")
    uninteresting_filenames = os.listdir("test_images/uninteresting")

    interesting_images = []
    for name in interesting_filenames:
        interesting_images.append(Image.open("test_images/interesting/%s" % name))
    uninteresting_images = []
    for name in uninteresting_filenames:
        uninteresting_images.append(Image.open("test_images/uninteresting/%s" % name))

    process_image_set(interesting_filenames, interesting_images, 'interesting')
    print '----'
    process_image_set(uninteresting_filenames, uninteresting_images, 'uninteresting')