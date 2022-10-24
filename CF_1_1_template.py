# CF_1_1_template.py
# chaos game

from libcfcg import cf
import sys
import time
import random

i_range = 256 # 64 # 128 # 512 
j_range = 256 # 64 # 128 # 512 
points = []
zaehler = 0
def Iteration(window):
    while True:
        # your code HERE
        global zaehler
        zaehler += 1
        randompoint = points[random.randrange(0, 3)]
        new_p_x = (points[3][0] + randompoint[0])/2
        new_p_y = (points[3][1] + randompoint[1])/2
        points[3] = (new_p_x,new_p_y)

        if zaehler % 100 == 0:
            p1 = cf.Point(new_p_x, new_p_y)
            window.setColor(p1.x, p1.y, cf.Color.RandomColor())
            window.drawCircle(p1, 13, 1, cf.Color.RandomColor())  # circle around point
            window.show()

        key = window.waitKey(1)
        if key == 27:
            break
    return

def main():

    window = cf.WindowRasterized(i_range, j_range, "CF_1_1")
    window.setWindowDisplayScale(512/i_range)
    window.show()

    print("Use mouse to set the points: q0, q1 and q2")
    for x in range(3):
        sys.stdout.flush() # force output
        time.sleep(0.1) # wait for console; increase if necessary
        point2 = window.waitMouseInput()
        window.drawCircle(point2, 2, -1, cf.Color.RED) # circle
        window.show()
        points.append([point2.x, point2.y])

    print("Now set your start point p")
    sys.stdout.flush()  # force output
    time.sleep(0.1)  # wait for console; increase if necessary
    point3 = window.waitMouseInput()
    window.drawCircle(point3, 2, -1, cf.Color.GREEN)  # circle
    window.show()
    points.append([point3.x, point3.y])

    print("Press ESC and keep pressed to exit iteration")
    Iteration(window) # implement your code there
    
    print("Press ENTER to exit")
    while True: 
        key = window.waitKey(1)          
        if key == 13: 
            break

main()
window = None # destroy window