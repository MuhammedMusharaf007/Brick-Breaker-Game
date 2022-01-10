from typing import overload
import pygame
from pygame.locals import *

pygame.init()
engine_width = 500
engine_height = 500
engine = pygame.display.set_mode((engine_width, engine_height))
pygame.display.set_caption("Smash'em All - MM007")
font = pygame.font.SysFont('Calibri', 30)
y_brick = (255, 255, 0)
r_brick = (255, 0, 0)
b_brick = (0, 0, 0)
white = (255, 255, 255)

rows = 6
columns = 6

game_rows = rows
game_columns = columns
clock = pygame.time.Clock()
framerate = 60
my_ball = False
game_over = 0
score=  0

class Ball():
    def __init__(self, x, y) -> None:
        self.radius = 10
        self.x = x - self.radius
        self.y = y - 50
        self.rect = Rect(self.x, self.y, self.radius*2, self.radius*2)
        self.x_speed = 4
        self.y_speed = -4
        self.max_speed = 5
        self.game_over = 0

    def motion(self):
        collision_threshold = 5
        block_object = Block.bricks
        brick_destroyed = 1
        count_row = 0
        for row in block_object:
            count_item = 0
            for item in row:
                #collision with engine boundary
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_threshold and self.y_speed > 0:
                        self.y_speed *= -1
                    if abs(self.rect.top - item[0].bottom) < collision_threshold and self.y_speed < 0:
                        self.y_speed *= -1
                    if abs(self.rect.right - item[0].left) < collision_threshold and self.x_speed > 0:
                        self.x_speed *= -1
                    if abs(self.rect.left - item[0].right) < collision_threshold and self.x_speed < 0:
                        self.x_speed *= -1

                    if block_object[count_row][count_item][1] > 1:
                        block_object[count_row][count_item][1] -= 1
                    else:
                        block_object[count_row][count_item][0] = (0, 0, 0, 0)
                
                if block_object[count_row][count_item][0] != (0, 0, 0, 0):
                    brick_destroyed = 0
                count_item += 1
            count_row += 1
        
        if brick_destroyed == 1:
            self.game_over = 1

        #collision with bricks
        if self.rect.left < 0 or self.rect.right > engine_width:
            self.x_speed *= -1
        if self.rect.bottom > engine_height:
            self.game_over = -1

        #collision with base
        if self.rect.colliderect(user_basepad):
            if abs(self.rect.bottom - user_basepad.rect.top) < collision_threshold and self.y_speed > 0:
                self.y_speed *= -1
                self.x_speed += user_basepad.direction
                if self.x_speed > self.max_speed:
                    self.x_speed = self.max_speed
                elif self.x_speed < 0 and self.x_speed < - self.max_speed:
                    self.x_speed *= -1
            
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        return self.game_over

    def draw(self):
        pygame.draw.circle(engine, (0,0,255), (self.rect.x +
        self.radius, self.rect.y + self.radius), self.radius)
        pygame.draw.circle(engine, (255,255,255), (self.rect.x + 
        self.radius, self.rect.y + self.radius), self.radius, 1)

    def reset(self, x, y):
        self.radius = 10
        self.x = x - self.radius
        self.y = y - 50
        self.rect = Rect(self.x, self.y, self.radius*2, self.radius * 2 )
        self.x_speed = 4
        self.y_speed = -4
        self.max_speed = 5
        self.game_over = 0


class Block():
    """
    Class to create breakable blocks in the game
    """

    def __init__(self) -> None:
        self.width = engine_width // game_columns
        self.height = 40

    def make_brick(self):
        self.bricks = []
        single_brick = []
        for row in range(game_rows):
            brick_row = []
            for column in range(game_columns):
                x_brick = column * self.width
                y_brick = column * self.height
                rect = pygame.Rect(x_brick, y_brick, self.width, self.height)
                #Row based power to the bricks
                if row < 2:
                    power = 3
                elif row < 4:
                    power = 2
                elif row < 6:
                    power = 1
                
                single_brick = [rect, power]
                brick_row.append(single_brick)
            self.bricks.append(brick_row)
    def draw_brick(self):
        for row in self.bricks:
            for brick in row:
                if brick[1] == 3:
                    brick_colour = b_brick
                elif brick[1] == 2:
                    brick_colour = r_brick
                elif brick[1] == 1:
                    brick_colour = y_brick
                pygame.draw.rect(engine, brick_colour, brick[0])
                pygame.draw.rect(engine, white, (brick[0]), 1)


class base():
    """
    Base pad for the game
    """
    def __init__(self) -> None:
        self.height = 20
        self.width = int(engine_width/game_columns)
        self.x = int((engine_width/2) - (self.width/2))
        self.y = engine_height - (self.height * 2)
        self.speed = 8
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
    
    def slide(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < engine_width:
            self.rect.x += self.speed
            self.direction = 1
        
    def draw(self):
        pygame.draw.rect(engine, (0, 0, 255), self.rect)
        pygame.draw.rect(engine, (255, 255, 255), self.rect, 1)

    def reset(self):
        self.height = 20
        self.width = int(engine_width/game_columns)
        self.x = int((engine_width/2) - (self.width/2))
        self.y = engine_height - (self.height * 2)
        self.speed = 8
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
   

def draw_text(text,font,r_brick, x, y):
    """
    Text output
    """
    image = font.render(text, True, r_brick)
    engine.blit(image, (x, y))


Block = Block()
Block.make_brick()
user_basepad = base()
ball = Ball(user_basepad.x + (user_basepad.width//2),
            user_basepad.y - user_basepad.height)

game = True
while game:
    clock.tick(framerate)
    engine.fill(white)
    Block.draw_brick()
    user_basepad.draw()
    ball.draw()

    if my_ball:
        user_basepad.slide()
        game_over = ball.motion()
        if game_over != 0:
            my_ball = False
    
    if not my_ball:
        if game_over == 0:
            draw_text('CLICK ANYWHERE TO START', font, r_brick, 90, engine_height//2 + 100)
        elif game_over == 1:
            draw_text('YOU WON!!!', font, r_brick, 180, engine_height//2 +50)
            draw_text('CLICK ANYWHERE TO RESTART', font, r_brick, 90, engine_height//2+100)
        elif game_over == -1:
            draw_text('GAME OVER!', font, r_brick, 180, engine_height //2 + 50)
            draw_text('CLICK ANYWHERE TO RESTART', font, r_brick, 90, engine_height//2 + 100)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.MOUSEBUTTONDOWN and my_ball == False:
            my_ball = True
            ball.reset(user_basepad.x + (user_basepad.width//2),
                        user_basepad.y - user_basepad.height)
            user_basepad.reset()
            Block.make_brick()
    
    pygame.display.update()

pygame.quit()