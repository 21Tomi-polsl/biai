from collections import deque
import random
from tracemalloc import start

from matplotlib.pyplot import grid
import json





def labirynth(GRID_W, GRID_H, wall_break_chance):
    while True:
        grid = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]
        for y in range(GRID_H):
            for x in range(GRID_W):
              if x%2==0 and y%2==0:
                if random.random() > wall_break_chance:
                    grid[y][x] = 1
                if y%3==0 and x%3==0:
                    if random.random() > wall_break_chance:
                        grid[y][x] = 1
                if y%5==0 and x%5==0:
                    if random.random() > wall_break_chance:
                        grid[y][x] = 1 
                if y%7==0 and x%7==0:
                    if random.random() > wall_break_chance:
                        grid[y][x] = 1
        base_grid = [row[:] for row in grid]
        for y in range(GRID_H):
            for x in range(GRID_W):
                if base_grid[y][x] == 1:
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            ny = y + j
                            nx = x + i
                        
                      
                            if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
                                if random.random() > 0.9:
                                    grid[ny][nx] = 1


        for y in range(GRID_H):
            for x in range(GRID_W):
                if y<2 and x<2:
                    grid[y][x] = 0
                if y>GRID_H-3 and x>GRID_W-3:
                    grid[y][x] = 0
        if validate_labirynth(grid,GRID_W, GRID_H):
            add_to_file(grid,"maps.jsonl")
            return grid
def validate_labirynth(grid,GRID_W, GRID_H):
        start = (0, 0)
        end = (GRID_W - 1, GRID_H - 1)
       
        def find_path(current_grid):
            queue = deque([[start]])
            visited = {start}
            while queue:
                    path = queue.popleft()
                    x, y = path[-1]
                    if (x, y) == end:
                        return path
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_W and 0 <= ny < GRID_H and current_grid[ny][nx] == 0 and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            new_path = list(path)
                            new_path.append((nx, ny))
                            queue.append(new_path)
            return None
        
        first_path = find_path(grid)
        if not first_path:
            return False
        temp_grid = [row[:] for row in grid]
        for x, y in first_path:
            if(x,y) != start and (x,y) != end:
                temp_grid[y][x] = 1
        second_path = find_path(temp_grid) 
        if not second_path:
            return False
        return True

def add_to_file(grid, filename="maps.jsonl"):
    
    map_string = json.dumps(grid, separators=(',', ':'))+"\n"

    line_count = 0 
    try:
        with open(filename, 'r') as f:
            for line in f:
                line_count += 1
    except  FileNotFoundError:
        pass
    with open(filename, 'a') as f:
        f.write(map_string)
    return line_count

def load_from_file(index,filename="maps.jsonl"):
    maps = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            if 0<=index < len(lines):
                return json.loads(lines[index])
            else:
                return None 
    except  FileNotFoundError:
        return None