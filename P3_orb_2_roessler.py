from libcfcg import cf


def opencv_wait(window):
    k = window.waitKey(0)

    if k == 27:  # ESC
        return True
    else:
        return False


a = 0.2
b = 0.2
c = 5.7
dt = 0.04


def calc_new_point(p_alt):
    def f_x(x, y, z):
        return - (y + z)

    def f_y(x, y, z):
        return a * y + x

    def f_z(x, y, z):
        return b + x * z - c * z

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


def draw():
    window = cf.WindowVectorized(512, cf.Interval(-12, 15), cf.Interval(-8, 25),
                                 f'ex two', cf.Color.WHITE)

    window.show()

    p_alt = (1, 1, 1)
    p_new = p_alt
    i = 0

    while i < 20000:
        p_alt = p_new
        p_new = calc_new_point(p_new)

        if i > 1000:
            # P’alt = [x_alt, y_alt/2.0 + z_alt]
            # P’neu = [x_neu, y_neu/2.0 + z_neu]
            window.drawLine(
                cf.Point(p_alt[0], (p_alt[1] / 2) + p_alt[2]),
                cf.Point(p_new[0], (p_new[1] / 2) + p_new[2]),
                1, cf.Color.BLACK
            )

            if (i - 1000) % 25 == 0:
                window.show()

        i += 1

    opencv_wait(window)


def main():
    draw()


if __name__ == '__main__':
    main()
