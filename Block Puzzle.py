import os
import pygame
import random
import sys


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

pygame.init()
screen = pygame.display.set_mode([1050, 770])
screen.fill((0, 0, 0))
count = 0
FPS = 50
board = None
GRAVITY = 0.005
clock = pygame.time.Clock()


class Mouse_my(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        self.rect.x = random.randrange(1050)
        self.rect.y = random.randrange(770)

    def update(self):
        self.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))


mouse1 = pygame.sprite.Group()
Mouse_my(mouse1)


def print_rules():
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
    fon = load_image('rules.png', 1)
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
        intro_rect.x = 100
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
    pygame.quit()
    sys.exit()


def start_screen():
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
                        rects[1].height):
                    return
                if (rects[0].left <= pygame.mouse.get_pos()[0] <= rects[0].left + rects[0].width and
                        rects[0].top <= pygame.mouse.get_pos()[1] <= rects[0].top +
                        rects[0].height):
                    print_rules()
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
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
    intro_text = ["Unfortunately, time is up!", "Restart", 'Game rules']
    fon = load_image('stop.png', 2)
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if (rects[1].left <= pygame.mouse.get_pos()[0] <= rects[1].left + rects[1].width and
                        rects[1].top <= pygame.mouse.get_pos()[1] <= rects[1].top +
                        rects[1].height):
                    play()
                if (rects[2].left <= pygame.mouse.get_pos()[0] <= rects[2].left + rects[2].width and
                        rects[2].top <= pygame.mouse.get_pos()[1] <= rects[2].top +
                        rects[2].height):
                    print_rules()
        pygame.display.flip()
        clock.tick(FPS)


def win(count):
    global all_sprites
    if count >= 10:
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


class Cuboc(pygame.sprite.Sprite):
    def __init__(self, group):
        self.image = pygame.transform.scale(load_image('kubok2.png', -1), (50, 50))
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = 610
        self.rect.y = 80


class MainField:
    # создание поля
    def __init__(self, width, height, top, left, color1, color2, prozr=0, lines=0):
        self.width = width
        self.height = height
        self.board = [[0 for i in range(width)] for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = 35
        self.color1 = color1
        self.color2 = color2
        self.lines = lines
        self.p = prozr

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0 and self.p == 0:
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
    def create_figure(self):
        p = random.randrange(0, 26)
        self.figure = LIST_OF_FIGURES[p]
        self.board = [[0 for i in range(self.width)] for _ in range(self.height)]
        for e in self.figure:
            self.board[e[0]][e[1]] = 1

    def click(self, x, y):
        otvet = False
        for i in range(len(self.figure)):
            if (self.left + self.figure[i][1] * 35 <= x <= self.left + self.figure[i][1] * 35 + 35
                    and self.top + self.figure[i][0] * 35 <= y <= self.top + self.figure[i][0] * 35
                    + 35):
                otvet = self.figure[i]
                break
        return otvet

    def update(self, x, y):
        self.top = y
        self.left = x

    def check_in_field(self):
        otvet = True
        for i in range(len(self.figure)):
            if not board.get_cell((self.left + self.figure[i][1] * 35, self.top + self.figure[i][0] * 35)):
                otvet = False
                break
        if otvet is True:
            for i in range(len(self.figure)):
                board.get_cell(
                    (self.left + self.figure[i][1] * 35, self.top + self.figure[i][0] * 35), draw=1)
        return otvet


screen_rect = (0, 0, 1050, 770)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, n, group):
        super().__init__(group)
        self.fire = [pygame.transform.scale(load_image(f"sn{n}.png", -1), (40, 40))]
        for scale in (12, 16):
            # scale(Surface, (width, height)) -> Surface  # resize to new resolution
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]  # скорости по осям координат
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity  # ускорение
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # test if two rectangles overlap
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles():
    particle_count = 30
    numbers = range(-1, 1)
    numbers2 = range(1, 4)  # скорости на выбор
    for z in range(particle_count):
        Particle((random.choice(range(0, 20)) * 50, random.choice(range(0, 1)) * 50),
                 random.choice(numbers), random.choice(numbers2), random.choice(range(1, 5)),
                 all_sprites)


start_screen()
all_sprites = pygame.sprite.Group()
cubok1 = pygame.sprite.Group()
Cuboc(all_sprites)


def play():
    global board, count, all_sprites
    board = MainField(15, 15, 35, 35, (221, 128, 204), (75, 0, 130), prozr=0, lines=1)
    miniboardone = MiniField(5, 5, 560, 35, (65, 105, 225), (75, 0, 130), prozr=1, lines=0)
    miniboardtwo = MiniField(5, 5, 560, 180, (65, 105, 225), (75, 0, 130), prozr=1, lines=0)
    miniboardthree = MiniField(5, 5, 560, 385, (65, 105, 225), (75, 0, 130), prozr=1, lines=0)
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
    counter = 60
    text = '1:00'.rjust(5)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('', 45)
    font2 = pygame.font.SysFont('', 55)
    pygame.display.flip()
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
        screen.fill((65, 105, 225))
        board.render()
        miniboardone.render()
        miniboardtwo.render()
        miniboardthree.render()
        screen.blit(font.render(text, True, (75, 0, 130)), (640, 35))
        screen.blit(font2.render(str(count), True, (75, 0, 130)), (690, 100))
        all_sprites.draw(screen)
        mouse1.update()
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.flip()
        win(count)


play()
pygame.quit()
