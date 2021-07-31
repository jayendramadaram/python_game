

import sys
import pygame
from pygame.sprite import Sprite,Group
from time import sleep
import pygame.font



class Alien(Sprite):

    def __init__(self, game_req , game ):
        super(Alien,self).__init__()
        self.game = game
        self.game_req = game_req

        self.image = pygame.image.load(r"C:\Users\jayendra\AppData\Local\Programs\Python\Python39\pyProjects\space_wars\images\1c4ea9a14de5e9eebb04387d1e9f54ec-removebg-preview.png")
        self.image = pygame.transform.scale(self.image , (50, 50)) 
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.game.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        

    def update(self):
        self.x +=  self.game_req.alien_speed*self.game_req.alien_direction
        self.rect.x = self.x

    def blitme(self):
        self.game.blit(self.image , self.rect)

def check_fleet(game_req ,aliens):
    for ufo in aliens.sprites():
        if ufo.check_edges():
            change_direction(game_req , aliens)
            break

def change_direction(game_req , aliens):
    for ufo in aliens.sprites():
        ufo.rect.y += game_req.drop
    game_req.alien_direction *= -1
        

class Bullet(Sprite):
    # adding bullet to jet

    def __init__(self , game_req , game , jet):
        super(Bullet , self).__init__()
        self.game = game

        #rect bullet formation
        self.rect = pygame.Rect(0,0,game_req.bullet_width,game_req.bullet_height)

        self.rect.centerx = jet.rect.centerx
        self.rect.top = jet.rect.top


        #now y axis location

        self.y = float(self.rect.y)
        self.color = game_req.bullet_color
        self.bullet_speed = game_req.bullet_spped

    def update(self):
        self.y -= self.bullet_speed
        self.rect.y = self.y
    def drawbull(self):
        pygame.draw.rect(self.game , self.color ,self.rect)

class ship_struct(Sprite):
    def __init__(self , game , game_req):
        super(ship_struct, self).__init__()

        self.game = game
        self.game_req = game_req

        self.move_right = False
        self.move_left = False

        self.image = pygame.image.load(r"C:\Users\jayendra\AppData\Local\Programs\Python\Python39\pyProjects\space_wars\images\istockphoto-1128766183-612x612-removebg-preview.png")
        self.image = pygame.transform.scale(self.image , (100, 100)) 
        self.rect = self.image.get_rect()

        self.screen_dim = game.get_rect()
        


        self.rect.centerx = self.screen_dim.centerx
        self.rect.bottom = self.screen_dim.bottom - 40

        

        #print(self.rect.bottom)

    def update(self ):
        # game jet boundary initialisation
        if self.move_right and self.rect.right < self.screen_dim.right:
            self.rect.centerx += self.game_req.ship_speed
        elif self.move_left and self.rect.left > 0:
            self.rect.centerx -= self.game_req.ship_speed

        

        

    def blitme(self):
        self.game.blit(self.image , self.rect)

def check_play_button(records, play_button, mouse_x, mouse_y ,game_req , aliens ,
                      bullets , game , jet,scores ):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not records.active:
        game_req.dyn_setts()
        pygame.mouse.set_visible(False)
        records.active = True
        records.reset()

        scores.prep_score()
        scores.prep_high_score()
        scores.prep_level()
        scores.prep_ships()
        
        aliens.empty()
        bullets.empty()

        

        create_fleet(game_req , game , aliens , jet)


def check(game_req , game , jet , bullets , records , play , aliens , scores ):
    for event in pygame.event.get(): ## records events donw by user
        #print(event.type)
        if event.type == pygame.QUIT:
                # when player clicks wrong button on top
                
            sys.exit() #end process

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            mx , my =  pygame.mouse.get_pos()
            check_play_button(records, play, mx, my , game_req ,
                              aliens , bullets , game , jet , scores)

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RIGHT:
                #print("uouo")
                jet.move_right = True
            elif event.key == pygame.K_LEFT:
                #print("uou")
                jet.move_left = True
            elif event.key == pygame.K_SPACE:
                #print("uo")
                if len(bullets) < game_req.bull_allowed:
                    new_bullet = Bullet(game_req , game , jet)
                    bullets.add(new_bullet)

        elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_RIGHT:
                jet.move_right = False
            elif event.key == pygame.K_LEFT:
                jet.move_left = False

            

class setts():
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.bg_col = (0, 0, 0)

        #bullet initilisation

##        self.bullet_spped = 10
        self.bullet_color = 214, 122, 41
        self.bullet_height = 15
        self.bullet_width = 9
        self.bull_allowed = 4
##        self.alien_speed = 2
##        self.alien_direction = 1
        self.drop = 10
        self.ships = 3


        
        self.speedup = 1.1
        self.score_scale = 1.5
        self.alien_points = 50
        self.dyn_setts()
        

        

        


    def dyn_setts(self):
        self.ship_speed = 3
        self.bullet_spped = 9
        self.alien_speed = 0.5
        self.alien_direction = 1
        

        
        

    def change(self):
        self.ship_speed *= self.speedup
        self.bullet_spped *= self.speedup
        self.alien_speed *= self.speedup
        
        

def get_row(game_req , ship_height , alien_height):
    space_y = (game_req.height - (3*alien_height) - ship_height)

    return int(space_y / (2*alien_height))


def create_fleet(game_req , game , aliens , jet):
    ufo = Alien(game_req , game)
    alien_width = ufo.rect.width
    space_x = game_req.width - 2*(alien_width)
    alien_num = int(space_x / (2*alien_width))

    row_num = get_row(game_req , jet.rect.height , ufo.rect.height)
    for row in range(row_num):
        for alien_coun in range(alien_num):
            ufo = Alien(game_req , game)
            ufo.x = alien_width +2*alien_width*alien_coun
            ufo.rect.x = ufo.x
            aliens.add(ufo)
            ufo.rect.y = ufo.rect.height +2*ufo.rect.height*row
        
        


def game_updation( game_req , game , jet , bullets , aliens ,records , play, scores ):
    game.fill(game_req.bg_col)
    for bullets in bullets.sprites():
        bullets.drawbull()
    jet.blitme()

    

    if not records.active:
        play.draw()
    aliens.draw(game)

    scores.show_score()

    pygame.display.flip() #earises old changes and gives new changes every time

def update_aliens(game_req , aliens , jet , records , game , bullets , scores):
    check_fleet(game_req ,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(jet , aliens):
        #
        ship_hit(game_req , records , game ,jet,aliens , bullets , scores)
    check_aliens_bottom(game_req, records, game, jet, aliens, bullets , scores)

        
    

def update_bullets(game_req , game , bullets , aliens , jet  , scores , records ):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions :
        for aliens in collisions.values():
            records.score += game_req.alien_points*len(aliens)
            scores.prep_score()

        check_high_score(records , scores)


    if len(aliens) == 0:
        bullets.empty()
        game_req.change()
        create_fleet(game_req , game , aliens , jet)

        records.lvl += 1
        scores.prep_level()

class score:
    def __init__(self , game_req , game , records):
        self.game =game
        self.screen_rect = game.get_rect()
        self.game_req = game_req
        self.records = records

        self.text_color = (245, 239, 66)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        self.ships = Group()

        for ship_n in range(self.records.ships):
            jet =  ship_struct( self.game , self.game_req)
            jet.rect.x = 10 + ship_n * jet.rect.width
            jet.rect.y = 10
            self.ships.add(jet)

    def prep_level(self):
        self.level_image = self.font.render("level :" + str(self.records.lvl), True,
 self.text_color, self.game_req.bg_col)


        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        high_score = int(round(self.records.high_score, -1))

        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.game_req.bg_col)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        score_str = str(self.records.score)
        self.score_image = self.font.render(score_str, True, self.text_color,self.game_req.bg_col)
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.game.blit(self.score_image, self.score_rect)

        self.game.blit(self.high_score_image, self.high_score_rect)
        self.game.blit(self.level_image, self.level_rect)
        self.ships.draw(self.game)


def check_high_score(records, sb):
    if records.score > records.high_score:
        records.high_score = records.score
        sb.prep_high_score()     

class  GameStats:
    def __init__(self , game_req):
        self.game_req = game_req
        self.reset()

        self.active = True
        self.high_score = 0

    def reset(self):
        self.ships = self.game_req.ships
        self.score = 0
        self.lvl = 1


class Button:
    def __init__(self , game_req , game , msg , scores):
        self.game = game
        self.screen_rect = game.get_rect()

        self.width , self.height = 200 , 50
        self.button_color = ( 245, 144, 66)
        self.txt = (255 , 255 , 255)
        self.font = pygame.font.SysFont(None , 48)

        self.rect = pygame.Rect(0,0,self.width , self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)
        self.scores = scores

    def prep_msg(self , msg):
        self.msg_image = self.font.render(msg, True, self.txt,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.game.fill(self.button_color , self.rect)
        self.game.blit(self.msg_image, self.msg_image_rect)
        self.scores.show_score()


def check_aliens_bottom(game_req, records, game, jet, aliens, bullets , scores):
    screen_rect = game.get_rect()
    for ufo in aliens.sprites():
        if ufo.rect.bottom >= screen_rect.bottom:
            ship_hit(game_req , records , game ,jet,aliens , bullets , scores)
            break
            


def ship_hit(game_req , records , game ,jet,aliens , bullets , scores):
    if records.ships >0:
        records.ships -= 1
        print(records.ships)

        scores.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(game_req , game , aliens , jet)
        sleep(1)

    else:
        records.active = False
        pygame.mouse.set_visible(True)

    

def game_window():
    # lets initialise window size and stuff later you can change

    
    print("running")
    pygame.init() # initialisation of working

    game_req = setts()
    pygame.display.set_caption("shooting game") #game title
    game = pygame.display.set_mode((game_req.width , game_req.height))  #game window size

    bg_color = game_req.bg_col
    

    jet = ship_struct(game , game_req)

    bullets = Group()

    aliens = Group()
    records = GameStats(game_req)

    
    create_fleet(game_req , game , aliens , jet)
    scores = score(game_req , game , records)
    play = Button(game_req , game , "play" , scores)

    
    
    while True: # running game until player clicks 
        
        check(game_req , game , jet , bullets ,  records , play , aliens , scores )
        if records.active:
            jet.update()
            update_bullets(game_req , game , bullets , aliens , jet ,scores ,records )
            update_aliens(game_req , aliens , jet , records , game , bullets , scores)
        game_updation( game_req , game , jet , bullets , aliens ,records , play , scores )

        # remove infinite mmoving bullets

        

        
        
game_window()
        

        
