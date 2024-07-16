
class Axis:
    def __init__(self, angle) -> None:
        self.angle = angle
         
    def angle_real(self):
        return self.angle 


axis_x = Axis(122)
axis_y = Axis(75)
axis_x = Axis(20)


class Robot:
    def find_steps(self, angle_x, angle_y, angle_z):
        angle_x0 = self.axis_x.angle_real()
        angle_y0 = self.axis_y.angle_real()
        angle_z0 = self.axis_z.angle_real()

        step_x = 0
        step_y = 0
        step_z = 0

        while True:
            if angle_x > angle_x0:
                step_x += 1
            else:
                step_x -= 1
