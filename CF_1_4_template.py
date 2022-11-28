# CF_1_4_template.py
# rectangle subdivision
# Here with "WindowRasterized" - that means (0,0) is top/left !!!

from libcfcg import cf
import sys
import time

color = cf.Color.BLACK
i_range = 512  # 64 #8
j_range = 512  # 64 #8
counter = 0

###
# Recursive function painting the top right rectangle
# window: surface of the framework
# bot_left: bottom left corner of the rectangle to be processed
# top_right: top right corner of the rectangle to be processed
###
def paint(window, bot_left, top_right):
    width = top_right.x - bot_left.x + 1
    height = bot_left.y - top_right.y + 1
    # Example for drawing a rectangle
    # (1. param: bottom left corner, 2. param: top right corner)
    middlepoint = cf.Point(bot_left.x + width / 2, bot_left.y - height / 2)
    middlepoint_l_b = cf.Point(middlepoint.x/2, middlepoint.y*1.5)
    middlepoint_r_b = cf.Point(middlepoint.x*1.5,middlepoint.y*1.5)
    middlepoint_l_t = cf.Point(middlepoint.x/2,middlepoint.y/2)

    uppermiddlepoint = cf.Point(middlepoint.x, 0)
    lowermiddlepoint = cf.Point(middlepoint.x, height-1)
    leftmiddlepoint = cf.Point(0, middlepoint.y)
    rightmiddlepoint = cf.Point(width-1, middlepoint.y)

    window.drawRectangle(middlepoint, top_right, -1, cf.Color.BLACK)
    window.drawRectangle(middlepoint_l_t, uppermiddlepoint,-1,cf.Color.BLACK)
    window.drawRectangle(middlepoint_l_b,middlepoint,-1,cf.Color.BLACK)
    window.drawRectangle(middlepoint_r_b,rightmiddlepoint,-1,cf.Color.BLACK)
    window.show()   # show the progress after every recursive function call
    window.waitKey()
    # Your code here:
    # 1.) Call the recursive function for the top left, bottom left and
    #     bottom right square

    paint(window,middlepoint,top_right)

    # 2.) Terminate process right in time



def main():
    window = cf.WindowRasterized(i_range, j_range, "CF_1_4")
    window.setWindowDisplayScale(512 / i_range)
    window.clear(cf.Color.RED)
    # Define initial corners
    bot_left = cf.Point(0, window.getHeight() - 1)
    top_right = cf.Point(window.getWidth() - 1, 0)
    # Call the recursive function
    paint(window, bot_left, top_right)
    window.show()
    print("Press any key to finish")
    sys.stdout.flush()
    time.sleep(0.1)
    window.waitKey()


main()

window = None