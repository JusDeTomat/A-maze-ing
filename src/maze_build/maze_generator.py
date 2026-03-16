#!/usr/bin/env python3
import random
from collections import deque
from typing import List, Tuple, Optional


class Cell:
    """Representation of a single maze cell with walls and state flags."""

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
    """Maze generation, solving and output utilities."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output: str,
        seed: Optional[str],
        perfect: bool,
        animated: bool
    ):

        if not (9 <= width <= 500):
            raise ValueError("The width must be between 9 and 500")

        if not (7 <= height <= 400):
            raise ValueError("The height must be between 7 and 400")

        self.width = width
        self.height = height
        self.start = entry
        self.end = exit
        self.output = output
        self.seed = seed
        self.perfect = perfect
        self.animated = animated
        self.grid = [
            [Cell() for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self.logo = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]
        start_logo_y = self.height // 2 - 2
        start_logo_x = self.width // 2 - 3
        for y in range(len(self.logo)):
            for x in range(len(self.logo[0])):
                if self.logo[y][x]:
                    self.grid[start_logo_y + y][start_logo_x + x].icon = True
                    self.grid[start_logo_y + y][start_logo_x + x].visited = \
                        True

        ex, ey = entry
        ox, oy = exit

        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError("Entry outside maze")

        if not (0 <= ox < width and 0 <= oy < height):
            raise ValueError("Exit outside maze")

        if (self.grid[ey][ex].icon):
            raise ValueError("Entry in the 42 logo")

        if (self.grid[oy][ox].icon):
            raise ValueError("Exit in the 42 logo")

        if entry == exit:
            raise ValueError("Entry and exit cannot be the same")

    def get_neighbors(self, x: int, y: int) -> List[Tuple[str, int, int]]:
        """Return list of unvisited non-icon neighbors as (dir, nx, ny)."""
        neighbors = []

        directions = {
            "N": (x, y - 1),
            "E": (x + 1, y),
            "S": (x, y + 1),
            "W": (x - 1, y)
        }

        for direction, (nx, ny) in directions.items():
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.grid[ny][nx].visited and \
                 not self.grid[ny][nx].icon:
                    neighbors.append((direction, nx, ny))

        return neighbors

    def remove_wall(self, x: int, y: int, direction: str) -> None:
        """Remove the wall between (x,y) and its neighbor in direction."""
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

    def generate_perfect(self, start_x: int = 0, start_y: int = 0) -> None:
        """Generate a perfect maze using DFS backtracker from start cell."""
        stack = []
        current_cell = (start_x, start_y)

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

    def generate_imperfect(self) -> None:
        """Generate an imperfect maze by
           creating additional random openings."""
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

            if self.grid[y][x].walls[direction]:
                self.remove_wall(x, y, direction)

    def generate(self) -> None:
        """Dispatch perfect or imperfect maze generation."""
        if self.perfect:
            self.generate_perfect()
        else:
            self.generate_imperfect()
        print(self.seed)

    def display(self) -> None:
        """Print compact hex representation of the maze to stdout."""
        for y in range(self.height):
            for x in range(self.width):
                cell_value = 0
                if self.grid[y][x].walls["N"]:
                    cell_value += 1
                if self.grid[y][x].walls["E"]:
                    cell_value += 2
                if self.grid[y][x].walls["S"]:
                    cell_value += 4
                if self.grid[y][x].walls["W"]:
                    cell_value += 8
                print(f"{cell_value:X}", end="")
            print()

    def display_ascii(self) -> None:
        """Print a human-readable ASCII representation of the maze."""
        print("+" + "---+" * self.width)

        for y in range(self.height):
            line1 = "|"
            for x in range(self.width):
                middle = " "
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

    def write_output(self, filename: str, path: str) -> None:
        """Write maze hex map, entry, exit and path directions to file."""
        with open(filename, "w") as f:

            for y in range(self.height):

                row = ""

                for x in range(self.width):

                    cell = self.grid[y][x]

                    value = (
                        cell.walls["N"] << 0
                        | cell.walls["E"] << 1
                        | cell.walls["S"] << 2
                        | cell.walls["W"] << 3
                    )

                    row += format(value, "X")

                f.write(row + "\n")

            f.write("\n")

            f.write(f"{self.start[0]},{self.start[1]}\n")
            f.write(f"{self.end[0]},{self.end[1]}\n")
            f.write(path + "\n")

    def solve(self) -> List[Tuple[int, int]]:
        """Solve the maze using BFS and mark
           the path; return list of coords."""
        for row in self.grid:
            for cell in row:
                cell.path = False

        sx, sy = self.start
        ex, ey = self.end

        if not (0 <= sx < self.width and 0 <= sy < self.height):
            return []
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            return []

        q = deque()
        q.append((sx, sy))
        parents = {(sx, sy): None}

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

        path_coords: List[Tuple[int, int]] = []
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


def path_to_directions(path: List[Tuple[int, int]]) -> str:
    """Convert a list of coordinates into direction letters (NESW)."""

    directions = ""

    for i in range(len(path) - 1):

        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        if x2 == x1 + 1:
            directions += "E"
        elif x2 == x1 - 1:
            directions += "W"
        elif y2 == y1 + 1:
            directions += "S"
        elif y2 == y1 - 1:
            directions += "N"

    return directions


def main():
    maze = Maze()
    if getattr(maze, "perfect", True):
        maze.generate_perfect()
    else:
        maze.generate_imperfect()
    maze.solve()
    maze.display_ascii()


if __name__ == "__main__":
    main()
