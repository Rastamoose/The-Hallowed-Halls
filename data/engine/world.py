import data.modules.noise as noise
import pygame
from pygame.locals import *


#-------------randomly generates terrain--------------#
def generate_chunk(CHUNK_SIZE, x, y, index_1, index_2, flat = True):
  chunk_data = []
  #gets co-ordinates of each tile#
  for y_pos in range(CHUNK_SIZE):
    for x_pos in range(CHUNK_SIZE):
      target_x = x * CHUNK_SIZE + x_pos
      target_y = y * CHUNK_SIZE + y_pos     # gets tile position based off of what chunk it is - e.g chunk is (2,2)(second chunk on both x and y) so it finds co-ords
      tile_type = 0  # nothing
      if not flat:              #if terrain is not flat it uses perlin noise to create rough terrain
        height = int(noise.pnoise1(target_x * 0.1, repeat=99999999)*1.75)   # 1d noise multiplied by 0.1 to spread the bumps out # noise gives small value so *1.75 make larger to get nicer bumps
        if target_y > 9 - height:
          #if random.randint(1,10) == 1:
            #tile_type = 3       #concrete with bones
          #else:
          tile_type = index_2  
        elif target_y == 9 - height:
          tile_type = index_1                         #assigns tiles based on their positions
      elif flat:                                  #If terrain is flat it generates basic terrain with a top layer and lower areas
        if target_y > 9:                    
          tile_type = index_2
        elif target_y == 9:
          tile_type = index_1                     #assigns tiles based on their positions
          
      if tile_type != 0:
        chunk_data.append([[target_x, target_y], tile_type])          #appends tile data to each chunk if it is not an air block

  return chunk_data

#--------------loads terrain in----------------#
def infinite_terrain(display, scroll, tile_index, CHUNK_SIZE, tile_size, index_1, index_2, flat = True):
  tile_rects = []
  game_map = {}
  for y in range(6):  # 6 chunks in display (rounded up) at a time
    for x in range(10):  # 10 chunk in display (rounded up) at a time
        target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*tile_size)))
        target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*tile_size)))  # what is on the display/pixels in chunk
        target_chunk = str(target_x) + ";" + str(target_y)  # puts the chunk in form (chunk number (x));(chunk number(y))
        if target_chunk not in game_map:
          game_map[target_chunk] = generate_chunk(CHUNK_SIZE, target_x, target_y, index_1, index_2, flat) # adds a keyword "target_chunk"(chunk_x;chunk_y):[[(tile_in_chunk_x),(tile_in_chunk_y)], tile_type] with the second value being repeated for every tile in the chunk
        for tile in game_map[target_chunk]:
          display.blit(tile_index[tile[1]], (tile[0][0]*tile_size-scroll[0], tile[0][1]*tile_size-scroll[1]))  # renders the tile image with the x co-ord being the target_x and the y being the target_y 
          if tile[1] in [index_1, index_2]:
            tile_rects.append(pygame.Rect(tile[0][0]*tile_size, tile[0][1]*tile_size, tile_size, tile_size))  # adds a rect to the tile_rects list with the x being target_x * tile_size, y being target_y * tile_size
  return tile_rects

def generate_map(file, display, scroll, tile_index, CHUNK_SIZE, tile_size):
  raw_map = []
  game_map = {}
  with open(file, "r") as f:
    for line in f:
      raw_map.append(list(line))
    
  for y, row in raw_map:
    for x, tile in row:
      if tile == '1':
        pass
  
#----------calculates floor level---------#
def get_floor_level(floor_level, tile_size):
  return floor_level * tile_size                    
