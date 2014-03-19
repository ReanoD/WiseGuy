#!/usr/bin/python

# Simulation for Neural Network

import pygame
import pygame.draw
import random

from pygame.locals import *

# Notes:
# 	Currently there are no hazards, enemies are static, and walls and enemies are
# 	statically placed.

# TODO:
# High Priority:
# 	* [X] Replace tiles with walls (rectangles that can be anywhere and are impassable)
# 	* [X] Manually place walls and hazards
# Low Priority:
# 	* [ ] Rewrite the draw methods to use actual images (for enemies, player, hazards, and goal)

# For Matt:
# 	* [ ] Implement the notify() method of the Player class to receive commands (from sockets), commands can be "turn left", "turn right", "forward", for now
# 	* [ ] Enemies need to move (write the 'update' function on the Enemy class)
# 	* [ ] Add controls to modify the environment while the ANN is running (add/rm walls? add/rm enemies?)

# For Diego:
# 	* [ ] Add socket code to connect to the ANN

# For Thomas:
# 	* [ ] Consider using Sprite class as a base for the GameObject class
# 	* [ ] Consider alternative to add_objects() and super method draw/update
# 	* [ ] Collision detection on walls + enemies + player
# 	* [ ] Add feelers (wall/obstacle sensors) and radar (enemy sensor) to Player

# Walls and enemy locations are hardcoded here for predictability
WALLS = [
	[(50, 30), (25, 100)],
	[(120, 250), (200, 50)],
]

ENEMIES = [
	(10, 20),
	(80, 400),
]

class Color(pygame.Color):
	white = pygame.Color(255, 255, 255)
	red = pygame.color.Color(255, 0, 0)
	yellow = pygame.color.Color(255, 255, 0)
	green = pygame.color.Color(0, 255, 0)
	blue = pygame.color.Color(0, 0, 255)
	black = pygame.color.Color(0, 0, 0)

class GameObject(object):

	def __init__(self, position=(0, 0), dimension=(0, 0)):
		self._rect = pygame.Rect(position, dimension)
		self.objects = []

	def add_objects(self, objs):
		self.objects.extend(objs)

	def update(self):
		for obj in self.objects:
			obj.update()

	def draw(self, surface):
		for obj in self.objects:
			obj.draw(surface)

	def notify(self, *args, **kwargs):
		print args
		print kwargs

	@property
	def rect(self):
		return self._rect

	@rect.setter
	def rect(self, value):
		self._rect = value

class Enemy(GameObject):

	def __init__(self, game_map, position, radius=10):
		super(Enemy, self).__init__(position, (2 * radius, 2 * radius))
		self.radius = radius
		self.game_map = game_map

	def draw(self, surface):
		pygame.draw.circle(surface, Color.red, self.rect.topleft, self.radius)

	def update(self):
		self.rect.centerx += 1

class Player(GameObject):

	def __init__(self, position, radius=10):
		super(Player, self).__init__(position)
		self.radius = radius

	def draw(self, surface):
		pygame.draw.circle(surface, Color.blue, self.rect.topleft, self.radius)

	# Use this for moving the player
	def notify(self, test):
		print test


		# Create the tiles and assign random types
		for i in xrange(self.tiles_x):
			self.tiles.append([])





			if path[movement_dir] == end[movement_dir]:
				movement_dir = 1 - movement_dir

			path[movement_dir] += 1


	def create_walls(self):
		walls = []
		for pos, dim in WALLS:
			new_wall = Wall(pos, dim)
			walls.append(new_wall)

		return walls

	def create_enemies(self):
		enemies = []
		for pos in ENEMIES:
			new_enemy = Enemy(self, pos)
			enemies.append(new_enemy)

		return enemies

	def draw(self, surface):
		surface.fill(Color.white)
		super(Map, self).draw(surface)

class Simulation(object):

	def __init__(self):
		self.running = True
		# 64 * 13, 64 * 10, so the images can be powers of 2 and easy to scale
		self.resolution = (832, 640)
		self.title = 'Simulation'
		self.framerate = 60
		self.clock = pygame.time.Clock()

		self.game_map = Map(*self.resolution)

	def quit(self):
		self.running = false

	def keytoggle(self, key, state):
		if key == K_q:
			self.running = False

	def update_input(self, events):
		for event in events:
			if event.type == QUIT:
				self.running = False
			elif event.type == KEYDOWN:
				self.running = False
				# self.keytoggle(event.key, True)
			elif event.type == KEYUP:
				self.keytoggle(event.key, False)

	def update_logic(self):
		self.game_map.update()

	def update_screen(self, window):
		self.game_map.draw(window)

	def mainloop(self, window):
		while self.running:
			time = self.clock.tick(self.framerate)

			self.update_input(pygame.event.get())
			self.update_logic()
			self.update_screen(window)

			pygame.display.flip()
			pygame.event.pump()

def drawText(surface, msg, location = (0,0), size = 20, color = Color.white):
	font = pygame.font.Font(None, size)
	msgsurface = font.render(msg, False, color)
	rect = msgsurface.get_rect()
	rect.topleft = location
	surface.blit(msgsurface, rect)
	return rect

def main():
	sim = Simulation()

	pygame.init()
	pygame.display.set_mode(sim.resolution)
	pygame.display.set_caption(sim.title)

	window = pygame.display.get_surface()
	sim.mainloop(window)

main()
