#  Source File Name: Zombie_Survival_Version_02
#  Author's Name: Jordan Cooper
#  Last Modified By: Jordan Cooper
#  Date Last Modified: Thursday, Aug 1, 2013
""" 
  Program Description:  Zombie Survival is about Doug the zombie. Doug, the lovable zombie is back from his
                        adventures in Brain Buster, and hes ready to share the brains! In this game Doug must
                        collect as many brains as he can to feed his hungry zombie friends. 
                        
        Version: 0.3   - Sprite DougTheZombie
                            - Jump function added
                                - the player can press the [space] bar to jump
                        - Level Difficulty started
                            -health changed depending on difficulty chosen
                        
                            
"""
import random
import pygame
import math

pygame.init()

screen = pygame.display.set_mode((640, 480))

# Create the Avatar Named Doug the Zombie
class DougTheZombie(pygame.sprite.Sprite):
    def __init__(self,spitAcid):
        pygame.sprite.Sprite.__init__(self)
        
        self.jumping = False
        
        self.spitAcid = spitAcid
        self.image = pygame.image.load("DougTheZombie.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.dy = 10
        self.yMax = 360
        
        # Incorporate Sound to the game
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.biteSound = pygame.mixer.Sound("bite.wav")
            self.painSound = pygame.mixer.Sound("pain.wav")
#             self.backgroundSound = pygame.mixer.Sound("background.wav")
#             self.backgroundSound.play(-1)      
    
    def checkAcid(self):
        keys = pygame.key.get_pressed()
            
        if keys[pygame.K_f]:
            self.spitAcid.x = self.rect.centerx
            self.spitAcid.y = self.rect.centery
            
    def jump(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.jumping = True

    def calculateJump(self):
        self.yMax -= self.dy
        
    def calculateDrop(self):
        self.yMax += self.dy
    
    def checkBounds(self):
        if self.yMax < 200:
            self.resetJump()
    
    def checkLandingBounds(self):
        if self.yMax < 360:
            self.calculateDrop()
 
    def resetJump(self):
            self.yMax = 200
            self.jumping = False
            
            
    # Update the Doug Avatar       
    def update(self):
        ''' Get Mouse position, set the y position and a fixed position to the sprite'''
        mousex , mousey = pygame.mouse.get_pos()
        
        if self.jumping == True:
            self.calculateJump()
            self.checkBounds()
            self.rect.center = (mousex, self.yMax)      
        else:
            self.checkLandingBounds()
            self.rect.center = (mousex,self.yMax)
        
        ''' If the Avatar is moving off the screen, set the avatar to the top of the screen.'''
        if mousex < (40): 
            self.rect.center = (40,360)
        if mousex > (600): 
            self.rect.center = (600,360)
        
        self.checkAcid()
        self.jump()
        
        
class SpitAcid(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        self.image = pygame.image.load("SpitAcid.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        self.dx = 10
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


    
    # Hide the acid when not in use
    def reset(self):
        self.x = -50
        self.y = -50

            
# Create the Objective sprit, the Brain           
class Brain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("brain.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 5

# Move the brain left 5px Until the brain leaves the player's feild of view
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
            
# Reset the brain to a randomized position BEHIND the player's feild of view           
    def reset(self):
        self.rect.left = 0
        self.rect.centerx = random.randrange(700, 1000)
        self.rect.centery = random.randrange(250, 360)
        
# Create the  enemy, the angry villager                
class Villager(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("villager.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 7

# Move the angry villager 7px to the left, to appear as if charging at the zombie    
    def update(self):
        self.rect.centerx -= self.dx
        if self.rect.right < 0:
            self.reset()
  
# Reset the villager's position to a randomized location off of the player's feild of view            
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
# Move the Background Image at a rate of 5px, Reset the image once almost 3/4 of the image has been displayed

# This will make the image seem as if it is never ending       
    def update(self):
        self.rect.left -= self.dx
        if self.rect.left <= -1900:
            self.reset() 

# Reset the Background Image to the left side of the page  
    def reset(self):
        self.rect.left = 0
        
# Calculate the score for the player and the player's health
class PointCalculator(pygame.sprite.Sprite):
    def __init__(self,difficultyLevel):
        pygame.sprite.Sprite.__init__(self)
        
        # Easy Difficulty. 150% health
        if difficultyLevel ==1:
            self.healthBar = 150
        # Medium Difficulty. 100% Health
        elif difficultyLevel ==2:
            self.healthBar = 100
        # Hard Difficulty. 25% Less health
        elif difficultyLevel ==3:
            self.healthBar = 75
            
        self.brainCount = 0
        self.font = pygame.font.SysFont("None", 50)
 
# Display the Health bar and Brain count as they are changed (See GameScreen's Collisison detection)       
    def update(self):

        self.text = "life: %d, Brains: %d" % (self.healthBar, self.brainCount)
        self.image = self.font.render(self.text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()

# The game's actual play screen           
def GameScreen(difficultyLevel):
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Zombie Survival Version 0.3")
        
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    
    # Zombie Acid
    spitAcid = SpitAcid(screen)
    # Avatar (100 health) (Takes Damage)
    dougTheZombie = DougTheZombie(spitAcid)
    
    # Objective, Brain, the Avatar(Above) must collide with the objective to earn a score
    brain1 = Brain()
    
    # Enemy, Villager, The Avatar(two Above) must avoid the enemy 
    # through jumps or Spitting Zombie Acid on them
    enemy1 = Villager()
    
    # Game screen background
    ground = Ground()
    
    # The game's score board 
    pointCalculator = PointCalculator(difficultyLevel)
    
    # Sprite groups
    friendSprites     = pygame.sprite.OrderedUpdates(ground,dougTheZombie,spitAcid)
    brainSprites      = pygame.sprite.OrderedUpdates(brain1)
    enemySprites      = pygame.sprite.OrderedUpdates(enemy1)
    scoreBoardSprites = pygame.sprite.OrderedUpdates(pointCalculator)
    
    # Game Loop
    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
               
        # Collision detection Avatar VS Brain (+ 1 Brain)
        brainHit = pygame.sprite.spritecollide(dougTheZombie, brainSprites, False)
        if brainHit:
            pointCalculator.brainCount += 1
            for thePBrain in brainHit:
                dougTheZombie.biteSound.play()
                thePBrain.reset()
        
        # Collision detection Avatar VS Villager (-25HP)
        vilagerHit = pygame.sprite.spritecollide(dougTheZombie, enemySprites, False)
        if vilagerHit:
            pointCalculator.healthBar -= 25
            if pointCalculator.healthBar <= 0:
                keepGoing = False
            for theVillager in vilagerHit:
                dougTheZombie.painSound.play()
                theVillager.reset()
        # Collision detection Avatar VS Brain (+ 1 Brain)
        enemyHit = pygame.sprite.spritecollide(spitAcid, enemySprites, False)
        if enemyHit:
            pointCalculator.brainCount += 1
            for theVillager in enemyHit:
                dougTheZombie.biteSound.play()
                theVillager.reset()
                spitAcid.reset()      
          
        # Update and draw friendSprites     
        friendSprites.update()
        friendSprites.draw(screen)
        
        # Update and draw brainSprites     
        brainSprites.update()
        brainSprites.draw(screen)
        
        # Update and draw enemySprites     
        enemySprites.update()
        enemySprites.draw(screen)
        
        # Update and draw enemySprites     
        scoreBoardSprites.update()
        scoreBoardSprites.draw(screen)
        
        pygame.display.flip()
 
    return pointCalculator.brainCount
   
def instructions(brainCount):
    pygame.display.set_caption("Zombie Survival!")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # Generate the Instructions screen
    insFont = pygame.font.SysFont(None, 40)
    insLabels = []
    instructions = (
    "Zombie Survival!.     Last score: %d" % brainCount ,
    "",
    "It's a great time to be a zombie!",
    "The villager's brain waggon has",
    "has a busted wheel and brains are",
    "all over the place!",
    "",
    "Instructions: Move Doug [MOUSE]",
    "back and forth to collect all the brains",
    "you can to feed your hungry friends!",
    "But watch out for the villagers, press",
    "[F] to shoot and [SPACE] to jump", 
    "",
    "",
    "Press [1] for Easy [2] for Normal",
    "[3] for Hard and [ESC] to quit"
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
                difficultyLevel = 0
                
            elif event.type == pygame.KEYDOWN:
                
                # Quit
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    difficultyLevel= 0
                
                # Easy    
                if event.key == pygame.K_1:
                    keepGoing   = False
                    difficultyLevel=1
                
                # Normal    
                if event.key == pygame.K_2:
                    keepGoing   = False
                    difficultyLevel=2
                
                # Hard
                if event.key == pygame.K_3:
                    keepGoing   = False
                    difficultyLevel=3
    
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
         
    pygame.mouse.set_visible(True)
    return difficultyLevel

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
    "Press [1] for Easy [2] for Normal",
    "[3] for Hard and [ESC] to quit",
    "",
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
                difficultyLevel= 0
            elif event.type == pygame.KEYDOWN:
                # Quit
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    difficultyLevel= 0
                
                # Easy    
                if event.key == pygame.K_1:
                    keepGoing   = False
                    difficultyLevel=1
                
                # Normal    
                if event.key == pygame.K_2:
                    keepGoing   = False
                    difficultyLevel=2
                
                # Hard
                if event.key == pygame.K_3:
                    keepGoing   = False
                    difficultyLevel=3
    
        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
         
    pygame.mouse.set_visible(True)
    return difficultyLevel
   
def main():
    donePlaying = False
    difficultyLevel=1
    brainCount = 0
    while difficultyLevel !=0 :
        difficultyLevel = instructions(brainCount)
        if difficultyLevel !=0:
            PointCalculator(difficultyLevel)
            brainCount  = GameScreen(difficultyLevel)
            difficultyLevel = endGame(brainCount)
    
if __name__ == "__main__":
    main()
            

            
