import csv
import sys

import numpy as np

from libcfcg import cf, helper
from libcfcg.cf import Color, Point

extension = "lut"  # one of {"lut", "evenness", "none"}


# used for handling the opencv window
def opencv_wait(window):
    k = window.waitKey(0)

    if k == 27:  # ESC
        window = None
        sys.exit(0)
    else:
        return


def read_ifs(filename):
    ifs = cf.IteratedFunctionSystem()
    ifs.read(filename)
    return ifs


def choose_transformation_for_sierpinski(point):
    if point[0] <= 0.5 and point[1] <= 0.5:
        return 0
    elif point[0] > 0.5 and point[1] <= 0.5:
        return 1
    else:
        return 2


def choose_transformation_for_test(point):
    if point[0] <= 0.5 and point[1] <= 0.5:
        return 0
    elif point[0] <= 0.5 and point[1] > 0.5:
        return 1
    else:
        return 2


# reads the palette file in basically just the given example
def read_file():
    # read LUT and copy to array 'colors'
    file = open('chaos_files/Multcol4.pal')
    reader = csv.reader(file, delimiter=',', quotechar='\n')
    read_colors = []
    for color in reader:
        read_colors.append(color)
    return read_colors


def main():
    # ifs = read_ifs("chaos_files/Invers.ifs")
    ifs = read_ifs("chaos_files/Invers.IFS")
    cfIntervalX = cf.Interval(ifs.getRangeX().getMin(),
                              ifs.getRangeX().getMax())
    cfIntervalY = cf.Interval(ifs.getRangeY().getMin(),
                              ifs.getRangeY().getMax())
    window = cf.WindowVectorized(512, cfIntervalX, cfIntervalY,
                                 "Inverser IFS Generator", cf.Color.WHITE)

    lut = read_file()

    window.show()

    steps = 15

    for i in range(512):
        for j in range(512):
            pixelPoint = Point(i, j)
            pointRe = window.transformPoint_fromImage_toInterval(pixelPoint)
            old_point = [pointRe.x, pointRe.y, 1]

            diverges = False
            iteration = 0

            for n in range(steps):
                transformation_index = choose_transformation_for_test(old_point)
                t = ifs.getTransformation(transformation_index)
                matrix = helper.convertMat3x3ToArray(t)
                new_point = np.matmul(matrix, old_point)
                if new_point[0] ** 2 + new_point[1] ** 2 >= 1000:
                    diverges = True
                    iteration = n
                    break
                else:
                    old_point = new_point
            if diverges:
                if extension == "evenness":
                    window.setColor(pointRe.x, pointRe.y, Color.GREEN if iteration % 2 == 0 else Color.RED)
                elif extension == "lut":
                    window.setColor(pointRe.x, pointRe.y, cf.Color(
                        int(lut[iteration][0]),
                        int(lut[iteration][1]),
                        int(lut[iteration][2])
                    ))
            else:
                window.setColor(pointRe.x, pointRe.y, Color.BLACK)

    window.show()

    while True:
        opencv_wait(window)


if __name__ == '__main__':
    main()

