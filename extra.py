import numpy as np
import collections
import tkinter as tk
import sys

class checkersGame(tk.Frame):

    def __init__(self, master=None):
        self.board = self.setupboard()
        #self.board = self.test_multi_jump()
        self.thismovejump = False
        self.currplayer = 1
        self.currstart = None
        self.currmove = None
        self.curr_validmoves = None

        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=400, height=430, background="white")
        self.canvas.pack(side="top", fill="both", expand=True)

#        self.board = self.test_king()


    def test_king(self):
        board = np.zeros((8, 8))
        board[(1, 2)] = 2
        board[(5, 1)] = 3
        board[(4, 0)] = 2
        board[(4, 2)] = 4
        board[(6, 0)] = 2
        return board

    def test_multi_jump(self):
        board = np.zeros((8, 8))
        board[(1, 2)] = 1
        board[(3, 4)] = 1
        board[(4, 5)] = 2
        self.currplayer = 2
        return board


    def setupboard(self):
        board = np.zeros((8,8))
        for i in range(0, 3):
            for j in range(0, 4):
                if i%2 == 0:
                    board[(i, (j*2)+1)] = 1
                else:
                    board[(i, (j*2))] = 1
        for i in range(5, 8):
            for j in range(0, 4):
                if i%2 == 0:
                    board[(i, (j*2)+1)] = 2
                else:
                    board[(i, (j*2))] = 2
        return board


    def print_moves_list(self, validmoves):
        i = 1
        for key in validmoves:
            if validmoves[key] == "jump":
                print("Move " + str(i) + ": " + str(key) + " *JUMP*")
            else:
                print("Move " + str(i) + ": " + str(key))
            i+=1


    def drawboard(self):
        '''Add a piece to the playing board'''
        self.canvas.delete("all")
        for i in range(0, 400, 100):
            for j in range(0, 400, 100):
                self.canvas.create_rectangle(i, j, i+50, j+50, fill="blue")
                self.canvas.create_rectangle(i+50, j+50, i+100, j+100, fill="blue")
        for r in range(0, 8):
            for c in range(0, 8):
                piece = self.board[(r, c)]
                if piece == 1:
                    self.canvas.create_oval(c*50 + 10, r*50 + 10, (c*50+50) - 10, (r*50+50)-10, fill = "black")
                elif piece == 2:
                    self.canvas.create_oval(c*50+10, r*50+10, (c*50+50)-10, (r*50+50)-10, fill = "red")
                elif piece == 3:
                   self.canvas.create_oval(c * 50 + 10, r * 50 + 10, (c * 50 + 50) - 10, (r * 50 + 50) - 10,
                                               fill="black", outline="gray")
                elif piece == 4:
                    self.canvas.create_oval(c * 50 + 10, r * 50 + 10, (c * 50 + 50) - 10, (r * 50 + 50) - 10,
                                                fill="red", outline="pink")
        if self.currplayer == 1:
            self.canvas.create_text(200, 420, text="it is BLACK's turn.", justify=tk.CENTER)
        elif self.currplayer == 2:
            self.canvas.create_text(200, 420, text= "it is RED's turn.", justify=tk.CENTER)


    def getclicksq(self, event):
        self.drawboard()
        print(event.x, event.y)
        r = int(np.floor(event.y / 50))
        c = int(np.floor(event.x / 50))
        print(r, c)
        if self.currplayer == 1 and self.board[(r,c)] == 1 or self.board[(r,c)] == 3:
            self.currstart = [r, c]
            moves = self.find_valid_moves(self.currstart[0], self.currstart[1])
            self.print_moves_list(moves)
            return
        if self.currplayer == 2 and self.board[(r,c)] == 2 or self.board[(r,c)] == 4:
            self.currstart = [r, c]
            moves = self.find_valid_moves(self.currstart[0], self.currstart[1])
            self.print_moves_list(moves)
            return
        if self.currstart != None:
            moves = self.find_valid_moves(self.currstart[0], self.currstart[1])
            if (r, c) in moves.keys():
                if moves[(r, c)] == "jump":
                    self.thismovejump = True
                self.currmove = [r, c]
                self.updateboard((r, c), self.currstart[0], self.currstart[1])
                return
            else:
                return
        if self.thismovejump:
            nextmoves = self.find_valid_moves(self.currmove[0], self.currmove[1])
            if (r, c) in nextmoves.keys() and nextmoves[(r, c)] == "jump":
                self.currstart = self.currmove
                self.currmove = [r, c]
                self.updateboard((r, c), self.currstart[0], self.currstart[1])
                return


    def updateboard(self, move, r, c):
        self.drawboard()
        piece = self.board[(r, c)]
        self.board[(r, c)] = 0
        self.board[move] = int(piece)
        if move[0] == 7 and piece == 1:
            self.board[move] = 3
        elif move[0] == 0 and piece == 2:
            self.board[move] = 4
        if self.thismovejump:
            if move[0] > r:
                r_j = r + 1
            else:
                r_j = r - 1
            if move[1] > c:
                c_j = c + 1
            else:
                c_j = c - 1
            self.board[(r_j, c_j)] = 0
            nextmoves = self.find_valid_moves(move[0], move[1])
            if nextmoves == None or "jump" not in nextmoves.values():
                self.switchplayer()
                self.drawboard()
        else:
            self.switchplayer()
            self.drawboard()

    def find_valid_moves(self, r, c):
        # return valid moves for a given piece
        validmoves = collections.OrderedDict()
        print(r, c)
        if r>7 or r<0 or c>7 or c<0 or self.board[(r, c)] == 0:
            return None #no valid moves, not a piece
        if ((self.board[(r, c)] == 1 or self.board[(r, c)] == 3) and self.currplayer == 1) or (self.board[(r, c)] == 4 and self.currplayer == 2 ): #king or o, move forward
            if r<7 and c>0 and self.board[(r+1, c-1)] == 0:
                validmoves[(r+1, c-1)] = "nojump"
            elif r<6 and c>1 and (self.board[(r+1, c-1)] == 2 or self.board[(r+1, c-1)] == 4) and self.board[(r+2, c-2)] == 0:
                validmoves[(r+2, c-2)] = "jump"
            if r<7 and c <7 and self.board[(r+1, c+1)] == 0:
                validmoves[(r+1, c+1)] = "nojump"
            elif r<6 and c<6 and (self.board[(r+1, c+1)] == 2 or self.board[(r+1, c+1)] == 4) and self.board[(r+2, c+2)] == 0: #can jump
                validmoves[(r+2, c+2)] = "jump"
        if ((self.board[(r, c)] == 2 or self.board[(r, c)] ==4) and self.currplayer == 2) or (self.board[(r, c)] == 3 and self.currplayer == 1): #king or x, move backward
            if r>0 and c>0 and self.board[(r-1, c-1)] == 0:
                validmoves[(r-1, c-1)] = "nojump"
            elif r>1 and c>1 and (self.board[(r-1,c-1)] == 1 or self.board[(r-1,c-1)] == 3) and self.board[(r-2, c-2)] == 0:
                validmoves[(r-2, c-2)] = "jump"
            if r>0 and c <7 and self.board[(r-1, c+1)] == 0:
                validmoves[(r-1, c+1)] = "nojump"
            elif r>1 and c<6 and (self.board[(r-1,c+1)] == 1 or self.board[(r-1,c+1)] == 3) and self.board[(r-2, c+2)] == 0: #can jump
                validmoves[(r-2, c+2)] = "jump"
        if self.board[(r, c)] == 3 and self.currplayer == 1: #player 1 king, move backward
            if r > 0 and c > 0 and self.board[(r - 1, c - 1)] == 0:
                validmoves[(r - 1, c - 1)] = "nojump"
            elif r > 1 and c > 1 and (self.board[(r - 1, c - 1)] == 2 or self.board[(r-1, c-1)] == 4) and self.board[(r - 2, c - 2)] == 0:
                validmoves[(r - 2, c - 2)] = "jump"
            if r > 0 and c < 7 and self.board[(r - 1, c + 1)] == 0:
                validmoves[(r - 1, c + 1)] = "nojump"
            elif r > 1 and c < 6 and (self.board[(r - 1, c + 1)] == 2 or self.board[(r - 1, c + 1)] == 4) and self.board[(r - 2, c + 2)] == 0:  # can jump
                validmoves[(r - 2, c + 2)] = "jump"
        if self.board[(r, c)] == 4 and self.currplayer == 2 : #X king, move forward
            if r<7 and c>0 and self.board[(r+1, c-1)] == 0:
                validmoves[(r+1, c-1)] = "nojump"
            elif r<6 and c>1 and  (self.board[(r+1,c-1)] == 1 or self.board[(r+1,c-1)] == 3) and self.board[(r+2, c-2)] == 0:
                validmoves[(r+2, c-2)] = "jump"
            if r<7 and c <7 and self.board[(r+1, c+1)] == 0:
                validmoves[(r+1, c+1)] = "nojump"
            elif r<6 and c<6 and  (self.board[(r+1,c+1)] == 1 or self.board[(r+1,c+1)] == 3) and self.board[(r+2, c+2)] == 0: #can jump
                validmoves[(r+2, c+2)] = "jump"
        if bool(validmoves):
            return validmoves
        return None

    def checkwinner(self):
        if not (2 in self.board or 4 in self.board):
            return 1
        elif not (1 in self.board or 3 in self.board):
            return 2
        return 0

    def switchplayer(self):
        if self.checkwinner() != 0:
            print("winner is player {}".format(str(self.checkwinner())))
            sys.exit()
        self.currstart = None
        self.currmove = None
        self.thismovejump = False
        if self.currplayer == 1:
            self.currplayer = 2
        else:
            self.currplayer = 1

    def playgame(self):
        print("Welcome to checkers! You can exit the game at any time by typing \"CTRL + z\".")
        winner = 0
        self.drawboard()
        self.canvas.bind("<Button-1>", self.getclicksq)
        self.canvas.pack()
        self.canvas.mainloop()
        return


def main():
    root = tk.Tk()
    board = checkersGame(root)
    board.pack(side="top", fill="both", expand="true")
    board.playgame()
    print("Exiting game.")
    return


if __name__ == "__main__":

    main()
