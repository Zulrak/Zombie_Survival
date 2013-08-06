# Source File Name: Zombie_Survival_Version_02
# Author's Name: Jordan Cooper
# Last Modified By: Jordan Cooper
# Date Last Modified: Saturday, July 27, 2013
""" 
  Program Description:  Zombie Survival is about Doug the zombie. Doug, the lovable zombie is back from his
                        adventures in Brain Buster, and hes ready to share the brains! In this game Doug must
                        collect as many brains as he can to feed his hungry zombie friends. 
                        
        Version: 0.2   - Created Sprite Villager
                            - the enemy sprite
                            - collision detection between villager and doug the avatar
                            - sound plays when collision
                        - Created Sprite SpitAcid
                            - shoots from doug's mouth
                            - collides with villager = dead villager
                        - created Intro screen
                            - not complete
                        - created end game screen
                            
"""
import random
import pygame
import math

pygame.init()

screen = pygame.display.set_mode((640, 480))

#Create the Avatar Named Doug the Zombie
class DougTheZombie(pygame.sprite.Sprite):
    def __init__(self,spitAcid):
        pygame.sprite.Sprite.__init__(self)
        
        self.spitAcid = spitAcid
        self.image = pygame.image.load("DougTheZombie.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()

#Incorporate Sound to the game
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.biteSound = pygame.mixer.Sound("bite.wav")
            self.painSound = pygame.mixer.Sound("pain.wav")
#            self.backgroundSound = pygame.mixer.Sound("background.wav")
#            self.backgroundSound.play(-1)      
    
    def checkAcid(self):
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_SPACE]:
            self.spitAcid.x = self.rect.centerx
            self.spitAcid.y = self.rect.centery

#Update the Doug Avatar       
    def update(self):
        ''' Get Mouse position, set the y position and a fixed position to the sprite'''
        mousex , mousey = pygame.mouse.get_pos()
        self.rect.center = (mousex,360)
        
        ''' If the Avatar is moving off the screen, set the avatar to the top of the screen.'''
        if mousex < (40): 
            self.rect.center = (40,360)
        if mousex > (600): 
            self.rect.center = (600,360)
        
        self.checkAcid()
        
class SpitAcid(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        self.image = pygame.image.load("SpitAcid.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.dx = 10
        self.dy = 0
        self.speed = 10
        self.reset()
        
    def update(self):
        self.calcPos()
        self.checkBounds()
        self.rect.center = (self.x, self.y)
    
    def calcVector(self):
        radians = self.dir * math.pi / 180
        
        self.dx = self.speed * math.cos(radians)
        
    def calcPos(self):
        self.x += self.dx
    
    def checkBounds(self):
        screen = self.screen
        if self.x > screen.get_width():
            self.reset()
        if self.x < 0:
            self.reset()
        if self.y > screen.get_height():
            self.reset()
        if self.y < 0:
            self.reset()
    
    def reset(self):
        """ move off stage and stop"""
        self.x = -100
        self.y = -100

            
#Create the Objective sprit, the Brain           
class Brain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("brain.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 5

#Move the brain left 5px Until the brain leaves the player's feild of view
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
#Reset the brain to a randomized position BEHIND the player's feild of view           
    def reset(self):
        self.rect.left = 0
        self.rect.centerx = random.randrange(700, 1000)
        self.rect.centery = random.randrange(250, 360)
        
#Create the  enemy, the angry villager                
class Villager(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("villager.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 7

#Move the angry villager 7px to the left, to appear as if charging at the zombie    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
  
#Reset the villager's position to a randomized location off of the player's feild of view            
    def reset(self):
        self.rect.left = 0
        self.rect.centerx = random.randrange(700, 1000)
        self.rect.centery = 360

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ground.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dx = 5
        self.reset()
#Move the Background Image at a rate of 5px, Reset the image once almost 3/4 of the image has been displayed

#This will make the image seem as if it is never ending       
    def update(self):
        self.rect.left -= self.dx
        if self.rect.left <= -1900:
            self.reset() 

#Reset the Background Image to the left side of the page  
    def reset(self):
        self.rect.left = 0
        
#Calculate the score for the player and the player's health
class PointCalculator(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.healthBar = 100
        self.brainCount = 0
        self.font = pygame.font.SysFont("None", 50)
 
#Display the Health bar and Brain count as they are changed (See GameScreen's Collisison detection)       
    def update(self):
        self.text = "life: %d, Brains: %d" % (self.healthBar, self.brainCount)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()

#The game's actual play screen           
def GameScreen():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Zombie Survival Version 0.1")
        
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    
    #Zombie Acid
    spitAcid = SpitAcid(screen)
    #Avatar (100 health) (Takes Damage)
    dougTheZombie = DougTheZombie(spitAcid)
    
    #Objective, Brain, the Avatar(Above) must collide with the objective to earn a score
    brain1 = Brain()
    
    #Enemy, Villager, The Avatar(two Above) must avoid the enemy 
    #through jumps or Spitting Zombie Acid on them
    enemy1 = Villager()
    
    #Game screen background
    ground = Ground()
    
    #The game's score board 
    pointCalculator = PointCalculator()
    
    #Sprite groups
    friendSprites     = pygame.sprite.OrderedUpdates(ground,dougTheZombie,spitAcid)
    brainSprites      = pygame.sprite.OrderedUpdates(brain1)
    enemySprites      = pygame.sprite.OrderedUpdates(enemy1)
    scoreBoardSprites = pygame.sprite.OrderedUpdates(pointCalculator)
    
    #Game Loop
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
        #Collision detection Avatar VS Brain (+ 1 Brain)
        brainHit = pygame.sprite.spritecollide(dougTheZombie, brainSprites, False)
        if brainHit:
            pointCalculator.brainCount += 1
            for thePBrain in brainHit:
                dougTheZombie.biteSound.play()
                thePBrain.reset()
        
        #Collision detection Avatar VS Villager (-25HP)
        vilagerHit = pygame.sprite.spritecollide(dougTheZombie, enemySprites, False)
        if vilagerHit:
            pointCalculator.healthBar -= 25
            if pointCalculator.healthBar <= 0:
                keepGoing = False
            for theVillager in vilagerHit:
                dougTheZombie.painSound.play()
                theVillager.reset()
        #Collision detection Avatar VS Brain (+ 1 Brain)
        enemyHit = pygame.sprite.spritecollide(spitAcid, enemySprites, False)
        if enemyHit:
            pointCalculator.brainCount += 1
            for theVillager in enemyHit:
                dougTheZombie.biteSound.play()
                theVillager.reset()
                spitAcid.reset()      
        
           
        #Update and draw friendSprites     
        friendSprites.update()
        friendSprites.draw(screen)
        
        #Update and draw brainSprites     
        brainSprites.update()
        brainSprites.draw(screen)
        
        #Update and draw enemySprites     
        enemySprites.update()
        enemySprites.draw(screen)
        
        #Update and draw enemySprites     
        scoreBoardSprites.update()
        scoreBoardSprites.draw(screen)
        
        pygame.display.flip()
 
    return pointCalculator.brainCount
   
def instructions(brainCount):
    pygame.display.set_caption("Zombie Survival!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    #Generate the Instructions screen
    insFont = pygame.font.SysFont(None, 40)
    insLabels = []
    instructions = (
    "Zombie Survival!.     Last score: %d" % brainCount ,
    "",
    "It's a great time to be a zombie!",
    "The villager's brain waggon has",
    "has a busted wheel and brains are",
    "all over the place!",
    "Instructions: Move Doug [MOUSE]",
    "back and forth to collect all the brains",
    "you can to feed your hungry friends!",
    "But watch out for the villagers, press",
    "[SPACE] to shoot your zombie acid", 
    "to defend yourself ",
    "",
    "good luck!",
    "",
    "click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
         
    pygame.mouse.set_visible(True)
    return donePlaying

def endGame(brainCount):
    pygame.display.set_caption("Zombie Survival!")

    
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
     
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Zombie Survival!.     Last score: %d" % brainCount ,
    "",
    "",
    "",
    "",
    "                You Have Died!",    
    "",
    "                      Score: %d" % brainCount,
    "",
    "                     REPLAY? ",
    "",
    "",
    "",
    "click to replay, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 255))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
         
    pygame.mouse.set_visible(True)
    return donePlaying
   
def main():
    donePlaying = False
    brainCount = 0
    while not donePlaying:
        donePlaying = instructions(brainCount)
        if not donePlaying:
            brainCount = GameScreen()
            donePlaying = endGame(brainCount)
    
if __name__ == "__main__":
    main()
            

            
