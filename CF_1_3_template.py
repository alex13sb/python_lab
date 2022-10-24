# CF_1_3_template.py
# Pascal triangle 
from libcfcg import cf
import sys
import time
import math

columns= 513 # 129 # 65 # 9 # ATTENTION: 1 additional column (x_range)
rows= 512 # 128 # 64 # 8 (y_range)

def combination(n, r): # correct calculation of combinations, n choose k
    return int((math.factorial(n)) / ((math.factorial(r)) * math.factorial(n - r)))

def calculateMatrix():
    matrix = [[]]
    for count in range(rows):
        row = [] #row element
        for element in range(count+1):
            row.append(combination(count, element))
        filled = len(row)
        zeros = [0] * (513-filled)
        row.extend(zeros)
        matrix.append(row)
    return matrix

def setOddValues(window, matrix):


    for x in range (columns):
        for y in range (rows):
            if (x * y) % 23 != 0:
                window.setColor(x,y, cf.Color.RED)
    return

def main():

    window = cf.WindowRasterized(columns-1, rows, "CF_1_3", cf.Color.BLACK)
    window.setWindowDisplayScale(512/rows)
    window.show()
    matrix = calculateMatrix() # implement your code there
    setOddValues(window, matrix) # implement your code there
    window.show()
    print("Press any key to finish")
    sys.stdout.flush()
    time.sleep(0.1)
    window.waitKey()

main()

window = None # destroy window



