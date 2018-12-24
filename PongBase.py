import random
import pygame
import sys

class PongMechanics:
    pygame.init()

    def __init__(self):
        self.WHITE = (255, 255, 255); # white colour
        self.BLACK = (0, 0, 0); # black colour
        self.clock = pygame.time.Clock(); # game clock for framerate
        self.FONT = pygame.font.SysFont("monospace", 32) # font

        self.size = width, height = 600, 400
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")

        self.main()

    # main runner function
    def main(self):
        # used to track the players' scores
        self.P1Score = 0
        self.P2Score = 0

        width, height = pygame.display.get_surface().get_size()
        # used to track the players' coordinates
        self.y1 = height / 2
        self.y2 = height / 2

        # used to keep track of the ball's coordinates
        self.bX = (width / 2) - 5
        self.bY = (height / 2) - 5
        # used to check if the ball is moving
        self.bM = False

        # sets the direction to 0, 0
        self.currentDirection = (0, 0)

        # game loop
        self.run = True
        while self.run == True:
            self.checkKey()

            self.drawStage()

            self.handleExit()

            self.clock.tick(60)
            pygame.display.flip()

    # draws the stage elements
    def drawStage(self):
        width, height = pygame.display.get_surface().get_size()

        # 'wipes' the screen
        self.screen.fill(self.BLACK)

        # draws the paddles
        self.paddle1UpperC = (40, self.y1 - 15)
        self.paddle1LowerC = (40, self.y1 + 15)
        self.paddle2UpperC = (560, self.y2 - 15)
        self.paddle2LowerC = (560, self.y2 + 15);
        pygame.draw.line(self.screen, self.WHITE, self.paddle1UpperC, self.paddle1LowerC, 5)
        pygame.draw.line(self.screen, self.WHITE, self.paddle2UpperC, self.paddle2LowerC, 5)

        # draws the ball
        self.ballVector()
        direction = self.currentDirection
        tX, tY = direction
        self.bX += tX
        self.bY += tY
        self.ball = pygame.draw.rect(self.screen, self.WHITE, (self.bX, self.bY, 10, 10))

        # draws the centre line
        lineStart = (width / 2, 0)
        lineEnd = (width / 2, height)
        pygame.draw.line(self.screen, self.WHITE, lineStart, lineEnd, 1)

        # draws the scores
        self.updateScore()
        ScoreP1 = self.FONT.render(str(self.P1Score), True, self.WHITE)
        ScoreP2 = self.FONT.render(str(self.P2Score), True, self.WHITE)
        self.screen.blit(ScoreP1, ((width * .25) - ScoreP1.get_width() / 2, (height * .1) - ScoreP1.get_height() / 2))
        self.screen.blit(ScoreP2, ((width * .75) - ScoreP2.get_width() / 2, (height * .1) - ScoreP2.get_height() / 2))

    # should update when a player scores
    def updateScore(self):
        width = pygame.display.get_surface().get_width()
        if self.bX < 35:
            self.P2Score += 1
            self.bX = width / 2
            self.bM = False
        if self.bX > 560:
            self.P1Score += 1
            self.bX = width / 2
            self.bM = False

    # decides the direction for the ball
    def ballVector(self):
        width, height = pygame.display.get_surface().get_size()
        paddle1LowerCW, paddle1LowerCH = self.paddle1LowerC
        paddle1UpperCW, paddle1UpperCH = self.paddle1UpperC
        paddle2LowerCW, paddle2LowerCH = self.paddle2LowerC
        paddle2UpperCW, paddle2UpperCH = self.paddle2UpperC

        directions = [(-2, -2), (-2, 2), (2, 2), (2, -2)]
        # if the ball isn't moving give it a random direction
        if self.bM == False and pygame.time.get_ticks() > 1800:
            startDirection = random.randint(0, 3)
            self.currentDirection = directions[startDirection]
            self.bM = True

        # top or bottom collisions
        if self.bY <= 2: # ifs for top collisions
            if self.currentDirection == directions[0]: # top and left
                self.currentDirection = directions[1]
            if self.currentDirection == directions[3]: # top and right
                self.currentDirection = directions[2]
        if self.bY >= 398: # ifs for the bottom collisions
            if self.currentDirection == directions[1]: # bottom and right
                self.currentDirection = directions[0]
            if self.currentDirection == directions[2]: # bottom and left
                self.currentDirection = directions[3]

        # ifs for player1's collisions with the ball (left player)
        if self.bX <= 40 and self.bX >= 35 and self.bY <= paddle1LowerCH + 5 and self.bY >= paddle1UpperCH - 5:
            if self.currentDirection == directions[0]: # left and up
                self.currentDirection = directions[3]
            if self.currentDirection == directions[1]: # left and down
                self.currentDirection = directions[2]

        # ifs for player2's collisions with the ball (right player)
        if self.bX >= 550 and self.bX <= 560 and self.bY <= paddle2LowerCH + 5 and self.bY >= paddle2UpperCH - 5:
            if self.currentDirection == directions[3]: # right and up
                self.currentDirection = directions[0]
            if self.currentDirection == directions[2]: # right and down
                self.currentDirection = directions[1]

    # checks to see if keys are pressed
    def checkKey(self):
        keys = pygame.key.get_pressed()
        # Player 1's Controls
        if keys[pygame.K_UP] and self.y1 > 15: # UP
            self.y1 -= 5
        if keys[pygame.K_DOWN] and self.y1 < 385: # DOWN
            self.y1 += 5
        # Player 2's Controls
        if keys[pygame.K_w] and self.y2 > 15: # UP
            self.y2 -= 5
        if keys[pygame.K_s] and self.y2 < 385: # DOWN
            self.y2 += 5

    # closes the game if the user is done playing
    def handleExit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 self.run = False

PongGame = PongMechanics()