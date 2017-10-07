
import os, sys
from enum import Enum
import pygame

#Constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FPS = 60

WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
RED = (250, 0, 0)

#Create The Backgound
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

#Object containers
allObjects = []
walls = []

#Enumerator for directions
class Direction(Enum):
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4

#Classes for our game objects
class Character(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y):
		self.x = start_x
		self.y = start_y
		self.radius = 10
		self.velocity = 0
		self.facing_direction = Direction.LEFT
		self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
		allObjects.append(self)

	def walk(self, direction):
		self.velocity = 10
		self.facing_direction = direction
		if direction == Direction.UP:
			self.y -= self.velocity
		elif direction == Direction.DOWN:
			self.y += self.velocity
		elif direction == Direction.RIGHT:
			self.x += self.velocity
		elif direction == Direction.LEFT:
			self.x -= self.velocity

	def stopWalk(self):
		self.velocity = 0

	def is_collided_with(self, other):
		if self.rect.colliderect(other.rect):
			if self.facing_direction == Direction.LEFT:
				self.stopWalk()
				self.x = other.x + other.size + self.radius + 1
			if self.facing_direction == Direction.RIGHT:
				self.stopWalk()
				self.x = other.x - self.radius - 1
			if self.facing_direction == Direction.UP:
				self.stopWalk()
				self.y = other.y + other.size + self.radius + 1
			if self.facing_direction == Direction.DOWN:
				self.stopWalk()
				self.y = other.y - self.radius - 1

	def draw(self):
		if self.velocity != 0:
			self.walk(self.facing_direction)
		pygame.draw.circle(gameDisplay, self.colour, (self.x, self.y), self.radius)
		self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)


class Player(Character):
	def __init__(self, start_x, start_y):
		Character.__init__(self, start_x, start_y)
		self.colour = BLACK


class Enemy(Character):
	def __init__(self, start_x, start_y):
		Character.__init__(self, start_x, start_y)
		self.colour = RED


class Wall(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y):
		self.x = start_x
		self.y = start_y
		self.size = 40
		self.colour = BLACK
		self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
		allObjects.append(self)
		walls.append(self)

	def draw(self):
		pygame.draw.rect(gameDisplay, self.colour, [self.x, self.y, self.size, self.size])

#Main Game 
def main():
	#Initialize Everything 
	pygame.init()
	pygame.display.set_caption('Gunfight')
	pygame.mouse.set_visible(0)
	clock = pygame.time.Clock()

	#Create The Backgound
	gameDisplay.fill(WHITE)

	#Prepare Game Objects
	player = Player(100, 100)
	enemy_1 = Enemy(200, 200)
	wall_1 = Wall(300, 300)

	#Main Loop
	while 1:
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


		#Update Views
		gameDisplay.fill(WHITE)

		for wall in walls:
		 	player.is_collided_with(wall)
		
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
