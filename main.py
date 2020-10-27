import pkg.rules as rules
import pkg.colour_maps as cmap
import pygame as pg
import numpy as np
import noise



##==== PYGAME SETUP

pg.init()

disp_size = (1600, 900)
disp = pg.display.set_mode(disp_size)

rungame = True
clock = pg.time.Clock()

FPS = 60
updt = 0
time = 0

##==== SETUP
#default
distance_list = [(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1)]
distance_weights = [1,1,1,1,1,1,1,1]

#wave 1
distance_list = [(1,0),(0,1)]
distance_weights = [2,2]

# #squares and spirals
# distance_list = [(1,0),(0,-1),(-1,0),(0,1)]
# distance_weights = [2,2,2,2]

# # zig-zag
# distance_list = [(1,0),(0,-1),(-1,0),(0,3)]
# distance_weights = [2,2,2,2]

# #hail
# distance_list = [(-1,0),(1,0),(0,1),(0,-2),(0,3)]
# distance_weights = [1,1,3,2,1]

# # zig-zag
# distance_list = [(2,0)]
# distance_weights = [1]



rule = rules.SoftReset(distance_list=distance_list, distance_weights=distance_weights)
array = rule.get_default_array(size=(400,225))
c = cmap.Ocean(minval=0, maxval=255)

skip_n_iters = 5000





##==== MAIN LOOP

for _ in range(skip_n_iters):
	array = rule.iterate(array)

while rungame:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			  rungame = False

	dT = clock.tick_busy_loop(FPS)/1000
	time += dT
	updt += 1


	array = rule.iterate(array)



	draw_surf = pg.surface.Surface(array.shape)

	pg.surfarray.blit_array(draw_surf, c[np.clip(array, 0, 255)])

	pg.transform.scale(draw_surf, disp_size, disp)

	pg.display.update()
