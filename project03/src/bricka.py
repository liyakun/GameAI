"""
 bricka (a breakout clone)
 Developed by Leonel Machava <leonelmachava@gmail.com>

 http://codeNtronix.com
"""
import sys
import pygame

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


SCREEN_SIZE = 640, 480
# Object dimensions
BRICK_WIDTH = 60
BRICK_HEIGHT = 15
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS = BALL_DIAMETER / 2

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
BRICK_COLOR = (200,200,0)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3
SPEED = 2

PADDLE_SPEED = 2

class Bricka:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("bricka (a breakout clone by codeNtronix.com)")
        
        self.clock = pygame.time.Clock()

        self.x_distance_to_ball = np.arange(0, SCREEN_SIZE[0], 1)
        # y_distance_to_ball = np.arange(0, SCREEN_SIZE[1], 1)
        self.paddle_movement = np.arange(0, SCREEN_SIZE[0], 1)

        # self.dist_to_ball_lo = fuzz.trimf(self.x_distance_to_ball, [0, 0, 50] )
        # self.dist_to_ball_md = fuzz.trimf(self.x_distance_to_ball, [0, 200, 200 )
        # self.dist_to_ball_hi = fuzz.trimf(self.x_distance_to_ball, [200, , SCREEN_SIZE[0]] )

        # self.paddle_movement_lo = fuzz.trimf(self.paddle_movement, [0, 0, 300])
        # self.paddle_movement_md = fuzz.trimf(self.paddle_movement, [0, SCREEN_SIZE[0]/2, SCREEN_SIZE[0]] )
        # self.paddle_movement_hi = fuzz.trimf(self.paddle_movement, [SCREEN_SIZE[0]/2, SCREEN_SIZE[0], SCREEN_SIZE[0]] )

        self.dist_to_ball_lo = fuzz.trimf(self.x_distance_to_ball, [0, 0, 100] )
        self.dist_to_ball_md = fuzz.trimf(self.x_distance_to_ball, [0, SCREEN_SIZE[0]/2, SCREEN_SIZE[0]] )
        self.dist_to_ball_hi = fuzz.trimf(self.x_distance_to_ball, [10, SCREEN_SIZE[0], SCREEN_SIZE[0]] )

        self.paddle_movement_lo = fuzz.trimf(self.paddle_movement, [0, 0, 20] )
        self.paddle_movement_md = fuzz.trimf(self.paddle_movement, [0, 20, 40] )
        self.paddle_movement_hi = fuzz.trimf(self.paddle_movement, [40, 60, 60] )


        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.init_game()

    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

        self.ball_vel = [5,-5]

        self.create_bricks()

    def create_bricks(self):
        y_ofs = 35
        self.bricks = []
        for i in range(7):
            x_ofs = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT))
                x_ofs += BRICK_WIDTH + 10
            y_ofs += BRICK_HEIGHT + 5

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 5 * PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 5 * PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [5,-5]
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()

    def move_ball(self):
        self.ball.left += SPEED*self.ball_vel[0]
        self.ball.top  += SPEED*self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:            
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
            self.screen.blit(font_surface, (205,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))

    def run(self):
        while 1:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit


            # print( abs(self.ball.left - self.paddle.left + 30 ) )

            # print(self.ball.left - self.paddle.left)
            
            # APPLY FUZZY LOGIC TO MOVE THE PADDLE
            if( self.state == STATE_PLAYING ):
                x_level_lo = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_lo, abs(self.ball.left+BALL_RADIUS - (self.paddle.left + PADDLE_WIDTH /2) ) ) #abs( self.ball.left - self.paddle.left + 31) 
                x_level_md = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_md, abs(self.ball.left+BALL_RADIUS - (self.paddle.left + PADDLE_WIDTH /2) ) )
                x_level_hi = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_hi, abs(self.ball.left+BALL_RADIUS - (self.paddle.left + PADDLE_WIDTH /2) ) )

                activation_lo = np.fmin(x_level_lo, self.paddle_movement_lo)
                activation_md = np.fmin(x_level_md, self.paddle_movement_md)
                activation_hi = np.fmin(x_level_hi, self.paddle_movement_hi)

                aggregated = np.fmax(activation_lo, np.fmax(activation_md, activation_hi))

                # Calculate defuzzified result
                movement = fuzz.defuzz(self.paddle_movement, aggregated, 'centroid')

                # --- UNCOMMENT TO VISULIZE RULES and how they fire -----

                # fig, ax0 = plt.subplots(figsize=(8, 3))
                # tip0 = np.zeros_like(self.paddle_movement)
                # ax0.fill_between(self.paddle_movement, tip0, activation_lo, facecolor='b', alpha=0.7)
                # ax0.plot(self.paddle_movement, self.paddle_movement_lo, 'b', linewidth=0.5, linestyle='--', )
                # ax0.fill_between(self.paddle_movement, tip0, activation_md, facecolor='g', alpha=0.7)
                # ax0.plot(self.paddle_movement, self.paddle_movement_md, 'g', linewidth=0.5, linestyle='--')
                # ax0.fill_between(self.paddle_movement, tip0, activation_hi, facecolor='r', alpha=0.7)
                # ax0.plot(self.paddle_movement, self.paddle_movement_hi, 'r', linewidth=0.5, linestyle='--')
                # ax0.plot([movement, movement], [0, 1], 'k', linewidth=1.5, alpha=0.9)
                # ax0.set_title('Output membership activity')

                # plt.tight_layout()
                # plt.show()

                if( (self.ball.left+BALL_RADIUS - (self.paddle.left + PADDLE_WIDTH /2) ) < 0 ):
                    self.paddle.left -= movement
                else:
                    self.paddle.left += movement


            self.clock.tick(10)
            self.screen.fill(BLACK)
            self.check_input()

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
              



            self.draw_bricks()

            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

            self.show_stats()

            pygame.display.flip()

if __name__ == "__main__":
    Bricka().run()
