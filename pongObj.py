import pygame
import math

#Ball class will hold all attrbutes for ball object
#attributes include position, speed, and radius
#methods include move, set_speed, get_position, and display
class Ball():
    #constructor for ball
    #attributes:
    #self - the instance of the ball object
    #int::x - the x position of the ball
    #int::y - the y position of the ball
    #int::dx - the change in x position
    #int::dy - the change in y position
    #int::radius - the radius of the ball
    #pygame.Rect::collision_area - the area of the ball for collision detection
    def __init__(self, screen:pygame.display, winner:bool):
        self.x = int(screen.get_width() / 2)
        self.y = int(screen.get_height() / 2)
        self.dx = int(screen.get_height() * .01)
        self.dy = 0
        self.radius = int(screen.get_height() / 50)
        self.collision_area = pygame.Rect(self.x - self.radius, self.y - self.radius, 2*self.radius, 2*self.radius)
        

    #purpose: move the ball by adding dx to x and dy to y
    #parameters:
    #self - the instance of the ball object
    def move(self):
        self.x += self.dx
        self.y += self.dy
        #update the collision area
        self.collision_area = pygame.Rect(self.x - self.radius, self.y - self.radius, 2*self.radius, 2*self.radius)

    #purpose: check to see if the ball has experienced a collision
    #parameters:
    #self - the instance of the ball object
    #left_paddle - the left paddle object
    #right_paddle - the right paddle object
    def check_collision(self, screen:pygame.display, left_paddle:"Player_Paddle", right_paddle:"Player_Paddle"):
        # Check collision with left paddle
        if self.collision_area.colliderect(left_paddle.collision_area):
            # Calculate hit position (distance from paddle center, normalized between -1 and 1)
            paddle_center = left_paddle.y + left_paddle.height / 2
            hit_pos = (self.y - paddle_center) / (left_paddle.height / 2)
            # Max bounce angle (in radians), e.g., 60 degrees
            max_bounce_angle = math.radians(60)
            bounce_angle = hit_pos * max_bounce_angle

            speed = math.hypot(self.dx, self.dy)  # Keep speed constant
            self.dx = abs(speed * math.cos(bounce_angle))  # Always to the right after left paddle
            self.dy = speed * math.sin(bounce_angle)

        # Check collision with right paddle
        elif self.collision_area.colliderect(right_paddle.collision_area):
            paddle_center = right_paddle.y + right_paddle.height / 2
            hit_pos = (self.y - paddle_center) / (right_paddle.height / 2)
            max_bounce_angle = math.radians(60)
            bounce_angle = hit_pos * max_bounce_angle

            speed = math.hypot(self.dx, self.dy)
            self.dx = -abs(speed * math.cos(bounce_angle))  # Always to the left after right paddle
            self.dy = speed * math.sin(bounce_angle)

        # Check collision with top and bottom walls
        if(self.y <= 0 or self.y >= screen.get_height()):
            self.dy = -self.dy
        # Checking for win conditions
        if(self.x <= 0):
            #left player wins
            self.x = int(screen.get_width() / 2)
            self.y = int(screen.get_height() / 2)
            self.dx = abs(int(screen.get_height() * .01))
            self.dy = 0
            return False
        if(self.x >= screen.get_width()):
            #right player wins
            self.x = int(screen.get_width() / 2)
            self.y = int(screen.get_height() / 2)
            self.dx = -abs(int(screen.get_height() * .01))
            self.dy = 0
            return True

            

    #parameters:
    #self - the instance of the ball object
    #int::dx - the change in x position
    #int::dy - the change in y position
    def set_speed(self, dx:int, dy:int):
        self.dx = dx
        self.dy = dy
    
    #purpose: return the current position of the ball
    #parameters:
    #self - the instance of the ball object
    def get_position(self):
        return (self.x, self.y)
    
    #purpose: display the ball on the screen using pygame
    #parameters:
    #self - the instance of the ball object
    #screen - the pygame screen object
    def display(self, screen:pygame.display):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.radius)
        pygame.draw.rect(screen, "red", self.collision_area, 1)

#Player_Paddle class will hold all attributes and methods for player paddle object
#attributes include position, width, height
#methods include move, display
class Player_Paddle():
    #constructor for player paddle
    #attributes:
    #self - the instance of the player paddle object
    #int::x - the x position of the paddle
    #int::y - the y position of the paddle
    #int::width - the width of the paddle
    #int::height - the height of the paddle
    #int::move_speed - the speed of the paddle movement
    def __init__(self, screen:pygame.display, x:int, y:int):
        #ensure incoming parameters are integers and set self values to incoming parameters
        self.x = int(x)
        self.y = int(y)
        self.width = screen.get_width() / 50
        self.height = screen.get_height() / 5
        self.move_speed = 0
        self.collision_area = pygame.Rect(self.x, self.y, self.width, self.height)

    #purpose: move the paddle by adding dt * move_speed to y
    #parameters:
    #self - the instance of the player paddle object
    #int::dt - time delta, amount of time since the last frame
    #int::screen_height - the height of the screen
    def move(self, dt:int, screen_height:int):
        # Makes move_speed dynamic based on screen height
        if self.move_speed == 0:
            self.move_speed = screen_height * 1.33
        
        self.y += dt * self.move_speed
        # Ensure the paddle stays within the screen bounds
        if self.y < 0:
            self.y = 0
        elif self.y > screen_height - self.height:
            self.y = screen_height - self.height
        
        #update the collision area
        self.collision_area = pygame.Rect(self.x, self.y, self.width, self.height)

    #purpose: display the paddle on the screen using pygame
    #parameters:
    #self - the instance of the player paddle object
    #screen - the pygame screen object
    def display(self, screen:pygame.display):
        pygame.draw.rect(screen, "white", (self.x, self.y, self.width, self.height))
        collsion_area = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, "red", collsion_area, 1)