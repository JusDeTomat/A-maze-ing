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
        self.icon = False


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
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
                    # protéger les cellules du logo: icône + marquée comme visitée
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
                # utiliser self.grid[ny][nx] (ligne, colonne)
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

        # grilles indexées [ligne][colonne] => [y][x]
        self.grid[y][x].walls[direction] = False
        self.grid[ny][nx].walls[opposite[direction]] = False
    

    def generate(self, start_x=0, start_y=0):
        stack = []
        current_cell = (start_x, start_y)

        # marquer la cellule de départ correctement (y, x)
        self.grid[start_y][start_x].visited = True
        stack.append(current_cell)

        while (stack):
            x, y = stack[-1]
            neighbors = self.get_neighbors(x, y)

            if neighbors:
                direction, nx, ny = random.choice(neighbors)
                self.remove_wall(x, y, direction)
                # marquer la cellule suivante correctement
                self.grid[ny][nx].visited = True
                stack.append((nx, ny))
            else:
                stack.pop()

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
                if (self.grid[y][x].icon):
                    middle = "x"
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


def main():
    maze = Maze(21, 19)
    maze.generate(10, 10)
    maze.display_ascii()

if __name__ == "__main__":
    main()