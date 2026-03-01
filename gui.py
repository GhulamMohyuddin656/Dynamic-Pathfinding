# gui.py

import pygame
import random
import time
from search import a_star, rbfs, HEURISTICS

pygame.init()
FONT = pygame.font.SysFont("consolas", 16)

CELL = 25
MARGIN = 2
SIDEBAR = 300
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)
WALL = (40,40,40)
START = (0,200,255)
GOAL = (255,80,80)
PATH = (0,200,0)
AGENT = (255,140,0)
UI_BG = (240,240,240)

class GUI:
    def __init__(self, rows=20, cols=25):
        self.rows = rows
        self.cols = cols
        self.width = cols*(CELL+MARGIN)+SIDEBAR
        self.height = rows*(CELL+MARGIN)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dynamic Pathfinding")

        self.clock = pygame.time.Clock()

        self.grid = [[0]*cols for _ in range(rows)]
        self.start = (0,0)
        self.goal = (rows-1, cols-1)

        self.algorithm = "A*"
        self.heuristic_names = list(HEURISTICS.keys())
        self.h_index = 0

        self.dynamic_mode = False
        self.spawn_prob = 0.02
        self.random_density = 0.3

        self.agent_pos = self.start
        self.path = None
        self.running = False

        self.nodes = 0
        self.cost = 0
        self.time_ms = 0

        self.last_move = 0
        self.move_delay = 0.15

    def random_maze(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) in (self.start, self.goal):
                    self.grid[r][c] = 0
                else:
                    self.grid[r][c] = 1 if random.random() < self.random_density else 0
        self.reset()

    def reset(self):
        self.path = None
        self.agent_pos = self.start
        self.running = False

    def compute_path(self):
        heuristic = HEURISTICS[self.heuristic_names[self.h_index]]

        if self.algorithm == "A*":
            self.path, self.nodes, self.time_ms = a_star(self.agent_pos, self.goal, self.grid, heuristic)
        else:
            self.path, self.nodes, self.time_ms = rbfs(self.agent_pos, self.goal, self.grid, heuristic)

        self.cost = len(self.path)-1 if self.path else 0

    def spawn_obstacles(self):
        for _ in range(3):
            if random.random() < self.spawn_prob:
                r = random.randrange(self.rows)
                c = random.randrange(self.cols)
                if (r,c) not in (self.start, self.goal, self.agent_pos):
                    self.grid[r][c] = 1

    def draw_grid(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x = c*(CELL+MARGIN)
                y = r*(CELL+MARGIN)
                rect = pygame.Rect(x,y,CELL,CELL)

                if (r,c) == self.start:
                    color = START
                elif (r,c) == self.goal:
                    color = GOAL
                elif (r,c) == self.agent_pos:
                    color = AGENT
                elif self.path and (r,c) in self.path:
                    color = PATH
                elif self.grid[r][c] == 1:
                    color = WALL
                else:
                    color = WHITE

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.screen.fill(UI_BG)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = pygame.mouse.get_pos()

                    if mx < self.cols*(CELL+MARGIN):
                        r = my//(CELL+MARGIN)
                        c = mx//(CELL+MARGIN)
                        if (r,c) not in (self.start,self.goal):
                            self.grid[r][c] ^= 1
                            self.reset()
                    else:
                        # buttons
                        y = my
                        if 10<y<40:
                            self.random_maze()
                        elif 50<y<80:
                            self.grid = [[0]*self.cols for _ in range(self.rows)]
                            self.reset()
                        elif 90<y<120:
                            self.algorithm = "RBFS" if self.algorithm=="A*" else "A*"
                            self.reset()
                        elif 130<y<160:
                            self.h_index = (self.h_index+1)%len(self.heuristic_names)
                            self.reset()
                        elif 170<y<200:
                            self.dynamic_mode = not self.dynamic_mode
                        elif 210<y<240:
                            self.compute_path()
                            if self.path:
                                self.running = True
                                self.agent_pos = self.start
                                self.last_move = time.time()

            # Agent movement
            if self.running:
                now = time.time()
                if now - self.last_move > self.move_delay:
                    self.last_move = now

                    if self.dynamic_mode:
                        self.spawn_obstacles()

                    if not self.path or len(self.path)<2:
                        self.running=False
                    else:
                        next_cell = self.path[1]
                        if self.grid[next_cell[0]][next_cell[1]]==1:
                            self.compute_path()
                        else:
                            self.agent_pos = next_cell
                            if self.agent_pos == self.goal:
                                self.running=False
                            else:
                                self.compute_path()

            self.draw_grid()

            # Sidebar text
            x0 = self.cols*(CELL+MARGIN)+20
            self.screen.blit(FONT.render("Random Maze",True,BLACK),(x0,10))
            self.screen.blit(FONT.render("Clear Grid",True,BLACK),(x0,50))
            self.screen.blit(FONT.render(f"Algorithm: {self.algorithm}",True,BLACK),(x0,90))
            self.screen.blit(FONT.render(f"Heuristic: {self.heuristic_names[self.h_index]}",True,BLACK),(x0,130))
            self.screen.blit(FONT.render(f"Dynamic Mode: {self.dynamic_mode}",True,BLACK),(x0,170))
            self.screen.blit(FONT.render("Start Agent",True,BLACK),(x0,210))

            self.screen.blit(FONT.render(f"Nodes: {self.nodes}",True,BLACK),(x0,260))
            self.screen.blit(FONT.render(f"Cost: {self.cost}",True,BLACK),(x0,290))
            self.screen.blit(FONT.render(f"Time: {self.time_ms:.2f} ms",True,BLACK),(x0,320))

            pygame.display.flip()

def launch():
    GUI().run()