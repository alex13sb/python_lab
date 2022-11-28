import numpy as np
from libcfcg import cf
from libcfcg import helper
import math
import sys
import time
from random import randrange, randint

# read ifs file
ifs = cf.IteratedFunctionSystem()
##DRACHENFLAECHE_4.IFS,
##DUERER_5_ECK.IFS, KRISTALL_1.IFS, MENGER_TEPPICH.IFS, SIERP_Verwandter_1.IFS
##und zuletzt FARN_1.IFS.

ifs.read("chaos_files/KRISTALL_1.IFS")
xInterval = [ifs.getRangeX().getMin(), ifs.getRangeX().getMax()] # float interval that is mapped to the image
yInterval = [ifs.getRangeY().getMin(), ifs.getRangeY().getMax()]
print("x in Interval: ", xInterval)
print("y in Interval: ", yInterval)
cfIntervalX = cf.Interval(xInterval[0], xInterval[1])
cfIntervalY = cf.Interval(yInterval[0], yInterval[1])
probs = []
# get probabilities for trafos
for i in range(ifs.getNumTransformations()):
    matrix = cf.GlmMat3x3(ifs.getTransformation(i))
    det = matrix.at(0, 0) * matrix.at(1, 1) - matrix.at(1, 0) - matrix.at(0, 1)
    probs.append(det)

probability_sum = np.sum(probs)
for i in probs:
    probs[i] = probs[i]/probability_sum
# image corresponding to the 2D float interval
window = cf.WindowVectorized(512, cfIntervalX, cfIntervalY,
        "Window ifs")
window.drawAxis() # buffered and not displayed until show()

# if you like to scale the output image set the desired float value
window.setWindowDisplayScale(1.0)
window.show() # all drawing instructions buffered so far are executed
print("Use mouse to set a point")
sys.stdout.flush() # force output
time.sleep(0.1) # wait for console; increase if necessary
point = window.waitMouseInput()
vector = [point.x, point.y, 1] # Punkt wie in ifs_example.cpp/py
# gezeigt als Vektor mit 3 Komponenten (letzte Komponente = 1)
window.setColor(vector[0], vector[1], cf.Color.RandomColor())

for i in range(15000):
    matrix = helper.convertMat3x3ToArray(ifs.getTransformation(randint(0,
    ifs.getNumTransformations()-1)))
    new_vector = np.matmul(matrix, vector)
    window.setColor(new_vector[0], new_vector[1], cf.Color.RandomColor())
    vector = new_vector
    if (i % 100 == 0):
        window.show()
        print("100 iterations achieved")
        sys.stdout.flush()  # force output
        time.sleep(0.1)  # wait for console; increase if necessary
        window.waitKey()

