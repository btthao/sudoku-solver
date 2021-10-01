import pygame, sys

# variables
BG_COLOR = (240, 240, 240)
GRID_COLOR = (27,44,84)
HIGHLIGHT_COLOR = (251,229,245)
CURRENT_SQUARE_COLOR = (205,137,186)
LINE_COLOR = (155,155,155)
TEXT_COLOR = (60,60,60)
TEXT_COLOR_2 = (76,194,181)
TEXT_COLOR_3 = (205,137,186)
FAIL_TEXT = (220, 55, 38)
WIDTH = 540
HEIGHT = 600
SQUARE_SIZE = WIDTH / 9
GRID_SIZE = WIDTH / 3
FPS = 60

board_example = [
        [0,0,0,7,0,0,2,1,8],
        [7,5,1,0,0,2,4,9,0],
        [0,0,0,0,9,6,7,5,3],
        [0,1,0,3,0,8,0,0,2],
        [0,6,0,0,0,0,0,8,5],
        [8,2,9,5,0,0,0,7,0],
        [1,0,0,0,5,0,0,4,9],
        [0,7,6,0,0,4,5,0,0],
        [0,0,0,6,0,3,8,0,0]
    ]

pygame.init()
pygame.font.init()
pygame.display.set_caption('SUDOKU') 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 26)
clock = pygame.time.Clock()



class Board():
    def __init__(self, board):
        self.initial_board = board
        self.solved = False
        self.current_square = None
        self.current_board = [[self.initial_board[r][c] for c in range(len(self.initial_board[0]))] for r in range(len(self.initial_board))]
        
    
    def find_empty(self):
        for r in range(len(self.current_board)):
            for c in range(len(self.current_board[0])):
                if self.current_board[r][c] == 0:
                    return (r, c)
        return None


    def is_valid(self, guess, pos):
        # check row      
        for c in range(len(self.current_board[0])):
            if self.current_board[pos[0]][c] == guess and pos[1] != c:
                return False
        # check col
        for r in range(len(self.current_board)):
            if self.current_board[r][pos[1]] == guess and pos[0] != r:
                return False
        
        # check box
        start_row = (pos[0] // 3) * 3
        start_col = (pos[1] // 3) * 3

        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.current_board[r][c] == guess and (r,c) != pos:
                    return False
        
        return True


    def find_highlight(self, row, col):
        list = []
        for r in range(len(self.current_board)):
            if r != row:
                list.append((r, col))
        for c in range(len(self.current_board[0])):
            if c != col:
                list.append((row, c))
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if r != row and c != col:
                    list.append((r,c))
        return list


    def draw_nums(self, num, row, col, color):
        if num == 0:
            val = ""
        else:
            val = str(num)
        text = font.render(val, 1, color)
        screen.blit(text, (SQUARE_SIZE*col + (SQUARE_SIZE/2 - text.get_width()/2), SQUARE_SIZE*row + (SQUARE_SIZE/2 - text.get_height()/2)))
          
    
    def draw_board(self):       
        grid_line_width = 3
        square_line_width = 1

        # draw small squares
        for i in range(1,9): 
            pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), square_line_width)
            pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE*i, 0), (SQUARE_SIZE*i, WIDTH), square_line_width)
        
    
        # draw big grids
        for i in range(4):
            pygame.draw.line(screen, GRID_COLOR, (0, GRID_SIZE*i), (WIDTH, GRID_SIZE*i), grid_line_width)
            pygame.draw.line(screen, GRID_COLOR, (GRID_SIZE*i, 0), (GRID_SIZE*i, WIDTH), grid_line_width)
            if (i == 3):
                pygame.draw.line(screen, GRID_COLOR, (GRID_SIZE*i,0), (GRID_SIZE*i, WIDTH), grid_line_width*2)
            
    
    def fill_values(self):

        if self.current_square:
            r, c = self.current_square

            for pos in self.find_highlight(r,c):
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (SQUARE_SIZE*pos[1], SQUARE_SIZE*pos[0], SQUARE_SIZE, SQUARE_SIZE))

            pygame.draw.rect(screen, CURRENT_SQUARE_COLOR, (SQUARE_SIZE*c, SQUARE_SIZE*r, SQUARE_SIZE, SQUARE_SIZE))
            
        
        for r in range(len(self.current_board)):
            for c in range(len(self.current_board[0])):
                if self.initial_board[r][c] != 0: 
                    self.draw_nums(self.initial_board[r][c], r, c, TEXT_COLOR_2)                                                   
                elif self.current_board[r][c] != 0:
                    self.draw_nums(self.current_board[r][c], r, c, TEXT_COLOR)
                
    
    def delete_guess(self):
        if self.current_square:
            r, c = self.current_square
            self.current_board[r][c] = 0


    def clear(self):
        self.current_square = None


    def set_current(self, row, col):
        if row >= 0 and col >= 0 and row < 9 and col < 9 and self.initial_board[row][col] == 0:
            self.current_square = (row, col)
        else:
            self.current_square = None
        
   
    def guess(self, value):
        if self.current_square:
            r, c = self.current_square
            self.current_board[r][c] = value


    def restart(self):
        self.solved = False
        self.current_board = [[self.initial_board[r][c] for c in range(len(self.initial_board[0]))] for r in range(len(self.initial_board))]
        self.current_square = None


    def check(self):
        self.current_square = None
        for r in range(len(self.current_board)):
            for c in range(len(self.current_board[0])):
                if self.current_board[r][c] == 0:
                    self.solved = False
                    return 'Board not finished!'
        
        for r in range(len(self.current_board)):
            for c in range(len(self.current_board[0])):
                if self.is_valid(self.current_board[r][c], (r,c)) == False:
                    self.solved = False
                    return 'Incorrect :('
        
        self.solved = True
        return 'Soduko solved!'  


    def solve(self):
        draw_screen()
        empty = self.find_empty()
        if not empty:
            return True
        else:
            row, col = empty
        
        for guess in range(1, 10):
            if self.is_valid(guess, (row, col)):
                self.current_board[row][col] = guess
                pygame.display.update()

                if self.solve():
                    return True
                
            self.current_board[row][col] = 0
            pygame.display.update()
            
        return False  



game = Board(board_example) 


# buttons
BUTTON_GAP = 10
BUTTON_WIDTH = 66
BUTTON_HEIGHT = 27

button_solve = pygame.Rect(BUTTON_GAP, WIDTH + (HEIGHT - WIDTH - BUTTON_HEIGHT)/2, BUTTON_WIDTH, BUTTON_HEIGHT)

button_check = pygame.Rect(2*BUTTON_GAP + BUTTON_WIDTH, WIDTH + (HEIGHT - WIDTH - BUTTON_HEIGHT)/2, BUTTON_WIDTH, BUTTON_HEIGHT)

button_restart = pygame.Rect(3*BUTTON_GAP + 2*BUTTON_WIDTH, WIDTH + (HEIGHT - WIDTH - BUTTON_HEIGHT)/2, BUTTON_WIDTH, BUTTON_HEIGHT)


# draw functions
def draw_button(text, button):
    pygame.draw.rect(screen, GRID_COLOR, button, 2)
    text_obj = font_small.render(text, 1, TEXT_COLOR_3)
    screen.blit(text_obj, (button.x + button.width/2 - text_obj.get_width()/2, button.y + button.height/2 - text_obj.get_height()/2))


def draw_message(text, color):
    text_obj = font.render(text, 1, color)
    screen.blit(text_obj, (5*BUTTON_GAP + 3*BUTTON_WIDTH, WIDTH + (HEIGHT - WIDTH - text_obj.get_height())/2))


def draw_screen():
    screen.fill(BG_COLOR)
    game.fill_values()
    game.draw_board()
    draw_button('Solve', button_solve)
    draw_button('Check', button_check)
    draw_button('Restart', button_restart)


# main game loop
def main():
    key = None
    message = ""

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                message = ""
                key = None
                mx, my = pygame.mouse.get_pos()

                if button_solve.collidepoint((mx, my)):
                    game.restart()
                    solved = game.solve()
                    if solved:
                        game.solved = True
                        message = 'Done!'
                    else:
                        game.solved = False
                        message = 'Cannot be solved.'
                    
                    
                elif button_check.collidepoint((mx, my)):
                    message = game.check()
                    
                elif button_restart.collidepoint((mx, my)):
                    game.restart()
                    
                else :
                    clicked_row = int(my // SQUARE_SIZE)
                    clicked_col = int(mx // SQUARE_SIZE)
                    game.set_current(clicked_row, clicked_col)

            
            if event.type == pygame.KEYDOWN:
                message = ""
                key = None
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9

                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    game.delete_guess()
                    key = None
                
                if event.key == pygame.K_UP and game.current_square:
                    r, c = game.current_square
                    if r > 0:
                        r -= 1
                        while r > 0 and game.initial_board[r][c] != 0:
                            r -= 1
                        if game.initial_board[r][c] == 0:
                            game.set_current(r, c)

                if event.key == pygame.K_DOWN and game.current_square:
                    r, c = game.current_square
                    if r < 8:
                        r += 1
                        while r < 8 and game.initial_board[r][c] != 0:
                            r += 1
                        if game.initial_board[r][c] == 0:
                            game.set_current(r, c)

                if event.key == pygame.K_RIGHT and game.current_square:
                    r, c = game.current_square
                    if c < 8:
                        c += 1
                        while c < 8 and game.initial_board[r][c] != 0:
                            c += 1
                        if game.initial_board[r][c] == 0:
                            game.set_current(r, c)

                if event.key == pygame.K_LEFT and game.current_square:
                    r, c = game.current_square
                    if c > 0:
                        c -= 1
                        while c > 0 and game.initial_board[r][c] != 0:
                            c -= 1
                        if game.initial_board[r][c] == 0:
                            game.set_current(r, c)

                if event.key == pygame.K_RETURN:
                    game.clear()
                    
        if game.current_square and key != None:
            game.guess(key)
            key = None


        draw_screen()

        if game.solved:
            draw_message(message, TEXT_COLOR_2)
        else:
            draw_message(message, FAIL_TEXT)


        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main()