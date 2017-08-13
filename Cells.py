import pygame, sys
from random import *
class Entity(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.Surface([10, 10])
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = position		
		#self.level = 1

class Nutrition(Entity):
	def __init__(self, position):
		Entity.__init__(self, position)
		#self.color = [100, 100, 255]
		self.image.fill([100, 100, 255])
		self.type = "Nutrition"

class Cell(Entity):
	def __init__(self, position):
		Entity.__init__(self, position)
		self.image.fill([0, 255, 0])
		self.speed = [5*uniform(-1,1), 5*uniform(-1,1)]
		self.health = 100
		self.type = "Cell"
	def move(self):
		self.rect = self.rect.move(self.speed)
		group.remove(self)
		item = pygame.sprite.spritecollide(self, group, False)
		if item:
			for i in range(len(item)):
				if item[i].type == "Nutrition":
					self.health += 10
					group.remove(item[i])
					group.add(self)
				else:
					if self.health<item[i].health:
						item[i].health += self.health
					elif self.health>item[i].health:
						self.health += item[i].health
						group.remove(item[i])
						group.add(self)
					else:
						self.speed[0] *= -1
						self.speed[1] *= -1
						item[i].speed[0] *= -1
						item[i].speed[1] *= -1
						group.add(self)
		else:
			group.add(self)
	
		if self.rect.left<0 or self.rect.left>width:
			self.speed[0] *= -1
		if self.rect.top<0 or self.rect.top>height:
			self.speed[1] *= -1
	def update(self):
		self.health -= 1
		if self.health<30:
			group.remove(self)
			del(self)
			return
		self.image = pygame.Surface([self.health/10, self.health/10])
		if self.health <60 :
			self.image.fill([255, 0, 0])
		elif self.health <80 :
			self.image.fill([255, 255, 0])
		else:
			self.image.fill([0, 255, 0])
		temp = self.rect.left, self.rect.top
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = temp
		

pygame.init()
SCREEN_SIZE = width, height = [640, 480]
SCREEN_COLOR = [255, 255, 250]
screen = pygame.display.set_mode(SCREEN_SIZE)

screen.fill(SCREEN_COLOR)
group = pygame.sprite.Group()
clock = pygame.time.Clock()
boss = Cell([200, 200])
boss.health = 100

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:sys.exit()
	screen.fill(SCREEN_COLOR)
	
	nutrition = Nutrition([randint(1, width), randint(1, height)])
	item = pygame.sprite.spritecollide(nutrition, group, False)
	if item:
		for i in range(len(item)):
			if item[i].type == "Nutrition":
				newCell = Cell([item[i].rect.left, item[i].rect.top])
				group.add(newCell)
				group.remove(item[i])
			else:
				item[i].health+=10
	else:
		group.add(nutrition)
	
	for item in group:
		if item.type == "Cell":
			item.update()
			item.move()
		screen.blit(item.image, item.rect)
	boss.update()
	boss.move()
	screen.blit(boss.image, boss.rect)
	pygame.display.flip()
	clock.tick(30)


