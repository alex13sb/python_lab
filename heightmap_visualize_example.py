from libcfcg import helper
from libcfcg import cf


def loadHeightMap(path):
    img = cf.WindowRasterized(path)
    heightMap = []
    for y in range(img.getHeight()):
        heightMap.append([])
        for x in range(img.getWidth()):
            value = img.getColor(x, y).r
            heightMap[-1].append(value)

    img.show()
    return heightMap

def loadColorsFromPalFile(path):
    file = open(path)
    colors = []
    while True:
        line = file.readline()
        if len(line) == 0:
            break

        s = line.split(',')
        colors.append(cf.Color(int(s[0]), int(s[1]), int(s[2])))

    file.close()
    return colors

def getCylinders(heightMap, colors):
    cylinders = cf.LinCylinderVec()
    for y in range(len(heightMap)):
        for x in range(len(heightMap[y])):
            height = heightMap[x][y]
            visualHeight = height / 4.0 + 1 # offset of 1 to avoid 'no cylinder'

            c = cf.Lin3DCylinder()
            c.diameter = 0.5
            c.color = colors[int(height)]
            c.position = helper.convertArrayToVec3([x, 0.0, y])
            c.direction = helper.convertArrayToVec3([0.0, visualHeight, 0.0])
            cylinders.push_back(c)

    return cylinders

# using Lin3D as a base isn't the best idea... sorry
window = cf.WindowLin3D(800, 800)

map = loadHeightMap("heightmap.png")
colors = loadColorsFromPalFile("chaos_files/Topo.pal")
cylinders = getCylinders(map, colors)
window.setCylinders(cylinders)

print("Ojbect very close to camera!!!")
print("Move object via keyboard or mouse: ")
print("Keyboard: q,e:Rotation; w,s:up/down; a/d:left/right; f/r:forward/back")
print("Mouse: right button or wheel: forward/back; left button: turn object")

print("Press ESC to finish; (then ignore ERROR and close 'Konsole')")
while True:
    key = window.waitKeyPressed(100)
    if key == 27: # 27 is 'ESC'
        break

window = None
