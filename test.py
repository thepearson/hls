SCREEN_SIZE=(1280, 768)
DATA_SIZE=32
WORLD_HEIGHT=5

OPTS_ENABLE_NORMALS=True
OPTS_ENABLE_TEXTURES=True
OPTS_ENABLE_FACES=True
OPTS_ENABLE_LIGHTING=True

VERTEX_BUFFERS=10000
NORMAL_BUFFERS=20000
TEXTURE_BUFFERS=30000

from math import radians
from texgen.tools import *

from Image import *
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy
import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *

texture = range(1)

class Image:
  sizeX = 0
  sizeY = 0
  data = None


def ImageLoad(filename, image):
  #PIL makes life easy...

  poo = open(filename)

  image.sizeX = poo.size[0]
  image.sizeY = poo.size[1]
  image.data = poo.tostring("raw", "RGBX", 0, -1)

# Load Bitmaps And Convert To Textures
def LoadGLTextures():
  global texture

  # Load Texture
  image1 = Image()
  ImageLoad("assets/grass_tex.jpg", image1)

  # Create Textures
  texture = glGenTextures(1)

  # linear filtered texture
  glBindTexture(GL_TEXTURE_2D, texture);   # 2d texture (x and y size)
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR); # scale linearly when image bigger than texture
  glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR); # scale linearly when image smalled than texture
  glTexImage2D(GL_TEXTURE_2D, 0, 4, image1.sizeX, image1.sizeY, 0, GL_RGBA, GL_UNSIGNED_BYTE, image1.data);

def resize(width, height):
  glViewport(0, 0, width, height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(60.0, float(width)/height, .1, 1000.)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()


def init():
  LoadGLTextures();                           # load the textures.
  glEnable(GL_TEXTURE_2D)
  glEnable(GL_DEPTH_TEST)
  glShadeModel(GL_FLAT)

  if not OPTS_ENABLE_FACES:
    glCullFace(GL_BACK)
    glPolygonMode(GL_BACK, GL_LINE)
    glPolygonMode(GL_FRONT, GL_LINE)

  glClearColor(0.5, 0.5, 1.0, 0.0)
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glEnable(GL_COLOR_MATERIAL)
  glEnable(GL_LIGHTING)

  glEnable(GL_LIGHT0)
  glLight(GL_LIGHT0, GL_POSITION, [20.0, 20.0, 0.0, 0.0])

  glDepthFunc(GL_LEQUAL)


def bind_data_arrays(data, size):
  world_width = 1.0
  modifier = WORLD_HEIGHT

  x_pos = 0.0
  y_pos = 0.0

  vertex_buffer = VERTEX_BUFFERS
  normal_buffer = NORMAL_BUFFERS
  texture_buffer = TEXTURE_BUFFERS

  for x in range(len(data)-1):

    row = []
    tex = []
    norms = []

    for y in range(len(data[x])-1):
      if (y % len(data)) == 0: y_pos = world_width

      z_pos = (1.0/255.)*float(data[x][y])*modifier
      z_pos_a = (1.0/255.)*float(data[x][y+1])*modifier
      z_pos_b = (1.0/255.)*float(data[x+1][y])*modifier
      z_pos_c = (1.0/255.)*float(data[x+1][y+1])*modifier

      x_world = x_pos+world_width
      y_world = y_pos+world_width

      v1 = Vector3(x_pos, y_pos, z_pos)
      v2 = Vector3(x_pos, y_world, z_pos_a)
      v3 = Vector3(x_world, y_pos, z_pos_b)
      v4 = Vector3(x_pos+world_width, y_pos+world_width, z_pos_c)

      vector = v1+v2+v3+v4
      n1, n2, n3 = vector.normalize().as_tuple()

      norms += [n1, n2, n3]
      norms += [n1, n2, n3]
      norms += [n1, n2, n3]
      norms += [n1, n2, n3]

      tex += [x_pos, y_pos,
              x_pos, y_world,
              x_world, y_pos,
              x_world, y_world]

      row += [x_pos, y_pos, z_pos,
              x_pos, y_world, z_pos_a,
              x_world, y_pos, z_pos_b,
              x_world, y_world, z_pos_c]

      y_pos += world_width
    x_pos += world_width

    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glBufferData(GL_ARRAY_BUFFER, numpy.array(row,dtype='float32'), GL_STATIC_DRAW)

    glBindBuffer(GL_ARRAY_BUFFER, normal_buffer)
    glBufferData(GL_ARRAY_BUFFER, numpy.array(norms,dtype='float32'), GL_STATIC_DRAW)

    glBindBuffer(GL_ARRAY_BUFFER, texture_buffer)
    glBufferData(GL_ARRAY_BUFFER, numpy.array(tex,dtype='float32'), GL_STATIC_DRAW)

    vertex_buffer += 1
    normal_buffer += 1
    texture_buffer += 1


def draw():
  glEnableClientState(GL_VERTEX_ARRAY)

  if OPTS_ENABLE_NORMALS: glEnableClientState(GL_NORMAL_ARRAY)
  if OPTS_ENABLE_TEXTURES: glEnableClientState(GL_TEXTURE_COORD_ARRAY)

  for i in range(DATA_SIZE):
    vertex_buffer = VERTEX_BUFFERS+i
    normal_buffer = NORMAL_BUFFERS+i
    texture_buffer = TEXTURE_BUFFERS+i

    glBindBuffer(GL_ARRAY_BUFFER, texture_buffer)
    glTexCoordPointer(2, GL_FLOAT, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
    glVertexPointer(3, GL_FLOAT, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, normal_buffer)
    glNormalPointer(GL_FLOAT, 0, None)

    glDrawArrays(GL_TRIANGLE_STRIP, 0, (DATA_SIZE*4)-1)

  if OPTS_ENABLE_NORMALS: glDisableClientState(GL_NORMAL_ARRAY);
  if OPTS_ENABLE_TEXTURES: glDisableClientState(GL_TEXTURE_COORD_ARRAY)
  glDisableClientState(GL_VERTEX_ARRAY)



'''
def draw(data):
  world_width = 1.0
  modifier = 5
  x_pos = world_width
  y_pos = world_width
  glBindTexture(GL_TEXTURE_2D, texture)     # pick the texture.

  #y = 0
  for x in range(len(data)-1):
    glBegin(GL_TRIANGLE_STRIP)
    for y in range(len(data[x])-1):
      if (y % len(data)) == 0:
        y_pos = world_width

      z_pos = (1.0/255.)*float(data[x][y])*modifier

      z_pos_a = (1.0/255.)*float(data[x][y+1])*modifier
      z_pos_b = (1.0/255.)*float(data[x+1][y])*modifier
      z_pos_c = (1.0/255.)*float(data[x+1][y+1])*modifier

      v1 = Vector3(x_pos, y_pos, z_pos)
      v2 = Vector3(x_pos, y_pos+world_width, z_pos_a)
      v3 = Vector3(x_pos+world_width, y_pos, z_pos_b)
      v4 = Vector3(x_pos+world_width, y_pos+world_width, z_pos_c)

      vector = v1+v2+v3+v4

      glNormal3dv(vector.normalize().as_tuple())

      glTexCoord2f(x_pos,y_pos)
      glVertex3f(x_pos, y_pos, z_pos);

      glTexCoord2f(x_pos,y_pos+world_width)
      glVertex3f(x_pos, y_pos+world_width, z_pos_a);

      glTexCoord2f(x_pos+world_width,y_pos)
      glVertex3f(x_pos+world_width, y_pos, z_pos_b);

      glTexCoord2f(x_pos+world_width, y_pos+world_width);
      glVertex3f(x_pos+world_width, y_pos+world_width, z_pos_c);

      y_pos += world_width
    x_pos += world_width
    glEnd()


def draw_points(data):
  world_width = 1.0
  modifier = 5
  x_pos = world_width
  y_pos = world_width
  y = 0
  for x in range(len(data)-1):
    glBegin(GL_TRIANGLE_STRIP)
    for y in range(len(data[x])-1):
      if (y % len(data)) == 0:
        y_pos = world_width

      z_pos = (1.0/255.)*float(data[x][y])*modifier

      z_pos_a = (1.0/255.)*float(data[x][y+1])*modifier
      z_pos_b = (1.0/255.)*float(data[x+1][y])*modifier
      z_pos_c = (1.0/255.)*float(data[x+1][y+1])*modifier

      v1 = Vector3(x_pos, y_pos, z_pos)
      v2 = Vector3(x_pos, y_pos+world_width, z_pos_a)
      v3 = Vector3(x_pos+world_width, y_pos, z_pos_b)
      v4 = Vector3(x_pos+world_width, y_pos+world_width, z_pos_c)

      vector = v1+v2+v3+v4

      glNormal3dv(vector.normalize().as_tuple())
      glEdgeFlag(GL_FALSE)

      vector = v1+v2+v3+v4
      glVertex3f(x_pos, y_pos, z_pos);
      glVertex3f(x_pos, y_pos+world_width, z_pos_a);
      glVertex3f(x_pos+world_width, y_pos, z_pos_b);
      glVertex3f(x_pos+world_width, y_pos+world_width, z_pos_c);

      y_pos += world_width
    x_pos += world_width
    glEnd()

'''

def run():
  pygame.init()

  screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
  resize(*SCREEN_SIZE)

  init()
  clock = pygame.time.Clock()

  # Camera transform matrix
  camera_matrix = Matrix44()
  camera_matrix.translate = (16.0, 16.0, 20.0)

  # white ambient light at half intensity (rgba)
  LightAmbient = [ 0.2, 0.5, 1.0, 0.1 ]

  # super bright, full intensity diffuse light.
  LightDiffuse = [ 0.0, 0.0, 1, 0.5 ]

  # position of light (x, y, z, (position of light))
  LightPosition = [ 32.0, 16.0, 5, 0.0 ]

  light_x = 1.0
  light_y = 1.0

  # Initialize speeds and directions
  rotation_direction = Vector3()
  rotation_speed = radians(90.0)
  movement_direction = Vector3()
  movement_speed = 10.0
  bind_data_arrays(get_perlin_data((DATA_SIZE, DATA_SIZE), 16.0, 2), DATA_SIZE)
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        return
      if event.type == KEYUP and event.key == K_ESCAPE:
        return

    # Clear the screen, and z-buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.

    pressed = pygame.key.get_pressed()

    # Reset rotation and movement directions
    rotation_direction.set(0.0, 0.0, 0.0)
    movement_direction.set(0.0, 0.0, 0.0)

    # Modify direction vectors for key presses
    if pressed[K_LEFT]:
        rotation_direction.y = +1.0
    elif pressed[K_RIGHT]:
        rotation_direction.y = -1.0

    if pressed[K_UP]:
        rotation_direction.x = -1.0
    elif pressed[K_DOWN]:
        rotation_direction.x = +1.0

    if pressed[K_z]:
        rotation_direction.z = -1.0
    elif pressed[K_x]:
        rotation_direction.z = +1.0

    if pressed[K_q]:
        movement_direction.z = -1.0
    elif pressed[K_a]:
        movement_direction.z = +1.0

    if pressed[K_i]:
      light_x = light_x+1.0
    elif pressed[K_k]:
      light_x = light_x-1.0

    if pressed[K_j]:
      light_y = light_y-1.0
    elif pressed[K_l]:
      light_y  = light_y+1.0

    # Calculate rotation matrix and multiply by camera matrix
    rotation = rotation_direction * rotation_speed * time_passed_seconds
    rotation_matrix = Matrix44.xyz_rotation(*rotation)
    camera_matrix *= rotation_matrix

    # Calcluate movment and add it to camera matrix translate
    heading = Vector3(camera_matrix.forward)
    movement = heading * movement_direction.z * movement_speed
    camera_matrix.translate += movement * time_passed_seconds

    # Upload the inverse camera matrix to OpenGL
    glLoadMatrixd(camera_matrix.get_inverse().to_opengl())

    # Light must be transformed as well
    #glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0))

    # set up light number 1.
    glShadeModel(GL_SMOOTH)
    #glLightfv(GL_LIGHT1, GL_AMBIENT, LightAmbient)  # add lighting. (ambient)

    glLight(GL_LIGHT0, GL_POSITION, [light_x, light_y, 0.0, 0.25])

    # draw textures
    # draw(data)

    # draw with arrays
    draw()

    # draw points
    #draw_points(data)

    # Show the screen
    pygame.display.flip()

if __name__ == "__main__":
  run()

