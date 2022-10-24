# CF_1_2a_template.py
# AND

from libcfcg import cf
import sys
import time

i_range = 512 # 128 # 512
j_range = 512 # 128 # 512

def setPixels(window):
    # your code
    # outer loop
    for i in range(i_range):
        #inner loop
        for j in range(j_range):
            if (i & j == 0):
                window.setColor(i,j,cf.Color.RED)
    return

def main():
    window = cf.WindowRasterized(i_range, j_range, "CF_1_2a")
    window.setWindowDisplayScale(512/i_range)
    window.show()
    setPixels(window) # implement your code there
    window.show()
    print("Press any key to finish")
    sys.stdout.flush() # force output
    time.sleep(0.1) # wait for console; increase if necessary
    window.waitKey()

main()

window = None # destroy window