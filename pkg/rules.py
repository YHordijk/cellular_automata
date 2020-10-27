import numpy as np
import noise 



class Rule:
	def iterate(self, array):
		return array


	def get_surrounding_cells(self, array, direction=(1,0)):
		'''
		direction is tuple specifying the direciton of the neighbour:
		North (1,0)
		West (0,-1)
		South (-1,0)
		East (0,1)
		'''

		return np.roll(array, shift=direction, axis=(0,1))



class Waves(Rule):
	def __init__(self, wind=(1,1), new_waves=5, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.wind = wind
		self.new_waves = new_waves


	def get_default_array(self, size=(100,100)):
		seed = 1000 * np.random.randn()
		array = np.zeros(size)
		for y in range(size[1]):
			for x in range(size[0]):
				array[y,x] = noise.snoise2(10*x/size[0],10*y/size[1], base=seed)

		return array


	def iterate(self, array):
		array_shape = array.shape
		split = array * np.random.random(array_shape)*1.5

		array = array - split

		#get 8 cardinal directions:
		N  = self.get_surrounding_cells(array, ( 1, 0))
		NW = self.get_surrounding_cells(array, ( 1,-1))
		W  = self.get_surrounding_cells(array, ( 0,-1))	
		SW = self.get_surrounding_cells(split, (-1,-1))
		S  = self.get_surrounding_cells(array, (-1, 0))
		SE = self.get_surrounding_cells(array, (-1, 1))
		E  = self.get_surrounding_cells(array, ( 0, 1))
		NE = self.get_surrounding_cells(array, ( 1, 1))

		array = array + 0.5*SW + 0.5*S

		# new_wave_indices = np.hstack((np.random.randint(array_shape[0], size=(self.new_waves, 1)), np.random.randint(array_shape[1], size=(self.new_waves, 1))))
		# array[new_wave_indices] = 0.8

		return array


class GOL(Rule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def get_default_array(self, size=(100,100), preset='random'):
		if preset == 'random':
			array = np.random.randint(2, size=size)
			print(array)

		if preset == 'blinker':
			array = np.array([[0, 0, 0, 0, 0],
					  		  [0, 0, 1, 0, 0],
					  		  [0, 0, 1, 0, 0],
					  		  [0, 0, 1, 0, 0],
					  		  [0, 0, 0, 0, 0]])

		return array


	def iterate(self, array):
		N  = self.get_surrounding_cells(array, ( 1, 0))
		NW = self.get_surrounding_cells(array, ( 1,-1))
		W  = self.get_surrounding_cells(array, ( 0,-1))	
		SW = self.get_surrounding_cells(array, (-1,-1))
		S  = self.get_surrounding_cells(array, (-1, 0))
		SE = self.get_surrounding_cells(array, (-1, 1))
		E  = self.get_surrounding_cells(array, ( 0, 1))
		NE = self.get_surrounding_cells(array, ( 1, 1))


		#rule 1: any cell with less than 2 live neighbours dies
		total_neighbours = N + NW + W + SW + S + SE + E + NE
		array = np.where(total_neighbours < 2, 0, array)

		#rule 3: any cell with more than 3 live neighbours dies
		array = np.where(total_neighbours > 3, 0, array)

		#rule 4: any cell with exactly 3 neighbours revives
		array = np.where(total_neighbours == 3, 1, array)

		return array


class SoftReset(Rule):
	# https://www.reddit.com/r/generative/comments/j5pnij/soft_reset/
	def __init__(self, comparison_number=240, dead_rule_range=(213, 250), dead_rule_increment=5, 
			live_rule_range=(146, 250), live_rule_increment=2, 
			distance_list=[(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1)], distance_weights=[1,1,1,1,1,1,1,1], *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.comparison_number = comparison_number
		self.dead_rule_range = dead_rule_range
		self.dead_rule_increment =dead_rule_increment
		self.live_rule_range = live_rule_range
		self.live_rule_increment = live_rule_increment
		self.distance_list = distance_list
		self.distance_weights = distance_weights


	def get_default_array(self, size=(100,100)):
		array = np.random.randint(200, 255, size=size)
		return array


	def iterate(self, array):
		# print(array)
		dist = 2
		total_neighbours = sum(w * self.get_surrounding_cells(array, d) for d, w in zip(self.distance_list, self.distance_weights))

		average_neighbours = total_neighbours / sum(self.distance_weights)

		#get dead cells first and apply dead rule
		#dead cells
		dead_array = array <= self.comparison_number
		#dead cells between specified average neighbour values:
		dead_cells_between = dead_array * np.logical_and(average_neighbours>self.dead_rule_range[0], average_neighbours<self.dead_rule_range[1])
		dead_cells_outside = dead_array ^ dead_cells_between

		#do dead rule
		array[dead_cells_between] = 0
		array[dead_cells_outside] = array[dead_cells_outside] + self.dead_rule_increment


		#live cells
		live_array = ~dead_array
		#live cells between specified average neighbour values:
		live_cells_between = live_array * np.logical_and(average_neighbours>self.live_rule_range[0], average_neighbours<self.live_rule_range[1])
		live_cells_outside = live_array ^ live_cells_between

		#do live rule
		array[live_cells_outside] = 0
		array[live_cells_between] = array[live_cells_between] + self.live_rule_increment

		return array


class TuringPatterns(Rule):
	def get_default_array(self, size=(100,100)):
		array = 2*np.random.random(size) - 1
		return array

