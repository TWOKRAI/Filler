from Filler_robot.Robots.robot_module import Robot_module




if __name__ == '__main__': 
    robot = Robot_module()
    # robot.inteface_on = True   
    # robot.run()
    robot.enable_motors(False)
    input()

    robot.enable_motors(True)

    robot.go_to_point(-10.8, 17.8, 11)
    input()
    robot.go_home()

    robot.enable_motors(True)
    input()

    robot.go_to_point(10.8, 17.8, 11)
    input()
    robot.go_home()

    input()
    robot.enable_motors(True)
    robot.go_to_point(0, 17.8, 11)
    input()
    robot.go_home()

    input()

    robot.go_to_point(12.8, 16.8, 11)
    robot.go_home()

    robot.go_to_point(0, 16.5, 15)
    robot.go_home()

    robot.go_to_point(-12.8, 16.5, 11)
    robot.go_home()