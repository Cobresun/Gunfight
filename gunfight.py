
import os, sys
from enum import Enum
import pygame

#Constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
BLOCK_SIZE = 40
CHARACTER_SPEED = 10
BULLET_SPEED = 10
FPS = 60

#Colours
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
RED = (250, 0, 0)
GREEN = (0, 250, 0)

#Initialize Everything 
pygame.init()
pygame.display.set_caption('Gunfight')
# pygame.mouse.set_visible(0)
clock = pygame.time.Clock()

#Create The Backgound
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

#Object containers
allObjects = []
walls = []
enemies = []
bullets = []

#Map
game_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
	   		[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
	   		[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	   		[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
	   		[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	   		[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
	   		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
	   		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
	   		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	   		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	   		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	   		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	   		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	   		[1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
	   		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#Enumerator for directions
class Direction(Enum):
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4

#Classes for our game objects
class Bullet(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, direction):
		self.x = start_x
		self.y = start_y
		self.velocity = 0
		self.facing_direction = direction
		bullets.append(self)

	def fire(self):
		self.velocity = BULLET_SPEED
		if self.direction == Direction.UP:
			self.y -= self.velocity
		elif self.direction == Direction.DOWN:
			self.y += self.velocity
		elif self.direction == Direction.RIGHT:
			self.x += self.velocity
		elif self.direction == Direction.LEFT:
			self.x -= self.velocity


class Character(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y):
		self.x = start_x + BLOCK_SIZE/2
		self.y = start_y + BLOCK_SIZE/2
		self.radius = 10
		self.velocity = 0
		self.facing_direction = Direction.LEFT
		self.moving_direction = Direction.LEFT
		self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
		allObjects.append(self)

	def walk(self, direction):
		self.velocity = CHARACTER_SPEED
		self.moving_direction = direction
		if direction == Direction.UP:
			self.y -= self.velocity
		elif direction == Direction.DOWN:
			self.y += self.velocity
		elif direction == Direction.RIGHT:
			self.x += self.velocity
		elif direction == Direction.LEFT:
			self.x -= self.velocity

	def orient(self, mpos_x, mpos_y):
		if self.x > mpos_x:
			self.facing_direction = Direction.LEFT
		elif self.x < mpos_x:
			self.facing_direction = Direction.RIGHT
		elif self.y > mpos_y:
			self.facing_direction = Direction.DOWN
		elif self.y < mpos_y:
			self.facing_direction = Direction.UP
		print(self.facing_direction)

	def stopWalk(self):
		self.velocity = 0

	def is_collided_with(self, other):
		if self.rect.colliderect(other.rect):
			if self.moving_direction == Direction.LEFT:
				self.stopWalk()
				self.x = other.x + other.size + self.radius*2
			if self.moving_direction == Direction.RIGHT:
				self.stopWalk()
				self.x = other.x - self.radius*2
			if self.moving_direction == Direction.UP:
				self.stopWalk()
				self.y = other.y + other.size + self.radius*2
			if self.moving_direction == Direction.DOWN:
				self.stopWalk()
				self.y = other.y - self.radius*2

	def shoot(self):
		pass

	def draw(self):
		if self.velocity != 0:
			self.walk(self.moving_direction)
		pygame.draw.circle(gameDisplay, self.colour, (int(self.x), int(self.y)), self.radius)
		self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)


class Player(Character):
	def __init__(self, start_x, start_y):
		Character.__init__(self, start_x, start_y)
		self.colour = GREEN


class Enemy(Character):
	def __init__(self, start_x, start_y):
		Character.__init__(self, start_x, start_y)
		self.colour = RED
		enemies.append(self)


class Wall(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y):
		self.x = start_x
		self.y = start_y
		self.size = BLOCK_SIZE
		self.colour = BLACK
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		allObjects.append(self)
		walls.append(self)

	def draw(self):
		pygame.draw.rect(gameDisplay, self.colour, [self.x, self.y, self.size, self.size])

#Main Game 
def main():
	#Create the Backgound
	gameDisplay.fill(WHITE)

	#Create the Map
	for i, row in enumerate(game_map):
		for j, item in enumerate(row):
			if item == 1:
				Wall( j*BLOCK_SIZE, i*BLOCK_SIZE )
			if item == 2:
				player = Player( j*BLOCK_SIZE, i*BLOCK_SIZE )
			if item == 3:
				Enemy( j*BLOCK_SIZE, i*BLOCK_SIZE )

	#Main Loop
	while True:
		clock.tick(FPS)

		#Controller
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return
				elif event.key == pygame.K_a:
					player.walk(Direction.LEFT)
				elif event.key == pygame.K_d:
					player.walk(Direction.RIGHT)
				elif event.key == pygame.K_w:
					player.walk(Direction.UP)
				elif event.key == pygame.K_s:
					player.walk(Direction.DOWN)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
					player.stopWalk()

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				player.orient( mouse_pos[0], mouse_pos[1] )
				player.shoot()

		#Orient player direction
		mouse_pos = pygame.mouse.get_pos()
		player.orient( mouse_pos[0], mouse_pos[1] )

		#Clear Screen
		gameDisplay.fill(WHITE)

		#Wall Collision Detection
		for wall in walls:
		 	player.is_collided_with(wall)
		 	for enemy in enemies:
		 		enemy.is_collided_with(wall)
		
		#Draw every object
		for item in allObjects:	
			item.draw()

		pygame.display.update()

	#End Game
	pygame.quit()


if __name__ == '__main__':
	main()

quit()

# Object oriented advice from: http://ezide.com/games/writing-games.html
# Pygame tips from https: //www.pygame.org/docs/tut/ChimpLineByLine.html
# Pygame tutorial by: https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
