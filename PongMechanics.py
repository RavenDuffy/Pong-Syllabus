import random
import pygame
import time
import sys

class PongMechanics:
    pygame.init()

    def __init__(self):
        # default colours to use
        self.WHITE = (255, 255, 255); # white colour
        self.BLACK = (0, 0, 0); # black colour

        # customised colours
        self.backgroundColour = self.BLACK # sets the colour of the background to black
        self.ballColour = self.WHITE # sets the colour of the ball to white
        self.paddle1Colour = self.WHITE # sets player one's paddle to white
        self.paddle2Colour = self.WHITE # sets player two's paddle to white
        self.centreLineColour = self.WHITE # sets the centre line to white
        self.P1ScoreColour = self.WHITE # sets player one's score colour to white
        self.P2ScoreColour = self.WHITE # sets player two's score colour to white

        self.clock = pygame.time.Clock(); # game clock for framerate
        self.FONT = pygame.font.SysFont("monospace", 32) # font

        self.size = width, height = 600, 400
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")

        self.run = True

    # main runner function should only be run once
    # MUST BE RUN BEFORE OTHER FUNCTIONS
    def start(self):
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
        # used to act as a multiplier for the ball's speed
        self.bV = 1

        # sets the direction to 0, 0
        self.currentDirection = (0, 0)

    # draws the stage elements
    def drawStage(self):
        self.clock.tick(60)
        pygame.display.flip()

        self.handleExit()

    # changes the background colour
    def changeBackgroundColour(self, colour = (0, 0, 0)):
        if colour != self.BLACK:
            self.backgroundColour = colour

    # changes the centre line colour
    def changeCentreLineColour(self, colour = (255, 255, 255)):
        if colour != self.WHITE:
            self.centreLineColour = colour

    # changes the ball's colour
    def changeBallColour(self, colour = (255, 255, 255)):
        if colour != self.WHITE:
            self.ballColour = colour

    # changes a player's paddle colour
    def changePaddleColour(self, colour = (255, 255, 255), player = None):
        if colour != self.WHITE:
            if player == None:
                self.paddle1Colour = colour
                self.paddle2Colour = colour
            else:
                if player.upper() == "P1":
                    self.paddle1Colour = colour
                elif player.upper() == "P2":
                    self.paddle2Colour = colour
                else:
                    raise ValueError("Invalid Player")

    # changes a player's score's colour
    def changeScoreColour(self, colour = (255, 255, 255), player = None):
        if player == None:
            self.P1ScoreColour = colour
            self.P2ScoreColour = colour
        else:
            if player.upper() == "P1":
                self.P1ScoreColour = colour
            elif player.upper() == "P2":
                self.P2ScoreColour = colour
            else:
                raise ValueError("Invalid Player")

    # wipes the screen
    def refreshScreen(self):
        self.screen.fill(self.backgroundColour)

    # draws the ball
    def drawBall(self):
        self.ballVector()
        direction = self.currentDirection
        tX, tY = direction
        self.bX += (tX * self.bV)
        self.bY += (tY * self.bV)
        self.ball = pygame.draw.rect(self.screen, self.ballColour, (self.bX, self.bY, 10, 10))

    # draws the paddles
    def drawPaddles(self):
        self.paddle1UpperC = (40, self.y1 - 15)
        self.paddle1LowerC = (40, self.y1 + 15)
        self.paddle2UpperC = (560, self.y2 - 15)
        self.paddle2LowerC = (560, self.y2 + 15)
        pygame.draw.line(self.screen, self.paddle1Colour, self.paddle1UpperC, self.paddle1LowerC, 5)
        pygame.draw.line(self.screen, self.paddle2Colour, self.paddle2UpperC, self.paddle2LowerC, 5)

    # draws the centre line
    def drawCentreLine(self):
        width, height = pygame.display.get_surface().get_size()
        lineStart = (width / 2, 0)
        lineEnd = (width / 2, height)
        pygame.draw.line(self.screen, self.centreLineColour, lineStart, lineEnd, 1)

    # draws the scores
    def drawScore(self):
        width, height = pygame.display.get_surface().get_size()
        ScoreP1 = self.FONT.render(str(self.P1Score), True, self.P1ScoreColour)
        ScoreP2 = self.FONT.render(str(self.P2Score), True, self.P2ScoreColour)
        self.screen.blit(ScoreP1, ((width * .25) - ScoreP1.get_width() / 2, (height * .1) - ScoreP1.get_height() / 2))
        self.screen.blit(ScoreP2, ((width * .75) - ScoreP2.get_width() / 2, (height * .1) - ScoreP2.get_height() / 2))

    # draws text on screen
    def drawText(self, text, colour = (255, 255, 255), xpos = -1, ypos = -1):
        width, height = pygame.display.get_surface().get_size()

        if xpos == -1 and ypos == -1:
            textD = self.FONT.render(str(text), True, colour)
            self.screen.blit(textD, ((width * .5) - textD.get_width() / 2, (height * .5) - textD.get_height() / 2))
        elif xpos != -1 and ypos == -1:
            textD = self.FONT.render(str(text), True, colour)
            self.screen.blit(textD, (xpos - textD.get_width() / 2, (height * .5) - textD.get_height() / 2))
        elif xpos == -1 and ypos != -1:
            textD = self.FONT.render(str(text), True, colour)
            self.screen.blit(textD, ((width * .5) - textD.get_width() / 2, ypos - textD.get_height() / 2))
        else:
            textD = self.FONT.render(str(text), True, colour)
            self.screen.blit(textD, (xpos - textD.get_width() / 2, ypos - textD.get_height() / 2))

    # checks to see if the ball is out of bounds, returns 'P1 or P2'
    def ballIsOutOfBounds(self):
        if self.bX < 25:
            return "P2"
        elif self.bX > 570:
            return "P1"
        else:
            return ""

    # should update when a player scores
    def updateScore(self, player, points):
        if player == "P1":
            self.P1Score += points
            self.resetBall()
        if player == "P2":
            self.P2Score += points
            self.resetBall()

    # returns the score of the specified player, throws exception if no player is selected
    def getScore(self, player = None):
        if player == None:
            raise ValueError("No player selected")
        elif player.upper() == "P1":
            return self.P1Score
        elif player.upper() == "P2":
            return self.P2Score


    # sends the ball back to the centre
    def resetBall(self):
        width = pygame.display.get_surface().get_width()
        self.bX = width / 2
        self.bM = False

    def setBallVelocity(self, velocity):
        self.bV = velocity

    # decides the direction for the ball
    def ballVector(self):
        width, height = pygame.display.get_surface().get_size()
        paddle1LowerCW, paddle1LowerCH = self.paddle1LowerC
        paddle1UpperCW, paddle1UpperCH = self.paddle1UpperC
        paddle2LowerCW, paddle2LowerCH = self.paddle2LowerC
        paddle2UpperCW, paddle2UpperCH = self.paddle2UpperC

        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        # if the ball isn't moving give it a random direction
        if self.bM == False and pygame.time.get_ticks() > 1800:
            startDirection = random.randint(0, 3)
            self.currentDirection = directions[startDirection]
            self.bM = True

        # ball's top or bottom collisions
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

    # checks to see if the Up arrow is pressed
    def checkP1Up(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            return True
        return False

    # checks to see if the Down arrow is pressed
    def checkP1Down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            return True
        return False

    # checks to see if the W key is pressed
    def checkP2Up(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return True
        return False

    # checks to see if the S key is pressed
    def checkP2Down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            return True
        return False

    # moves Player 1 up
    def moveP1Up(self):
        if self.y1 > 15:
            self.y1 -= 5

    # moves Player 1 down
    def moveP1Down(self):
        if self.y1 < 385:
            self.y1 += 5

    # moves Player 2 up
    def moveP2Up(self):
        if self.y2 > 15:
            self.y2 -= 5

    # moves Player 2 down
    def moveP2Down(self):
        if self.y2 < 385:
            self.y2 += 5

    # closes the game if the user is done playing
    def handleExit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 self.run = False