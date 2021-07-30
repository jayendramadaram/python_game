import sys
import pygame
from pygame.sprite import Sprite,Group
from time import sleep
import pygame.font

class Alien(Sprite):

    def __init__(self, game_req , screen ):
        super(Alien,self).__init__()
        self.screen = screen
        self.game_req = game_req

        self.image = pygame.image.load(r"C:\Users\jayendra\AppData\Local\Programs\Python\Python39\pyProjects\space_wars\images\1c4ea9a14de5e9eebb04387d1e9f54ec-removebg-preview.png")
        self.image = pygame.transform.scale(self.image , (50, 50)) 
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        

    def update(self):
        self.x +=  self.game_req.alien_speed*self.game_req.alien_direction
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image , self.rect)

def check_fleet(game_req ,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_direction(game_req , aliens)
            break

def change_direction(game_req , aliens):
    for alien in aliens.sprites():
        alien.rect.y += game_req.drop
    game_req.alien_direction *= -1
        

class Bullet(Sprite):
    # adding bullet to ship

    def __init__(self , game_req , screen , ship):
        super(Bullet , self).__init__()
        self.screen = screen

        #rect bullet formation
        self.rect = pygame.Rect(0,0,game_req.bullet_width,game_req.bullet_height)

        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top


        #now y axis location

        self.y = float(self.rect.y)
        self.color = game_req.bullet_color
        self.bullet_speed = game_req.bullet_spped

    def update(self):
        self.y -= self.bullet_speed
        self.rect.y = self.y
    def drawbull(self):
        pygame.draw.rect(self.screen , self.color ,self.rect)

class ship_struct(Sprite):
    def __init__(self , screen , game_req):
        super(ship_struct, self).__init__()
        self.screen = screen
        self.game_req = game_req

        self.move_right = False
        self.move_left = False

        self.image = pygame.image.load(r"C:\Users\jayendra\AppData\Local\Programs\Python\Python39\pyProjects\space_wars\images\istockphoto-1128766183-612x612-removebg-preview.png")
        self.image = pygame.transform.scale(self.image , (100, 100)) 
        self.rect = self.image.get_rect()

        self.screen_dim = screen.get_rect()
        


        self.rect.centerx = self.screen_dim.centerx
        self.rect.bottom = self.screen_dim.bottom - 40

        

        #print(self.rect.bottom)

    def update(self ):
        # game ship boundary initialisation
        if self.move_right and self.rect.right < self.screen_dim.right:
            self.rect.centerx += self.game_req.ship_speed
        elif self.move_left and self.rect.left > 0:
            self.rect.centerx -= self.game_req.ship_speed

        

        

    def blitme(self):
        self.screen.blit(self.image , self.rect)

def check_play_button(stats, play_button, mouse_x, mouse_y ,game_req , aliens ,
                      bullets , game , ship,scores ):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.active:
        game_req.dyn_setts()
        pygame.mouse.set_visible(False)
        stats.active = True
        stats.reset()

        scores.prep_score()
        scores.prep_high_score()
        scores.prep_level()
        scores.prep_ships()
        
        aliens.empty()
        bullets.empty()

        

        create_fleet(game_req , game , aliens , ship)


def check(game_req , game , ship , bullets , stats , play , aliens , scores ):
    for event in pygame.event.get(): ## records events donw by user
        #print(event.type)
        if event.type == pygame.QUIT:
                # when player clicks wrong button on top
                
            sys.exit() #end process

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            mx , my =  pygame.mouse.get_pos()
            check_play_button(stats, play, mx, my , game_req ,
                              aliens , bullets , game , ship , scores)

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RIGHT:
                #print("uouo")
                ship.move_right = True
            elif event.key == pygame.K_LEFT:
                #print("uou")
                ship.move_left = True
            elif event.key == pygame.K_SPACE:
                #print("uo")
                if len(bullets) < game_req.bull_allowed:
                    new_bullet = Bullet(game_req , game , ship)
                    bullets.add(new_bullet)

        elif event.type == pygame.KEYUP:
            
            if event.key == pygame.K_RIGHT:
                ship.move_right = False
            elif event.key == pygame.K_LEFT:
                ship.move_left = False

            

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


def create_fleet(game_req , screen , aliens , ship):
    alien = Alien(game_req , screen)
    alien_width = alien.rect.width
    space_x = game_req.width - 2*(alien_width)
    alien_num = int(space_x / (2*alien_width))

    row_num = get_row(game_req , ship.rect.height , alien.rect.height)
    for row in range(row_num):
        for alien_coun in range(alien_num):
            alien = Alien(game_req , screen)
            alien.x = alien_width +2*alien_width*alien_coun
            alien.rect.x = alien.x
            aliens.add(alien)
            alien.rect.y = alien.rect.height +2*alien.rect.height*row
        
        


def game_updation( game_req , game , ship , bullets , aliens ,stats , play, scores ):
    game.fill(game_req.bg_col)
    for bullets in bullets.sprites():
        bullets.drawbull()
    ship.blitme()

    

    if not stats.active:
        play.draw()
    aliens.draw(game)

    scores.show_score()

    pygame.display.flip() #earises old changes and gives new changes every time

def update_aliens(game_req , aliens , ship , stats , game , bullets , scores):
    check_fleet(game_req ,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship , aliens):
        #
        ship_hit(game_req , stats , game ,ship,aliens , bullets , scores)
    check_aliens_bottom(game_req, stats, game, ship, aliens, bullets , scores)

        
    

def update_bullets(game_req , game , bullets , aliens , ship  , scores , stats ):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions :
        for aliens in collisions.values():
            stats.score += game_req.alien_points*len(aliens)
            scores.prep_score()

        check_high_score(stats , scores)


    if len(aliens) == 0:
        bullets.empty()
        game_req.change()
        create_fleet(game_req , game , aliens , ship)

        stats.lvl += 1
        scores.prep_level()

class score:
    def __init__(self , game_req , screen , stats):
        self.screen =screen
        self.screen_rect = screen.get_rect()
        self.game_req = game_req
        self.stats = stats

        self.text_color = (245, 239, 66)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        self.ships = Group()

        for ship_n in range(self.stats.ships):
            ship =  ship_struct( self.screen , self.game_req)
            ship.rect.x = 10 + ship_n * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_level(self):
        self.level_image = self.font.render("level :" + str(self.stats.lvl), True,
 self.text_color, self.game_req.bg_col)


        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))

        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,self.text_color, self.game_req.bg_col)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color,self.game_req.bg_col)
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)

        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
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
    def __init__(self , game_req , screen , msg , scores):
        self.screen = screen
        self.screen_rect = screen.get_rect()

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
        self.screen.fill(self.button_color , self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.scores.show_score()


def check_aliens_bottom(game_req, stats, game, ship, aliens, bullets , scores):
    screen_rect = game.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_req , stats , game ,ship,aliens , bullets , scores)
            break
            


def ship_hit(game_req , stats , game ,ship,aliens , bullets , scores):
    if stats.ships >0:
        stats.ships -= 1
        print(stats.ships)

        scores.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(game_req , game , aliens , ship)
        sleep(1)

    else:
        stats.active = False
        pygame.mouse.set_visible(True)

    

def game_window():
    # lets initialise window size and stuff later you can change

    
    print("running")
    pygame.init() # initialisation of working

    game_req = setts()
    pygame.display.set_caption("shooting game") #game title
    game = pygame.display.set_mode((game_req.width , game_req.height))  #game window size

    bg_color = game_req.bg_col
    

    ship = ship_struct(game , game_req)

    bullets = Group()

    aliens = Group()
    stats = GameStats(game_req)

    
    create_fleet(game_req , game , aliens , ship)
    scores = score(game_req , game , stats)
    play = Button(game_req , game , "play" , scores)

    
    
    while True: # running game until player clicks 
        
        check(game_req , game , ship , bullets ,  stats , play , aliens , scores )
        if stats.active:
            ship.update()
            update_bullets(game_req , game , bullets , aliens , ship ,scores ,stats )
            update_aliens(game_req , aliens , ship , stats , game , bullets , scores)
        game_updation( game_req , game , ship , bullets , aliens ,stats , play , scores )

        # remove infinite mmoving bullets

        

        
        
game_window()
        
