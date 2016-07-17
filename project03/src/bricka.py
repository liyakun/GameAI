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
SPEED = 20

PADDLE_SPEED = SPEED/4
MIN_PADDLE_STEP = 1

class Bricka:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("bricka (a breakout clone by codeNtronix.com)")
        
        self.clock = pygame.time.Clock()

        MAX_PADDLE_MOVEMENT = 300
        
        # generate universe variables
        # 1. x distance from paddle to ball
        self.x_distance_to_ball = np.arange(0, SCREEN_SIZE[0], 1)
        # 2. movement range of paddle
        self.paddle_movement = np.arange(0, MAX_PADDLE_MOVEMENT, 1)
        
        window_width = SCREEN_SIZE[0]
        # low: from 0 to window_width/8, and when self.x_distance_to_ball=0 lowest
        self.dist_to_ball_lo = fuzz.trimf(self.x_distance_to_ball, [0, 0, window_width/8] )
        # semi low: from 0 to window_width/4, and when self.x_distance_to_ball=0 lowest
        self.dist_to_ball_semi_lo = fuzz.trimf(self.x_distance_to_ball, [0, window_width/4, window_width/2] )
        # medium: from 0 to SCREEN_SIZE[0], and when self.x_distance_to_ball=SCREEN_SIZE[0]/2 most medium
        self.dist_to_ball_md = fuzz.trimf(self.x_distance_to_ball, [window_width/4, window_width/2, 3*window_width/4] )
        # semi high: from window_width/2 to window_width, and when self.x_distance_to_ball=3*window_width/4, highest
        self.dist_to_ball_semi_hi = fuzz.trimf(self.x_distance_to_ball, [window_width/2, 3*window_width/4, window_width] )
        # high: from 10 to SCREEN_SIZE[0], and when self.x_distance_to_ball=SCREEN_SIZE[0], highest
        self.dist_to_ball_hi = fuzz.trimf(self.x_distance_to_ball, [3*window_width/4, window_width, window_width] )

        # paddle movement control with distance of movement unit
        self.paddle_movement_lo = fuzz.trimf(self.paddle_movement, [0, 20, 40] )
#self.paddle_movement_semi_lo = fuzz.trimf(self.paddle_movement, [0, 2, 4] )
        self.paddle_movement_md = fuzz.trimf(self.paddle_movement, [20, 40, 60] )
#       self.paddle_movement_semi_high = fuzz.trimf(self.paddle_movement, [8, 20, 32] )
        self.paddle_movement_hi = fuzz.trimf(self.paddle_movement, [40, MAX_PADDLE_MOVEMENT, MAX_PADDLE_MOVEMENT] )


        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        self.init_game()

    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle = pygame.Rect(0, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball   = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)

        self.ball_vel = [1,-1]

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
            self.paddle.left -= MIN_PADDLE_STEP * PADDLE_SPEED
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += MIN_PADDLE_STEP * PADDLE_SPEED
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [1,-1]
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()

    def move_ball(self):
        # generally move ball from current position with default direction multiply with speed
        self.ball.left += SPEED * self.ball_vel[0]
        self.ball.top  += SPEED * self.ball_vel[1]

        # when ball move to the border of the screen, then reset x, y coordinate, and direction of movement
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
        # if ball hit any brick, change ball velocity and remove brick
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break
        # if no brick left, then win game
        if len(self.bricks) == 0:
            self.state = STATE_WON
        # if ball hit paddle, change y coordinate and velocity of ball
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        # if ball.top is below the paddle.top, then fail game once
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

    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))

    def get_intersection_point(self, ball, ball_vel):
        '''
        get the intersection point when the ball is going to hit screen border
        1. hit on the right border, with ball_vel[0] > 0
        2. hit on the left border, with ball_vel[0] < 0    
        3. move down, with ball_vel[1] > 0
        4. move up, with ball_vel[1] < 0
        '''
        # ball distance w.r.t the screen bottom
        top = SCREEN_SIZE[1] - ball.top 
        # ball distance w.r.t the right border 
        right = SCREEN_SIZE[0] - ball.left
        # we move right down
        if ball_vel[0] > 0 and ball_vel[1] > 0: 
            if right < top : # bouncing case when distance to right border is smaller than distance to bottom border
                bouncing_pose_y = top - right
                return SCREEN_SIZE[0] - bouncing_pose_y
            else:
                return ball.left + top
        # we move left down
        elif ball_vel[0] < 0 and ball_vel[1] > 0:
            if ball.left < top: # bouncing case when distance to left border less than distance to bottom border
                bouncing_pose_y = top - ball.left
                return bouncing_pose_y
            else:
                return ball.left - top
        else:
            return SCREEN_SIZE[0]//2


    def run(self):
        while 1:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit

            # distance_to_the_ball = abs(self.ball.left+BALL_RADIUS - (self.paddle.left + PADDLE_WIDTH /2) )
            # get the intersection point when the ball move down
            intersection_point = self.get_intersection_point(self.ball, self.ball_vel)
            # get the distance to the intersection_point, w.r.t paddle center_x, and ball center_x
            distance_to_the_intesection_point = abs(intersection_point + BALL_RADIUS - (self.paddle.left + PADDLE_WIDTH / 2))

            # APPLY FUZZY LOGIC TO MOVE THE PADDLE
            if self.state == STATE_PLAYING:
                
                # Calculate how much percent we are in low, medium and high w.r.t the distance to the intersection point
                x_level_lo = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_lo, distance_to_the_intesection_point)
                x_level_semi_lo = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_semi_lo, distance_to_the_intesection_point)
                x_level_md = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_md, distance_to_the_intesection_point)
                x_level_semi_hi = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_semi_hi, distance_to_the_intesection_point)
                x_level_hi = fuzz.interp_membership(self.x_distance_to_ball, self.dist_to_ball_hi, distance_to_the_intesection_point)
                
                rule1 = np.fmax(x_level_lo, x_level_semi_lo)
                rule2 = np.fmax(x_level_semi_hi, x_level_hi)
                # paddle movement is low or semi_lo
                # active_rule1 = np.fmax(self.paddle_movement_lo, self.paddle_movement_semi_lo)
                # paddle movement is high or semi_high
                # active_rule3 = np.fmax(self.paddle_movement_semi_high, self.paddle_movement_hi) 
                # activate rule 1 and rule 3
                activation_lo = np.fmin(self.paddle_movement_lo, rule1)
                activation_md = np.fmin(self.paddle_movement_md, x_level_md)
                activation_hi = np.fmin(self.paddle_movement_hi, rule2)
                # activation_lo = np.fmin(x_level_lo, active_rule1)
                # activation_hi = np.fmin(x_level_hi, active_rule3)
                # activate paddle movement medium

                # aggregate three rule functions
                aggregated = np.fmax(activation_lo, np.fmax(activation_md, activation_hi))

                # Calculate defuzzified result
                speed = fuzz.defuzz(self.paddle_movement, aggregated, 'centroid')
                PADDLE_SPEED = speed

                # --- UNCOMMENT TO VISULIZE RULES and how they fire -----

                # fig, ax0 = plt.subplots(figsize=(8, 3))
                # tip0 = np.zeros_like(self.paddle_movement)
                # ax0.fill_between(self.paddle_movement, tip0, activation_lo, facecolor='b', alpha=0.7)
                # ax0.plot(self.paddle_movement, active_rule1, 'b', linewidth=0.5, linestyle='--', )
                # ax0.fill_between(self.paddle_movement, tip0, activation_md, facecolor='g', alpha=0.7)
                # ax0.plot(self.paddle_movement, self.paddle_movement_md, 'g', linewidth=0.5, linestyle='--')
                # ax0.fill_between(self.paddle_movement, tip0, activation_hi, facecolor='r', alpha=0.7)
                # ax0.plot(self.paddle_movement, active_rule3, 'r', linewidth=0.5, linestyle='--')
                # ax0.plot([speed, speed], [0, 1], 'k', linewidth=1.5, alpha=0.9)
                # ax0.set_title('Output membership activity')

                # plt.tight_layout()
                # plt.show()

                if intersection_point + BALL_RADIUS - (self.paddle.left + PADDLE_WIDTH / 2) < 0:
                    self.paddle.left -= MIN_PADDLE_STEP * PADDLE_SPEED
                else:
                    self.paddle.left += MIN_PADDLE_STEP * PADDLE_SPEED


            self.clock.tick(100)
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
