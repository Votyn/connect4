# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 01:16:23 2017

@author: ImreF

Connect 4, aka Four in a Row

VERSION 2 (06/11/2017)

Changelog:
    - Added option to choose your counters at the start of the game.
    - Made the check_win functions also change the winning row into + symbols.
    - Added another error catch for player_input ( -1 < play < 7 )
    - maybe some other things?
    - Created changelog.

VERSION 3 (t<09/11/2017 AM)

Comments:
    A total 287 lines or so worth of pretty good code, if I say so myself. All 
    I really *need* to do at this point is create a fully functional graphical
    display function. OTher than that the basis of the game is, at this point,
    finished! (now it's just extra stuff like making a slightly harder bot and
    stuff.)

Changelog:
    - Created an easy bot for the player to play against.
    - Constructed a more wholesome "game()" function, that runs the game, with 
      some more introductory options.
    - Created a dud graphical display function
    - oh and I fixed the diagonal upwards check function misplacing one of the 
      +'s later on... 
      I'll be using the +'s to make the tokens larger in the graphical 
      showcase. They *are* useful!! :P
    - Removed some redundant checking statements and stuff. Most checking has 
      been based on playing it for a while now.
    - Also removed some redundant "empty lines", neating up my style a little
      and making it more consistent.

TODO:
    - Graphical display using pyplot.
    - What the hell is up with that mess of a thing for token changing?
        > make a seperate function for the gamemode choice, maybe? 
        > that or make token changing a better function? 
        > or not bother because there is little that can be made more efficient 
          with it...
    - Line 84?
    - Replace is and js with rows/columns
   
VERSION 4 (09/11/2017 PM)

Changelog:
    - lots. Created graphical display.
    - made rows/columns things more standard.
    - changed the token changing to make it so tokens can only be b, g, r, c, m, y, k, or w.
    
Didn't really finish the TODO list as yet but eh -shrug-
    
"""

import numpy as np
import matplotlib.pyplot as plt

"""------------------------ BASIC GAME BUILDING ------------------------"""

def create_board():
    """creates an empty 6*7 matrix filled with '-'."""
    columns = ['-', '-', '-', '-', '-', '-', '-']
    rows = [columns, columns, columns, columns, columns, columns]
    board = np.array(rows)
    return board

def display(board):
    """displays the game board in a simple ASCII format, with a seperator and a scale of columns."""
    print                      #V adding a ' ' to each '-' #V adding a '/n' to each '- - - - - - -'
    print '\n'.join(' '.join(column for column in row) for row in board) # making it readable
    print '-------------' # a seperator
    print "1 2 3 4 5 6 7" # a scale
    
    
def displaygraph(board, tokenp1, tokenp2):
    """Displays the game board in a graphical format, using pyplot."""
    plt.axes(facecolor='#4180cd')
    plt.xlim([0.5, 7.5])
    plt.ylim([0.5, 6.5])
    plt.xticks([1, 2, 3, 4, 5, 6, 7])
    plt.yticks([])
    column = 0
    while column < 7:
        row = 1
        while row < 7:
            if board[-row][column] == tokenp1:
                plt.plot((column + 1), row, color=tokenp1, marker='o', markersize=20)
            elif board[-row][column] == tokenp2:
                plt.plot((column + 1), row, color=tokenp2, marker='o', markersize=20)
            elif board[-row][column] == '1':
                plt.plot((column + 1), row, color=tokenp1, marker='o', markersize=25)
            elif board[-row][column] == '2':
                plt.plot((column + 1), row, color=tokenp2, marker='o', markersize=25)
            elif board[-row][column] == '-':
                plt.plot((column + 1), row, color='#d4dcea', marker='o', markersize=20)
            row = row + 1
        column = column + 1
    plt.show()
    

def place_token(column, token):
    """Automatically "drops" vertically the token into given column. """
    row = 1
    while row < 7:
        if board[-row][column] == '-': # negative so that it counts upwards rather than downwards.
            board[-row][column] = token
            break
        row = row + 1

def player_input(token, tokenp1, tokenp2):
    """Allows the player to pick which column they wanna drop their token into."""
    while True:
        play = raw_input("Player " + token + "'s turn. Please choose a column 1 through 7: ")
        if play == 'exit':
            print 'The game has ended at the behest of player ' + token
            return False # "Game continue?"
            break
        else:
            try:
                play = int(play) - 1
            except ValueError:
                print
                print 'Please enter a number.'
                continue
            else:
                if -1 < play < 7:  
                    place_token(play, token) # place the piece
                    displaygraph(board, tokenp1, tokenp2) # show the updated gameboard
                    return True # "Game continue?"
                    break
                else:
                    print 'Please choose a number between 1 and 7 (inclusive)'
                    continue
            
"""------------------------ GAMEPLAY FUNCTIONS ------------------------"""

def player_v_player(tokenp1, tokenp2):
    """Carries out the game for 2 human players"""
    while True:
        if player_input(tokenp1, tokenp1, tokenp2) == False: # "Game continue?"
            break
        elif check_for(tokenp1, 1) == True:
            displaygraph(board, tokenp1, tokenp2)
            break
        elif player_input(tokenp2, tokenp1, tokenp2) == False: # "Game continue?"
            break
        elif check_for(tokenp2, 2) == True:
            displaygraph(board, tokenp1, tokenp2)
            break  
        
def player_v_rancomp(tokenp1, tokenp2):
    """Carries out the game for one human player and a randomly placing computer player."""
    while True:
        if player_input(tokenp1, tokenp1, tokenp2) == False: # "Game continue?"
            break
        elif check_for(tokenp1, 1) == True:
            displaygraph(board, tokenp1, tokenp2)
            break
        print
        print("Bot Player " + tokenp2 + "'s turn.")
        place_token(np.random.randint(0, 7), tokenp2)
        displaygraph(board, tokenp1, tokenp2)
        if check_for(tokenp2, 2) == True:
            displaygraph(board, tokenp1, tokenp2)
            break 

def custom_token(): # defecit function, for now...
    """Allows the player(s) to choose the tokens."""
    while True:
        tokenp1 = raw_input("Please choose a token for the first player: ")
        if tokenp1 == 'exit':
            print 'The game has ended at the behest of player 1'
            return False # "Game continue?"
            break
        elif len(tokenp1) > 1:
            print("Please make your token only one character long.")
            continue
        else:
            break
    while True:
        tokenp2 = raw_input("Please choose a token for the second player: ")
        if tokenp2 == 'exit':
            print 'The game has ended at the behest of player 1'
            return False # "Game continue?"
            break
        elif tokenp2 == tokenp1:
            print("Don't make them the same!")
            continue
        elif len(tokenp2) > 1:
            print("Please make your token only one character long.")
            continue
        else:
            break

"""------------------------ FOUR IN A ROW CHECK ------------------------"""
def vcheck_for(token, player):
    """Performs a vertical check for four in a row"""
    win = np.array([token, token, token, token])
    column = 0
    while column < 7:
        row = 0
        while row < 3:
            check = board[row:(row+4), column]
            if (win == check).all():
                print
                print token + ' has won vertically! Below is the finished board with the winning line emboldened'
                if player == 1:    
                    board[row:(row+4), column] = np.array(['1', '1', '1', '1'])
                elif player == 2:
                    board[row:(row+4), column] = np.array(['2', '2', '2', '2'])
                return True
                break
            else:
                row = row + 1
        if (win == check).all():
            break
        else:
            column = column + 1

def hcheck_for(token, player):
    """Performs a horizontal check for four in a row"""
    win = np.array([token, token, token, token])
    column = 0
    while column < 4:
        row = 1
        while row < 7:
            check = board[-row, column:(column+4)]
            if (win == check).all():
                print str(column) + 'col + row' + str(row)
                print token + ' has won horizontally! Below is the finished board with the winning line emboldened.'
                if player == 1:
                    board[-row, column:(column+4)] = np.array(['1', '1', '1', '1'])
                elif player == 2:
                    board[-row, column:(column+4)] = np.array(['2', '2', '2', '2'])
                return True
                break
            else:
                row = row + 1
        if (win == check).all():
            break
        else:
            column = column + 1

def ddcheck_for(token, player):
    """Performs a diagonal downwards check for four in a row"""
    j = 0
    while j < 4:
        i = 0
        while i < 3:
            if board[i][j] == token:
                if board[i][j] == board[i+1][j+1]:
                    if board[i][j] == board[i+2][j+2]:
                        if board[i][j] == board[i+3][j+3]:
                            print
                            print token + ' has won diagonally downwards! Below is the finished board with the winning line emboldened'
                            board[i][j] = str(player)
                            board[i+1][j+1] = str(player)
                            board[i+2][j+2] = str(player)
                            board[i+3][j+3] = str(player)
                            return True
                            break
            i+=1
        j+=1

def ducheck_for(token, player):
    """Performs a diagonal upwards check for four in a row"""
    j = 0
    while j < 4:
        i = 1
        while i < 4:
            if board[-i][j] == token:
                if board[-i][j] == board[-(i+1)][j+1]:
                    if board[-i][j] == board[-(i+2)][j+2]:
                        if board[-i][j] == board[-(i+3)][j+3]:
                            print
                            print token + ' has won diagonally upwards! Below is the finished board with the winning line emboldened'
                            board[-i][j] = str(player)
                            board[-(i+1)][j+1] = str(player)
                            board[-(i+2)][j+2] = str(player)
                            board[-(i+3)][j+3] = str(player)
                            print
                            return True
                            break
            i+=1
        j+=1
        
def check_for(token, player):
    if vcheck_for(token, player) or hcheck_for(token, player) or ddcheck_for(token, player) or ducheck_for(token, player):
        return True
    
"""------------------------ FUNCTIONS OVER IT IS GAMETIME NOW ------------------------"""
board = create_board() # all functions depend on there being a board "board"

def game():
    print
    print "This is Connect 4, written by Imre Oks."
    print
    displaygraph(board, 'X', 'O')
    print
    print "The board is laid out as above."
    print
    print "The default tokens are red and yellow. To change this type 'TOK' below."
    print
    print "Which gamemode would you like to play in?"
    print "    'PVP' = a human player vs another human player."
    print "    'RAN' = a human player vs an easy bot."
    print
    print "To exit at any point type 'exit'"
    while True:
        tokenp1 = 'R'
        tokenp2 = 'Y'
        inp = raw_input("    Please type your choice here.")
        if inp.lower() == "exit":
            break
        elif inp.upper() == "TOK": # TOKEN CHANGE START
            print "Your tokens must be the first letter of some colour, that is not the same for both, otherwise it will default to red and yellow."
            print "The choice is as follows; b, g, r, c, m, y, k, or w"
            while True:
                print
                tokenp1 = raw_input("Please choose a token for the first player: ")
                if tokenp1.lower() == 'exit':
                    print 'The game has ended at the behest of player 1'
                    break
                elif len(tokenp1) > 1:
                    print("Please make your token only one character long.")
                    continue
                elif tokenp1 not in ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']:
                    print 'your token can only be b, g, r, c, m, y, k, or w'
                    continue
                else:
                    break
            if tokenp1.lower() == 'exit':
                break
            while True:
                tokenp2 = raw_input("Please choose a token for the second player: ")
                if tokenp2.lower() == 'exit':
                    print 'The game has ended at the behest of player 2'
                    break
                elif tokenp2 == tokenp1:
                    print("Don't make them the same!")
                    continue
                elif len(tokenp2) > 1:
                    print("Please make your token only one character long.")
                    continue
                elif tokenp2 not in ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']:
                    print 'your token can only be b, g, r, c, m, y, k, or w'
                    continue
                else:
                    break # TOKEN CHANGE END
            if tokenp2.lower() == 'exit':
                    break
            print
            print "The new tokens are " + tokenp1 + " and " + tokenp2 +"."
            print
            print "Would you like to do a PVP match or a RAN match?"
            while True:
                inp = raw_input("    Please type your choice here.")
                if inp.lower() == "exit":
                    break
                elif inp.upper() == "PVP": # converting input into upper case to make it always work
                    player_v_player(tokenp1, tokenp2)
                elif inp.upper() == "RAN":
                    player_v_rancomp(tokenp1, tokenp2)
                else:
                    print "Please choose a valid option."
                    continue
                break
            break
        elif inp.upper() == "PVP":
            player_v_player(tokenp1, tokenp2)
        elif inp.upper() == "RAN":
            player_v_rancomp(tokenp1, tokenp2)
        else:
            print "Please choose a valid option."
            continue
        break

game()