import math
from PIL import Image, ImageFilter, ImageChops
import operator
import os
import numpy as np


# https://stackoverflow.com/questions/1927660/compare-two-images-the-python-linux-way
def rmsdiff(ha, hb):
    h1 = ha.histogram()
    h2 = hb.histogram()

    return math.sqrt(reduce(operator.add,
                            map(lambda a, b: (a - b) ** 2, h1, h2)) / len(h1))


# https://www.hdm-stuttgart.de/~maucher/Python/MMCodecs/html/basicFunctions.html
def entropy(signal):
    lensig = signal.size
    symset = list(set(signal))
    numsym = len(symset)
    propab = [np.size(signal[signal == i]) / (1.0 * lensig) for i in symset]
    ent = np.sum([p * np.log2(1.0 / p) for p in propab])
    return ent


# https://www.hdm-stuttgart.de/~maucher/Python/MMCodecs/html/basicFunctions.html
def entropy_matrix(greyIm, N = 3):
    S = greyIm.shape
    E = np.array(greyIm)
    for row in range(S[0]):
        for col in range(S[1]):
            Lx = np.max([0, col - N])
            Ux = np.min([S[1], col + N])
            Ly = np.max([0, row - N])
            Uy = np.min([S[0], row + N])
            region = greyIm[Ly:Uy, Lx:Ux].flatten()
            E[row, col] = entropy(region)

    return E


def entropy_matrix_image(colorIm):
    greyIm = colorIm.convert('L')
    colorIm = np.array(colorIm)
    greyIm = np.array(greyIm)

    return entropy_matrix(greyIm)


def complexity_score(ha):
    return np.sum(entropy_matrix(entropy_matrix_image(
        ha
    )))


def is_interesting(image, bottom_threshold=500, width=80, height=80):
        image.resize((width, height), Image.ANTIALIAS)
        score = complexity_score(image)

        return bottom_threshold < score


def process_image_set(filenames, images, type, bottom_threshold=500, top_threshold=9999999):
    imin = -1
    imax = 0

    correct_count = 0

    for i in range(0, len(filenames)):
        print 'Processing %s...' % filenames[i]
        img = images[i].resize((80, 80))
        score = complexity_score(img)

        interesting = score<top_threshold and score>bottom_threshold

        correct = (type.lower() == 'interesting') == interesting

        if correct:
            correct_count += 1

        print '%s, %s, %s\t\t%s\t(%s)' % (type, filenames[i], score, 'INTERESTING' if interesting else 'NONINTERESTING','correct' if correct else 'incorrect')


        if imin is -1:
            imin = score

        if imin > score:
            imin = score

        if imax < score:
            imax = score

    stats = (imin, imax, imax - imin, float(correct_count)/float(len(images))*100)

    print 'min: %s, max: %s, range: %s, accuracy: %s%%' % stats

    return stats


def main(root="test_images"):
    interesting_filenames = os.listdir("%s/interesting" % root)
    uninteresting_filenames = os.listdir("%s/uninteresting" % root)

    interesting_images = []
    for name in interesting_filenames:
        interesting_images.append(Image.open("%s/interesting/%s" % (root, name)))
    uninteresting_images = []
    for name in uninteresting_filenames:
        uninteresting_images.append(Image.open("%s/uninteresting/%s" % (root, name)))

    interesting_stats = process_image_set(interesting_filenames, interesting_images, 'interesting')
    print '----'
    uninteresting_stats = process_image_set(uninteresting_filenames, uninteresting_images, 'uninteresting')

    print '----'

    print uninteresting_stats[1] - interesting_stats[0]


if __name__ == "__main__":
    main(root="test_images")