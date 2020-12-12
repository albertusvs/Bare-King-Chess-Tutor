# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import chess, chess.pgn, chess.svg
from flask import Flask,render_template, request, Markup, redirect
import random

app = Flask(__name__)

app.secret_key = 'secret'

# Initial specified pieces locations
position1 = ''
position2 = ''
position3 = ''
# Initial position for the Kings
positionking = ''
positionoppking = ''
# AI Type 1= Random 2 = Avoid Corners 3 = Avoid Check
AItype = 1

gameboard = chess.Board(None) 

# Load specified pieces location into variables
def loadposition(position):
    global position1
    global position2
    global position3
    if not position1 :
        position1 = position
    else :
        if not position2 : 
            position2 = position
        else :
            if not position3 :
                position3 = position

# Error checking all initial positions                
def checkpositions():
    global position1
    global position2
    global position3
    global positionking
    global positionoppking
    error = ''
    
    # Checks if more than two pieces are specified for the same square
    if position1 == position2 and position1 or position1 == position3 and position1 or position2 == position3 and position2 or positionking == position1 and positionking or positionking == position2 and positionking or positionking == position3 and positionking or positionoppking == position1 and positionoppking or positionoppking == position2 and positionoppking or positionoppking == position3 and positionoppking  or positionking == positionoppking  and positionoppking  :
        error += 'Pieces cannot be in the same square <br>'

        
    if not positionking or not positionoppking :
        error += 'The two Kings must be specified <br>'
        
    if not position1 : 
        error += 'At least one extra other piece needs to be specified <br>'
    
    # Check that the first specified piece is not next to the Opposition King
    if position1 and positionoppking : 
        if ord(position1[0]) - 1 == ord(positionoppking[0]) or ord(position1[0]) + 1 == ord(positionoppking[0]) :
            if ord(position1[1]) - 1 == ord(positionoppking[1]) or ord(position1[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(position1[0]) == ord(positionoppking[0]) :
            if ord(position1[1]) - 1 == ord(positionoppking[1]) or ord(position1[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(position1[1]) == ord(positionoppking[1]) :
            if ord(position1[0]) == ord(positionoppking[0]) - 1 or ord(position1[0]) == ord(positionoppking[1]) + 1 :
                error += 'No pieces must be next to the Opposing King'
                
    # Check that the second specified piece is not next to the Opposition King
    if position2 and positionoppking : 
        if ord(position2[0]) - 1 == ord(positionoppking[0]) or ord(position2[0]) + 1 == ord(positionoppking[0]) :
            if ord(position2[1]) - 1 == ord(positionoppking[1]) or ord(position2[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(position2[0]) == ord(positionoppking[0]) :
            if ord(position2[1]) - 1 == ord(positionoppking[1]) or ord(position2[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(position2[1]) == ord(positionoppking[1]) :
            if ord(position2[0]) == ord(positionoppking[0]) - 1 or ord(position2[0]) == ord(positionoppking[1]) + 1 :
                error += 'No pieces must be next to the Opposing King'

    # Check that the third specified piece is not next to the Opposition King    
    if position3 and positionoppking : 
        if ord(position3[0]) - 1 == ord(positionoppking[0]) or ord(position3[0]) + 1 == ord(positionoppking[0]) :
            if ord(position3[1]) - 1 == ord(positionoppking[1]) or ord(position3[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(position3[0]) == ord(positionoppking[0]) :
            if ord(position3[1]) - 1 == ord(positionoppking[1]) or ord(position3[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(position3[1]) == ord(positionoppking[1]) :
            if ord(position3[0]) == ord(positionoppking[0]) - 1 or ord(position3[0]) == ord(positionoppking[1]) + 1 :
                error += 'No pieces must be next to the Opposing King'

    # Check that the Player King not next to the Opposition King    
    if positionking and positionoppking : 
        if ord(positionking[0]) - 1 == ord(positionoppking[0]) or ord(positionking[0]) + 1 == ord(positionoppking[0]) :
            if ord(position1[1]) - 1 == ord(positionoppking[1]) or ord(positionking[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(positionking[0]) == ord(positionoppking[0]) :
            if ord(positionking[1]) - 1 == ord(positionoppking[1]) or ord(positionking[1]) + 1 == ord(positionoppking[1]) :
                error += 'No pieces must be next to the Opposing King'
        if ord(positionking[1]) == ord(positionoppking[1]) :
            if ord(positionking[0]) == ord(positionoppking[0]) - 1 or ord(positionking[0]) == ord(positionoppking[1]) + 1 :
                error += 'No pieces must be next to the Opposing King'
                                                        
    
    # Resets all the position to zero if there is an error
    if error :
        position1 = ''
        position2 = ''
        position3 = ''
        positionking = ''
        positionoppking = ''
        
    
    return error  

# Initial PAge Render
@app.route('/')
def setup():
    # Clear Everything when Page Reloaded
    global position1
    global position2
    global position3
    global positionking
    global positionoppking
    position1 = ''
    position2 = ''
    position3 = ''
    positionking = ''
    positionoppking = ''
    global gameboard
    gameboard.clear_board()
    gameboard = chess.Board(None)
        
    return render_template('chess.html', board = Markup(chess.svg.board(gameboard, size = 350)))

# POST/GET for Initial Page
# Loads Positions from HTML into Python and Error Checks
# If ERROR: Clears html fields and renders Intial Page with Error Messages
# If CORRECT: Redirects to Playing Page
@app.route('/', methods=['POST', 'GET'])
def setup_submit():
    global position1
    global postiion2
    global position3
    global positionking
    global positionoppking
    global gameboard
    global AItype
    
    #Loads positions into variables
    positionking = request.form['kingposition']
    positionoppking = request.form['oppkingpostion']
    if request.form.get('rook1') :
        loadposition(request.form['rook1position'])
    if request.form.get('rook2') :
        loadposition(request.form['rook2position'])
    if request.form.get('bishopwhite') :
        loadposition(request.form['bishopwhitepostion'])
    if request.form.get('bishopblack') :
        loadposition(request.form['bishopblackposition'])
    if request.form.get('horse1') :
        loadposition(request.form['horse1position'])
    if request.form.get('horse2') :
        loadposition(request.form['horse2position'])
    if request.form.get('queen') :
        loadposition(request.form['queenposition'])
    
   #Check positions for errors     
    error = checkpositions()
    
    #If ERROR: Renders the Initial Page, with fields blank en error messages
    # ELSE: Setup the intial board
    if error : 
        return render_template('chess.html', errors = error, board = Markup(chess.svg.board(gameboard, size = 350)))
    else :
        
        # Load Kings Positions on Chess.Board
        gameboard.set_piece_at(chess.parse_square(positionking), chess.Piece(chess.KING, chess.WHITE))
        gameboard.set_piece_at(chess.parse_square(positionoppking), chess.Piece(chess.KING, chess.BLACK))
                               
        # Load Individualy Specified Pieces on Chess.Board
        if request.form.get('rook1') :
            gameboard.set_piece_at(chess.parse_square(request.form['rook1position']), chess.Piece(chess.ROOK, chess.WHITE))
        if request.form.get('rook2') :
            gameboard.set_piece_at(chess.parse_square(request.form['rook2position']), chess.Piece(chess.ROOK, chess.WHITE))
        if request.form.get('bishopwhite') :
            gameboard.set_piece_at(chess.parse_square(request.form['bishopwhitepostion']), chess.Piece(chess.BISHOP, chess.WHITE))
        if request.form.get('bishopblack') :
            gameboard.set_piece_at(chess.parse_square(request.form['bishopblackposition']), chess.Piece(chess.BISHOP, chess.WHITE))
        if request.form.get('horse1') :
            gameboard.set_piece_at(chess.parse_square(request.form['horse1position']), chess.Piece(chess.KNIGHT, chess.WHITE))
        if request.form.get('horse2') :
            gameboard.set_piece_at(chess.parse_square(request.form['horse2position']), chess.Piece(chess.KNIGHT, chess.WHITE))
        if request.form.get('queen') :
            gameboard.set_piece_at(chess.parse_square(request.form['queenposition']), chess.Piece(chess.QUEEN, chess.WHITE))
        
        #legacy
        AItype = 3
        
        #Check to make sure that the Opposite Black King does not start in Check
        if gameboard.is_attacked_by(chess.WHITE, chess.parse_square(positionoppking)):
            error += 'The initial setup cannot place the Opposing Black King already in Check'
        
        #Temporarily moves the turn to the opposing Black side and performs Checkmate and Stalemate checking
        gameboard.push(chess.Move.null())
        if gameboard.is_checkmate():
            error += ' The initial setup cannot place the Opposing Black King already in Checkmate'
        
        if gameboard.is_stalemate():
            error += ' The initial setup cannot place the Opposing Black King already in Stalemate'
        
        gameboard.pop()
        
        #Checks if there are insufficient material to win
        if gameboard.is_insufficient_material() :
            error += 'This combination of pieces will always draw against a Opposing King. Select a set of pieces that can win. <br>'
            
        if error :
            gameboard.clear()
            return render_template('chess.html', errors = error, board = Markup(chess.svg.board(gameboard, size = 350)))
        else :
            return redirect('/game')

@app.route('/game')
def game():
    global gameboard
    #If board empty redirect to / to setup board  
    if gameboard.board_fen() == '8/8/8/8/8/8/8/8' :
        return redirect('/') 
    #Else render game playing page
    else :
        return render_template('game.html', board = Markup(chess.svg.board(gameboard, size = 350)))

@app.route('/game', methods=['POST', 'GET'])
def game_move():
    global gameboard
    global AItype
    
    if request.form.get("resetbutton"):
        gameboard.clear()
        return redirect('/')
    
    if request.form['nextmove'] == '':
        return redirect('/game')
    
    if gameboard.board_fen() == '8/8/8/8/8/8/8/8' :
        return redirect('/')
    
    if request.form.get("submitbutton"):
        error = ''
        random.seed()
        
        nextmovetext = request.form['nextmove']
        
        nextmove = '' 
        try:
            nextmove = chess.Move.from_uci(nextmovetext)
        except:
            error += 'Invalid Move <br>'
        
        if nextmove not in gameboard.legal_moves:
            error += 'Invalid Move <br>'
        
        
        #Tutor 1: Don't move King into Check    
        if nextmove not in gameboard.legal_moves and nextmove in gameboard.pseudo_legal_moves and nextmove.from_square == gameboard.king(chess.WHITE) :
            error += 'Remember, A King can never be moved into Check, even if it is protected in that position by another piece. <br> '
        
        #Tutor 2: Don't cause Stalemate
        if nextmove in gameboard.legal_moves:
            gameboard.push(nextmove)
            if gameboard.is_stalemate() :
                error += 'That move would cause a Stalemate, and therefore a Draw, try again.'
                gameboard.pop()
                return render_template('game.html', board = Markup(chess.svg.board(gameboard, size = 350)), errors = error)
            gameboard.pop() 
                
        #Tutor 3: Don't move next to King unprotected
        if nextmove in gameboard.legal_moves:
            gameboard.push(nextmove)
            for blackmoves in gameboard.legal_moves:
                if nextmove.to_square == blackmoves.to_square:
                    error += 'Piece placed unprotected near Opposing King'
                    gameboard.pop()
                    return render_template('game.html', board = Markup(chess.svg.board(gameboard, size = 350)), errors = error)
            gameboard.pop()
        
        #Tutor 4: Restrict movement of Opposing King &  Tutor 8: Apply presuure with King
        if nextmove in gameboard.legal_moves:
            gameboard.push(chess.Move.null())
            legalblackmovesbefore = list(gameboard.legal_moves)
            beforecount = len(legalblackmovesbefore)
            gameboard.pop()
            gameboard.push(nextmove)
            legalblackmovesafter = list(gameboard.legal_moves)
            aftercount = len(legalblackmovesafter)
            gameboard.pop()
            goodmove = False
            if (beforecount - aftercount) > 1:
                error += 'That is a good move. The Opposing King went from being able to make ' + str(beforecount) + ' moves to ' + str(aftercount) + ' moves <br>'
                goodmove = True
            if (aftercount - beforecount) > 1:
                error += 'That is not so good move. The Opposing King went from being able to make ' + str(beforecount) + ' moves to ' + str(aftercount) + ' moves <br>'      
            
            gamepiece = gameboard.piece_at(nextmove.from_square)
            if goodmove == False and gamepiece.piece_type != chess.KING:
                whitekingposition = gameboard.king(chess.WHITE)
                whitekingx = whitekingposition % 8
                whitekingy = whitekingposition // 8
                
                blackkingposition = gameboard.king(chess.BLACK)
                blackkingx = blackkingposition % 8
                blackkingy = blackkingposition // 8
                
                kingnotapplyingpressure = False
                
                if whitekingx < blackkingx:
                    if (blackkingx - whitekingx) > 2:
                        kingnotapplyingpressure = True
                else:
                    if blackkingx < whitekingx:
                        if (whitekingx - blackkingx) > 2:
                            kingnotapplyingpressure = True
            
                if whitekingy < blackkingy:
                    if (blackkingy - whitekingy) > 2:
                        kingnotapplyingpressure = True
                else:
                    if blackkingy < whitekingy:
                        if (whitekingy - blackkingy) > 2:
                            kingnotapplyingpressure = True
                
                if kingnotapplyingpressure == True:
                    error += "Apply more pressure with your King <br>"
        
        #Tutor 5: Move away threatened piece
        for square in range(64):
            if gameboard.piece_at(square) and gameboard.color_at(square) == chess.WHITE and gameboard.is_attacked_by(chess.BLACK, square):
                if nextmove.from_square != square:
                    error += 'Must move piece threatened by King <br>'
                    return render_template('game.html', board = Markup(chess.svg.board(gameboard, size = 350)), errors = error)       
                            
        
        if nextmove in gameboard.legal_moves:
            #Make(Push) Player's next move
            gameboard.push(nextmove)
            
            #Check if the game has ended either in a Draw or Checkmate
            if gameboard.is_game_over() and not gameboard.can_claim_draw():
                gamehistory = 'You win by Checkmate !!!<br>'
                gamehistory += 'Moves played in this game <br>:'
                
                for i in gameboard.move_stack:
                    gamehistory += gameboard.uci(i) + '<br>'
                gameboard.clear_board()
                return gamehistory
            if gameboard.can_claim_draw() or gameboard.is_stalemate() or gameboard.is_insufficient_material():
               gamehistory = 'It is a draw )-:!<br>'
               gamehistory += 'Moves played in this game <br>:'
                
               for i in gameboard.move_stack:
                   gamehistory += gameboard.uci(i) + '<br>'
               gameboard.clear_board()
               return gamehistory
                
    
            if AItype == 3 :
               #Search is done to depth of 5 for performance reasons. It is not implemented as a recursive function for performance reasons. 
               checkmate = False 
               startblack = list(gameboard.legal_moves)
               print(startblack)
               #Assign Next Blackmove to Random Move
               blackmove = startblack[random.randint(0,len(startblack)-1)]
               drawposibilities = list()
               checkposibilities = list()
               for firstblackmove in gameboard.legal_moves:
                   drawposibilities.append(0)
                   checkposibilities.append(0)
                   gameboard.push(firstblackmove)
                   if gameboard.can_claim_draw():
                       blackmove = firstblackmove
                       gameboard.pop()
                       drawposibilities[startblack.index(firstblackmove)] = 1
                       break
                   else:
                       firstmovelegalmoves = list(gameboard.legal_moves)
                       firstmovedrawposibilities = list()
                       firstmovecheckposibilities = list()
                       for firstwhitemove in gameboard.legal_moves:
                           gameboard.push(firstwhitemove)
                           firstmovedrawposibilities.append(0)
                           firstmovecheckposibilities.append(0)
                           if gameboard.can_claim_draw():
                               firstmovedrawposibilities[firstmovelegalmoves.index(firstwhitemove)] = 1
                           if gameboard.is_checkmate():
                               checkmate = True
                               firstmovecheckposibilities[firstmovelegalmoves.index(firstwhitemove)] = 1
                           else:
                                for secondblackmove in gameboard.legal_moves:
                                    gameboard.push(secondblackmove)
                                    if gameboard.can_claim_draw():
                                        firstmovedrawposibilities[firstmovelegalmoves.index(firstwhitemove)] = 1
                                    if gameboard.is_checkmate():
                                        checkmate = True
                                    else:
                                        secondmovelegalmoves = list(gameboard.legal_moves)
                                        secondmovedrawposibilities = list()
                                        secondmovecheckposibilities = list()
                                        for secondwhitemove in gameboard.legal_moves:
                                            secondmovedrawposibilities.append(0)
                                            secondmovecheckposibilities.append(0)
                                            gameboard.push(secondwhitemove)
                                            if gameboard.can_claim_draw():
                                                secondmovedrawposibilities[secondmovelegalmoves.index(secondwhitemove)] = 1
                                            if gameboard.is_checkmate():
                                                checkmate = True
                                                secondmovecheckposibilities[secondmovelegalmoves.index(secondwhitemove)] = 1
                                            else:
                                                for thirdblackmove in gameboard.legal_moves:
                                                    gameboard.push(thirdblackmove)
                                                    if gameboard.can_claim_draw():
                                                        secondmovedrawposibilities[secondmovelegalmoves.index(secondwhitemove)] = 1
                                                    gameboard.pop()
                                            gameboard.pop()
                                        secondmovedrawprobability = 0
                                        for i in secondmovedrawposibilities:
                                            secondmovedrawprobability += i
                                        secondmovedrawprobability = secondmovedrawprobability/len(secondmovedrawposibilities)
                                        firstmovedrawposibilities[firstmovelegalmoves.index(firstwhitemove)] = secondmovedrawprobability
                                       
                                        secondmovecheckprobability = 0
                                        for i in secondmovecheckposibilities:
                                            secondmovecheckprobability += i
                                        secondmovecheckprobability = secondmovecheckprobability/len(secondmovecheckposibilities)
                                        firstmovecheckposibilities[firstmovelegalmoves.index(firstwhitemove)] = secondmovecheckprobability
                                    gameboard.pop()    
                           gameboard.pop()
                       firstdrawmoveprobability = 0
                       for i in firstmovedrawposibilities:
                           firstdrawmoveprobability += i
                       firstdrawmoveprobability = firstdrawmoveprobability/len(firstmovedrawposibilities)
                       drawposibilities[startblack.index(firstblackmove)] = firstdrawmoveprobability
                       
                       firstcheckprobability = 0
                       for i in firstmovecheckposibilities:
                           firstcheckprobability += i
                       firstcheckprobability = firstcheckprobability/len(firstmovecheckposibilities)
                       checkposibilities[startblack.index(firstblackmove)] = firstcheckprobability
                       
                   gameboard.pop()
                   
               print(drawposibilities)
               print(checkposibilities)
               biggestvalue = 0.0
               #Assign Next Black Move to the Move with the biggest probability of Drawing
               for i in drawposibilities:
                   if i > biggestvalue:
                       biggestvalue = i;
                       blackmove = startblack[drawposibilities.index(i)-1]
               print(biggestvalue)
               #Tutor 6
               if biggestvalue > 0:
                   error += 'Black can draw in 2 Moves or Less <br>'
                   
               #Try to move Black into the Middle if no Draw is possible in 3 moves
               if biggestvalue == 0:
                   blackmoves = list(gameboard.legal_moves)
                
                   blackkingposition = gameboard.king(chess.BLACK)
                   blackkingx = blackkingposition % 8
                   blackkingy = blackkingposition // 8
                
                   maximumcorner = blackmoves[0]
                   maximummoveawayfromcorner = 0
                
                   for i in blackmoves :
                        uci = i.uci()
                    
                        movex = ord(uci[3]) - 49
                        movey = ord(uci[2]) - 97
        
                        moveawayfromcorner = 0
                        
                        #If Blacking is already in the centre, keep it in the centre if possible
                        if blackkingx == 3 or blackkingx == 4:
                            if movex == 3 or movex == 4:
                                moveawayfromcorner += 1
                            else :
                                moveawayfromcorner += -1
                        
                        if blackkingy == 3 or blackkingy == 4:
                            if movey == 3 or movey == 4:
                                moveawayfromcorner += 1
                            else :
                                moveawayfromcorner += -1
                        
                        #if Black King is to the left on the x-axis:
                        if blackkingx < 3 :
                            moveawayfromcorner += movex - blackkingx
                        #if Black King is to the right on the x-axis:
                        if blackkingx > 4 :
                            moveawayfromcorner += blackkingx - movex
                        
                        #if Black King is to the bottom on the y-axis:
                        if blackkingy < 3 :
                            moveawayfromcorner += movey - blackkingy
                        #if Black King is to the top on the y-axis:
                        if blackkingy > 4 :
                            moveawayfromcorner += blackkingy - movey    
                        
                        
                        if moveawayfromcorner > maximummoveawayfromcorner :
                            maximummoveawayfromcorner = moveawayfromcorner
                            maximumcorner = i
                    
                        blackmove = maximumcorner
                  
               #If Selected Move Puts Black at the posibility of check, try to assign a move that does not
               if checkposibilities[startblack.index(blackmove)] > 0:
                   lowestprobabilityofcheck = checkposibilities[startblack.index(blackmove)]
                   for i in checkposibilities:
                       if lowestprobabilityofcheck < i:
                           lowestprobabilityofcheck = i
                   blackmove = startblack[checkposibilities.index(lowestprobabilityofcheck)]
               
               #Tutor 7
               if checkmate == True:
                   error += 'Checkmate Possible within 2 Moves or Less of White <br>'
                    
               gameboard.push(blackmove)
        
        return render_template('game.html', board = Markup(chess.svg.board(gameboard, size = 350)), errors = error)

if __name__ == '__main__':
    app.run()