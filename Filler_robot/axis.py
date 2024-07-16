from motor import Motor

class Axis():
	def __init__(self, name_axis) -> None:
		self.name_axis = name_axis
		                                                                        
		self.motor = None

		self.distance_move = 0
		self.direction_move = False
		self.ready = False
		
		self.limit_min = -7
		self.limit_max = 700
		self.error_limit = False
		
		self.arm_lenght = 12

		self.angle_0 = 0
		self.angle = 0
		self.step_angle = 0.18

		self.x0 = 0
		self.y0 = 0
		self.z0 = 0
		self.x = 0
		self.y = 0
		self.z = 0


	def go_coord(self, multi, angle) -> None:
		if self.ready == False:
			angle_real = self.motor.value * self.step_angle

			angle_distance = abs(angle_real + angle)
			#print(self.name_axis, self.distance)
			distance = angle_distance / self.step_angle

			if distance > 0:
				if angle >= angle_real:
					self.motor.move(multi, True, distance)
				else:
					self.motor.move(multi, False, distance)
			else: 
				self.ready = True
			
				print(self.name_axis, self.ready)


axis_x = Axis('x')
axis_x.motor = Motor(4, 3, 26)
axis_x.angle = 0
axis_x.angle_0 = 0
axis_x.limit_min = -500
axis_x.limit_max = 500

axis_y = Axis('y')
axis_y.motor = Motor(2, 17, 13)
axis_y.angle = 0
axis_y.angle_0 = 120
axis_y.y0 = 0
axis_y.z0 = 22
axis_y.limit_min = -1000
axis_y.limit_max = 1200

axis_z = Axis('z')
axis_z.motor = Motor(14, 15, 19)
axis_z.angle = 0
axis_z.angle_0 = -30
axis_z.limit_min = -500
axis_z.limit_max = 500