from PongMechanics import PongMechanics

class PongGameR:
    PG = PongMechanics()

    # Functionallity
    # This class imports the class PongMechanics which contails the base methods and variables to use here. The available
    # functions and variables are as follows:
    # All colours must be in the form (r, g, b)
    #   Functions
    #   .changeBackgroundColour()   :   changes the background to a specified colour
    #   .changeBallColour()         :   changes the colour of the ball to a specified colour
    #   .changePaddleColour()       :   changes the colour of a specific paddle
    #   .changeCentreLineColour()   :   changes the colour of the centre line
    #   .changeScoreColour()        :   changes the colour of a specified score (either "P1" or "P2")
    #   .getScore()                 :   returns the score of a specified player (either "P1 or "P2")
    #   .start()                    :   runs the required code to run the program
    #   .drawPaddles()              :   draws the players' paddles on screen
    #   .drawCentreLine()           :   draws the centre line on screen
    #   .drawScore()                :   draws the scores on the screen
    #   .drawBall()                 :   draws the ball on screen
    #   .drawStage()                :   must run at the end of the game loop everytime, contains important info
    #   .checkP1Up, .checkP1Down    :   checks to see if player 1 is pressing the up or down arrow keys
    #   .checkP2Up, .checkP2Down    :   checks to see if player 2 is pressing the w or s keys (up or down)
    #   .ballIsOutOfBOunds()        :   returns "P1" or "P2" depending on who missed the ball (i.e "P1" if player 1 missed)
    #   .updateScore()              :   adds a specified number of points to the specified player's score
    #   .refreshScreen()            :   removes everything on the screen and replaces it with .backgroundColour
    #   .drawText()                 :   draws text on screen at specific coordinates in a specific colour
    #   .setBV                      :   changes the ball's velocity
    #
    #   Variables
    #   .run                        :   a boolean value that determines if the program will run or not

    # conditions
    PG.changeBackgroundColour((55, 55, 135)) # optional to change background colour
    PG.changeBallColour((200, 40, 45)) # optional to change the ball's colour
    PG.changePaddleColour((230, 254, 50), "P1") # optional to change a paddle's colour (can be done individually)
    PG.changeCentreLineColour((25, 255, 50)) # optional to change the centre line's colour
    PG.changeScoreColour((255, 40, 170), "P1") # optional to change the colour of the scores (can be done individually)

    # game loop

    # inside this loop the user can do many things such as: changing colours based on conditions, putting text on screen
    # based on conditions, create a working pong simulator

    PG.start()
    PG.setBallVelocity(2)
    counter = 0 # additional variables to hold the colour change
    add = 1

    while PG.run == True:
        PG.refreshScreen()

        PG.drawPaddles()
        PG.drawCentreLine()
        PG.drawScore()
        PG.drawBall()

        if PG.checkP1Up() == True:
            PG.moveP1Up()
        if PG.checkP1Down() == True:
            PG.moveP1Down()
        if PG.checkP2Up() == True:
            PG.moveP2Up()
        if PG.checkP2Down() == True:
            PG.moveP2Down()

        if (PG.ballIsOutOfBounds() == "P1"):
            PG.updateScore("P1", 1)
        elif (PG.ballIsOutOfBounds() == "P2"):
            PG.updateScore("P1", 1)

        counter += add
        if counter >= 255 or counter <= 0:
            add *= -1

        PG.changeBallColour((255, counter, 50))
        PG.changeBackgroundColour((125, 50, counter))

        PG.drawStage()
