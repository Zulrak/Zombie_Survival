# Source File Name: Zombie_Survival_Version_0_1
# Author's Name: Jordan Cooper
# Last Modified By: Jordan Cooper
# Date Last Modified: Friday, July 26, 2013
""" 
  Program Description:  Zombie Survival is about Doug the zombie. Doug, the lovable zombie is back from his
                        adventures in Brain Buster, and hes ready to share the brains! In this game Doug must
                        collect as many brains as he can to feed his hungry zombie friends. 
        Version: 0.1    - Created Sprite 'DougTheZombie' who is the avatar
                        - Set boundaries for DougTheZombie he cannot go past the screen's fixed boundaries
                        - Created a Background sprite 
                        - Displayed the background sprite
                        - Created and displayed 1 brain 
                            - the brain currently has collision detection
                            - spawns above the player (Player must jump)
"""
import random
import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))

#Create the Avatar Named Doug the Zombie
class DougTheZombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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


#The game's actual play screen           
def GameScreen():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Zombie Survival Version 0.1")
        
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 255))
    screen.blit(background, (0, 0))
    
    #Avatar (100 health) (Takes Damage)
    dougTheZombie = DougTheZombie()

    brain1 = Brain()
    #Game screen background
    ground = Ground()
    
    #Sprite groups
    friendSprites = pygame.sprite.OrderedUpdates(ground,dougTheZombie)
    brainSprites = pygame.sprite.OrderedUpdates(brain1)
    
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
            for thePBrain in brainHit:
                dougTheZombie.biteSound.play()
                thePBrain.reset()
           
        #Update and draw friendSprites     
        friendSprites.update()
        friendSprites.draw(screen)
        
        #Update and draw brainSprites     
        brainSprites.update()
        brainSprites.draw(screen)
        
        pygame.display.flip()
 

   
def main():
    GameScreen()

    
if __name__ == "__main__":
    main()
            

            
