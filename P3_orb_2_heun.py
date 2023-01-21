from libcfcg import cf


def opencv_wait(window):
    k = window.waitKey(0)

    if k == 27:  # ESC
        return True
    else:
        return False


a = 10.0 #aus Aufgabe
b = 2.667 #aus Aufgabe
c = [28.0]
dt = 0.01 #Schrittweite aus Aufgabe


def calc_new_point(p_alt, c_value):
    def f_x(x, y, z):
        return a * y - a * x

    def f_y(x, y, z):
        return c_value * x - y - x * z

    def f_z(x, y, z):
        return x * y - b * z

    return (
        p_alt[0] + (dt / 2) * (f_x(p_alt[0], p_alt[1], p_alt[2]) + f_x(
            p_alt[0] + f_x(p_alt[0], p_alt[1], p_alt[2]) * dt,
            p_alt[1] + f_y(p_alt[0], p_alt[1], p_alt[2]) * dt,
            p_alt[2] + f_z(p_alt[0], p_alt[1], p_alt[2]) * dt
        )),
        p_alt[1] + (dt / 2) * (f_y(p_alt[0], p_alt[1], p_alt[2]) + f_y(
            p_alt[0] + f_x(p_alt[0], p_alt[1], p_alt[2]) * dt,
            p_alt[1] + f_y(p_alt[0], p_alt[1], p_alt[2]) * dt,
            p_alt[2] + f_z(p_alt[0], p_alt[1], p_alt[2]) * dt
        )),
        p_alt[2] + (dt / 2) * (f_z(p_alt[0], p_alt[1], p_alt[2]) + f_z(
            p_alt[0] + f_x(p_alt[0], p_alt[1], p_alt[2]) * dt,
            p_alt[1] + f_y(p_alt[0], p_alt[1], p_alt[2]) * dt,
            p_alt[2] + f_z(p_alt[0], p_alt[1], p_alt[2]) * dt
        ))
    )


def draw(c_value=28.0):
    window = cf.WindowVectorized(512, cf.Interval(-22, 22), cf.Interval(-1, 55),
                                 f'ex two, C: {c_value}', cf.Color.WHITE)

    window.show()

    p_alt = (1, 1, 1) #startpunkt aus Aufgabe
    p_new = p_alt
    i = 0

    while i < 20000:
        p_alt = p_new
        p_new = calc_new_point(p_new, c_value)

        if i > 1000:
            # P’alt = [x_alt, z_alt] und P’neu = [x_neu, z_neu]
            window.drawLine(cf.Point(p_alt[0], p_alt[2]), cf.Point(p_new[0], p_new[2]), 1, cf.Color.BLACK)

            if i % 25 == 0:
                window.show()

        i += 1

    opencv_wait(window)


def main():
    for c_val in c:
        draw(c_val)


if __name__ == '__main__':
    main()
