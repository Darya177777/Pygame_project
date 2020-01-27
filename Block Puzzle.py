import os
import pygame
import random
import sys

# list of figures where are the coordinates of the shaded cells of minifield
LIST_OF_FIGURES = (((2, 1), (3, 1), (3, 2), (3, 3)), ((2, 1), (2, 2), (2, 3), (3, 1)),
                   ((2, 1), (2, 2), (2, 3), (3, 3)), ((1, 2), (2, 2), (3, 1), (3, 2)),
                   ((3, 0), (3, 1), (3, 2), (3, 3)), ((3, 1), (3, 2)), ((3, 1), (3, 2), (3, 3)),
                   ((1, 1), (1, 2), (2, 1), (3, 1)), ((1, 1), (2, 1), (3, 1), (3, 2)),
                   ((1, 1), (2, 1), (3, 1), (3, 2)), ((3, 1), (3, 2), (3, 3), (2, 3)),
                   ((2, 1), (2, 2), (3, 2), (3, 3)), ((2, 2), (2, 3), (3, 1), (3, 2)),
                   ((1, 2), (2, 1), (2, 2), (3, 1)), ((1, 1), (2, 1), (2, 2), (3, 2)),
                   ((1, 1), (2, 1), (3, 1), (4, 1)), ((1, 1), (2, 1), (3, 1)), ((2, 1), (3, 1)),
                   ((2, 1), (2, 2), (3, 1), (3, 2)), ((2, 1), (3, 1), (3, 2)),
                   ((2, 1), (2, 2), (3, 2)), ((2, 1), (2, 2), (3, 1)), ((2, 2), (3, 1), (3, 2)),
                   ((1, 2), (2, 1), (2, 2), (3, 2)), ((2, 2), (3, 1), (3, 2), (3, 3)),
                   ((1, 1), (2, 1), (2, 2), (3, 1)), ((2, 1), (2, 2), (2, 3), (3, 2)))
# initializing the game, the assignment of values to the constants and important variables
pygame.init()
screen = pygame.display.set_mode([1050, 770])
screen.fill((0, 0, 0))
count = 0
FPS = 50
board = None
board_of_levels = None
GRAVITY = 0.005
level = 0
clock = pygame.time.Clock()


class MouseMy(pygame.sprite.Sprite):
    """mouse class for implementing click actions on an object"""
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        self.rect.x = random.randrange(1050)
        self.rect.y = random.randrange(770)

    def update(self):
        self.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))


mouse1 = pygame.sprite.Group()
MouseMy(mouse1)


def print_rules():
    """this function shows a screen with the rules of the game"""
    intro_text = ["Back", ' ', 'Welcome to Block Puzzle!',
                  ' The game consists of 9 levels, each more difficult than the previous one. The ',
                  'screen shows the main field and 3 figures below it. Also on the right there '
                  'is a timer, ', 'the number of points and a table of levels. You need to drag the'
                                  ' shapes to the main field ',
                  'so that you get as many rows or columns completely filled with cubes. After the '
                  'column ',
                  '(row) is completely filled, it disappears and snowflakes begin to fall. You '
                  'need to ', 'click on them to collect as many points as possible in the allotted '
                              'time. As soon as ',
                  'you get the right number of points, you go to the next level. If the time has '
                  'expired, and ',
                  'the points are not enough, then you can start playing the game again. To '
                  'complete the ', '         victory you need to pass all the levels.', ' ',
                  ' Good luck!']
    screen.fill((255, 255, 255))
    fon = load_image('rules2.png', 1)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 80
    rects = []
    run1 = True
    for line in intro_text:
        string_rendered = font.render(line, 1, (150, 30, 20))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        rects.append(intro_rect)
        screen.blit(string_rendered, intro_rect)
    while run1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (rects[0].left <= pygame.mouse.get_pos()[0] <= rects[0].left + rects[0].width and
                        rects[0].top <= pygame.mouse.get_pos()[1] <= rects[0].top +
                        rects[0].height):
                    run1 = False
                    start_screen()
                    break
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    """this function closes the game window and stops the program"""
    pygame.quit()
    sys.exit()


def start_screen(f=0):
    """this function shows a start screen"""
    intro_text = ["Game rules", "Play"]
    fon = load_image('Zastavka.png', 2)
    screen.fill((0, 0, 0))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 120
    rects = []
    for line in intro_text:
        string_rendered = font.render(line, 1, (150, 30, 20))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        rects.append(intro_rect)
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (rects[1].left <= pygame.mouse.get_pos()[0] <= rects[1].left + rects[1].width and
                        rects[1].top <= pygame.mouse.get_pos()[1] <= rects[1].top +
                        rects[1].height) and f == 0:
                    return
                if (rects[1].left <= pygame.mouse.get_pos()[0] <= rects[1].left + rects[1].width and
                        rects[1].top <= pygame.mouse.get_pos()[1] <= rects[1].top +
                        rects[1].height) and f == 1:
                    play(1)
                if (rects[0].left <= pygame.mouse.get_pos()[0] <= rects[0].left + rects[0].width and
                        rects[0].top <= pygame.mouse.get_pos()[1] <= rects[0].top +
                        rects[0].height):
                    print_rules()
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    """function converts the image for ease of working with it"""
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey == -1:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    elif colorkey == 2:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image


def stop():
    """function shows the screen when you lose and resets the variables"""
    global level
    intro_text = ["Unfortunately, time is up!", "Restart", 'Game rules']
    fon = load_image('stop.png', 2)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 120
    rects = []
    level = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, (150, 30, 20))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        rects.append(intro_rect)
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if (rects[1].left <= pygame.mouse.get_pos()[0] <= rects[1].left + rects[1].width and
                        rects[1].top <= pygame.mouse.get_pos()[1] <= rects[1].top +
                        rects[1].height):
                    start_screen(1)
                if (rects[2].left <= pygame.mouse.get_pos()[0] <= rects[2].left + rects[2].width and
                        rects[2].top <= pygame.mouse.get_pos()[1] <= rects[2].top +
                        rects[2].height):
                    print_rules()
        pygame.display.flip()
        clock.tick(FPS)


def win():
    """function shows the screen when you win"""
    global all_sprites, level, board_of_levels, images, count
    if count >= (level + 1) * 11:
        board_of_levels.get_cell(level)
        level += 1
        if level == 9:
            big_win()
        else:
            images.update()
            intro_text = ["Сongratulations, you have won", "Play", 'Game rules']
            fon = load_image('win.png', 2)
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 60)
            text_coord = 120
            rects = []
            for line in intro_text:
                string_rendered = font.render(line, 1, (250, 30, 20))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 30
                text_coord += intro_rect.height
                rects.append(intro_rect)
                screen.blit(string_rendered, intro_rect)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        if (rects[1].left <= pygame.mouse.get_pos()[0] <= rects[1].left + rects[
                            1].width and
                                rects[1].top <= pygame.mouse.get_pos()[1] <= rects[1].top +
                                rects[1].height):
                            all_sprites = pygame.sprite.Group()
                            play()
                        if (rects[2].left <= pygame.mouse.get_pos()[0] <= rects[2].left + rects[
                            2].width and
                                rects[2].top <= pygame.mouse.get_pos()[1] <= rects[2].top +
                                rects[2].height):
                            print_rules()
                pygame.display.flip()
                clock.tick(FPS)


def big_win():
    """function shows the screen when you win and passed all levels"""
    global level
    intro_text = ["You have won this game!", "Restart"]
    fon = load_image('win.png', 2)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 120
    rects = []
    level = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, (150, 30, 20))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        rects.append(intro_rect)
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if (rects[1].left <= pygame.mouse.get_pos()[0] <= rects[1].left + rects[1].width and
                        rects[1].top <= pygame.mouse.get_pos()[1] <= rects[1].top +
                        rects[1].height):
                    start_screen(1)
        pygame.display.flip()
        clock.tick(FPS)


class Beaker(pygame.sprite.Sprite):
    """class for show image Beaker"""
    def __init__(self, group):
        self.image = pygame.transform.scale(load_image('kubok2.png', -1), (50, 50))
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = 610
        self.rect.y = 80


class Table(pygame.sprite.Sprite):
    """class for show image table of results"""
    def __init__(self, group):
        self.image = load_image('table.png', 2)
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 170


class ChristmasImage(pygame.sprite.Sprite):
    """class for show Christmas images which change at each level"""
    def __init__(self, group):
        self.image = load_image('image1.png', 2)
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 450
        self.number = 1

    def update(self):
        self.number += 1
        self.image = load_image(f'image{self.number}.png', 2)

    def zero(self):
        self.number = 1
        self.image = load_image('image1.png', 2)


class MainField:
    """this is main field, shapes are dragged here"""
    def __init__(self, width, height, top, left, color1, color2, visibility=0, lines=0):
        self.width = width
        self.height = height
        self.board = [[0 for i in range(width)] for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = 35
        self.color1 = color1
        self.color2 = color2
        self.lines = lines
        self.visibility = visibility

    def render(self):
        # draw field
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0 and self.visibility == 0:
                    pygame.draw.rect(screen, self.color1, (self.left + j * self.cell_size,
                                                           self.top + i * self.cell_size,
                                                           self.cell_size, self.cell_size))
                    if self.lines == 1:
                        pygame.draw.rect(screen, self.color2, (self.left + j * self.cell_size,
                                                               self.top + i * self.cell_size,
                                                               self.cell_size, self.cell_size), 1)
                elif self.board[i][j] == 1:
                    pygame.draw.rect(screen, self.color2, (self.left + j * self.cell_size,
                                                           self.top + i * self.cell_size,
                                                           self.cell_size, self.cell_size))

    def get_cell(self, pos, draw=0):
        # the cell is checked(empty or not) if the flag 'draw' is set (all cells of the figure are
        # checked) then the cell is painted over
        global count
        cell = None
        for i in range(self.height):
            for j in range(self.width):
                if (self.left + j * self.cell_size < pos[0] + 14 <
                        self.left + (j + 1) * self.cell_size and
                        self.top + i * self.cell_size < pos[1] + 14 <
                        self.top + (i + 1) * self.cell_size):
                    cell = [i, j]
                    if self.board[i][j] == 1:
                        cell = False
        if draw == 1:
            if self.board[cell[0]][cell[1]] == 0:
                self.board[cell[0]][cell[1]] = 1
            else:
                cell = None
            s_str = [0 for q in range(self.width)]
            for l in range(self.height):
                if sum(self.board[l]) == self.height:
                    self.board[l] = [0 for f in range(self.width)]
                    create_particles()
                for k in range(self.width):
                    s_str[k] += self.board[l][k]
            for t in range(len(s_str)):
                if s_str[t] == self.height:
                    create_particles()
                    for v in range(self.height):
                        self.board[v][t] = 0
        return cell


class MiniField(MainField):
    """this is field with figure which forms random"""
    def create_figure(self):
        # form figure, field
        self.figure = LIST_OF_FIGURES[random.randrange(0, 26)]
        self.board = [[0 for i in range(self.width)] for _ in range(self.height)]
        for e in self.figure:
            self.board[e[0]][e[1]] = 1

    def click(self, x, y):
        # checking the mouse click on the figure
        answer = False
        for i in range(len(self.figure)):
            if (self.left + self.figure[i][1] * 35 <= x <= self.left + self.figure[i][1] * 35 + 35
                    and self.top + self.figure[i][0] * 35 <= y <= self.top + self.figure[i][0] * 35
                    + 35):
                answer = self.figure[i]
                break
        return answer

    def update(self, x, y):
        self.top = y
        self.left = x

    def check_in_field(self):
        # check whether the field falls into the field
        answer = True
        for i in range(len(self.figure)):
            if not board.get_cell((self.left + self.figure[i][1] * 35, self.top + self.figure[i][0] * 35)):
                answer = False
                break
        if answer is True:
            for i in range(len(self.figure)):
                board.get_cell(
                    (self.left + self.figure[i][1] * 35, self.top + self.figure[i][0] * 35), draw=1)
        return answer


screen_rect = (0, 0, 1050, 770)


class Particle(pygame.sprite.Sprite):
    """snowflake class"""
    def __init__(self, pos, dx, dy, n, group):
        super().__init__(group)
        self.fire = [pygame.transform.scale(load_image(f"sn{n}.png", -1), (40, 40))]
        for scale in (12, 16):
            # scale(Surface, (width, height)) -> Surface  # resize to new resolution
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        # falling snowflakes
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # test if two rectangles overlap
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles():
    """random formation of snowflakes"""
    particle_count = 30
    numbers = range(-1, 1)
    numbers2 = range(1, 4)
    for z in range(particle_count):
        Particle((random.choice(range(0, 20)) * 50, random.choice(range(0, 1)) * 50),
                 random.choice(numbers), random.choice(numbers2), random.choice(range(1, 5)),
                 all_sprites)


class BoardOfLevels:
    """the Board noted the passing of the levels"""
    def __init__(self, width, height, top, left):
        self.width = width
        self.height = height
        self.board = [[0 for i in range(width)] for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = 44

    def render(self):
        # draw board if the level is passed it is marked with a tick otherwise a circle
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 182, 193), (self.left + j * self.cell_size,
                                                           self.top + i * self.cell_size,
                                                           self.cell_size, self.cell_size))
                pygame.draw.rect(screen, (220, 20, 60), (self.left + j * self.cell_size,
                                                         self.top + i * self.cell_size,
                                                         self.cell_size, self.cell_size), 1)
                if self.board[i][j] == 0:
                    pygame.draw.circle(screen, (220, 20, 60), (self.left + j * self.cell_size +
                                                               self.cell_size // 2,
                                                               self.top + i * self.cell_size +
                                                               self.cell_size // 2),
                                       self.cell_size // 2, 1)
                elif self.board[i][j] == 1:
                    pygame.draw.line(screen, (220, 20, 60), (self.left + j * self.cell_size,
                                                             self.top + i * self.cell_size),
                                     (self.cell_size // 2 + self.left + j * self.cell_size,
                                      self.cell_size + self.top + i * self.cell_size), 3)
                    pygame.draw.line(screen, (220, 20, 60), (self.cell_size // 2 + self.left +
                                                             j * self.cell_size,
                                                             self.cell_size + self.top +
                                                             i * self.cell_size),
                                     (self.left + j * self.cell_size + self.cell_size,
                                      self.top + i * self.cell_size), 3)

    def get_cell(self, number):
        # mark level is passed
        self.board[number // self.height][number % self.width] = 1

    def zero(self):
        # reset game results
        self.board = [[0 for i in range(self.width)] for _ in range(self.height)]


table = pygame.sprite.Group()
Table(table)
board_of_levels = BoardOfLevels(3, 3, 270, 730)
images = pygame.sprite.Group()
ChristmasImage(images)
all_sprites = pygame.sprite.Group()
beaker1 = pygame.sprite.Group()
Beaker(beaker1)


def play(f=0):
    """main function of the game"""
    global board, count, all_sprites, board_of_levels, images, level
    # set the main elements and variables
    board = MainField(15, 15, 35, 35, (221, 128, 204), (75, 0, 130), 0, 1)
    miniboardone = MiniField(5, 5, 560, 35, (65, 105, 225), (75, 0, 130), 1, 0)
    miniboardtwo = MiniField(5, 5, 560, 180, (65, 105, 225), (75, 0, 130), 1, 0)
    miniboardthree = MiniField(5, 5, 560, 385, (65, 105, 225), (75, 0, 130), 1, 0)
    if f == 1:
        board_of_levels.zero()
        for e in images:
            e.zero()
    all_sprites = pygame.sprite.Group()
    running = True
    count = 0
    r1one = 0
    r2one = 0
    fone = 0
    r1two = 0
    r2two = 0
    ftwo = 0
    r1three = 0
    r2three = 0
    fthree = 0
    miniboardone.create_figure()
    miniboardtwo.create_figure()
    miniboardthree.create_figure()
    counter = (level + 1) * 60
    text = f'{level + 1}:00'.rjust(5)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('', 45)
    font2 = pygame.font.SysFont('', 55)
    pygame.display.flip()
    # the main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            if event.type == pygame.USEREVENT:
                counter -= 1
                minutes = counter % 60
                if len(str(minutes)) < 2:
                    minutes = '0' + str(minutes)
                else:
                    minutes = str(minutes)
                text = (str(counter // 60) + ':' + minutes).rjust(3) if counter > 0 else stop()
            if event.type == pygame.MOUSEBUTTONUP:
                for j in all_sprites:
                    for t in mouse1:
                        if pygame.sprite.collide_rect(j, t):
                            j.kill()
                            count += 1
            if event.type == pygame.MOUSEBUTTONDOWN and miniboardone.click(event.pos[0], event.pos[1]):
                r1one = event.pos[0] - 35
                r2one = event.pos[1] - 560
                fone = 1
            if event.type == pygame.MOUSEBUTTONDOWN and miniboardtwo.click(event.pos[0], event.pos[1]):
                r1two = event.pos[0] - 180
                r2two = event.pos[1] - 560
                ftwo = 1
            if event.type == pygame.MOUSEBUTTONDOWN and miniboardthree.click(event.pos[0], event.pos[1]):
                r1three = event.pos[0] - 385
                r2three = event.pos[1] - 560
                fthree = 1
            if event.type == pygame.MOUSEMOTION and fone == 1:
                xone = event.pos[0] - r1one
                yone = event.pos[1] - r2one
                miniboardone.update(xone, yone)
            if event.type == pygame.MOUSEMOTION and ftwo == 1:
                xtwo = event.pos[0] - r1two
                ytwo = event.pos[1] - r2two
                miniboardtwo.update(xtwo, ytwo)
            if event.type == pygame.MOUSEMOTION and fthree == 1:
                xthree = event.pos[0] - r1three
                ythree = event.pos[1] - r2three
                miniboardthree.update(xthree, ythree)
            if event.type == pygame.MOUSEBUTTONUP:
                if fone == 1:
                    xone = 35
                    fone = 0
                    yone = 560
                    r1one = 0
                    r2one = 0
                    if miniboardone.check_in_field() is True:
                        miniboardone.update(xone, yone)
                        miniboardone.create_figure()
                    else:
                        miniboardone.update(xone, yone)
                if ftwo == 1:
                    xtwo = 180
                    ftwo = 0
                    ytwo = 560
                    r1two = 0
                    r2two = 0
                    if miniboardtwo.check_in_field() is True:
                        miniboardtwo.update(xtwo, ytwo)
                        miniboardtwo.create_figure()
                    else:
                        miniboardtwo.update(xtwo, ytwo)
                if fthree == 1:
                    xthree = 385
                    fthree = 0
                    ythree = 560
                    r1three = 0
                    r2three = 0
                    if miniboardthree.check_in_field() is True:
                        miniboardthree.update(xthree, ythree)
                        miniboardthree.create_figure()
                    else:
                        miniboardthree.update(xthree, ythree)
        # updating and drawing elements
        screen.fill((65, 105, 225))
        board.render()
        miniboardone.render()
        miniboardtwo.render()
        miniboardthree.render()
        table.draw(screen)
        board_of_levels.render()
        images.draw(screen)
        screen.blit(font.render(text, True, (75, 0, 130)), (640, 35))
        screen.blit(font2.render(str(count), True, (75, 0, 130)), (690, 100))
        all_sprites.draw(screen)
        mouse1.update()
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.flip()
        # check on win
        win()


start_screen()
play()
pygame.quit()
# final version
