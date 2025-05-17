#imports
import pygame
import tkinter
from pongObj import Ball, Player_Paddle

#pygame setup
#initialize the pygame library
pygame.init()

#window handling
#hardcoded size
size = width, height = 500, 300
#dynamcally set size to the size of the screen
root = tkinter.Tk()
size = root.winfo_screenwidth(), root.winfo_screenheight()
#print(size)
#sets window to specified size
screen = pygame.display.set_mode(size)
#sets the window title
pygame.display.set_caption("Pygame Pong")

#makes a clock object to control various time dependent game functions
clock = pygame.time.Clock() 
#game is running
running = True 

#game variables
#misc parameters
dt = 0 #delta time in seconds since last frame, used for framerate independent physics
speedup_time = 0 #time since last ball speedup
tick_rate = 120 #frames per second
screen_height = screen.get_height() #creating variable to prevent mutiple function calls
screen_width = screen.get_width() #creating variable to prevent mutiple function calls

#ball instantiation
ball = Ball(screen, 1) #value 1 initializes ball movement left, 0 intializes ball movement right

#--------------------
#can reduce codesize by doing calculation in parameter list
#---------------------
#rectangle instantiation
#initializes the left and right player positions
leftPlayerPos = pygame.Vector2(screen_width * 0.04, screen_height / 2)
rightPlayerPos = pygame.Vector2(screen_width - (screen_width * 0.04), screen_height / 2)
#initializes the left and right player objects
leftPlayer = Player_Paddle(screen, leftPlayerPos.x, leftPlayerPos.y)
rightPlayer = Player_Paddle(screen, rightPlayerPos.x, rightPlayerPos.y)

#GUI/UX
#centerline = pygame.Rect(screen_width / 2 - , 0, 1, screen_height) #centerline for the screen

#game loop
while running:
    #pygame.QUIT event means that the user closed the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #fill the screen with a color to wipe away anything from the last frame
    screen.fill("black")

    #draw the left and right player rectangles
    leftPlayer.display(screen)
    rightPlayer.display(screen)
    ball.display(screen)

    #move the ball
    ball.check_collision(screen, leftPlayer, rightPlayer)
    ball.move()

    # Can add move_down method to Player_Paddle class in order to not need to pass in negative dt
    #movement of player rectangles
    keys = pygame.key.get_pressed()
    #left player moves with W and S keys
    if keys[pygame.K_w]:
        leftPlayer.move((-dt), screen_height) #negate dt to induce upward movement
    if keys[pygame.K_s]:
        leftPlayer.move((dt), screen_height)
    #right player moves with UP and DOWN keys
    if keys[pygame.K_UP]:
        rightPlayer.move((-dt), screen_height)
    if keys[pygame.K_DOWN]:
        rightPlayer.move((dt), screen_height)

    #flip() the display to put work on screen
    pygame.display.flip()
    #limit to 60 frames per second
    clock.tick(tick_rate)

    #escape key quitting implementation
    if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
        running = False
    #update the dt variable to be the time since the last frame
    dt = clock.tick(tick_rate) / 1000
    #if the ball has been moving for 5 seconds, increase the speed of the ball,
    #max ball speed set at 20
    speedup_time += dt
    if ball.dx < screen_height * 0.015 and speedup_time >= 5:
        ball.set_speed(ball.dx * 1.1, ball.dy * 1.1)
        speedup_time = 0

#quit the game
pygame.quit()