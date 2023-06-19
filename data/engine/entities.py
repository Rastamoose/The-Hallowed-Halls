import pygame
from pygame.locals import *
import data.engine.polish as polish

#-------------class for objects that use physics------------#
class physics_obj:

  def __init__(self, rect):
    self.rect = rect                            #assigns class rect to obj rect
    self.collision_types = {"top":False,
                            "bottom":False,     #creats collision_types variable to keep track of different collisions
                            "right":False, 
                            "left":False}

  #-------------positions the object as per its collisions-------------#
  def collisions(self, movement, platforms, entity_move_x, entity_move_y, display, scroll, dt, assign_self, assign_rect):
    entity_move_x(dt)                                              #moves entity on x axis based off their physics
    assign_rect()                                                 #assigns physics rect to entity pos
    collision_list = self.collision_test(platforms)               #checks for collisions with objects (platforms)
    self.collision_types = {"top": False,
                            "bottom": False, 
                            "right": False,                      #empties collision types so that it gets a new round of collision data for each axis to maximise accuracy
                            "left": False}
    for block in collision_list:
      if movement[0] > 0:
        self.rect.right = block.left                            #iterates through blocks that entity has collided with
        self.collision_types["right"] = True                    
      elif movement[0] < 0:                                     #moves the player to a diffferent side of the block based on which way player is moving
        self.rect.left = block.right
        self.collision_types["left"] = True
      assign_self()                                              #updates player coords to rect coords after adjustment
    entity_move_y(dt)                                             #moves entity on y axis based off their physics
    assign_rect()                                                #assigns physics rect to entity pos
    collision_list = self.collision_test(platforms)              #checks for collisions with objecs
    self.collision_types = {"top": False,                       
                            "bottom": False,                    
                            "right": False,                     #empties collision types so that it gets a new round of collision data for each axis to maximise accuracy         
                            "left": False}
    for block in collision_list:
      if movement[1] > 0:
        self.rect.bottom = block.top                           #iterates through blocks that entity has collided with
        self.collision_types["bottom"] = True         
      elif movement[1] < 0:
        self.rect.top = block.bottom                          #moves the player to a diffferent side of the block based on which way player is moving
        self.collision_types["top"] = True
      assign_self()                                           #updates player coords to rect coords after adjustment
    
  #-------------checks for collisions---------------#
  def collision_test(self, obj_list):
    collision_list = []
    for obj in obj_list:
      if obj.colliderect(self.rect):              #checks for collisions with tiles
        collision_list.append(obj)
    return collision_list

#-------------class for entities------------#
class entity:

  def __init__(self, x, y, w, h, e_type, hp):
    self.position = pygame.math.Vector2(x,y)
    self.rect = pygame.Rect(self.position.x, self.position.y, w, h)
    self.type = e_type  # used for animations
    self.action = "idle"
    self.img = None
    self.isflip = False
    self.animation_frame = 0
    self.obj = physics_obj(self.rect)
    self.animation_frames = {}
    self.animation_database = {}
    self.particle_colour = None
    self.particle_timer = 0
    self.particles = []
    self.direction = "left"
    self.hp = hp
    
  #----------gathers entity animation frames and processes them----------#
  def load_animation(self, animation_name, frame_durations):
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
      animation_frame_id = animation_name + "_" + str(n)          #gets frame name using animation name and frame number
      img_loc = "data/entities/" + self.type + "/" + \
          animation_name + "/" + animation_frame_id + ".png"              #gets exact image names
      animation_image = pygame.image.load(img_loc).convert_alpha()        #loads in image
      self.animation_frames[animation_frame_id] = animation_image.copy()            #puts a copy of the image in animation frame database
      for i in range(frame):
        animation_frame_data.append(animation_frame_id)                   #appends each frame's id to a database
      n += 1
    return animation_frame_data

  #-----------assigns entity animations to a term for them in a dictionary----------#
  def animations(self, **animation):
    for animation, duration in animation.items():
      self.animation_database[animation] = self.load_animation(animation, duration)             #Loads animations into database
      
  #----------sets entity animation to what needed if entity is not already in the middle of that animation---------#
  def set_action(self, new_action):
    if self.action != new_action:
      self.action = new_action                         
      self.animation_frame = 0

  #------------update entity rects-----------#
  def update_rects(self):
    self.rect = self.obj.rect
    self.position.x, self.position.y = self.rect.x, self.rect.y 
    
  #---------updates the entity animation by changing the frame----------#
  def change_frame(self, amount):
    self.animation_frame += amount
    if self.animation_frame >= len(self.animation_database[self.action]):     #checks if animaiton is complete
      self.animation_frame = 0

  #----------updates entity dimensions as per frame---------#
  def set_dimensions(self):
    self.rect.w, self.rect.h = self.img.get_size()
  
  #--------------updates particle timer------------#
  def change_particle_timer(self): 
    if self.particle_timer > 0:
      self.particle_timer -= 1
      
  #-----------handles entity movement + particles on feet----------#
  def move(self, movement, platforms, scroll, display, entity_move_x, entity_move_y, dt, assign_self, assign_rect):
    collision_types = self.obj.collisions(movement, platforms, entity_move_x, entity_move_y, display, scroll, dt, assign_self, assign_rect)     #handles movement + collisions
    self.update_rects()           #updates rects to new positions
    self.change_particle_timer()            #updates particle timer
    polish.render_particles(display, self.particles, movement) 
    if self.obj.collision_types["bottom"]:
      if movement[0] != 0:
        if self.particle_timer == 0:
          polish.generate_particles(self.particles, 7, self.rect.x-scroll[0], self.rect.y-scroll[1]+self.rect.h, -1, -2, self.particle_colour, self.direction, self.rect.w)  #sets up movement particles based on entity movement
          self.particle_timer = 15

  #---------handles entity flipping---------#
  def set_flip(self, boolean):
    self.isflip = boolean  # used in game code to change flip status
    self.set_direction()

  def flip(self, img, boolean=True):
    return pygame.transform.flip(img, boolean, False)   # used in engine to flip entity img

  #--------handles which direction an entity is facing---------#
  def set_direction(self):
    if self.isflip:
      self.direction = "right"
    else:
      self.direction = "left"

  #----------displays entity-----------#
  def display(self, surface, scroll):
    img = self.animation_database[self.action][self.animation_frame]
    self.img = self.flip(self.animation_frames[img], self.isflip).copy()        #gets current player image
    self.set_dimensions()
    surface.blit(self.img, ((int(self.position.x)-scroll[0]), int(self.position.y)-scroll[1]))      #displays current image
    
#----------------------child class of entity 'player' for further physics-------------------------#
class player(entity):
  
  def __init__(self, x, y, w, h, e_type, hp):
    self.moving = {"right":False,
                   "left":False,}
    self.state = {"is_jumping":False,
                  "on_ground":False}
    self.gravity = .35
    self.friction = -.14            #negative to simulate opposite force on player
    self.position = pygame.math.Vector2(0,0)            #store position seperately so that calculations do not mess up in making it int every frame (blit pos requires int)
    self.velocity = pygame.math.Vector2(0,0)
    self.acceleration = pygame.math.Vector2(0, self.gravity)
    super().__init__(self.position.x, self.position.y, w, h, e_type, hp)       
      
  def horizontal_movement(self, dt):
    self.position.x = self.rect.x
        
    self.acceleration.x = 0
    if self.moving["left"]:
      self.acceleration.x -= 1
    elif self.moving["right"]:
      self.acceleration.x += 1
    self.acceleration.x += self.velocity.x * self.friction          #multiplied by friction (-number) to simulate a force on the opposite direction
    self.velocity.x += self.acceleration.x * dt           #newton's equations of motion (v = u + at)
    self.limit_velocity(4)
    self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)          #newton's equations of motion (s = ut + 1/2(at ^ 2))
    self.rect.x = int(self.position.x)

  def vertical_movement(self, dt):
    self.position.y = self.rect.y                  #assigns player location to rect (to work with physics obj/collisions)
    self.velocity.y += self.acceleration.y * dt   #newton's equations of motion (v = u + at)
    if self.velocity.y > 7:                 
      self.velocity.y = 7                         #sets a limit to player vel so it doesnt zap into the air
    self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)          #newton's equations of motion (s = ut + 1/2(at ^ 2))
    if self.obj.collision_types["bottom"]:
      self.velocity.y = 0                                      #sets velocity to 0  if player is on ground
    self.rect.y = int(self.position.y)                         #assigns phys rect to new player position

  def limit_velocity(self, max_vel):
    min(-max_vel, max(self.velocity.x, max_vel))
    if abs(self.velocity.x) < .01:
      self.velocity.x = 0

  def move_x(self, dt):
    self.horizontal_movement(dt)
        
  def move_y(self, dt):
    self.vertical_movement(dt)

  def assign_rect(self):
    self.obj.rect = self.rect
    
  def assign_self(self):
    self.rect = self.obj.rect  
    if self.obj.collision_types["bottom"]:
      self.state["on_ground"] = True          #updates player states
      self.state["is_jumping"] = False        
      self.velocity.y = 0        
    if self.obj.collision_types["right"]:
      self.moving["right"] = False
      self.velocity.x = 0
    if self.obj.collision_types["left"]:
      self.moving["left"] = False
      self.velocity.x = 0
      
  def jump(self):
    if self.state["on_ground"]:
      self.state["is_jumping"] = True
      self.velocity.y -= 8                  #updates playere states with jumping
      self.state["on_ground"] = False
      
  def assign(self):
    self.position.x = self.rect.x
    self.position.y = self.rect.y

  def update(self, dt, platforms, scroll, display):
    super().move(self.velocity, platforms, scroll, display, self.move_x, self.move_y, dt, self.assign_self, self.assign_rect)
    