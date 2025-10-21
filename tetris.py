#cmd 
#pip install pygame
import pygame
import random
import sys

# 화면/그리드 설정
CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLUMNS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# 색상
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
COLORS = [
    (0, 240, 240),  # I
    (0, 0, 240),    # J
    (240, 160, 0),  # L
    (240, 240, 0),  # O
    (0, 240, 0),    # S
    (160, 0, 240),  # T
    (240, 0, 0),    # Z
]

# 테트로미노(4x4 매트릭스 회전 상태들)
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]

class Piece:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (col, row), color in locked_positions.items():
        if row >= 0:
            grid[row][col] = color
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        for j, char in enumerate(line):
            if char == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(COLUMNS) if grid[i][j] == BLACK] for i in range(ROWS)]
    accepted = [pos for row in accepted_positions for pos in row]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted and pos[1] > -1:
            return False
    return True

def check_lost(positions):
    for (x, y) in positions:
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(COLUMNS // 2 - 2, 0, random.randrange(0, len(SHAPES)))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, ((WIDTH - label.get_width()) // 2, (HEIGHT - label.get_height()) // 2))

def draw_grid(surface, grid):
    for i in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        for j in range(COLUMNS):
            pygame.draw.line(surface, GRAY, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

def clear_rows(grid, locked):
    inc = 0
    for i in range(ROWS-1, -1, -1):
        if BLACK not in grid[i]:
            inc += 1
            for j in range(COLUMNS):
                try:
                    del locked[(j, i)]
                except:
                    pass
    if inc > 0:
        # shift down
        new_locked = {}
        for (x, y), color in sorted(locked.items(), key=lambda item: item[0][1], reverse=True):
            new_y = y + inc
            new_locked[(x, new_y)] = color
        locked.clear()
        locked.update(new_locked)
    return inc

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 24)
    label = font.render('Next', 1, WHITE)
    sx = WIDTH + 50
    sy = 50
    surface.blit(label, (sx + 10, sy - 30))
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        for j, char in enumerate(line):
            if char == '0':
                pygame.draw.rect(surface, piece.color, (sx + j*CELL_SIZE, sy + i*CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)
    font = pygame.font.SysFont('comicsans', 40)
    label = font.render('TETRIS', 1, WHITE)
    surface.blit(label, ((WIDTH - label.get_width()) // 2, 10))

    # 점수
    font2 = pygame.font.SysFont('comicsans', 24)
    score_label = font2.render(f'Score: {score}', 1, WHITE)
    surface.blit(score_label, (WIDTH + 30, HEIGHT // 2 - 100))

    for i in range(ROWS):
        for j in range(COLUMNS):
            pygame.draw.rect(surface, grid[i][j],
                             (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255,255,255), (0,0, WIDTH, HEIGHT), 4)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH + 200, HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.25  # 기존 0.5에서 2배 빠르게 (값을 절반으로)
    current_piece = get_shape()
    next_piece = get_shape()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP or event.key == pygame.K_x:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_z:
                    current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                elif event.key == pygame.K_SPACE:
                    # hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)
        for (x, y) in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            cleared = clear_rows(grid, locked_positions)
            if cleared:
                score += (cleared * 100)
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            if check_lost(list(locked_positions.keys())):
                draw_text_middle(win, "GAME OVER", 60, WHITE)
                pygame.display.update()
                pygame.time.delay(1500)
                run = False

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()