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
def entropy_matrix(colorIm):
    greyIm = colorIm.convert('L')
    colorIm = np.array(colorIm)
    greyIm = np.array(greyIm)

    N = 5
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


def image_entropy(image):
    return np.mean(entropy_matrix(image))


def complexity_score(ha):
    return image_entropy(ha.filter(ImageFilter.BLUR))


def is_interesting(image, top_threshold=4.9, bottom_threshold=4, width=80, height=80):
        image.thumbnail((width, height))
        score = complexity_score(image)

        return bottom_threshold < score < top_threshold


def process_image_set(filenames, images, type, top_threshold=4.9, bottom_threshold=4):
    imin = -1
    imax = 0

    correct_count = 0

    for i in range(0, len(filenames)):
        print 'Processing %s...' % filenames[i]
        images[i].thumbnail((80, 80))
        score = complexity_score(images[i])

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


def main():
    interesting_filenames = os.listdir("test_images/interesting")
    uninteresting_filenames = os.listdir("test_images/uninteresting")

    interesting_images = []
    for name in interesting_filenames:
        interesting_images.append(Image.open("test_images/interesting/%s" % name))
    uninteresting_images = []
    for name in uninteresting_filenames:
        uninteresting_images.append(Image.open("test_images/uninteresting/%s" % name))

    interesting_stats = process_image_set(interesting_filenames, interesting_images, 'interesting')
    print '----'
    uninteresting_stats = process_image_set(uninteresting_filenames, uninteresting_images, 'uninteresting')

    print '----'

    print uninteresting_stats[1] - interesting_stats[0]


if __name__ == "__main__":
    main()
    # img = Image.open("test_images/uninteresting/monochrome_rand_591.jpg")
    # img.thumbnail((80,80))
    # filtered = img.filter(ImageFilter.BLUR)
    # filtered.save("test.jpg")
    # print complexity_score(img)
    # print complexity_score(filtered)