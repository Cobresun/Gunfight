#!usr/bin/env python
import os, sys
import math
from enum import Enum
import pygame

#Constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLOCK_SIZE = 40
CHARACTER_SIZE = BLOCK_SIZE
BULLET_SIZE = 5
RADAR_WIDTH = 5
RADAR_LENGTH = 3 * BLOCK_SIZE
HEARING_RANGE = 9 * BLOCK_SIZE

CHARACTER_SPEED = 10
BULLET_SPEED = 60

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
			[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 3, 0, 1, 1, 1], 
			[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], 
			[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
			[1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
			[1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#Enumerator for directions
class Direction(Enum):
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4


class CountDownClock():
	def __init__(self):
		self.clock_running = False
		self.start_ticks = pygame.time.get_ticks()

	def restart(self):
		self.start_ticks = pygame.time.get_ticks()
		self.clock_running = False
		pygame.mixer.music.load("reload.aiff")
		pygame.mixer.music.play()

	def act(self):
		if int((pygame.time.get_ticks() - self.start_ticks)/1000)  == 5:
			self.restart()


class Radar(pygame.sprite.Sprite):
	#TODO: Change to a cone shaped sprite
	def __init__(self, start_x, start_y, direction):
		self.x = start_x
		self.y = start_y
		self.facing_direction = direction
		self.rect = pygame.Rect(self.x, self.y, RADAR_LENGTH, RADAR_WIDTH)
		self.blocked = self.blocked_by_wall()[0]
		radars.append(self)
		allObjects.append(self)

	def destroy(self):
		try:
			radars.remove(self)
			allObjects.remove(self)
			del self
		except ValueError:
			pass

	def orient(self):
		if self.facing_direction == Direction.RIGHT:
			self.rect = pygame.Rect(self.x, self.y, RADAR_LENGTH, RADAR_WIDTH)
			if self.blocked_by_wall()[0]:
				self.blocked = True
				distance_to_wall = self.blocked_by_wall()[1].x - self.x
				self.rect = pygame.Rect(self.x, self.y, distance_to_wall, RADAR_WIDTH)

		elif self.facing_direction == Direction.LEFT:
			self.rect = pygame.Rect(self.x - RADAR_LENGTH, self.y, RADAR_LENGTH, RADAR_WIDTH)
			if self.blocked_by_wall()[0]:
				self.blocked = True
				distance_to_wall = self.x - self.blocked_by_wall()[1].x - BLOCK_SIZE
				self.rect = pygame.Rect(self.x - distance_to_wall, self.y, distance_to_wall, RADAR_WIDTH)

		elif self.facing_direction == Direction.UP:
			self.rect = pygame.Rect(self.x, self.y - RADAR_LENGTH, RADAR_WIDTH, RADAR_LENGTH)
			if self.blocked_by_wall()[0]:
				self.blocked = True
				distance_to_wall = self.y - self.blocked_by_wall()[1].y - BLOCK_SIZE
				self.rect = pygame.Rect(self.x, self.y - distance_to_wall, RADAR_WIDTH, distance_to_wall)

		elif self.facing_direction == Direction.DOWN:
			self.rect = pygame.Rect(self.x, self.y, RADAR_WIDTH, RADAR_LENGTH)
			if self.blocked_by_wall()[0]:
				self.blocked = True
				distance_to_wall = self.blocked_by_wall()[1].y - self.y
				self.rect = pygame.Rect(self.x, self.y, RADAR_WIDTH, distance_to_wall)


	def blocked_by_wall(self):
		for wall in walls:
			if self.rect.colliderect(wall):
				return (True, wall)
		self.blocked = False
		return (False, None)

	def draw(self):
		pygame.draw.rect(gameDisplay, RED, self.rect, 1)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, direction):
		self.velocity = 0
		self.facing_direction = direction
		self.size = BULLET_SIZE
		self.colour = BLUE
		self.direction = direction
		self.rect = pygame.Rect(start_x, start_y, self.size, self.size)
		bullets.append(self)
		allObjects.append(self)

	def fire(self):
		self.velocity = BULLET_SPEED
		if self.direction == Direction.UP:
			self.rect.y -= self.velocity
		elif self.direction == Direction.DOWN:
			self.rect.y += self.velocity
		elif self.direction == Direction.RIGHT:
			self.rect.x += self.velocity
		elif self.direction == Direction.LEFT:
			self.rect.x -= self.velocity

	def draw(self):
		pygame.draw.rect(gameDisplay, self.colour, self.rect)

	def destroy(self):
		bullets.remove(self)
		allObjects.remove(self)
		del self

	def is_collided_with(self, other):
		return self.rect.colliderect(other.rect)


class Character(pygame.sprite.Sprite):
	def __init__(self, start_x, start_y, facing_direction):
		self.size = CHARACTER_SIZE
		self.velocity = 0
		self.facing_direction = facing_direction
		self.rect = pygame.Rect(start_x, start_y, self.size, self.size)
		self.radar = Radar(start_x, start_y, self.facing_direction)
		allObjects.append(self)
		allCharacters.append(self)

	def walk(self, direction):
		if direction == Direction.LEFT:
			self.move_single_axis(- CHARACTER_SPEED, 0)
		if direction == Direction.RIGHT:
			self.move_single_axis(CHARACTER_SPEED, 0)
		if direction == Direction.UP:
			self.move_single_axis(0, - CHARACTER_SPEED)
		if direction == Direction.DOWN:
			self.move_single_axis(0, CHARACTER_SPEED)

	def move_single_axis(self, dx, dy):
		# Move the rect
		self.rect.x += dx
		self.rect.y += dy

		#If you collide with a wall, move out based on velocity
		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if dx > 0: # Moving right; Hit the left side of the wall
					self.rect.right = wall.rect.left
				if dx < 0: # Moving left; Hit the right side of the wall
					self.rect.left = wall.rect.right
				if dy > 0: # Moving down; Hit the top side of the wall
					self.rect.bottom = wall.rect.top
				if dy < 0: # Moving up; Hit the bottom side of the wall
					self.rect.top = wall.rect.bottom

	def orient(self, pos_x, pos_y):
		if self.rect.x + self.size/2 > pos_x:
			if self.rect.y + self.size/2 == pos_y:
				self.facing_direction = Direction.LEFT
			if self.rect.y + self.size/2 > pos_y:
				theta = math.degrees( math.atan( (self.rect.y + self.size/2 - pos_y) / (self.rect.x + self.size/2 - pos_x) ) )
				if theta > 45:
					self.facing_direction = Direction.UP
				else:
					self.facing_direction = Direction.LEFT

		if self.rect.x + self.size/2 > pos_x:
			if self.rect.y + self.size/2 == pos_y:
				self.facing_direction = Direction.LEFT
			if self.rect.y + self.size/2 < pos_y:
				theta = math.degrees( math.atan( (self.rect.y + self.size/2 - pos_y) / (self.rect.x + self.size/2 - pos_x) ) )
				if theta > -45:
					self.facing_direction = Direction.LEFT
				else:
					self.facing_direction = Direction.DOWN

		if self.rect.x + self.size/2 < pos_x:
			if self.rect.y + self.size/2 == pos_y:
				self.facing_direction == Direction.RIGHT
			if self.rect.y + self.size/2 < pos_y:
				theta = math.degrees( math.atan( (self.rect.y + self.size/2 - pos_y) / (self.rect.x + self.size/2 - pos_x) ) )
				if theta > 45:
					self.facing_direction = Direction.DOWN
				else:
					self.facing_direction = Direction.RIGHT

		if self.rect.x + self.size/2 < pos_x:
			if self.rect.y + self.size/2 == pos_y:
				self.facing_direction = Direction.RIGHT
			if self.rect.y + self.size/2 > pos_y:
				theta = math.degrees( math.atan( (self.rect.y + self.size/2 - pos_y) / (self.rect.x + self.size/2 - pos_x) ) )
				if theta > -45 :
					self.facing_direction = Direction.RIGHT
				else:
					self.facing_direction = Direction.UP		

	def shoot(self):
		pygame.mixer.music.load("gunshot.aiff")
		pygame.mixer.music.play()
		if self.facing_direction == Direction.LEFT:
			bullet_params = (self.rect.x - 5, self.rect.y + self.size/2, self.facing_direction)
		elif self.facing_direction == Direction.RIGHT:
			bullet_params = (self.rect.x + self.size + 5, self.rect.y + self.size/2, self.facing_direction)
		elif self.facing_direction == Direction.UP:
			bullet_params = (self.rect.x + self.size/2 , self.rect.y - 5, self.facing_direction)
		elif self.facing_direction == Direction.DOWN:
			bullet_params = (self.rect.x + self.size/2 , self.rect.y + self.size + 5, self.facing_direction)

		bullet = Bullet(bullet_params[0], bullet_params[1], bullet_params[2])

	def draw(self):
		#Remaking radar for new location
		self.radar.destroy()
		self.radar = Radar(self.rect.x + self.size/2, self.rect.y + self.size/2, self.facing_direction)
		self.radar.orient()

		#Draw character
		pygame.draw.rect(gameDisplay, self.colour, self.rect)


class Player(Character):
	def __init__(self, start_x, start_y, facing_direction):
		Character.__init__(self, start_x, start_y, facing_direction)
		self.colour = GREEN

	def die(self):
		try:
			self.radar.destroy()
			allObjects.remove(self)
			del self
		except ValueError:
			pass


class Enemy(Character):
	def __init__(self, start_x, start_y, facing_direction):
		Character.__init__(self, start_x, start_y, facing_direction)
		self.colour = SILVER
		self.triggered = False
		enemies.append(self)

	def die(self):
		try:
			self.radar.destroy()
			enemies.remove(self)
			allObjects.remove(self)
			del self
		except ValueError:
			pass

	def listen(self, pos_x, pos_y):
		distance_x = math.fabs(self.rect.x - pos_x)
		distance_y = math.fabs(self.rect.y - pos_y)
		displacement = math.sqrt((distance_x**2) + (distance_y**2))
		if displacement < HEARING_RANGE:
			self.triggered = True
			self.target_x = pos_x
			self.target_y = pos_y

	def follow(self):
		#TODO: Stay triggered until the enemy reaches the target location
		if (self.target_x - 5) <= self.rect.x <= (self.target_x + 5) and (self.target_y - 5) <= self.rect.y <= (self.target_y + 5):
			self.triggered = False
		else:
			self.orient(self.target_x, self.target_y)
			if not self.radar.blocked:
				self.walk(self.facing_direction)
				return
			if self.rect.x > self.target_x:
				self.facing_direction = Direction.LEFT
				if not self.radar.blocked:
					self.walk(self.facing_direction)
					return
			if self.rect.x < self.target_x:
				self.facing_direction = Direction.RIGHT
				if not self.radar.blocked:
					self.walk(self.facing_direction)
					return
			if self.rect.y < self.target_y:
				self.facing_direction = Direction.DOWN
				if not self.radar.blocked:
					self.walk(self.facing_direction)
					return
			if self.rect.y > self.target_y:
				self.facing_direction = Direction.UP
				if not self.radar.blocked:
					self.walk(self.facing_direction)
					return


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

	def destroy(self):
		walls.remove(self)
		allObjects.remove(self)
		del self


def pickFont(size):
	font = pygame.font.SysFont("comicsansms", size)
	return font


def message_to_screen(msg, colour, pos_x, pos_y, size):
	textSurf = pickFont(size).render(msg, True, colour)
	textRect = pickFont(size).render(msg, True, colour).get_rect()
	textRect.center = (pos_x), (pos_y)
	gameDisplay.blit(textSurf, textRect)


#Main Game 
def gameLoop():
	gameExit = False
	gameLost = False
	gameRestart = True
	gameRunning = False
	gameWon = False

	#TODO: Make it so that each enemy's countdown is part of their object, right now all 3 abide by same cooldown we do !!
	playerCountDown = CountDownClock()

	#Main Loop
	while not gameExit:
		clock.tick(FPS)

		while gameRestart:

			for character in allCharacters:
				character.die()
			for wall in walls:
				wall.destroy()
			for bullet in bullets:
				bullet.destroy()

			#Create the Map
			for i, row in enumerate(game_map):
				for j, item in enumerate(row):
					if item == 1:
						Wall( j*BLOCK_SIZE, i*BLOCK_SIZE )
					if item == 2:
						player = Player( j*BLOCK_SIZE, i*BLOCK_SIZE, Direction.LEFT )
					if item == 3:
						Enemy( j*BLOCK_SIZE, i*BLOCK_SIZE, Direction.LEFT )
					if item == 4:
						Enemy( j*BLOCK_SIZE, i*BLOCK_SIZE, Direction.RIGHT )
					if item == 5:
						Enemy( j*BLOCK_SIZE, i*BLOCK_SIZE, Direction.UP )
					if item == 6:
						Enemy( j*BLOCK_SIZE, i*BLOCK_SIZE, Direction.DOWN )

			gameRestart = False
			gameRunning = True


		while gameLost:
			for character in allCharacters:
				character.die()
			for wall in walls:
				wall.destroy()
			for bullet in bullets:
				bullet.destroy()

			gameDisplay.fill(WHITE)
			message_to_screen("You Died! Press 'r' to restart level.", RED, DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2, size=50)
			pygame.display.update()

			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					gameExit = True
					gameLost = False
				if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
					gameExit = True
					gameLost = False
				if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
					gameLost = False
					gameRestart = True


		while gameWon:
			#TODO: Switch to next level
			for character in allCharacters:
				character.die()
			for wall in walls:
				wall.destroy()
			for bullet in bullets:
				bullet.destroy()

			gameDisplay.fill(WHITE)
			message_to_screen("You won! Press 'r' to restart level.", RED, DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2, size=50)
			pygame.display.update()
			
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					gameExit = True
					gameWon = False
				if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
					gameExit = True
					gameWon = False
				if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
					gameRestart = True
					gameWon = False


		while gameRunning:

			#Create the Backgound
			gameDisplay.fill(WHITE)

			#Clear Screen
			gameDisplay.fill(WHITE)

			if playerCountDown.clock_running:
				playerCountDown.act()

			#Controller
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					gameExit = True
					gameRunning = False
				if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
					gameExit = True
					gameRunning = False
				if e.type == pygame.KEYDOWN and e.key == pygame.K_b:
					for enemy in enemies:
						enemy.shoot()
				if e.type == pygame.MOUSEBUTTONDOWN:
					if not playerCountDown.clock_running:
						player.shoot()
						playerCountDown.clock_running = True
						for enemy in enemies:
							enemy.listen( player.rect.x, player.rect.y )
					
			
			# Move the player if an arrow key is pressed
			key = pygame.key.get_pressed()
			if key[pygame.K_a]:
				player.walk(Direction.LEFT)
			if key[pygame.K_d]:
				player.walk(Direction.RIGHT)
			if key[pygame.K_w]:
				player.walk(Direction.UP)
			if key[pygame.K_s]:
				player.walk(Direction.DOWN)

			#Orient player direction
			mouse_pos = pygame.mouse.get_pos()
			player.orient( mouse_pos[0], mouse_pos[1] )

			#Fire bullets
			for bullet in bullets:
				bullet.fire()

			#Wall Collision Detection
			for wall in walls:
				for bullet in bullets:
					if bullet.is_collided_with(wall):
						bullet.destroy()

			for enemy in enemies:
				if enemy.radar.rect.colliderect(player.rect):
					enemy.shoot()


			#Check if any bullets hit a character
			for bullet in bullets:
				for enemy in enemies:
					if bullet.is_collided_with(enemy):
						bullet.destroy()
						enemy.die()
						break
				if bullet.is_collided_with(player):
					player.die()
					gameLost = True
					gameRunning = False

			#Enemy following
			for enemy in enemies:
				if enemy.triggered:
					enemy.follow()

			#Check if all enemies are dead
			if len(enemies) == 0:
				gameWon = True
				gameRunning = False

			#Draw every object
			for item in allObjects:	
				item.draw()

			#Draw instructions last so that it covers all other objects
			message_to_screen("Kill all the bad guys!", RED, 400, 400, 50)

			pygame.display.update()


def main():
	#Main body
	gameLoop()


if __name__ == '__main__':
	main()
	pygame.quit()
	quit()

# Object oriented advice from: http://ezide.com/games/writing-games.html
# Pygame tips from https: //www.pygame.org/docs/tut/ChimpLineByLine.html
# Pygame tutorial by: https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
# Collision tips from: http://www.pygame.org/project-Rect+Collision+Response-1061-.html
