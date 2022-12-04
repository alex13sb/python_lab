import random
import random
import sys

import numpy as np

from libcfcg import cf, helper
from libcfcg.cf import Color


# used for handling the opencv window
def opencv_wait(window):
    k = window.waitKey(0)

    if k == 27:  # ESC
        sys.exit(0)
    else:
        return


def read_ifs(filename):
    ifs = cf.IteratedFunctionSystem()
    ifs.read(filename)
    return ifs


def choose(prop_array):
    random_real_number = random.randrange(1000) / 1000
    prop_sum = 0
    for j in range(len(prop_array)):
        prop_sum += prop_array[j]
        if random_real_number < prop_sum:
            return j


def calc_fixpunkt(transformation_matrix):
    matrix = helper.convertMat3x3ToArray(transformation_matrix)
    a_k = matrix[0][0]
    b_k = matrix[0][1]
    c_k = matrix[1][0]
    d_k = matrix[1][1]
    e_k = matrix[0][2]
    f_k = matrix[1][2]
    x_f = (-e_k * (d_k - 1.0) + b_k * f_k) / ((a_k - 1) * (d_k - 1) - b_k * c_k)
    y_f = (-f_k * (a_k - 1) + c_k * e_k) / ((a_k - 1) * (d_k - 1) - b_k * c_k)
    return [x_f, y_f, 1]


def draw(filename, do_calc_fixpunkt: bool = True):
    ifs = read_ifs(filename)
    cfIntervalX = cf.Interval(ifs.getRangeX().getMin(),
                              ifs.getRangeX().getMax())
    cfIntervalY = cf.Interval(ifs.getRangeY().getMin(),
                              ifs.getRangeY().getMax())
    window = cf.WindowVectorized(512, cfIntervalX, cfIntervalY,
                                 f'IFS Generator: {filename}', cf.Color.WHITE)

    steps = 15000

    window.show()

    if do_calc_fixpunkt:
        old_point = calc_fixpunkt(ifs.getTransformation(0))
    else:
        point = window.waitMouseInput()
        old_point = [point.x, point.y, 1]

    # calculate probabilities for each transformation
    prob_array = []
    sum_determinants = 0
    for i in range(ifs.getNumTransformations()):
        # get the transformation
        t = ifs.getTransformation(i)
        matrix = helper.convertMat3x3ToArray(t)

        # calculate the determinant
        det = abs(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])
        # if it is 0 use a small number instead
        prob_array.append(0.01 if det == 0 else det)

        # calculate the sum of all determinants
        sum_determinants += prob_array[i]
    # divide all determinants by the this sum
    # to compute the probabilities p in (0, 1]
    prob_array = [prob_array[i] / sum_determinants
                  for i in range(len(prob_array))]

    for _ in range(steps):
        random_index = choose(prob_array)
        t = ifs.getTransformation(random_index)
        matrix = helper.convertMat3x3ToArray(t)
        new_point = np.matmul(matrix, old_point)
        window.setColor(new_point[0], new_point[1], Color.BLACK)
        old_point = new_point
    window.show()
    return window


def ex_ifs2():
    file_list = ["farn_1.ifs", "filmstreifen.ifs", "wirbel_blatt.ifs", "strauch.ifs", "swirl.ifs"]

    for filename in file_list:
        window = draw("chaos_files/" + filename)
        opencv_wait(window)

if __name__ == '__main__':
    ex_ifs2()

