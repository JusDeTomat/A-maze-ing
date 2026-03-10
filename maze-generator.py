#!/usr/bin/env python3

config = {
    "width" : 20,
    "height": 20,
    "entry": (0,0),
    "exit": (19,14),
    "output_file": "maze.txt",
    "perfect": True
}

class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    # def maze_generator(self) -> None: