#!/usr/bin/env python3
import sys
from parsing import parsing
from maze_generator import Maze, path_to_directions
from visual import App, display_maze

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config = parsing(config_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        maze = Maze(
            config["WIDTH"],
            config["HEIGHT"],
            config["ENTRY"],
            config["EXIT"],
            config["SEED"],
            config["PERFECT"]
        )

        maze.generate()

        path = maze.solve()

        directions = path_to_directions(path)

        maze.write_output(config["OUTPUT_FILE"], directions)
        
        display_maze(maze)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
