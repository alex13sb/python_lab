# CF_1_4_template.py
# rectangle subdivision
# Here with "WindowRasterized" - that means (0,0) is top/left !!! 

from libcfcg import cf
import sys
import time

color = cf.Color.BLACK
i_range = 512 #64 #8
j_range = 512 #64 #8
zaehler = 0
###
# Recursive function painting the top right rectangle
# window: surface of the framework
# bot_left: bottom left corner of the rectangle to be processed
# top_right: top right corner of the rectangle to be processed
###
def paint(window, bot_left, top_right):
    width = top_right.x - bot_left.x + 1 # berechnet max-X - min-X
    height = bot_left.y - top_right.y + 1 # berechnet max-Y - min-Y
    #top right rectangle
    middle = cf.Point(bot_left.x + width/2, bot_left.y - height/2)

    # draw top right rectangle
    window.drawRectangle(middle, top_right,
                         -1, cf.Color.BLACK)  # -1 indicates 'fill rect'

    window.show()
    global zaehler
    zaehler += 1
    if zaehler == 1:
        bot_left.y = bot_left.y + height/2
        top_right.y = top_right.y + height/2
        paint(window, bot_left, top_right)
    if zaehler == 2:
        bot_left.x = bot_left.x - width/2
        top_right.x = top_right.x - width/2
        paint(window, bot_left, top_right)
    if zaehler == 3:
        bot_left.y = bot_left.y - height/2
        top_right.y = top_right.y - height/2
        paint(window, bot_left, top_right)



def main():
    window = cf.WindowRasterized(i_range, j_range, "CF_1_4")
    window.setWindowDisplayScale(512/i_range)
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