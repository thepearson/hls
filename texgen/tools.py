import Image
import StringIO
from noise import pnoise2

def get_perlin_data(size,freq=16.0,octaves=1):
  noise = [];
  for y in range(size[1]):
    line = []
    for x in range(size[0]):
      line.append(int(pnoise2(x / freq, y / freq, octaves) * 127.0 + 128.0))
    noise.append(line)
  return noise

def generate_perlin_image(file,size,freq=16.0,octaves=1,trans=None):
  data = get_perlin_data(size,freq,octaves)
  im = Image.new('RGBA', (size[0],size[1]), (0,0,0,255))
  d = im.load()
  x = y = 0
  for row in data:
    for column in row:
      if (x % size[0]) == 0:
        x = 0
      d[x,y] = (trans,trans,trans,column) if trans is not None else (column,column,column)
      x+=1
    y+=1
  im.save(file, "PNG")
  return True

def generate_grass(file,size):
  im = Image.new('RGB', size, (0,128,0))

