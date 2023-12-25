import copy, math, functools
from enum import Enum

#
# Constants
#
TEST_AREA_MIN = 200000000000000 # 7
TEST_AREA_MAX = 400000000000000 # 27

#
# Functions
#
def is_in_test_area(xy_intersection: tuple):
    px, py, px_rem, py_rem, _ = xy_intersection
    if TEST_AREA_MIN <= px <= TEST_AREA_MAX and TEST_AREA_MIN <= py <= TEST_AREA_MAX:
        if px == TEST_AREA_MAX and px_rem > 0: return False
        elif py == TEST_AREA_MAX and py_rem >0: return False
        else: return True
    else: return False

def cross_product(A: tuple, B: tuple):
    Ax, Ay, Az = A
    Bx, By, Bz = B
    Cx = Ay * Bz - Az * By
    Cy = Az * Bx - Ax * Bz
    Cz = Ax * By - Ay * Bx
    return Cx, Cy, Cz

def simplify_vector(V: tuple):
    Vx, Vy, Vz = V
    dem = functools.reduce(math.gcd, V)
    return Vx // dem, Vy // dem, Vz // dem

def find_intersection(D1: tuple, P2: tuple, D2: tuple):
    D = cross_product(D1, D2)
    Dx = cross_product(P2, D2)
    Dy = cross_product(D1, P2)
    det_D = sum(D)
    t1 = sum(Dx) // det_D
    t2 = sum(Dy) // det_D
    intersection_point = [t1 * d for d in D1]
    # intersection_point = [p - t2 * d for p, d in zip(P2, D2)]
    return intersection_point

#
# Classes
#
class Direction(Enum):
    AHEAD = 1
    BEHIND = -1

class HailStone:
    def __init__(self, init_string: str):
        p_str, v_str = init_string.split(' @ ')
        self.px, self.py, self.pz = map(int, p_str.split(', '))
        self.vx, self.vy, self.vz = map(int, v_str.split(', '))
        if self.vy == 0 or self.vx == 0: print("Vertical or Horisontal!")

    def reframe(self, other: 'HailStone', reverse = False):
        self.px -= other.px if reverse == False else -other.px
        self.py -= other.py if reverse == False else -other.py
        self.pz -= other.pz if reverse == False else -other.pz
        self.vx -= other.vx if reverse == False else -other.vx
        self.vy -= other.vy if reverse == False else -other.vy
        self.vz -= other.vz if reverse == False else -other.vz

    def get_pos_at_t(self, time: int):
        return self.px + self.vx * time, self.py + self.vy * time, self.pz + self.vz * time

    def get_t_from_pos(self, pos: tuple):
        pos_x, pos_y, pos_z = pos
        tx = (pos_x - self.px) // self.vx
        ty = (pos_y - self.py) // self.vy
        tz = (pos_z - self.pz) // self.vz
        if tx == ty == tz: return tx
        else: return None

    def get_v(self):
        return self.vx, self.vy, self.vz

    def is_parallell_xy(self, other: 'HailStone'):
        return self.vx * other.vy == self.vy * other.vx
        
    def find_intersection_xy(self, other: 'HailStone'):
        den = self.vx * other.vy - self.vy * other.vx
        delta_px = other.px - self.px
        delta_py = self.py - other.py
        part = delta_px * other.vy + delta_py * other.vx
        num_px = self.px * den + part * self.vx
        num_py = self.py * den + part * self.vy
        return num_px // den, num_py // den, num_px % den, num_py % den, den

    def get_insersection_direction_xy(self, xy_intersection: tuple):
        px, _, px_rem, _, _ = xy_intersection
        if self.vx > 0:
            if px > self.px or (px == self.px and px_rem > 0): return Direction.AHEAD
            else: return Direction.BEHIND
        else:
            if px < self.px: return Direction.AHEAD
            else: return Direction.BEHIND

#
# Process input
#
with open('day 24/input.txt') as file:
    hailstones = list(map(lambda x: HailStone(x), file.read().splitlines()))

#
# Puzzle 1
#
result = 0
for i, a in enumerate(hailstones):
    for j, b in enumerate(hailstones[i+1:]):
        if not a.is_parallell_xy(b):
            xy_intersection = a.find_intersection_xy(b)
            if a.get_insersection_direction_xy(xy_intersection) == Direction.AHEAD and b.get_insersection_direction_xy(xy_intersection) == Direction.AHEAD:
                if is_in_test_area(xy_intersection):
                    result += 1
            
print(f'Puzzle 1 solution is: {result}')

#
# Puzzle 2
#

# Copy two hailstones (chose any two except for 0)
hs = copy.deepcopy(hailstones[1:3])
hs_N = list()
for h in hs:
    # Reframe to the reference frame of hailstone 0
    h.reframe(hailstones[0])

    # Calculate normals of plane through which the hailstones travel
    hs_N.append(cross_product(h.get_pos_at_t(0), h.get_v()))

# Calculate the line vector through which the stone travels (i.e. that all hailstones will intersect)
stone_V = simplify_vector(cross_product(hs_N[0], hs_N[1]))

# Find intersections where the hailstones meet the stone
I = list()
I_time = list()
for h in hs:
    intersection = find_intersection(stone_V, h.get_pos_at_t(0), h.get_v())
    I.append(intersection)
    I_time.append(h.get_t_from_pos(intersection))

# Calculate velocity of the stone (in the modified reference frame)
V_mod = tuple((a - b)//(I_time[1]-I_time[0]) for a, b in zip(I[1], I[0]))

# Where was the stone at t=0 (in the modified reference frame)
P_mod = tuple(i-v*I_time[0] for i, v in zip(I[0], V_mod))

# Calculate position and velocity of the hailstone in the original reference frame
V = tuple(v+v0 for v, v0 in zip(V_mod, hailstones[0].get_v()))
P = tuple(p+p0 for p, p0 in zip(P_mod, hailstones[0].get_pos_at_t(0)))

print(f'Puzzle 2 solution is: {sum(P)}')