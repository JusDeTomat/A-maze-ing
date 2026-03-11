#!/usr/bin/env python3
import random
import sys
from collections import deque

config = {
    "width" : 20,
    "height": 20,
    "entry": (0,0),
    "exit": (19,14),
    "output_file": "maze.txt",
    "perfect": True
}

class Cell:
    def __init__(self):
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }
        self.visited = False
        self.icon = False
        self.path = False


class Maze:
    def __init__(self, width: int, height: int, seed: str) -> None:
        self.width = width
        self.height = height
        self.seed = seed or None
        self.grid = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]
        self.logo = [
            [1,0,0,0,1,1,1],
            [1,0,0,0,0,0,1],
            [1,1,1,0,1,1,1],
            [0,0,1,0,1,0,0],
            [0,0,1,0,1,1,1],
        ]
        start_logo_y = height // 2 - 2
        start_logo_x = width // 2 - 3
        for y in range(len(self.logo)):
            for x in range(len(self.logo[0])):
                if self.logo[y][x]:
                    self.grid[start_logo_y + y][start_logo_x + x].icon = True
                    self.grid[start_logo_y + y][start_logo_x + x].visited = True

    def get_neighbors(self, x, y):
        neighbors = []

        directions = {
            "N": (x, y - 1),
            "E": (x + 1, y),
            "S": (x, y + 1),
            "W": (x - 1, y)
        }

        for direction, (nx, ny) in directions.items():
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.grid[ny][nx].visited and not self.grid[ny][nx].icon:
                    neighbors.append((direction, nx, ny))

        return neighbors
    
    def remove_wall(self, x, y, direction):
        dx = {"E": 1, "W": -1, "N": 0, "S": 0}
        dy = {"E": 0, "W": 0, "N": -1, "S": 1}

        opposite = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        }

        nx = x + dx[direction]
        ny = y + dy[direction]

        self.grid[y][x].walls[direction] = False
        self.grid[ny][nx].walls[opposite[direction]] = False
    

    def generate_perfect(self, start_x=0, start_y=0):
        stack = []
        current_cell = (start_x, start_y)

        if self.seed is not None:
            random.seed(self.seed)

        self.grid[start_y][start_x].visited = True
        stack.append(current_cell)

        while (stack):
            x, y = stack[-1]
            neighbors = self.get_neighbors(x, y)

            if neighbors:
                direction, nx, ny = random.choice(neighbors)
                self.remove_wall(x, y, direction)
                self.grid[ny][nx].visited = True
                stack.append((nx, ny))
            else:
                stack.pop()
    
    def generate_imperfect(self):
        self.generate_perfect()
        if self.seed is not None:
            random.seed(self.seed)
        maze_size = self.height * self.width
        for _ in range(max(1, maze_size // 10)):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            direction = random.choice(["N", "S", "E", "W"])

            dx = {"E": 1, "W": -1, "N": 0, "S": 0}
            dy = {"E": 0, "W": 0, "N": -1, "S": 1}
            nx = x + dx[direction]
            ny = y + dy[direction]

            if not (0 <= nx < self.width and 0 <= ny < self.height):
                continue

            if self.grid[y][x].icon or self.grid[ny][nx].icon:
                continue

            if self.grid[y][x].walls[direction] == True:
                self.remove_wall(x, y, direction)


    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                cell_value = 0
                if self.grid[y][x].walls["N"] == True:
                    cell_value += 1
                if self.grid[y][x].walls["E"] == True:
                    cell_value += 2
                if self.grid[y][x].walls["S"] == True:
                    cell_value += 4
                if self.grid[y][x].walls["W"] == True:
                    cell_value += 8
                print(f"{cell_value:X}", end="")
            print()

    def display_ascii(self):
        print("+" + "---+" * self.width)

        for y in range(self.height):
            line1 = "|"
            for x in range(self.width):
                middle = " "
                # priorité d'affichage: logo (x) > chemin (o)
                if self.grid[y][x].icon:
                    middle = "x"
                elif self.grid[y][x].path:
                    middle = "o"
                if self.grid[y][x].walls["E"]:
                    line1 += f" {middle} |"
                else:
                    line1 += f" {middle}  "
            print(line1)
            line2 = "+"
            for x in range(self.width):
                if self.grid[y][x].walls["S"]:
                    line2 += "---+"
                else:
                    line2 += "   +"

            print(line2)

    def solve(self, start=None, end=None):
        for row in self.grid:
            for cell in row:
                cell.path = False

        sx, sy = start
        ex, ey = end

        if not (0 <= sx < self.width and 0 <= sy < self.height):
            return []
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            return []
        
        q = deque()
        q.append((sx, sy))
        parents = { (sx, sy): None }

        found = False
        while q:
            x, y = q.popleft()
            if (x, y) == (ex, ey):
                found = True
                break

            directions = {
                "N": (0, -1),
                "E": (1, 0),
                "S": (0, 1),
                "W": (-1, 0),
            }
            for d, (dx, dy) in directions.items():
                if not self.grid[y][x].walls[d]:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in parents:
                            parents[(nx, ny)] = (x, y)
                            q.append((nx, ny))

        path_coords = []
        if found:
            cur = (ex, ey)
            while cur is not None:
                path_coords.append(cur)
                cur = parents.get(cur)
            path_coords.reverse()
            for x, y in path_coords:
                self.grid[y][x].path = True

        self.path = path_coords
        return path_coords


def main():
    seed = None
    if len(sys.argv) == 2:
        seed = sys.argv[1]
    maze = Maze(20, 20, seed)
    maze.generate_perfect()
    maze.solve((0,0), (19,19))
    maze.display_ascii()

if __name__ == "__main__":
    main()