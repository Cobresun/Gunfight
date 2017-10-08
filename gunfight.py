
import os, sys
import math
from enum import Enum
import pygame

#Constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
BLOCK_SIZE = 40
BULLET_SIZE = 5
RADAR_WIDTH = 5
RADAR_LENGTH = 3 * BLOCK_SIZE

CHARACTER_SPEED = 10
BULLET_SPEED = 20

FPS = 60

#Colours
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
RED = (250, 0, 0)
GREEN = (0, 250, 0)
BLUE = (0, 0, 250)
SILVER = (192, 192, 192)

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
allCharacters = []
radars = []

#Map
game_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
	   		[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 1],
	   		[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
	   		[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1], 
	   		[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
	   		[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1], 
	   		[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
	   		[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
	   		[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	   		[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	   		[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	   		[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	   		[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	   		[1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	   		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#Enumerator for directions
class Direction(Enum):
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4

#Classes for our game objects
class Radar(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, radius, direction):
		self.x = start_x
		self.y = start_y
		self.radius = radius
		self.facing_direction = direction
		radars.append(self)

	def draw(self):
		#TODO: have radar cut off by walls
		if self.facing_direction == Direction.RIGHT:
			pygame.draw.rect(gameDisplay, RED, (self.x + self.radius, self.y, RADAR_LENGTH, RADAR_WIDTH))
		elif self.facing_direction == Direction.LEFT:
			pygame.draw.rect(gameDisplay, RED, (self.x - self.radius - RADAR_LENGTH, self.y, RADAR_LENGTH, RADAR_WIDTH))
		elif self.facing_direction == Direction.UP:
			pygame.draw.rect(gameDisplay, RED, (self.x, self.y - self.radius - RADAR_LENGTH, RADAR_WIDTH, RADAR_LENGTH))
		elif self.facing_direction == Direction.DOWN:
			pygame.draw.rect(gameDisplay, RED, (self.x, self.y + self.radius, RADAR_WIDTH, RADAR_LENGTH))


class Bullet(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, direction):
		self.x = start_x
		self.y = start_y
		self.velocity = 0
		self.facing_direction = direction
		self.size = BULLET_SIZE
		self.colour = BLUE
		self.direction = direction
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		bullets.append(self)
		allObjects.append(self)

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

	def draw(self):
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		pygame.draw.rect(gameDisplay, self.colour, [self.x, self.y, self.size, self.size])

	def is_collided_with(self, other):
		return self.rect.colliderect(other.rect)


class Character(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, facing_direction):
		self.x = start_x + BLOCK_SIZE/2
		self.y = start_y + BLOCK_SIZE/2
		self.radius = 10
		self.velocity = 0
		self.facing_direction = Direction.RIGHT
		self.moving_direction = Direction.LEFT
		self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
		self.radar = Radar(self.x, self.y, self.radius, self.facing_direction)
		allObjects.append(self)
		allCharacters.append(self)

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

	def orient(self, pos_x, pos_y):
		if self.x > pos_x:
			if self.y > pos_y:
				theta = math.degrees( math.atan( (self.y - pos_y) / (self.x - pos_x) ) )
				if theta > 45:
					self.facing_direction = Direction.UP
				else:
					self.facing_direction = Direction.LEFT

		if self.x > pos_x:
			if self.y < pos_y:
				theta = math.degrees( math.atan( (self.y - pos_y) / (self.x - pos_x) ) )
				if theta > 45:
					self.facing_direction = Direction.LEFT
				else:
					self.facing_direction = Direction.DOWN

		if self.x < pos_x:
			if self.y < pos_y:
				theta = math.degrees( math.atan( (self.y - pos_y) / (self.x - pos_x) ) )
				if theta > 45:
					self.facing_direction = Direction.DOWN
				else:
					self.facing_direction = Direction.RIGHT

		if self.x < pos_x:
			if self.y > pos_y:
				theta = math.degrees( math.atan( (self.y - pos_y) / (self.x - pos_x) ) )
				if theta > 45:
					self.facing_direction = Direction.RIGHT
				else:
					self.facing_direction = Direction.UP		

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
		if self.facing_direction == Direction.LEFT:
			bullet_params = (self.x - self.radius*2, self.y, self.facing_direction)
		elif self.facing_direction == Direction.RIGHT:
			bullet_params = (self.x + self.radius*2 , self.y, self.facing_direction)
		elif self.facing_direction == Direction.UP:
			bullet_params = (self.x , self.y - self.radius*2, self.facing_direction)
		elif self.facing_direction == Direction.DOWN:
			bullet_params = (self.x , self.y + self.radius*2, self.facing_direction)

		bullet = Bullet(bullet_params[0], bullet_params[1], bullet_params[2])
		bullet.fire()

	def draw(self):
		#If the player still has their finger on the key then the player keeps moving
		if self.velocity != 0:
			self.walk(self.moving_direction)

		radars.remove(self.radar)
		del self.radar

		self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
		self.radar = Radar(self.x, self.y, self.radius, self.facing_direction)
		self.radar.draw()
		

		pygame.draw.circle(gameDisplay, self.colour, (int(self.x), int(self.y)), self.radius)


class Player(Character):
	def __init__(self, start_x, start_y, facing_direction):
		Character.__init__(self, start_x, start_y, facing_direction)
		self.colour = GREEN

	def die(self):
		print("You died!")


class Enemy(Character):
	def __init__(self, start_x, start_y, facing_direction):
		Character.__init__(self, start_x, start_y, facing_direction)
		self.colour = SILVER
		enemies.append(self)

	def die(self):
		print("You hit!")
		radars.remove(self.radar)
		del self.radar
		enemies.remove(self)
		allObjects.remove(self)
		del self

	def listen(self, pos_x, pos_y):
		pass


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
				player = Player( j*BLOCK_SIZE, i*BLOCK_SIZE, Direction.LEFT )
			if item == 3:
				Enemy( j*BLOCK_SIZE, i*BLOCK_SIZE, Direction.LEFT )

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
				player.shoot()

		#Orient player direction
		mouse_pos = pygame.mouse.get_pos()
		player.orient( mouse_pos[0], mouse_pos[1] )

		#Clear Screen
		gameDisplay.fill(WHITE)

		#Fire bullets
		for bullet in bullets:
		 	bullet.fire()

		#Wall Collision Detection
		for wall in walls:
		 	player.is_collided_with(wall)
		 	for enemy in enemies:
		 		enemy.is_collided_with(wall)
	 		for bullet in bullets:
	 			if bullet.is_collided_with(wall):
	 				bullets.remove(bullet)
	 				allObjects.remove(bullet)
	 				del bullet

	 	#Check if any bullets hit a character
		for character in allCharacters:
			for bullet in bullets:
				if bullet.is_collided_with(character):
			 		character.die()

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
