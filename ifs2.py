import numpy as np
from libcfcg import cf
from libcfcg import helper
import math
import sys
import time
import random

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


def draw(filename):
# read ifs file
    ifs = read_ifs(filename)
    xInterval = [ifs.getRangeX().getMin(), ifs.getRangeX().getMax()]
    yInterval = [ifs.getRangeY().getMin(), ifs.getRangeY().getMax()]
    cfIntervalX = cf.Interval(xInterval[0], xInterval[1])
    cfIntervalY = cf.Interval(yInterval[0], yInterval[1])

    dets = []
    # get probabilities for trafos
    for i in range(ifs.getNumTransformations()):
        matrix = cf.GlmMat3x3(ifs.getTransformation(i))
        det = abs(matrix.at(0, 0) * matrix.at(1, 1) - matrix.at(1, 0) * matrix.at(0, 1))
        dets.append(0.01 if det == 0 else det)

    probability_sum = np.sum(dets)
    probs = []
    for index in dets:
        probs.append(index/probability_sum)

    window = cf.WindowVectorized(512, cfIntervalX, cfIntervalY,
        "Window ifs", cf.Color.WHITE)

    # if you like to scale the output image set the desired float value
    window.setWindowDisplayScale(1.0)
    window.show() # all drawing instructions buffered so far are executed
    print("Use mouse to set a point")
    sys.stdout.flush() # force output
    time.sleep(0.1) # wait for console; increase if necessary
    point = window.waitMouseInput()
    vector = [point.x, point.y, 1]
    window.setColor(vector[0], vector[1], cf.Color.BLACK)

    for i in range(15000):
        random_number = random.uniform(0,1)
        counter = 0
        total = probs[0]
        for elem in probs:
            if total < random_number:
                counter += 1
                total += elem
                if counter == len(probs):
                    matrix = helper.convertMat3x3ToArray(
                        ifs.getTransformation(counter-1))
                    new_vector = np.matmul(matrix, vector)
                    window.setColor(new_vector[0], new_vector[1],
                                cf.Color.BLACK)
                    vector = new_vector
            else:
                matrix = helper.convertMat3x3ToArray(
                    ifs.getTransformation(counter))
                new_vector = np.matmul(matrix, vector)
                window.setColor(new_vector[0], new_vector[1],
                                cf.Color.BLACK)
                vector = new_vector
                break

        """
        if i % 100 == 0:
            window.show()
            print("100 iterations achieved")
            sys.stdout.flush()  # force output
            time.sleep(0.1)  # wait for console; increase if necessary
            window.waitKey()
        """
    window.show()
    return window

def ex_ifs2():
    file_list = ["farn_1.ifs", "filmstreifen.ifs", "wirbel_blatt.ifs", "strauch.ifs", "swirl.ifs"]
    for filename in file_list:
        window = draw("chaos_files/" + filename)
        opencv_wait(window)

if __name__ == '__main__':
    ex_ifs2()




