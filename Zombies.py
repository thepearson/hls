SCREEN_SIZE = (1280, 756)             # windowed screen size
SCREEN_SIZE_FULL = (1280, 756)        # screen res when in full screen, not really supported
BASE_POSITION = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

WEAPON_PRIMARY = 0
WEAPON_SECONDARY = 1

TARGET_SYSTEM_DIRECT=0
TARGET_SYSTEM_REV=1
TARGET_SYSTEM=TARGET_SYSTEM_DIRECT

HEADING_N    = 3
HEADING_NE   = 4
HEADING_E    = 5
HEADING_SE   = 6
HEADING_S    = 7
HEADING_SW   = 0
HEADING_W    = 1
HEADING_NW   = 2

SPRITE_STANDING_START = 0
SPRITE_STANDING_END = 4

SPRITE_WALKING_START = 4
SPRITE_WALKING_END = 12

SAVING_GRACE_AMMO_DROP_LIKELIHOOD = 500 # if you've run out of ammo then w in SAVING_GRACE_AMMO_DROP_LIKELIHOOD
                                        # the game will randomly drop you a refill
SAVING_GRACE_AMMO_DROP_SIZE = 100       # saving grace ammo drop size
WEAPON_DEFAULT_AMMO = 250              # default ammunition
AMMO_DROP_VALUE = 12
DROP_LIKLIHOOD = 5                  # 1 in DROP_LIKLIHOOD kills will drop ammo

WEAPON_RIFLE_DEFAULT_AMMO = 24
WEAPON_RIFLE_RATE = 1
WEAPON_RIFLE_RELOAD = 1000
WEAPON_RIFLE_POWER = 50
WEAPON_RIFLE_RANGE = 600
WEAPON_RIFLE_SPEED = 600
WEAPON_RIFLE_ACCURACY = 30
WEAPON_RIFLE_KICK = 1

WEAPON_MACHINE_DEFAULT_AMMO = 100
WEAPON_MACHINE_RATE = 8
WEAPON_MACHINE_RELOAD = 0
WEAPON_MACHINE_POWER = 15
WEAPON_MACHINE_RANGE = 400
WEAPON_MACHINE_SPEED = 400
WEAPON_MACHINE_ACCURACY = 5
WEAPON_MACHINE_KICK = 20


BASE_SIZE = 20.                       # Size of the base
BASE_WALL_SIZE = 5                    # how big are the base walls
BASE_HEALTH = 2000                    # how much health do the base walls have

TURRET_HEALTH = 200                   # unused

BULLLET_RANGE = 500                   # range of bullets
BULLET_SPEED = 600                    # Speed of bullets
BULLET_FIRE_RATE_PER_SECOND = 6       # machine gun bullets fired per second
BULLET_RAND = 15                      # Machine gun kickback randmiser, makes bullet spray
BULLET_STRENGTH = 25                  # How stron bullets are

POINTS_SHOT = 25                      # how many points for shooting a zombie
POINTS_KILL = 2000                    # how many points for killing a zombie

PLAY_ZOMBIE_SPAWN_SOUND = True        # Play a sound when zombies spawn
ZOMBIE_HEALTH = 50                    # How much health zombies have
ZOMBIE_DAMAGE = 25                    # Damage zombies do to the base walls per zombie per second
ZOMBIE_HEALTH_RANDOM = 5              # Amount of randomness zombies strength has
ZOMBIE_HEALTH_DAMAGED_POSS = 10       # 1 in how many zombies are pre damaged
ZOMBIE_LIKLIHOOD = 45                 # 1 in ZOMBIE_LIKLIHOOD that a zombie will spawn every tick
ZOMBIE_SPEED_WALK = 10.               # speed zombies walk when not charging
ZOMBIE_SPEED_CHARGE = 55.            # base speed zombies move at
ZOMBIE_SPEED_RAND = 5                 # randomiser for speed
ZOMBIE_RANDOM_CHANGE_DIRECTION = 100  # likliness of a zombie to change direction when wandering around
ZOMBIE_SPAWN_REGION_OFFSCREEN = 20    # area off screen in pixels where zombies can spawn
ZOMBIE_RANGE_TO_BASE = 250            # the range in pixels when a zombie will charge at the base
ZOMBIE_LIKELIHOOD_TO_CHARGE = 100     # The liklihood that a zombie will charge when in range

SHOOTING_EVENT = 1                    # int to add to USEREVENT to assign to Shooting event
UNDER_SIEGE_EVENT = 0                 # int to define that the base is under siege

FLIP_MOUSE = 0                        # flip the mouse shooting

# images
ZOMBIE_IMAGE_FILENAME = 'assets/zombie.png'
ZOMBIE_DEAD_IMAGE_FILENAME = 'assets/zombie_dead.png'
BULLET_IMAGE_FILENAME = 'assets/bullet.png'
BACKGROUND_IMAGE_FILENAME = 'assets/grass.png'
BASE_IMAGE_FILENAME = 'assets/base.png'
TURRET_IMAGE_FILENAME = 'assets/turret.png'
AMMO_DROP_RIFLE_FILENAME = 'assets/ammo_drop_rifle.png'
AMMO_DROP_MACHINE_FILENAME = 'assets/ammo_drop_machine.png'
WEAPON_SELECT_MACHINE_FILENAME = 'assets/machine-weapon-select.png'
WEAPON_SELECT_RIFLE_FILENAME = 'assets/rifle-weapon-select.png'
ZOMBIE_IMAGE_SPRITE_FILENAME = 'assets/zombie_topdown.png'

# sounds
GAME_MUSIC='assets/music.mp3'
GUN_SOUND_FILENAME='assets/cg1.wav'
ZOMBIE_DEATH='assets/zombie_death.wav'
ZOMBIE_SHOT='assets/zombie_shot.wav'
ZOMBIE_SCREAM='assets/zscream.wav'
OUT_OF_AMMO='assets/ooa.wav'
LOADING_AMMO='assets/loading.wav'
ZOMBIE_BASE_FILE='assets/zombies/zombie-'
GUN_SOUND_RIFLE_FILENAME='assets/rifle.wav'

import pygame, math
from pygame.locals import *

from random import randint, choice
from gameobjects.vector2 import Vector2

def load_sliced_sprites(self, w, h, filename):
  '''
  Specs :
    Master can be any height.
    Sprites frames width must be the same width
    Master width must be len(frames)*frame.width
  Assuming you ressources directory is named "ressources"
  '''
  images = []
  master_image = pygame.image.load(filename).convert_alpha()

  master_width, master_height = master_image.get_size()
  for i in xrange(int(master_width/w)):
    images.append(master_image.subsurface((i*w,0,w,h)))
  return images

def render_transparent_circle(color, radius, width = 0):
  size = radius * 2
  temp_surf = pygame.Surface((size, size), SRCALPHA)
  temp_surf.fill(Color(0, 0, 0, 0))
  pygame.draw.circle(temp_surf, color, (radius, radius), radius, width)
  return temp_surf

'''
State base class
'''
class State(object):
  def __init__(self, name):
    self.name = name

  def do_actions(self):
    pass

  def check_conditions(self):
    pass

  def entry_actions(self):
    pass

  def exit_actions(self):
    pass



'''
State machine base class
'''
class StateMachine(object):
  def __init__(self):
    self.states = {}
    self.active_state = None

  def add_state(self, state):
    self.states[state.name] = state

  def think(self):
    if self.active_state is None:
      return
    self.active_state.do_actions()
    new_state_name = self.active_state.check_conditions()
    if new_state_name is not None:
      self.set_state(new_state_name)

  def get_active_state(self):
    return self.active_state_name

  def set_state(self, new_state_name):
    if self.active_state is not None:
      self.active_state.exit_actions()
    self.active_state = self.states[new_state_name]
    self.active_state_name = new_state_name
    self.active_state.entry_actions()



'''
World entity
'''
class World(object):
  def __init__(self):
    self.entities = {}
    self.assets = {}
    self.seconds = 0
    self.ammo_types = []
    self.active_weapon = WEAPON_PRIMARY
    self.active_primary = 0
    self.weapon_primary = []
    self.active_secondary = 0
    self.weapon_secondary = []
    self.music_playing = False
    self.entity_id = 0
    self.score = 0
    self.target_location = None
    self.background = pygame.image.load(BACKGROUND_IMAGE_FILENAME).convert()

  def add_ammo_type(self, name):
    self.ammo_types.append(name);

  def get_ammo_types(self):
    return self.ammo_types

  def get_ammo_drop(self):
    type = choice(self.get_ammo_types())
    if type == "rifle_ammo":
      return RifleAmmoDrop(self)
    elif type == "machine_ammo":
      return MachineAmmoDrop(self)

  def apply_ammo_drop(self, drop):
    for weapon in self.weapon_primary:
      if weapon.get_ammo_type() == drop.name:
        weapon.ammunition += drop.value
        weapon.ammo_loading_sound().play()

  def add_asset(self, name, asset):
    self.assets[name] = asset

  def get_asset(self, name):
    if self.assets.has_key(name):
      return self.assets[name]
    return None

  def switch_weapon(self, type=WEAPON_PRIMARY, index=None):
    if type == WEAPON_PRIMARY:
      if index is not None:
        self.active_primary = index
      else:
        if self.active_primary == len(self.weapon_primary)-1:
          self.active_primary = 0
        else:
          self.active_primary += 1
    elif type == WEAPON_SECONDARY:
      if index is not None:
        self.active_secondary = index
      else:
        if self.active_secondary == len(self.weapon_secondary)-1:
          self.active_secondary = 0
        else:
          self.active_secondary += 1

  def get_assets(self, starts_with=None):
    assets = []
    for name, asset in self.assets.iteritems():
      if starts_with is None:
        assets.append(asset)
      else:
        if name.startswith(starts_with):
          assets.append(asset)
    return assets

  def remove_asset(self, name):
    if self.assets.has_key(name):
      del self.assets[name]

  def set_active_weapon(self, type, weapon_name):
    if type == WEAPON_PRIMARY:
      if self.weapon_primary.has_key(weapon_name):
        self.active_primary = weapon_name
    elif type == WEAPON_SECONDARY:
      if self.weapon_secondary.has_key(weapon_name):
        self.active_primary = weapon_name

  def get_weapon(self, weapon, type=WEAPON_PRIMARY):
    if type == WEAPON_PRIMARY:
      for w in self.weapon_primary:
        if w.name == weapon:
          return w
    elif type == WEAPON_SECONDARY:
      for w in self.weapon_primary:
        if w.name == weapon:
          return w
    return None

  def add_weapon(self, weapon, type=WEAPON_PRIMARY):
    if type == WEAPON_PRIMARY:
      self.weapon_primary.append(weapon)
    elif type == WEAPON_SECONDARY:
      self.weapon_secondary.append(weapon)

  def get_active_weapon(self, type=None):
    if type is None:
      type = self.active_weapon

    if type == WEAPON_PRIMARY:
      return self.weapon_primary[self.active_primary]
    elif type == WEAPON_SECONDARY:
      return self.weapon_secondary[self.active_secondary]

  def get_weapons(self, type=WEAPON_PRIMARY):
    if type == WEAPON_PRIMARY:
      return self.weapon_primary
    elif type == WEAPON_SECONDARY:
      return self.weapon_secondary
    else:
      return self.weapon_primary + self.weapon_secondary

  def get_entity(self, entity_name):
    for entity in self.entities:
      if entity.name == entity_name:
        return entity

  def add_entity(self, entity):
    self.entities[self.entity_id] = entity
    entity.id = self.entity_id
    self.entity_id += 1

  def remove_entity(self, entity):
    del self.entities[entity.id]

  def get(self, entity_id):
    if entity_id in self.entities:
      return self.entities[entity_id]
    else:
      return None

  def process(self, time_passed):
    time_passed_seconds = time_passed / 1000.0
    if self.music_playing is False:
      self.music_playing = True
      pygame.mixer.music.play()

    for entity in self.entities.values():
      entity.process(time_passed_seconds)

  def set_target_location(self, location):
    self.target_location = location

  def draw_target_circle(self, size = 0):
    if TARGET_SYSTEM == TARGET_SYSTEM_DIRECT:
      surface = pygame.display.get_surface()
      surf = render_transparent_circle(pygame.Color(255, 0, 0, 128), size)
      surface.blit(surf, self.target_location)

  def render(self, surface):
    surface.blit(self.background, (0, 0))
    self.time = pygame.time.get_ticks()/1000.

    font=pygame.font.SysFont("arial", 16)
    surface.blit(font.render("Score: " + str(self.score), True, (255, 255, 0)), (10, 10))
    surface.blit(font.render("%.1f" % self.time, True, (255, 255, 0)), (SCREEN_SIZE[0]/2, 10))
    surface.blit(font.render("Ammo: " + str(self.get_active_weapon().ammunition), True, (255, 255, 0)), (SCREEN_SIZE[0]-100, 10))

    primary_hud = self.get_active_weapon(WEAPON_PRIMARY).get_hud_icon()
    surface.blit(primary_hud, (10, SCREEN_SIZE[1]-(primary_hud.get_size()[1]+10)))

    for entity in self.entities.itervalues():
      entity.render(surface)

  def is_hud(self, location):
    x, y = location
    primary_hud = self.get_active_weapon(WEAPON_PRIMARY).get_hud_icon()
    if x > 10 and x < 10+primary_hud.get_size()[0] and y > SCREEN_SIZE[1]-(primary_hud.get_size()[1]+10) and y < SCREEN_SIZE[1]+10:
      return True
    return False

  def get_first_entity_of_name(self, name):
    for entity in self.entities.itervalues():
      if entity.name == name:
        return entity

  def get_entities_in_state(self, name, state):
    state_entities = []
    for entity in self.entities.itervalues():
      if entity.name == name and entity.brain.get_active_state() == state:
        state_entities.append(entity)
    return state_entities

  def get_drop_entity(self, location):
    location = Vector2(*location)
    for entity in self.entities.itervalues():
      if isinstance(entity, AmmoDrop):
        distance = location.get_distance_to(entity.location)
        if distance < 20:
          return entity
    return None

  def get_close_entity(self, name, location, range=100.):
    location = Vector2(*location)
    for entity in self.entities.itervalues():
      if entity.name == name:
        distance = location.get_distance_to(entity.location)
        if distance < range:
          return entity
    return None

'''
Game entity
'''
class GameEntity(pygame.sprite.Sprite):
  def __init__(self, world, name, image):
    pygame.sprite.Sprite.__init__(self)
    self.world = world
    self.name = name
    self.image = image
    self.direction = 0
    self.location = Vector2(0, 0)
    self.destination = Vector2(0, 0)
    self.speed = 0.
    self.brain = StateMachine()
    self.id = 0

  def render(self, surface):
    x, y = self.location
    w, h = self.image.get_size()
    surface.blit(self.image, (x-w/2, y-h/2))

  def process(self, time_passed):
    self.brain.think()
    if self.speed > 0. and self.location != self.destination:
      vec_to_destination = self.destination - self.location
      distance_to_destination = vec_to_destination.get_length()
      heading = vec_to_destination.get_normalized()
      travel_distance = min(distance_to_destination, time_passed * self.speed)
      self.location += travel_distance * heading

  def get_heading_degrees(self):
    heading = Vector2.from_points(self.location, self.destination)
    if heading.x == 0.0 and heading.y == 0.0:
      return 0.0

    deg1 =  math.atan2(heading.x, heading.y)*180/math.pi
    if deg1 > 0 and deg1 < 180:
      deg1 = 180-deg1
    if deg1 < 0:
      deg = 180.0+abs(deg1)
    else:
      deg = deg1
    return deg

  def get_heading(self):
    deg = self.get_heading_degrees()
    if deg is None or deg <= 22.5 and deg > 337.5:
      return HEADING_N
    elif deg >= 22.5 and deg < 67.5:
      return HEADING_NE
    elif deg >= 67.5 and deg < 112.5:
      return HEADING_E
    elif deg >= 112.5 and deg < 157.5:
      return HEADING_SE
    elif deg >= 157.5 and deg < 202.5:
      return HEADING_S
    elif deg >= 202.5 and deg < 247.5:
      return HEADING_SW
    elif deg >= 247.5 and deg < 292.5:
      return HEADING_W
    elif deg >= 292.5 and deg < 360.0:
      return HEADING_NW
    else:
      return randint(0, 7)

'''
Base
'''
class Base(GameEntity):

  def __init__(self, world):
    GameEntity.__init__(self, world, "base", world.get_asset('image_base_image'))
    self.size = self.image.get_size()
    self.under_siege = False
    self.health = BASE_HEALTH

  def render(self, surface):
    if self.health > 0:
      x, y = self.location
      w, h = self.image.get_size()
      surface.blit(self.image, (x-w/2, y-h/2))
      bar_x = x - w/2
      bar_y = y + h/2
      green = (float(w)/BASE_HEALTH)*self.health
      surface.fill((255, 0, 0), (bar_x, bar_y, w, 6))
      surface.fill((0, 255, 0), (bar_x, bar_y, green, 6))


'''
Turret image
'''
class Turret(GameEntity):
  def __init__(self, world):
    GameEntity.__init__(self, world, "turret", world.get_asset('image_turret'))
    self.world = world
    self.health = TURRET_HEALTH


'''
Turret image
'''
class AmmoDrop(GameEntity):
  def __init__(self, world, name, image):
    GameEntity.__init__(self, world, name, image)
    self.world = world
    self.value = 0

  def get_weapon_name(self):
    return self.weapon_name

class RifleAmmoDrop(AmmoDrop):
  def __init__(self, world):
    AmmoDrop.__init__(self, world, "rifle_ammo", world.get_asset('image_ammo_drop_rifle'))
    self.value = 12
    self.weapon_name = "rifle"

class MachineAmmoDrop(AmmoDrop):
  def __init__(self, world):
    AmmoDrop.__init__(self, world, "machine_ammo", world.get_asset('image_ammo_drop_machine'))
    self.value = 24
    self.weapon_name = "machine"

'''
Zombie entity
'''
class Zombie(GameEntity):
  def __init__(self, world):
    GameEntity.__init__(self, world, "zombie", world.get_asset('image_zombie'))

    walking_state = ZombieStateWalking(self)
    chaging_state = ZombieStateCharging(self)
    sieging_state = ZombieStateSieging(self)
    dead_state = ZombieStateDead(self)

    self.brain.add_state(walking_state)
    self.brain.add_state(chaging_state)
    self.brain.add_state(sieging_state)
    self.brain.add_state(dead_state)
    # set states
    self.sprite_last_render = 0
    self.sprite_current_frame = 0
    self.sprite_anim_speed = 500

    self.sprite = world.get_asset('image_zombie_sprite')
    self.dead_image = world.get_asset('image_zombie_dead')
    self.sounds = world.get_assets('sfx_zombie_spawn_')
    self.scream = world.get_asset('sfx_zombie_scream')
    self.shot = world.get_asset('sfx_zombie_shot')
    self.death = world.get_asset('sfx_zombie_death')

    self.health = ZOMBIE_HEALTH
    if randint(1, ZOMBIE_HEALTH_DAMAGED_POSS) == 1:
      self.health -= randint(1, ZOMBIE_HEALTH/2)
    self.speed = ZOMBIE_SPEED_CHARGE + randint(0, ZOMBIE_SPEED_RAND)

  def choose_spawn(self):
    w, h = SCREEN_SIZE
    # Randomly place zombie somewhere on screen, north, south east or west
    spawn_direction = randint(0, 3)
    if spawn_direction == 0: # north
      self.location = Vector2(randint(-ZOMBIE_SPAWN_REGION_OFFSCREEN, w+ZOMBIE_SPAWN_REGION_OFFSCREEN), randint(-ZOMBIE_SPAWN_REGION_OFFSCREEN, 0))
    elif spawn_direction == 1: # east
      self.location = Vector2(randint(w, w+ZOMBIE_SPAWN_REGION_OFFSCREEN), randint(-ZOMBIE_SPAWN_REGION_OFFSCREEN, h+ZOMBIE_SPAWN_REGION_OFFSCREEN))
    elif spawn_direction == 2: # south
      self.location = Vector2(randint(-ZOMBIE_SPAWN_REGION_OFFSCREEN, w+ZOMBIE_SPAWN_REGION_OFFSCREEN), randint(h, h+ZOMBIE_SPAWN_REGION_OFFSCREEN))
    else: # west
      self.location = Vector2(randint(-ZOMBIE_SPAWN_REGION_OFFSCREEN, 0), randint(-ZOMBIE_SPAWN_REGION_OFFSCREEN, h+ZOMBIE_SPAWN_REGION_OFFSCREEN))

  def render(self, surface):
    #GameEntity.render(self, surface)
    if self.health > 0:
      sprite_size = 32
      x, y = self.location
      w, h = (sprite_size, sprite_size) #self.image.get_size()

      now = pygame.time.get_ticks()

      # increment the frame
      if (now - self.sprite_last_render) >= self.sprite_anim_speed:
        self.sprite_current_frame += 1
        self.sprite_last_render = now

        # reset the sprite if reached the end
        if self.sprite_current_frame >= (SPRITE_WALKING_END - SPRITE_WALKING_START):
          self.sprite_current_frame = 0

      direction = self.direction
      sprite_loc = ((SPRITE_WALKING_START*sprite_size)+(self.sprite_current_frame*sprite_size), direction*sprite_size, sprite_size, sprite_size)
      self.image = self.sprite.subsurface(sprite_loc)

      surface.blit(self.image, (x-w/2, y-h/2))

      bar_size = 32
      bar_width = 4
      bar_x = x - bar_size/2
      bar_y = y - h/2 - bar_width
      green = (float(bar_size)/ZOMBIE_HEALTH)*self.health
      surface.fill((255, 0, 0), (bar_x, bar_y, bar_size, bar_width))
      surface.fill((0, 255, 0), (bar_x, bar_y, green, bar_width))

  def play_sound(self, type = "first_shot"):
    if type == "first_shot":
      choice(self.sounds).play()
      self.scream.play()
      self.shot.play()
    elif type == "shot":
      self.shot.play()
    elif type == "dead":
      self.death.play()



class Weapon(object):
  def __init__(self, world, name):
    self.world = world
    self.world.add_ammo_type(self.get_ammo_type())
    self.ammunition = 0
    self.name = name
    self.rate = 1
    self.accuracy = 100
    self.power = 1
    self.range = 100
    self.ordnance = "bullet"

  def ammo_loading_sound(self):
    return self.world.get_asset('sfx_loading_ammo')

  def get_ammo_type(self):
    return self.ammo_type

  def get_ordnance(self):
    if self.ordnance == "bullet":
      return Bullet(self.world, self)

  #def show_target_area(self):
  #  pygame.draw.circle(self.world, (255, 0,  0, 0.5), (self.location[0], self.location[1]), self.kick)

  #def flip_xy(self, x, y):

  def get_hud_icon(self):
    return self.hud_icon

  def begin_fire(self):
    pygame.time.set_timer(USEREVENT+SHOOTING_EVENT, int(1000/self.rate));

  def fire(self):
    pass

  def end_fire(self):
    pygame.time.set_timer(USEREVENT+SHOOTING_EVENT, 0);

'''
Rifle weapon
'''
class Rifle(Weapon):

  def __init__(self, world):
    self.ammo_type = "rifle_ammo"
    Weapon.__init__(self, world, "rifle")
    self.ordnance = "bullet"
    self.ammunition = WEAPON_RIFLE_DEFAULT_AMMO
    self.sound = self.world.get_asset('sfx_rifle_fire')
    self.rate = WEAPON_RIFLE_RATE
    self.reload = WEAPON_RIFLE_RELOAD
    self.power = WEAPON_RIFLE_POWER
    self.kick = WEAPON_RIFLE_KICK
    self.range = WEAPON_RIFLE_RANGE
    self.accuracy = WEAPON_RIFLE_ACCURACY
    self.speed = WEAPON_RIFLE_SPEED
    self.hud_icon = world.get_asset('image_hud_rifle')
    self.fire_time = 0.

  def fire(self):
    now = pygame.time.get_ticks()
    diff = now - self.fire_time
    if diff >= self.reload:
      Weapon.fire(self)
      # get mouse co'ords
      if self.ammunition > 0:
        self.sound.play()
        mouse = Vector2(*pygame.mouse.get_pos())
        base = Vector2(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

        if TARGET_SYSTEM == TARGET_SYSTEM_REV:
          bullet = (-1*((mouse-base)*1.5)) + base
        else:
          bullet = mouse

        x = bullet.x
        y = bullet.y

        x = x + randint(0, self.kick) if randint(0, 1) == 1 else x - randint(0, self.kick)
        y = y + randint(0, self.kick) if randint(0, 1) == 1 else y - randint(0, self.kick)



        ord = self.get_ordnance()
        ord.location = base
        ord.destination = Vector2(x, y)
        self.ammunition -= 1
        self.world.add_entity(ord)
        self.fire_time = now
      else:
        self.world.get_asset('sfx_out_of_ammo').play()


class Machine(Weapon):

  def __init__(self, world):
    self.ammo_type = "machine_ammo"
    Weapon.__init__(self, world, "machine")
    self.ordnance = "bullet"
    self.ammunition = WEAPON_MACHINE_DEFAULT_AMMO
    self.sound = self.world.get_asset('sfx_machinegun_fire')
    self.rate = WEAPON_MACHINE_RATE
    self.reload = WEAPON_MACHINE_RELOAD
    self.power = WEAPON_MACHINE_POWER
    self.kick = WEAPON_MACHINE_KICK
    self.range = WEAPON_MACHINE_RANGE
    self.accuracy = WEAPON_MACHINE_ACCURACY
    self.speed = WEAPON_MACHINE_SPEED
    self.hud_icon = world.get_asset('image_hud_machine')
    self.fire_time = 0.

  def fire(self):
    now = pygame.time.get_ticks()
    diff = now - self.fire_time
    if diff >= self.reload:
      Weapon.fire(self)
      # get mouse co'ords
      if self.ammunition > 0:
        mouse = Vector2(*pygame.mouse.get_pos())
        base = Vector2(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)


        if TARGET_SYSTEM == TARGET_SYSTEM_REV:
          bullet = (-1*((mouse-base)*1.5)) + base
        else:
          bullet = mouse

        x = bullet.x
        y = bullet.y

        x = x + randint(0, self.kick) if randint(0, 1) == 1 else x - randint(0, self.kick)
        y = y + randint(0, self.kick) if randint(0, 1) == 1 else y - randint(0, self.kick)

        ord = self.get_ordnance()
        ord.location = Vector2(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
        ord.destination = Vector2(x, y)
        self.ammunition -= 1
        self.world.add_entity(ord)
        self.fire_time = now
        self.sound.play()
      else:
        self.world.get_asset('sfx_out_of_ammo').play()

'''
Ordnance
'''
class Ordnance(GameEntity):
  def __init__(self, world, type, weapon, image):
    GameEntity.__init__(self, world, "bullet", world.get_asset('image_bullet'))
    self.weapon = weapon


'''
Bullet object
'''
class Bullet(Ordnance):
  def __init__(self, world, weapon):
    Ordnance.__init__(self, world, "bullet", weapon, world.get_asset('image_bullet'))
    shooting_state = BulletStateShooting(self)
    self.world = world
    self.brain.add_state(shooting_state)
    self.brain.set_state("shooting")
    self.speed = BULLET_SPEED


'''
Bullet shooting state
'''
class BulletStateShooting(State):
  def __init__(self, bullet):
    State.__init__(self, "shooting")
    self.bullet = bullet

  def do_actions(self):
    x, y = self.bullet.location
    if x < 0 or x > SCREEN_SIZE[0]:
      if y < 0 or y > SCREEN_SIZE[1]:
        # remove bullets that are off the screen
        self.bullet.world.remove_entity(self.bullet)

    # if bullet reaches destination, remove it
    if self.bullet.location.get_distance_to(self.bullet.destination) < 15.:
      self.bullet.world.remove_entity(self.bullet)

    zombie = self.bullet.world.get_close_entity("zombie", self.bullet.location, 15)
    if zombie is not None and zombie.brain.get_active_state() != "dead":
      if self.bullet.location.get_distance_to(zombie.location) < 10.:
        zombie.health -= self.bullet.weapon.power
        self.bullet.world.score += POINTS_SHOT
        if zombie.brain.get_active_state() == "walking":
          zombie.brain.set_state("charging")
        else:
          zombie.play_sound("shot")

        if zombie.health <= 0:
          self.bullet.world.score += POINTS_KILL
          zombie.brain.set_state("dead")
        else:
          self.bullet.location = self.bullet.destination


'''
Zombie hunting state
'''
class ZombieStateCharging(State):
  def __init__(self, zombie):
    State.__init__(self, "charging")
    self.zombie = zombie

  def check_conditions(self):
    x, y = self.zombie.location
    base = self.zombie.world.get_first_entity_of_name("base")
    blx, bly = base.location
    bw, bh = base.size

    if base.health > 0:
      if x > (blx-(bw/2)-BASE_WALL_SIZE) and x < (blx+(bw/2)+BASE_WALL_SIZE):
        if y > (bly-(bh/2)-BASE_WALL_SIZE) and y < (bly+(bh/2)+BASE_WALL_SIZE):
          self.zombie.destination = self.zombie.location
          return "sieging"

  def entry_actions(self):
    self.zombie.play_sound()
    self.zombie.sprite_anim_speed = 100
    self.zombie.destination = BASE_POSITION
    self.zombie.speed = ZOMBIE_SPEED_CHARGE


'''
Zombie hunting state
'''
class ZombieStateDead(State):
  def __init__(self, zombie):
    State.__init__(self, "dead")
    self.zombie = zombie

  def check_conditions(self):
    current_time = pygame.time.get_ticks()
    if (current_time-self.dead_time) >= 5000:
      if randint(1, DROP_LIKLIHOOD) == 1:
        drop = self.zombie.world.get_ammo_drop()
        drop.location = self.zombie.location
        self.zombie.world.add_entity(drop)

      self.zombie.world.remove_entity(self.zombie)

  def entry_actions(self):
    self.dead_time = pygame.time.get_ticks()
    self.zombie.play_sound("dead")
    self.zombie.destination = self.zombie.location
    self.zombie.image = self.zombie.dead_image


'''
Random walking about state
'''
class ZombieStateWalking(State):

  def __init__(self, zombie):
    State.__init__(self, "walking")
    self.zombie = zombie
    self.last_dir_change = 0

  def random_destination(self):
    w, h = SCREEN_SIZE
    self.zombie.destination = Vector2(randint(0, w), randint(0, h))

  def do_actions(self):
    if randint(1, ZOMBIE_RANDOM_CHANGE_DIRECTION) == 1:
      time = pygame.time.get_ticks()
      if time-self.last_dir_change > 5000:
        self.last_dir_change = time
        self.random_destination()
        self.zombie.direction = self.zombie.get_heading()

  def check_conditions(self):
    base = self.zombie.world.get_first_entity_of_name("base")
    if base is not None:
      if self.zombie.location.get_distance_to(base.location) < ZOMBIE_RANGE_TO_BASE:
        if randint(1, ZOMBIE_LIKELIHOOD_TO_CHARGE) == 1:
          return "charging"

    return None

  def entry_actions(self):
    self.zombie.speed = ZOMBIE_SPEED_WALK
    self.random_destination()
    self.zombie.direction = self.zombie.get_heading()


'''
Zombie sieging state
'''
class ZombieStateSieging(State):

  def __init__(self, zombie):
    State.__init__(self, "sieging")
    self.zombie = zombie

  def entry_actions(self):
    pass

  def do_actions(self):
    pass


'''
Run
'''
def run():
  Fullscreen = False

  pygame.mixer.pre_init(44100, -16, 2, 1024*4)
  pygame.init()
  screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
  world = World()

  clock = pygame.time.Clock()

  world.add_asset('image_turret', pygame.image.load(TURRET_IMAGE_FILENAME).convert_alpha())
  world.add_asset('image_ammo_drop_rifle', pygame.image.load(AMMO_DROP_RIFLE_FILENAME).convert_alpha())
  world.add_asset('image_ammo_drop_machine', pygame.image.load(AMMO_DROP_MACHINE_FILENAME).convert_alpha())
  world.add_asset('image_base_image', pygame.image.load(BASE_IMAGE_FILENAME).convert_alpha())

  world.add_asset('image_zombie_sprite', pygame.image.load(ZOMBIE_IMAGE_SPRITE_FILENAME).convert_alpha())
  world.add_asset('image_zombie', pygame.image.load(ZOMBIE_IMAGE_FILENAME).convert_alpha())

  world.add_asset('image_bullet', pygame.image.load(BULLET_IMAGE_FILENAME).convert_alpha())
  world.add_asset('image_zombie_dead', pygame.image.load(ZOMBIE_DEAD_IMAGE_FILENAME).convert_alpha())


  world.add_asset('sfx_rifle_fire', pygame.mixer.Sound(GUN_SOUND_RIFLE_FILENAME))
  world.add_asset('sfx_machinegun_fire', pygame.mixer.Sound(GUN_SOUND_FILENAME))
  gun_sound = pygame.mixer.Sound(GUN_SOUND_FILENAME)

  world.add_asset('sfx_out_of_ammo', pygame.mixer.Sound(OUT_OF_AMMO))
  world.add_asset('sfx_loading_ammo', pygame.mixer.Sound(LOADING_AMMO))
  world.add_asset('image_hud_rifle', pygame.image.load(WEAPON_SELECT_RIFLE_FILENAME).convert_alpha())
  world.add_asset('image_hud_machine', pygame.image.load(WEAPON_SELECT_MACHINE_FILENAME).convert_alpha())

  # add zombie spawn sounds
  for i in range(1, 10):
    world.add_asset('sfx_zombie_spawn_' + str(i), pygame.mixer.Sound(ZOMBIE_BASE_FILE + str(i) + '.wav'))

  world.add_asset('sfx_zombie_scream', pygame.mixer.Sound(ZOMBIE_SCREAM))
  world.add_asset('sfx_zombie_shot', pygame.mixer.Sound(ZOMBIE_SHOT))
  world.add_asset('sfx_zombie_death', pygame.mixer.Sound(ZOMBIE_DEATH))

  # add the music
  world.add_asset('music_inspire', pygame.mixer.music.load(GAME_MUSIC))

  # add weapons
  rifle = Rifle(world)
  world.add_weapon(rifle)

  machine = Machine(world)
  world.add_weapon(machine)

  # add the base
  turret = Turret(world)
  turret.location = ((SCREEN_SIZE[0]/2), (SCREEN_SIZE[1]/2))
  world.add_entity(turret)

  # add the base
  base = Base(world)
  base.location = turret.location
  world.add_entity(base)

  '''
  zombie = Zombie(world)
  zombie.choose_spawn()
  zombie.brain.set_state("walking")
  world.add_entity(zombie)
  '''

  '''
  def shoot(sound, out_of_ammo):
    # get mouse co'ords
    if world.ammo > 0:
      x, y = pygame.mouse.get_pos()
      bullet = Bullet(world, bullet_image, sound)
      bullet.location = Vector2(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

      if FLIP_MOUSE == 1:
        if x > SCREEN_SIZE[0]/2: # mouse is to the right of base
          op_x = (SCREEN_SIZE[0]/2)-(x-(SCREEN_SIZE[0]/2))
        elif x < SCREEN_SIZE[0]/2: # mouse is to the left of the base
          op_x = (SCREEN_SIZE[0]/2)+((SCREEN_SIZE[0]/2)-x)
        else:
          op_x = x

        if y > SCREEN_SIZE[1]/2: # mouse is below the base
          op_y = (SCREEN_SIZE[1]/2)-(y-(SCREEN_SIZE[1]/2))
        elif y < SCREEN_SIZE[1]/2: # mouse is above the base
          op_y = (SCREEN_SIZE[1]/2)+((SCREEN_SIZE[1]/2)-y)
        else:
          op_y = y
        op_x = randint(op_x-BULLET_RAND, op_x+BULLET_RAND)
        op_y = randint(op_y-BULLET_RAND, op_y+BULLET_RAND)
      else:
        op_x = x
        op_y = y

      bullet.destination = Vector2(op_x, op_y)
      world.ammo -= 1
      world.add_entity(bullet)
    else:
      out_of_ammo.play()
  '''

  while True:
    time_passed = clock.tick(30)

    for event in pygame.event.get():

      # Check key presses
      if event.type == KEYDOWN:

        # f = fullscreen toggle
        if event.key == K_f:
          Fullscreen=not Fullscreen
          if Fullscreen:
            screen=pygame.display.set_mode(SCREEN_SIZE_FULL, FULLSCREEN, 32)
          else:
            screen=pygame.display.set_mode(SCREEN_SIZE, 0, 32)

        # escape will close
        if event.key == K_ESCAPE:
          return

      # Quit event
      if event.type == QUIT:
        return

      # if base is under siege take some health off
      # TOOD: convert to state machine SiegeState for Base
      if event.type == USEREVENT+UNDER_SIEGE_EVENT:
        sieging_zombies = world.get_entities_in_state("zombie", "sieging")
        base.health -= ZOMBIE_DAMAGE*len(sieging_zombies)

        # base has been destroyed
        if base.health <= 0:
          for zombie in sieging_zombies:
            zombie.brain.set_state("charging")

      # turn on the shooting event
      if event.type == MOUSEBUTTONDOWN:

        if pygame.mouse.get_pressed()[0] == True:
          if world.is_hud(pygame.mouse.get_pos()):
            world.switch_weapon()
          else:
            # hud (10, SCREEN_SIZE[1]-(primary_hud.get_size()[1]+10))
            ammo = world.get_drop_entity(pygame.mouse.get_pos())
            if ammo:
              world.apply_ammo_drop(ammo)
              world.remove_entity(ammo)
            else:
              weapon = world.get_active_weapon()
              weapon.begin_fire()
              weapon.fire()

      if event.type == MOUSEMOTION and pygame.mouse.get_pressed()[0] == True:
        pygame.draw.circle(screen, (255, 0,  0), pygame.mouse.get_pos(), 30)

      # remove the shooting event
      if event.type == MOUSEBUTTONUP and pygame.mouse.get_pressed()[0] == False:
        #pygame.time.set_timer(USEREVENT+SHOOTING_EVENT, 0);
        weapon = world.get_active_weapon()
        weapon.end_fire()

      # check if shooting and do so
      if event.type == USEREVENT+SHOOTING_EVENT:
        weapon = world.get_active_weapon()
        weapon.fire()


    # base can only be under siege if it exists
    if base.health > 0:

      # see how many zombies are sieging the base
      if len(world.get_entities_in_state("zombie", "sieging")) > 0:

        # if the base isn't already under siege, (we dont want to restart the event)
        if base.under_siege is not True:
          base.under_siege = True
          pygame.time.set_timer(USEREVENT+UNDER_SIEGE_EVENT, 2000);
      else:
        # only set the base out of siege if it is currently under sieve
        if base.under_siege:
          base.under_siege = False
          pygame.time.set_timer(USEREVENT+UNDER_SIEGE_EVENT, 0);

    # if you dont have any ammo then randomly drop some
    '''
    if world.ammo == 0 and randint(1, SAVING_GRACE_AMMO_DROP_LIKELIHOOD) == 1:
      drop = AmmoDrop(world)
      drop.location = (randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1]))
      drop.value = SAVING_GRACE_AMMO_DROP_SIZE
      world.add_entity(drop)
      '''

    # Generate zombies
    if randint(1, ZOMBIE_LIKLIHOOD) == 1:
      if PLAY_ZOMBIE_SPAWN_SOUND:
        choice(world.get_assets('sfx_zombie_spawn_')).play()

      zombie = Zombie(world)
      zombie.choose_spawn()
      zombie.brain.set_state("walking")
      world.add_entity(zombie)

    # Process the world
    world.process(time_passed)
    world.render(screen)
    pygame.display.update()

if __name__ == "__main__":
  run()

