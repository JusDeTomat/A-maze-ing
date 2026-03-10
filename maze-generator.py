#!/usr/bin/env python3
import random 

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


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

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
                if not self.grid[nx][ny].visited:
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
    

    def generate(self, start_x=0, start_y=0):
        stack = []
        current_cell = (start_x, start_y)

        self.grid[start_x][start_y].visited = True
        stack.append(current_cell)

        while (stack):
            x, y = stack[-1]
            neighbors = self.get_neighbors(x, y)

            if neighbors:
                direction, nx, ny = random.choice(neighbors)
                self.remove_wall(x, y, direction)
                self.grid[nx][ny].visited = True
                stack.append((nx, ny))
            else:
                stack.pop()

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                cell_value = 0
                if self.grid[x][y].walls["N"] == True:
                    cell_value += 8
                if self.grid[x][y].walls["E"] == True:
                    cell_value += 4
                if self.grid[x][y].walls["S"] == True:
                    cell_value += 2
                if self.grid[x][y].walls["W"] == True:
                    cell_value += 1
                print(f"{cell_value:X}", end="")
            print()

    def display_ascii(self):
        print("+" + "---+" * self.width)

        for y in range(self.height):
            line1 = "|"
            for x in range(self.width):
                if self.grid[y][x].walls["E"]:
                    line1 += "   |"
                else:
                    line1 += "    "
            print(line1)
            line2 = "+"
            for x in range(self.width):
                if self.grid[y][x].walls["S"]:
                    line2 += "---+"
                else:
                    line2 += "   +"

            print(line2)


def main():
    maze = Maze(100, 100)
    maze.generate()
    maze.display_ascii()

if __name__ == "__main__":
    main()