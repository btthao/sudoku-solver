class Game():
    def __init__(self, board):
        self.board = board
    
    def print_board(self):
        for r in range(len(self.board)):
            if r % 3 == 0 and r != 0:
                print("- - - - - - - - - - -")
            for c in range(len(self.board[0])):
                if c % 3 == 0 and c != 0:
                    print("| ", end="")
                if c == 8:
                    print(self.board[r][c])
                else:
                    print(str(self.board[r][c]) + " ", end="")
    
    def find_empty(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == 0:
                    return (r, c)
        return None
    
    def is_valid(self, guess, pos):
        # check row      
        for c in range(len(self.board[0])):
            if self.board[pos[0]][c] == guess and pos[1] != c:
                return False
        # check col
        for r in range(len(self.board)):
            if self.board[r][pos[1]] == guess and pos[0] != r:
                return False
        
        # check box
        start_row = (pos[0] // 3) * 3
        start_col = (pos[1] // 3 )* 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == guess and (r,c) != pos:
                    return False
        
        return True
        

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        else:
            row, col = empty
        
        for guess in range(1, 10):
            if self.is_valid(guess, (row, col)):
                self.board[row][col] = guess

                if self.solve():
                    return True
                
                self.board[row][col] = 0
            
        return False

        


if __name__ == '__main__':
    example = [
        [0,6,0,0,0,0,0,0,5],
        [9,0,0,0,0,1,0,0,0],
        [0,1,0,0,7,0,0,0,2],
        [6,0,2,0,0,4,0,3,0],
        [0,0,0,0,5,0,0,4,0],
        [0,4,0,0,1,0,0,0,0],
        [0,0,7,0,0,2,0,0,6],
        [2,0,0,0,9,0,7,0,0],
        [3,0,0,0,0,0,0,1,0]
    ]

    game = Game(example)
    if game.solve():
        game.print_board()
    else:
        print("Can't be solved")
