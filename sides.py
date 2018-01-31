import generators
from display import *
from cube import *
import random

def get_layer_coord(direction, index):
  """Gets the 0,0 coordinate on the given layer, where layer 0 is the one furthest in the given direction."""
  return (direction.value * (SIZE - 1 - index)) if is_direction_positive(direction) else (-direction.value * index)

def corner(start_dir, end_dir, hue1, hue2):
  line_dir = get_perpendicular_direction(start_dir, end_dir)
  if abs(hue2 - hue1) > abs(hue2 + 360 - hue1):
    hue2 += 360
  h = (hue2 - hue1) / 4 # 5 animation frames, so 4 gaps
  start_i = [get_layer_coord(start_dir, i) for i in range(SIZE)]
  end_i = [get_layer_coord(end_dir, i) for i in range(SIZE)]
  while True:
    c = Cube()
    c.fill_layer(start_dir, 3, hue_to_colour(hue1))
    yield c
    c.clear()
    cs = [hue_to_colour(hue1 + h) for i in range(SIZE)]
    c.fill_line(line_dir, start_i[0] + end_i[0], cs)
    c.fill_line(line_dir, start_i[0] + end_i[1], cs)
    c.fill_line(line_dir, start_i[1] + end_i[2], cs)
    c.fill_line(line_dir, start_i[1] + end_i[3], cs)
    yield c
    c.clear()
    cs = [hue_to_colour(hue1 + 2*h) for i in range(SIZE)]
    c.fill_line(line_dir, start_i[0] + end_i[0], cs)
    c.fill_line(line_dir, start_i[1] + end_i[1], cs)
    c.fill_line(line_dir, start_i[2] + end_i[2], cs)
    c.fill_line(line_dir, start_i[3] + end_i[3], cs)
    yield c
    c.clear()
    cs = [hue_to_colour(hue1 + 3*h) for i in range(SIZE)]
    c.fill_line(line_dir, start_i[0] + end_i[0], cs)
    c.fill_line(line_dir, start_i[1] + end_i[0], cs)
    c.fill_line(line_dir, start_i[2] + end_i[1], cs)
    c.fill_line(line_dir, start_i[3] + end_i[1], cs)
    yield c
    c.clear()
    c.fill_layer(end_dir, 3, hue_to_colour(hue2))
    yield c
    yield True

def straight(end_direction, hue1, hue2):
  if abs(hue2 - hue1) > abs(hue2 + 360 - hue1):
    hue2 += 360
  h = (hue2 - hue1) / (SIZE - 1)
  while True:
    for i in range(SIZE):
      c = Cube()
      c.fill_layer(end_direction, i, hue_to_colour(hue1 + (h * i)))
      yield c
    yield True

def sides():
  hues = [Colour.RED_HUE, Colour.GREEN_HUE, Colour.BLUE_HUE]
  hue = random.choice(hues)
  direction = random.choice([d for d in Direction])
  while True:
    new_direction = random.choice([d for d in Direction if d != direction])
    new_hue = random.choice([h for h in hues if h != hue])
    if new_direction.value == -direction.value:
      gen = straight(new_direction, hue, new_hue)
    else:
      gen = corner(direction, new_direction, hue, new_hue)
    for val in gen:
      if type(val) is bool:
        break
      yield val
    direction = new_direction
    hue = new_hue
    c = Cube()
    c.fill_layer(direction, 3, hue_to_colour(hue))
    yield c
    yield c
    yield c
    yield c
    yield True


if __name__ == "__main__":
  with Display('/dev/ttyUSB0') as d:
    generators.generate(d, sides(), delay=0.05)

