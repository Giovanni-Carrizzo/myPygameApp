#imports
import pygame as pg
import random

from os import path
img_dir = path.join(path.dirname(__file__),'img')#img is the folder where the graphics are
snd_dir = path.join(path.dirname(__file__),'snd')#snd is the folder where the sounds are 
#parameters
WIDTH, HEIGHT, FPS = (750,650,60)
#define colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#Initialise common pygame objects
pg.init()
pg.mixer.init() #required for sound

#a sprite will be an object which inherits from the built in sprite class
class Player(pg.sprite.Sprite):
    #sprite for the player
    def __init__(self):
        #constructor
        pg.sprite.Sprite.__init__(self) #inheritance
        self.image = pg.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        #useful for moving, size, position and collision
        self.rect = self.image.get_rect()
        self.radius = 21 #assumption made since width of sprite is 50 - radius is 25
        #we will draw a circle so we see how big it is so we can adjust the radius
        #we will draw it in red at the centre of the rectangle and using the radius above
        

        #looks at the image and gets its rect
        self.rect.centerx = WIDTH/2 #places image in the centre
        self.rect.bottom = HEIGHT-10 #puts it in 10px from bottom of screen
        #it needs to move side to side so we need speed
        self.speedx = 0

    def update(self):
        #we will keep the default speed of object to zero and only alter it with a key press
        #this way we avoid coding for what happens when the key is released
        self.speedx = 0
        keystate = pg.key.get_pressed() #returned a list of keys that are down
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx #move at speed to be set by controls
        #to ensure it does not run off the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        #spawns new bullet at centerx of player
        #y will spawn at the top - i.e. bottom of the bullet at the top of the player
        bullet = Bullet(self.rect.centerx,self.rect.top)
        #add bullet to all sprites grouo so that its updated
        all_sprites.add(bullet)
        #add bullet to the bullets sprite group
        bullets.add(bullet)
        #play a sound
        shoot_sound.play()

class Mob(pg.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        mob_img = random.choice(mob_images)
        self.image_orig = pg.transform.scale(mob_img,(40,40))
        self.image_orig.set_colorkey(BLACK)
        #set sprite image to a copy
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * 0.9/2)
        #make the enemy spawn off top of screen to appear off thescreen and then start dropping down
        self.rect.x = random.randrange(0,WIDTH - self.rect.width) #appears within the limits of the screen
        self.rect.y = random.randrange(-100,-40) #this is off the screen
        self.speedy = random.randrange(1,8)
        #rotating the enemy sprite
        self.rot = 0 #angle of rotation
        self.rot_speed = random.randrange(-8,8)

        #get time since last update
        #the variable will be updated each time the rotation happens
        self.last_update = pg.time.get_ticks() 

    def rotate(self):
        #rotation code
        #find out whether its time to rotate
        now = pg.time.get_ticks()
        #figure out how long it has been in milliseconds and if its more than 50 rotate
        if now - self.last_update > 50:
            self.last_update = now #take last update and set it to now 
            self.rot = (self.rot + self.rot_speed) % 360 #modulo 360 will ensure rotation doesnt exceed 360
            self.image = pg.transform.rotate(self.image_orig, self.rot) #rotate original image at rot speed

            #rotated image will be set to new image 
            #figure out where the original center of the rect was
            #set the image to new image and get the new rectangle
            #take the new rect and put it at the same spot as the old center
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        #move downwards
        self.rect.y += self.speedy
        #deal with enemy when they get to bottom of the screen
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
            self.rect.y = random.randrange(-100,-40) #this is off the screen
            self.speedy = random.randrange(1,8)          

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        #x and y and respawn positions based on the player's position
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(bullets_img,(30,30 ))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #set respawn position to right in front of the player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        #rect moves upwards at the speed
        self.rect.y += self.speedy
        #kill it if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

#create the display
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('My Game')
clock = pg.time.Clock() #handles the speed

#search for a matching font
font_name = pg.font.match_font('arial')

def draw_text(surf,text,size,x,y):
    #create a font object
    font = pg.font.Font(font_name,size)#this will create text
    text_surface = font.render(text,True,WHITE) #True is for anti aliasing
    text_rect = text_surface.get_rect()#get the rectangle for the text
    text_rect.midtop = (x,y) #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)


background = pg.image.load(path.join(img_dir, "Joe.jpg ")).convert()
background_rect = background.get_rect()

player_img = pg.image.load(path.join(img_dir, "Garley.jpg")).convert()
mob_img = pg.image.load(path.join(img_dir, "Sean.jpg")).convert()
bullets_img = pg.image.load(path.join(img_dir, "Lucian.jpg")).convert()

#create a list of enemy images
mob_images = []
mob_list = ["Sean.jpg", "Stefan.jpg", "Szymon.jpg", "Cody.jpg"]

#loop through list of files
for img in mob_list:
    mob_images.append(pg.image.load(path.join(img_dir,img)).convert())

#load sound files
shoot_sound = pg.mixer.Sound(path.join(snd_dir, 'laser_sound_effect.mp3'))
death_sound = pg.mixer.Sound(path.join(snd_dir, 'falling-mario.mp3'))

#load background sound
pg.mixer.music.load(path.join(snd_dir, 'Symphony.mp3'))
pg.mixer.music.set_volume(0.6)
#create a sprite group
all_sprites = pg.sprite.Group()
mobs = pg.sprite.Group()  #creating another group would aid during collision detection
bullets = pg.sprite.Group()  
#instatiate the player object and add it to the sprite group
player = Player()
#Spawn some mobs
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

all_sprites.add(mobs)
all_sprites.add(player)

score = 0
#play background audio
#parameters could include - play list, looping
#Loops=-1 - tells pygame to loop each time audio gets to the end
pg.mixer.music.play(loops=-1)
#GameLoop
running = True
while running:
    #keep the game running at the right speed
    clock.tick(FPS)
    #process input (events)
    for event in pg.event.get():
        #check event for closing the window
        if event.type == pg.QUIT:
            running = False
        #check event for keydown to shoot
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()

    #update
    all_sprites.update()
    #Check if a bullet hits a mob
    hits = pg.sprite.groupcollide(mobs,bullets,True,True)
    #respawn mobs destroyed by bullets 
    for hit in hits:
        score += 1 #1 point for every hit you make - challenge is c
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    #Check to see if a mob hits the player
    hits = pg.sprite.spritecollide(player,mobs,False, pg.sprite.collide_circle) #parameters are object to check against and group against
    #False indicates whether hit item in group should be deleted or not
    
    if hits:
        death_sound.play()
        running = False
    #draw/render
    screen.fill(BLACK)
    #draw background on screen
    screen.blit(background,background_rect)

    all_sprites.draw(screen)
    #draw the score here
    draw_text(screen,str(score),18,WIDTH/2,10)
    #always do this after drawing anything
    pg.display.flip()
#terminate the game window and close everything up    
pg.quit