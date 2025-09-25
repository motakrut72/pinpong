import pygame
from random import randint
from random import choice
class GameStates():

    def __init__(self):
       self.is_working = False

    def start_game(self):
        self.is_working = True
    
    def stop_game(self):
        self.is_working = False

class Hit_box():

    def __init__(self, screen, x, y, width, height, color, hitbox_size,string):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.string = string
        
        if hitbox_size < 1:
            hitbox_size = 1
        self.hitbox_size = hitbox_size

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.main_font = pygame.font.SysFont(None, 36)
        self.text = self.main_font.render(self.string, True, (0, 0, 0))
        self.with_text = False
        self.is_working = True

    
    def draw_hitbox(self):
        if self.is_working:
            pygame.draw.rect(self.screen, self.color, self.rect, self.hitbox_size)
    
    def is_clicked(self, click_position):
        return self.rect.collidepoint(click_position[0], click_position[1])
    
    def draw_text(self,shift_x, shift_y):
        if self.is_working:
            pygame.draw.rect(self.screen, self.color, self.rect)
            pygame.draw.rect(self.screen, (0, 0, 255), self.rect, 2)
            screen.blit(pygame.font.SysFont(None, 36).render('PRESS TO RESTART ' , True, (255, 255, 255)), (180,100))
            if self.with_text == True:
                self.screen.blit(self.text, (self.rect.x + shift_x, self.rect.y + shift_y))


class Picture(Hit_box):

    def __init__(self, screen, x, y, width, height, color, hitbox_size,string, path):
        Hit_box.__init__(self, screen, x, y, width, height, color, hitbox_size,string)
        self.path = path
        self.image = pygame.transform.scale(pygame.image.load(self.path).convert_alpha(), (self.width, self.height))
        
    def draw_picture(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(Picture):
    
    def __init__(self, screen, x, y, width, height, color, hitbox_size,string, path, speed):
        Picture.__init__(self, screen, x, y, width, height, color, hitbox_size,string, path)
        self.speed = speed
        self.dx = 0


    def move(self):
        self.rect.x += self.speed * self.dx

    def controller(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and not keys[pygame.K_d]:
            self.dx = -1
        elif keys[pygame.K_d] and not keys[pygame.K_a]:
            self.dx = 1
        else:
            self.dx = 0
    
    def controller_with_another_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.dx = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.dx = 1
        else:
            self.dx = 0

    def colide_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

    def collide_ball(self, sprite):
        if sprite.rect.colliderect(self.rect):
            delta_x = min(abs(self.rect.left - sprite.rect.right), abs(self.rect.right - sprite.rect.left))
            delta_y = min(abs(self.rect.top - sprite.rect.bottom), abs(self.rect.bottom - sprite.rect.top))
            kick_sound.play()
            if delta_x > delta_y:
                collision = 'vertical'
            elif delta_x < delta_y:
                collision = 'horizontal'
            else:
                collision = 'other'

            if collision == 'vertical':
                if sprite.dy > 0:
                    sprite.rect.bottom = self.rect.top
                elif sprite.dy < 0:
                    sprite.rect.top = self.rect.bottom
                sprite.dy *= -1
            elif collision == 'horizontal':
                if sprite.dx > 0:
                    self.rect.left += 1
                    sprite.rect.right = self.rect.left
                elif sprite.dx < 0:
                    self.rect.right -= 1
                    sprite.rect.left = self.rect.right
                sprite.dx *= -1
            elif collision == 'other':
                if sprite.dy > 0:
                    sprite.rect.bottom = self.rect.top - 1
                elif sprite.dy < 0:
                    sprite.rect.top = self.rect.bottom + 1
                sprite.dy *= -1
                if sprite.dx > 0:
                    self.rect.left += 1
                    sprite.rect.right = self.rect.left - 1
                elif sprite.dx < 0:
                    self.rect.right -= 1
                    sprite.rect.left = self.rect.right + 1
                sprite.dx *= -1




class Ball(Picture):

    def __init__(self,screen,x, y, width, height, color, hitbox_size, string,path, speed):
        Picture.__init__(self,screen,x, y, width, height, color, hitbox_size, string,path)
        self.speed = speed
        self.dx = choice([-1,1])
        self.dy = choice([-1,1])

    def move(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        if self.rect.left < 0:
            self.rect.left = 0
            self.dx *= -1
            kick_sound.play()
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
            self.dx *= -1
            kick_sound.play()



    def draw_ball(self):
        self.draw_picture()



pygame.init()

screen_title = 'Пинпонг'
screen_width = 500
screen_height = 700
screen_color = (255,255,255)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)

fps = 60
clock = pygame.time.Clock()

states = GameStates()
states.start_game()

kick_sound = pygame.mixer.Sound('kick.ogg')
kick_sound.set_volume(0.1)


#создание объектов
test = Hit_box(screen,225, 200, 100, 100,(255,255,255),3, 'PRESS!' )
test.with_text = True
test.is_working = False
background = Picture(screen, 0, 0, 500, 700, (0,0,0), 3,'', '38758.jpg')
sprite1 = Player(screen, 20, screen_height - 64 - 30, 80,10, (0,0,0), 3,'', 'platform.png', 7)
sprite2 = Player(screen, 20, screen_height - 606, 80,10, (0,0,0), 3,'', 'platform.png', 7)
ball = Ball(screen, 250, screen_height - 350, 50,50, (0,0,0), 3,'', 'ball.png', 4)
p1 = 0 
p2 = 0

main_font = pygame.font.SysFont(None,36)
player1_text = main_font.render('Player 1: ' + str(p1), True, (255,255,255))
player2_text = main_font.render('Player 2:' + str(p2), True, (255,255,255))




while states.is_working:
    # например обработчик выхода из игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            states.stop_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_position = event.pos
            if test.is_clicked(click_position) and test.is_working:
                test.is_working = False
                sprite1 = Player(screen, 0, screen_height - 64 - 30, 80,10, (0,0,0), 3,'', 'platform.png', 7)
                sprite2 = Player(screen, 20, screen_height - 606, 80,10, (0,0,0), 3,'', 'platform.png',7)
                ball = Ball(screen, 250, screen_height - 350, 50,50, (0,0,0), 3,'', 'ball.png', 4)
                p1 = 0 
                p2 = 0
                player1_text = main_font.render('Player 1: ' + str(p1), True, (255,255,255))
                player2_text = main_font.render('Player 2:' + str(p2), True, (255,255,255))


    screen.fill(screen_color)
    background.draw_picture()
    sprite1.draw_picture()
    sprite1.move()
    sprite1.controller()
    sprite1.colide_screen()
    sprite2.draw_picture()
    sprite2.move()
    sprite2.controller_with_another_player()
    sprite2.colide_screen()
    sprite1.collide_ball(ball)
    sprite2.collide_ball(ball)
    ball.move()
    ball.draw_ball()

    if ball.rect.bottom < 0:
        p1 += 1
        player1_text = main_font.render('Player 1: ' + str(p1), True, (255,255,255))
        ball = Ball(screen, 250, screen_height - 350, 50,50, (0,0,0), 3,'', 'ball.png', 4)

    if ball.rect.top > screen_height:
        p2 += 1
        player2_text = main_font.render('Player 2: ' + str(p2), True, (255,255,255))
        ball = Ball(screen, 250, screen_height - 350, 50,50, (0,0,0), 3,'', 'ball.png', 4)
    

    test.draw_hitbox()
    test.draw_text(2,35)

    screen.blit(player1_text, (0,20))
    screen.blit(player2_text, (0,60))

    if p1 >= 5:
        test.draw_hitbox()
        test.draw_text(2,35)
        test.is_working = True
        screen.blit(pygame.font.SysFont(None, 36).render('PLAYER 1 WIN!' , True, (255, 255, 255)), (180,50))
        ball.speed = 0
        sprite1.speed = 0
        sprite2.speed = 0

    if p2 >= 5:
        test.draw_hitbox()
        test.draw_text(2,35)
        test.is_working = True
        screen.blit(pygame.font.SysFont(None, 36).render('PLAYER 2 WIN!' , True, (255, 255, 255)), (180,50))
        ball.speed = 0
        sprite1.speed = 0
        sprite2.speed = 0




        
            
    
    pygame.display.update()
    clock.tick(fps)