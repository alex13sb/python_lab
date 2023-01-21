from libcfcg import cf
from libcfcg import helper
import sys
import math
import time


def opencv_wait(window):
    k = window.waitKey(0)
    if k == 27:  # ESC
        return True
    else:
        return False


def mySign(value):  # difference to NumPy:  mySign(0)=1    !!!
    if value < 0:
        return -1
    return 1


def read_orb(filename):
    orb = cf.Orbit()
    orb.read(filename)
    return orb


def step_point(factors, point):
    critical = (abs(factors[6] * point[0] + factors[7]) ** float((1 / 2)))
    new_x = factors[0] + \
            factors[1] * point[1] + \
            factors[2] * abs(point[0]) + \
            factors[3] * (point[0] ** 2 + factors[4]) + \
            mySign(point[0]) * factors[5] * critical
    new_y = factors[8] + factors[9] * point[0]
    return [new_x, new_y, 1]


def calculate(x_old, y_old, factors):
    x_new = y_old - (mySign(x_old) * math.sqrt(
        math.fabs(factors[6] * x_old + factors[7])))
    y_new = factors[8] + (factors[9] * x_old)
    return [x_new, y_new]


def draw(filename, henon_value=None):
    orb = read_orb(filename)

    if henon_value is None:
        window = cf.WindowVectorized(512, orb.getRangeX(), orb.getRangeY(),
                                 f'{filename}', cf.Color.WHITE)
    else:
        window = cf.WindowVectorized(512, orb.getRangeX(), orb.getRangeY(),
                                     f'{filename}, {henon_value}', cf.Color.WHITE)

    steps = 100000
    counter = 0
    factors = list(orb.getAllFactors())
    startingPoints = orb.getAllStartingPoints()
    for sp in startingPoints:
        if orb.getNumStartingPoints() == 1:
            vec = helper.convertVec3ToArray(sp)
    point = vec

    if henon_value is not None:
        factors[3] = henon_value

    for iteration in range(steps):
        if iteration % 200 == 0:
            changeColor = cf.Color_RandomColor()
            #window.show()  ##optional für ausgabe
            #window.waitKey()  ##optional für ausgabe
        counter += 1
        point = step_point(factors, point)
        if counter > 50:
            if orb.getRangeX().getMin() < point[
                0] < orb.getRangeX().getMax() and \
                    orb.getRangeY().getMin() < point[
                1] < orb.getRangeY().getMax():
                window.setColor(point[0], point[1], changeColor)
    window.show()
    return window


def ex_orb():
    file_list = ["brezel_1.orb", "kissen_1.orb", "spinne_1.orb", "gingerm.orb",
                 "henon.orb"]
    henon_values = iter([-1.4, -0.367, -0.912, -1.025, -1.051, -1.2, -1.25,
                         -1.26])
    for filename in file_list:
        if "henon" in filename:
            for henon_value in henon_values:
                window = draw("chaos_files/" + filename, henon_value)
                opencv_wait(window)
        else:
            window = draw("chaos_files/" + filename)
        opencv_wait(window)


if __name__ == '__main__':
    ex_orb()
