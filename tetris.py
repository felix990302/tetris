from typing import List
from enum import Enum, auto
from random import choice

import pygame


colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure:
    def __init__(self, matrix: List[List[bool]]):
        self.position = matrix
        self.color = choice(colors)

    def image(self):
        return self.position

    def rotate(self):
        N = len(self.position)

        for x in range(N//2):
            for y in range(x, N-x-1):
                temp = self.position[x][y]
                self.position[x][y] = self.position[N-y-1][x]
                self.position[N-y-1][x] = self.position[N-x-1][N-y-1]
                self.position[N-x-1][N-y-1] = self.position[y][N-x-1]
                self.position[y][N-x-1] = temp

    def rotate_back(self):
        N = len(self.position)

        for x in range(N//2):
            for y in range(x, N-x-1):
                temp = self.position[x][y]
                self.position[x][y] = self.position[y][N-x-1]
                self.position[y][N-x-1] = self.position[N-x-1][N-y-1]
                self.position[N-x-1][N-y-1] = self.position[N-y-1][x]
                self.position[N-y-1][x] = temp

class HorizontalLine(Figure):
    def __init__(self):
        matrix = [
                [False, False, False, False],
                [True, True, True, True],
                [False, False, False, False],
                [False, False, False, False]]

        super().__init__(matrix)

class Square(Figure):
    def __init__(self):
        matrix = [
                [False, False, False, False],
                [False, True, True, False],
                [False, True, True, False],
                [False, False, False, False]]

        super().__init__(matrix)

class BentLeft(Figure):
    def __init__(self):
        matrix = [
                [False, False, False, False],
                [True, False, False, False],
                [True, True, True, True],
                [False, False, False, False]]

        super().__init__(matrix)

class BentRight(Figure):
    def __init__(self):
        matrix = [
                [False, False, False, False],
                [False, False, False, True],
                [True, True, True, True],
                [False, False, False, False]]

        super().__init__(matrix)

class ZigZag(Figure):
    def __init__(self):
        matrix = [
                [False, False, True, False],
                [False, True, True, False],
                [False, True, False, False],
                [False, False, False, False]]

        super().__init__(matrix)

class ZagZig(Figure):
    def __init__(self):
        matrix = [
                [False, True, False, False],
                [False, True, True, False],
                [False, False, True, False],
                [False, False, False, False]]

        super().__init__(matrix)

class Tee(Figure):
    def __init__(self):
        matrix = [
                [False, True, False, False],
                [True, True, True, False],
                [False, False, False, False],
                [False, False, False, False]]

        super().__init__(matrix)

class State(Enum):
    START = auto()
    GAMEOVER = auto()

class Tetris:
    level = 2
    score = 0
    state = State.START
    field = None
    height = 0
    width = 0
    x = 0
    y = 0
    zoom = 20
    figure = None

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

        self.newfigure()
        self.field = [[False]*width for _ in range(height)]

    def intersects(self):
        position = self.figure.image()

        for i in range(len(position)):
            for j in range(len(position[0])):
                abs_x, abs_y = self.x + i, self.y + j
                if not position[i][j]:
                    continue
                elif abs_x < 0 or abs_y < 0 or abs_x >= self.height or abs_y >= self.width:
                    return True
                elif position[i][j] and self.field[abs_x][abs_y]:
                    return True

        return False

    def breaklines(self):
        while self.field[-1][0]:
            if not all(self.field[-1]):
                return
            self.field.pop()
            self.field.insert(0, [False]*self.width)
            self.score += self.width
    
    def newfigure(self):
        self.figure = choice([
            HorizontalLine, Square, BentLeft,
            BentRight, ZigZag, ZagZig, Tee])()
        self.x, self.y = 0, 0

    def freeze(self):
        position = self.figure.image()

        for i in range(len(position)):
            for j in range(len(position[0])):
                if position[i][j]:
                    abs_x, abs_y = self.x + i, self.y + j
                    self.field[abs_x][abs_y] = True

        self.breaklines()
        self.newfigure()
    
        if self.intersects():
            self.state = State.GAMEOVER

    def go_left(self):
        self.y -= 1
        if self.intersects():
            self.y += 1

    def go_right(self):
        self.y += 1
        if self.intersects():
            self.y -= 1

    def go_down(self):
        self.x += 1
        if self.intersects():
            self.x -= 1
            self.freeze()

    def rotate(self):
        self.figure.rotate()
        if self.intersects():
            self.figure.rotate_back()

if __name__ == "__main__":
# Initialize the game engine
    pygame.init()

# Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)

    size = (400, 500)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(20, 10)
    counter = 0

    while game.state != State.GAMEOVER:
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0:
            game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.state = State.GAMEOVER
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    game.go_down()
                if event.key == pygame.K_LEFT:
                    game.go_left()
                if event.key == pygame.K_RIGHT:
                    game.go_right()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

        screen.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [0 + game.zoom * j, 0 + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, BLACK if game.field[i][j] else WHITE,
                                     [0 + game.zoom * j + 1, 0 + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

            for i in range(4):
                for j in range(4):
                    if game.figure.image()[i][j]:
                        pygame.draw.rect(screen, game.figure.color,
                                         [0 + game.zoom * (j + game.y) + 1,
                                          0 + game.zoom * (i + game.x) + 1,
                                          game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        screen.blit(text, [0, 0])
        if game.state == State.GAMEOVER:
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
