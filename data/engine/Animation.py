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
  def load_animation(self, path, animation_name, frame_durations):
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
      animation_frame_id = animation_name + "_" + str(n)          #gets frame name using animation name and frame number
      img_loc = path + self.type + "/" + \
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

  #---------updates the entity animation by changing the frame----------#
  def change_frame(self, amount):
    self.animation_frame += amount
    if self.animation_frame >= len(self.animation_database[self.action]):     #checks if animaiton is complete
      self.animation_frame = 0
  
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
    return [self.img, [int(self.position.x)-scroll[],int(self.position.y)-scroll[1])] #returns data to display
