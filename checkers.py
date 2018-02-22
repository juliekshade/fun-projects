import numpy as np
import sys


def str_to_int(str):
    # Try to convert string into corresponding column for checkers game
    ch = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    str = str.lower()
    for i in range(0,8):
        if str == ch[i]:
            return i
    return None


def int_to_str(num):
    # try to convert int into corresponding column for checkers game
    ch = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    if num >= 0 and num < 8:
        return ch[num]
    raise ValueError


class checkersGame:

    def __init__(self):
        self.thismovejump = False
        self.currplayer = 1
        self.board = self.setup_board()
        # lines below can be uncommented for testing
        # self.board = self.multi_jump_p2_board()
        # self.board = self.multi_jump_p1_board()


    def multi_jump_p1_board(self):
        # test board for "backward" jumps
        board = np.zeros((8, 8))
        board[(2, 1)] = 2
        board[(2, 3)] = 2
        board[(4, 3)] = 2
        board[(4, 5)] = 2
        board[(6, 5)] = 2
        board[(7, 6)] = 1
        board[(7, 1)] = 1
        return board


    def multi_jump_p2_board(self):
        # test board for "forward" jumps
        board = np.zeros((8, 8))
        board[(5, 1)] = 1
        board[(5, 3)] = 1
        board[(3, 3)] = 1
        board[(3, 5)] = 1
        board[(1, 5)] = 1
        board[(0, 6)] = 2
        self.currplayer = 2
        return board


    def setup_board(self):
        # Initalize the board for a regular game of checkers
        board = np.zeros((8,8))
        for i in range(0, 3):
            for j in range(0, 4):
                if i%2 == 0:
                    board[(i, (j*2)+1)] = 2
                else:
                    board[(i, (j*2))] = 2
        for i in range(5, 8):
            for j in range(0, 4):
                if i%2 == 0:
                    board[(i, (j*2)+1)] = 1
                else:
                    board[(i, (j*2))] = 1
        return board


    def display_board(self):
        # print the board
        for i in range (0, 8):
            rowstr = str(i) + " "
            for j in range(0, 8):
                if self.board[(i, j)] == 0:
                    rowstr += " - "
                elif self.board[(i, j)] == 1:
                    rowstr += " o "
                elif self.board[(i, j)] == 2:
                    rowstr += " x "
            print(rowstr)
        print("   a  b  c  d  e  f  g  h \n")


    def print_moves_list(self, validmoves):
        # Print list of valid moves. Mostly used for debugging purposes, should delete.
        i = 1
        print("Valid moves from the selected square are:")
        for key in validmoves:
            pos = str(key[0]) + int_to_str(key[1])
            print("Move " + str(i) + ": " + pos)
            i+=1


    def check_jump_done(self, currmove):
        # Check if there is another jump that can be performed from a given position, if not, next player's turn.
        if self.thismovejump == False:
            return
        moves = self.find_valid_moves(currmove)
        if moves == None:
            self.thismovejump = False
            return
        else:
            nextmove = None
            while nextmove not in moves:
                try:
                    m = input("Enter row and column of the next square you would like to jump to (ex. 1a):")
                    m_r,m_c = self.parse_square(m)
                    if (m_r, m_c) in moves:
                        nextmove = (m_r, m_c)
                    else:
                        print("Invalid input, please try again.")
                except (TypeError, ValueError, IndexError) as e:
                    print("Invalid input, please try again.")
                    continue
            self.move_piece(nextmove, currmove)


    def move_piece(self, end, start):
        # Update the board to move the piece at start to the end
        piece = self.board[start]
        self.board[start] = 0
        self.board[end] = piece
        if self.thismovejump:
            r = start[0]
            c = start[1]
            if end[0] > r:
                r_j = r + 1
            else:
                r_j = r - 1
            if end[1] > c:
                c_j = c + 1
            else:
                c_j = c - 1
            self.board[(r_j, c_j)] = 0
            self.display_board()
            self.check_jump_done(end)


    def find_valid_moves(self, pos):
        # Return a list of valid moves for piece at a given position
        validmoves = []
        r = pos[0]
        c = pos[1]
        if r>7 or r<0 or c>7 or c<0 or self.board[(r, c)] == 0:
            raise TypeError
        if self.thismovejump:
            if self.board[(r, c)] == 2 and self.currplayer == 2:  # move forward
                if r < 6 and c > 1 and self.board[(r + 1, c - 1)] == 1 and self.board[(r + 2, c - 2)] == 0:
                    validmoves.append((r + 2, c - 2))
                if r < 6 and c < 6 and self.board[(r + 1, c + 1)] == 1 and self.board[(r + 2, c + 2)] == 0:
                    validmoves.append((r + 2, c + 2))
            elif self.board[(r, c)] == 1 and self.currplayer == 1:  # move backward
                if r > 1 and c > 1 and self.board[(r - 1, c - 1)] == 2 and self.board[(r - 2, c - 2)] == 0:
                    validmoves.append((r - 2, c - 2))
                if r > 1 and c < 6 and self.board[(r - 1, c + 1)] == 2 and self.board[(r - 2, c + 2)] == 0:
                    validmoves.append((r - 2, c + 2))
        else:
            if self.board[(r, c)] == 2 and self.currplayer == 2: # move forward
                if r<7 and c>0 and self.board[(r + 1, c - 1)] == 0:
                    validmoves.append((r + 1, c - 1))
                if r<7 and c <7 and self.board[(r + 1, c + 1)] == 0:
                    validmoves.append((r + 1, c + 1))
            elif self.board[(r, c)] == 1 and self.currplayer == 1: # move backward
                if r>0 and c>0 and self.board[(r - 1, c - 1)] == 0:
                    validmoves.append((r - 1, c - 1))
                if r>0 and c <7 and self.board[(r - 1, c + 1)] == 0:
                    validmoves.append((r - 1, c + 1))
        if len(validmoves) > 0:
            return validmoves
        return None


    def switch_player(self):
        # Switch the current player
        if self.currplayer == 1:
            self.currplayer = 2
        else:
            self.currplayer = 1


    def parse_square(self, s):
        # Attempt to parse input from "[letter a-g][integer 0-7]" to [row, col]. Also handles quit message
        if(str(s).lower() =="quit"):
            sys.exit()
        r = int(s[0])
        c = str_to_int(s[1])
        return (r, c)


    def check_if_jump_exists(self):
        # Check if any jump can be performed given the current state of the game
        for r in range(0, 8):
            for c in range(0, 8):
                if self.board[(r, c)] == 2 and self.currplayer == 2:  # move forward
                    if r < 6 and c > 1 and self.board[(r + 1, c - 1)] == 1 and self.board[(r + 2, c - 2)] == 0:
                        return True
                    elif r < 6 and c < 6 and self.board[(r + 1, c + 1)] == 1 and self.board[(r + 2, c + 2)] == 0:
                        return True
                if self.board[(r, c)] == 1 and self.currplayer == 1:  # move backward
                    if r > 1 and c > 1 and self.board[(r - 1, c - 1)] == 2 and self.board[(r - 2, c - 2)] == 0:
                        return True
                    elif r > 1 and c < 6 and self.board[(r - 1, c + 1)] == 2 and self.board[(r - 2, c + 2)] == 0:
                        return True
        return False


    def playgame(self):
        # Main driver for checkers game
        print("Welcome to checkers! You can exit the game at any time by typing \"quit\".")
        gameover = False
        while not gameover:
            print("\n")
            if self.currplayer == 1:
                piecetype = "o"
            elif self.currplayer == 2:
                piecetype = "x"
            self.thismovejump = self.check_if_jump_exists()
            if self.thismovejump:
                print("You have a jump available! You must jump this turn.")
            currmove = None
            while currmove == None:
                moves = None
                while moves == None:
                    self.display_board()
                    pos = input("Player {}: Input the row and column of the {} piece you would like to move (ex: 1a):".format(self.currplayer, piecetype))
                    try:
                        r, c = self.parse_square(pos)
                        moves = self.find_valid_moves((r, c))
                        if moves == None:
                            print("Invalid piece, please try again.")
                    except (TypeError, ValueError, IndexError) as e:
                        print("Invalid input, please try again.")
                        continue
                while currmove not in moves:
                    try:
                        m = input("Player {}: Input the row and column of the square you would like to move to (ex: 1a):".format(self.currplayer))
                        m_r,m_c = self.parse_square(m)
                        if (m_r, m_c) in moves:
                            currmove = (m_r, m_c)
                        else:
                            print("Invalid input, please try again.")
                    except (TypeError, ValueError, IndexError) as e:
                        print("Invalid input, please try again.")
                        continue
            self.move_piece(currmove, (r, c))
            self.switch_player()


def main():
    game = checkersGame()
    game.playgame()
    print("Exiting game.")
    return


if __name__ == "__main__":
    main()