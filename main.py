import pygame
import sys
import random
from pettingzoo import ParallelEnv
from gymnasium import spaces
from labirynth import labirynth

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 30
GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

COLOR_WALL = (44, 62, 80)
COLOR_PATH = (236, 240, 241)
COLOR_CAT = (231, 76, 60)
COLOR_MOUSE = (52, 152, 219)
COLOR_GRID = (189, 195, 199)
COLOR_TEXT = (46, 204, 113)


class CatMouseEnv(ParallelEnv):
    metadata = {"render_modes": ["human"], "name": "cat_mouse_v0"}

    def __init__(self):
        self.possible_agents = ["cat", "mouse"]
        self.grid = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]
        self.action_spaces = {agent: spaces.Discrete(4) for agent in self.possible_agents}
        self.observation_spaces = {
            agent: spaces.Box(low=0, high=max(GRID_W, GRID_H), shape=(4,), dtype=int)
            for agent in self.possible_agents
        }
        self.reset()

    def action_space(self, agent):
        return self.action_spaces[agent]

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        self.cat_pos = [0, 0]
        self.mouse_pos = [GRID_W - 1, GRID_H - 1]
        self.game_over = False

        self.grid = labirynth(GRID_W, GRID_H, 0.3)
        observations = {agent: self._get_obs() for agent in self.agents}
        infos = {agent: {} for agent in self.agents}
        return observations, infos

    def _get_obs(self):
        return [self.cat_pos[0], self.cat_pos[1], self.mouse_pos[0], self.mouse_pos[1]]

    def check_los(self):
        x1, y1 = self.cat_pos
        x2, y2 = self.mouse_pos
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return True
        if dx != 0 and dy != 0 and abs(dx) != abs(dy):
            return False
        step_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
        step_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
        curr_x, curr_y = x1 + step_x, y1 + step_y
        while [curr_x, curr_y] != [x2, y2]:
            if self.grid[curr_y][curr_x] == 1:
                return False
            curr_x += step_x
            curr_y += step_y
        return True

    def step(self, actions):
        if self.game_over:
            return {}, {}, {}, {}, {}

        move_map = {
            0: (0, -1),
            1: (0, 1),
            2: (-1, 0),
            3: (1, 0)
        }

        old_cat_pos = list(self.cat_pos)
        old_mouse_pos = list(self.mouse_pos)

        if "cat" in actions:
            dx, dy = move_map[actions["cat"]]
            self._move_agent(self.cat_pos, dx, dy)

        if "mouse" in actions:
            dx, dy = move_map[actions["mouse"]]
            self._move_agent(self.mouse_pos, dx, dy)

        if self.cat_pos == self.mouse_pos:
            self.game_over = True
        elif self.cat_pos == old_mouse_pos and self.mouse_pos == old_cat_pos:
            self.game_over = True
            self.mouse_pos = list(self.cat_pos)

        observations = {agent: self._get_obs() for agent in self.agents}
        rewards = {agent: 0.0 for agent in self.agents}
        terminations = {agent: self.game_over for agent in self.agents}
        truncations = {agent: False for agent in self.agents}
        infos = {agent: {} for agent in self.agents}

        if self.game_over:
            self.agents = []

        return observations, rewards, terminations, truncations, infos

    def _move_agent(self, agent_pos, dx, dy):
        new_x = agent_pos[0] + dx
        new_y = agent_pos[1] + dy
        if 0 <= new_x < GRID_W and 0 <= new_y < GRID_H:
            if self.grid[new_y][new_x] == 0:
                agent_pos[0] = new_x
                agent_pos[1] = new_y

    def set_wall(self, pos, value):
        if self.game_over: return
        x, y = pos[0] // CELL_SIZE, pos[1] // CELL_SIZE
        if 0 <= x < GRID_W and 0 <= y < GRID_H:
            if [x, y] != self.cat_pos and [x, y] != self.mouse_pos:
                self.grid[y][x] = value

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

        if self.game_over:
            font = pygame.font.SysFont('Arial', 40, bold=True)
            text_surface = font.render("Cat wins", True, COLOR_TEXT)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            shadow_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(surface, (0, 0, 0), shadow_rect)
            surface.blit(text_surface, text_rect)

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PettingZoo Multi-Agent Environment")
    clock = pygame.time.Clock()
    env = CatMouseEnv()
    step_timer = 0

  

    move_map = {
        0: (0, -1),
        1: (0, 1),
        2: (-1, 0),
        3: (1, 0)
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    env.reset()

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]: env.set_wall(pygame.mouse.get_pos(), 1)
        if mouse_buttons[2]: env.set_wall(pygame.mouse.get_pos(), 0)

        if not env.game_over:
            step_timer += 1
            if step_timer >= 10:
                has_sight = env.check_los()

                if has_sight:
                    cat_action = env.action_space("cat").sample()
                    min_dist = float('inf')
                    for act, (dx, dy) in move_map.items():
                        nx, ny = env.cat_pos[0] + dx, env.cat_pos[1] + dy
                        if 0 <= nx < GRID_W and 0 <= ny < GRID_H and env.grid[ny][nx] == 0:
                            d = (nx - env.mouse_pos[0]) ** 2 + (ny - env.mouse_pos[1]) ** 2
                            if d < min_dist:
                                min_dist = d
                                cat_action = act

                    mouse_action = env.action_space("mouse").sample()
                    max_dist = -1
                    for act, (dx, dy) in move_map.items():
                        nx, ny = env.mouse_pos[0] + dx, env.mouse_pos[1] + dy
                        if 0 <= nx < GRID_W and 0 <= ny < GRID_H and env.grid[ny][nx] == 0:
                            d = (nx - env.cat_pos[0]) ** 2 + (ny - env.cat_pos[1]) ** 2
                            if d > max_dist:
                                max_dist = d
                                mouse_action = act
                else:
                    cat_action = env.action_space("cat").sample()
                    mouse_action = env.action_space("mouse").sample()

                actions = {"cat": cat_action, "mouse": mouse_action}
                env.step(actions)
                step_timer = 0

        screen.fill(COLOR_PATH)
        env.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()