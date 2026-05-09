import pygame
import sys

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

COLOR_WALL = (44, 62, 80)
COLOR_PATH = (236, 240, 241)
COLOR_CAT = (231, 76, 60)
COLOR_MOUSE = (52, 152, 219)
COLOR_GRID = (189, 195, 199)


class Environment:
    def __init__(self):

        self.grid = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]


        self.cat_pos = [0, 0]
        self.mouse_pos = [GRID_W - 1, GRID_H - 1]

    def draw(self, surface):
        for y in range(GRID_H):
            for x in range(GRID_W):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = COLOR_WALL if self.grid[y][x] == 1 else COLOR_PATH
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, COLOR_GRID, rect, 1)


        cat_rect = pygame.Rect(self.cat_pos[0] * CELL_SIZE + 5, self.cat_pos[1] * CELL_SIZE + 5, CELL_SIZE - 10,
                               CELL_SIZE - 10)
        pygame.draw.ellipse(surface, COLOR_CAT, cat_rect)


        mouse_rect = pygame.Rect(self.mouse_pos[0] * CELL_SIZE + 5, self.mouse_pos[1] * CELL_SIZE + 5, CELL_SIZE - 10,
                                 CELL_SIZE - 10)
        pygame.draw.ellipse(surface, COLOR_MOUSE, mouse_rect)

    def set_wall(self, pos, value):
        x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        if 0 <= x < GRID_W and 0 <= y < GRID_H:
            self.grid[y][x] = value

    def move_agent(self, agent_pos, dx, dy):
        new_x = agent_pos[0] + dx
        new_y = agent_pos[1] + dy
        if 0 <= new_x < GRID_W and 0 <= new_y < GRID_H:
            if self.grid[new_y][new_x] == 0:
                agent_pos[0] = new_x
                agent_pos[1] = new_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cat & Mouse")
    clock = pygame.time.Clock()
    env = Environment()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: env.move_agent(env.cat_pos, 0, -1)
                if event.key == pygame.K_s: env.move_agent(env.cat_pos, 0, 1)
                if event.key == pygame.K_a: env.move_agent(env.cat_pos, -1, 0)
                if event.key == pygame.K_d: env.move_agent(env.cat_pos, 1, 0)

                if event.key == pygame.K_UP:    env.move_agent(env.mouse_pos, 0, -1)
                if event.key == pygame.K_DOWN:  env.move_agent(env.mouse_pos, 0, 1)
                if event.key == pygame.K_LEFT:  env.move_agent(env.mouse_pos, -1, 0)
                if event.key == pygame.K_RIGHT: env.move_agent(env.mouse_pos, 1, 0)

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            env.set_wall(pygame.mouse.get_pos(), 1)
        if mouse_buttons[2]:
            env.set_wall(pygame.mouse.get_pos(), 0)


        screen.fill(COLOR_PATH)
        env.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()