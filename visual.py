#!/usr/bin/env python3
from mlx import Mlx
from maze_generator import Maze
import time


class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0
        self.bpp = 0
        self.iformat = 0

    def put_pixel(self, x, y, color):
        offset = y * self.sl + x * (self.bpp // 8)
        self.data[offset + 0] = color & 0xFF
        self.data[offset + 1] = (color >> 8) & 0xFF
        self.data[offset + 2] = (color >> 16) & 0xFF
        self.data[offset + 3] = (color >> 24) & 0xFF


class Button:

    def __init__(self, mlx, mlx_ptr, win, x, y, w, h, text):
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win = win
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.pressed = False
        self.hover = False

    def draw(self):
        color = 0xFF00AAFF if not self.hover else 0xFF005577
        for i in range(self.w):
            for j in range(self.h):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr,
                    self.win,
                    self.x + i,
                    self.y + j,
                    color
                )

        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win,
            self.x + (self.w // 2 - len(self.text) * 5),
            self.y + 15,
            0xFFFFFFFF,
            self.text
        )

    def contains(self, mx, my):
        return (
            self.x <= mx <= self.x + self.w
            and
            self.y <= my <= self.y + self.h
        )

    def click(self, button, mx, my):
        if button == 1 and self.contains(mx, my):
            self.pressed = True
        else:
            self.pressed = False
        return self.pressed

    def update_hover(self, mx, my):
        if self.contains(mx, my):
            self.hover = True
            self.draw()
        else:
            self.hover = False
            self.draw()


class App:
    def __init__(self, maze: Maze):
        self.mlx = None
        self.mlx_ptr = None
        self.win = None
        self.maze_size = (0, 0)
        self.img = ImgData()
        self.scene_nb = 0
        self.button = {}
        self.click = 0
        self.maze = maze
        self.size = 0
        self.i_color = 0
        self.i_color_42 = 0
        self.path = False
        self.animate = True
        self.during_animate = False
        self.case = (-1, -1)
        self.color_maze = 0xFF1B2631
        self.color_back = 0xFFD6EAF8
        self.color_icon = 0xFF2ECC71
        self.color_path = 0xFFF4D03F
        self.color_start = 0xFFFFFF00
        self.color_end = 0xFFFF6347
        self.wall_size = 1
        self.speed = 1
        self.img_png = {}
        self.win_size = (0, 0)

    def add_img(self, name):
        self.img_png[name] = ImgData()

    def close_win(self, _):
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def load_image(self):
        self.img.img = self.mlx.mlx_new_image(self.mlx_ptr,
                                              (self.maze_size[0] *
                                               self.size) + (self.size),
                                              (self.maze_size[1] *
                                               self.size) + (self.size))
        (self.img.data,
         self.img.bpp,
         self.img.sl,
         self.img.iformat) = self.mlx.mlx_get_data_addr(self.img.img)

    def draw_image(self, name):
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win,
                                         self.img_png[name].img, 0, 0)

    def cal_win_size(self):
        w = 0
        h = 0
        if (self.maze_size[1] * (self.size) + self.size) < 300:
            h = 300
        else:
            h = (self.maze_size[1] * (self.size) + self.size)
        w = int((self.maze_size[0] * (self.size) + self.size))
        return (w + 300, h)

    def check(self, name):
        ret, x, y = self.mlx.mlx_mouse_get_pos(self.win)
        self.button[name].update_hover(x, y)
        if (self.button[name].click(self.click, x, y)):
            self.click = 0
            return True
        return False

    def change_color(self):
        colors = [
            (0xFF1B2631, 0xFFD6EAF8, 0xFFF4D03F),
            (0xFF145A32, 0xFFD4EFDF, 0xFFE74C3C),
            (0xFF4A235A, 0xFFE8DAEF, 0xFF1ABC9C),
            (0xFF154360, 0xFFA9CCE3, 0xFFFF7F50),
            (0xFF641E16, 0xFFF5B7B1, 0xFF2ECC71),
            (0xFF7D6608, 0xFFFCF3CF, 0xFF3498DB),
            (0xFF17202A, 0xFFD5DBDB, 0xFFFF00FF),
            (0xFF0B5345, 0xFFD1F2EB, 0xFFFF8C00),
            (0xFF512E5F, 0xFFD7BDE2, 0xFF00FFFF),

            (0xFF273746, 0xFFEAECEE, 0xFFFF1493),
            (0xFF784212, 0xFFFAD7A0, 0xFF00FF7F),
            (0xFF4D5656, 0xFFEBF5FB, 0xFFFFA500),
            (0xFF7B241C, 0xFFFADBD8, 0xFF7FFF00),
            (0xFF1F618D, 0xFFD6EAF8, 0xFFFF4500),
            (0xFF186A3B, 0xFFA9DFBF, 0xFF8A2BE2),
            (0xFF6E2C00, 0xFFF5CBA7, 0xFF00CED1),
            (0xFF212F3C, 0xFFEAECEE, 0xFFFFD700),
            (0xFF424949, 0xFFF2F4F4, 0xFFADFF2F),
            (0xFF2C3E50, 0xFFECF0F1, 0xFFFF6347)
        ]
        self.i_color += 1
        if (self.i_color >= len(colors)):
            self.i_color = 0
        self.color_maze = colors[self.i_color][1]
        self.color_back = colors[self.i_color][0]
        self.color_path = colors[self.i_color][2]

    def change_42_color(self):
        colors = [
            0xFFFF0000,
            0xFFFF4500,
            0xFFFF6A00,
            0xFFFFA500,
            0xFFFFD700,
            0xFFFFFF00,
            0xFFADFF2F,
            0xFF7FFF00,
            0xFF00FF00,
            0xFF00FF7F,
            0xFF00FFFF,
            0xFF00BFFF,
            0xFF1E90FF,
            0xFF0000FF,
            0xFF4B0082,
            0xFF8A2BE2,
            0xFF9400D3,
            0xFFFF00FF,
            0xFFFF1493,
            0xFFFF69B4,
            0xFFFF007F,
            0xFFFF3F3F,
            0xFFFF7F50,
            0xFFFF8C00,
            0xFFFFE600,
            0xFFBFFF00,
            0xFF32FF32,
            0xFF00FFBF,
            0xFF00E5FF,
            0xFF3399FF
            ]
        self.i_color_42 += 1
        if (self.i_color_42 >= len(colors)):
            self.i_color_42 = 0
        self.color_icon = colors[self.i_color_42]

    def scene(self, _):
        if self.during_animate:
            self.animation()
            self.mlx.mlx_put_image_to_window(self.mlx_ptr,
                                            self.win,
                                            self.img.img,
                                            0,
                                            0
                                            )
            return

        if (self.scene_nb == 0):
            self.draw_back()
            if self.path and not self.during_animate:
                self.maze.solve()
                self.aff_path()
            aff_maze(self, self.maze)
            self.mlx.mlx_put_image_to_window(self.mlx_ptr,
                                             self.win,
                                             self.img.img,
                                             0,
                                             0
                                             )
            self.scene_nb = 1

        if (self.scene_nb == 1):
            if self.check("show_path"):
                if not self.during_animate:
                    if (self.path):
                        self.path = False
                    else:
                        if (self.animate):
                            self.during_animate = True
                        self.path = True
                    self.scene_nb = 0
            if self.check("exit"):
                self.close_win(None)
            if self.check("color_maze"):
                if not self.during_animate:
                    self.change_color()
                    self.scene_nb = 0
            if self.check("generate"):
                if not self.during_animate:
                    maze = Maze(
                        self.maze.width,
                        self.maze.height,
                        self.maze.start,
                        self.maze.end,
                        self.maze.seed,
                        self.maze.perfect
                    )
                    maze.generate()
                    maze.solve()
                    self.maze = maze
                    self.scene_nb = 0
            if self.check("42color"):
                if not self.during_animate:
                    self.change_42_color()
                    self.scene_nb = 0
            self.click = 0

    def animation(self):
        for _ in range(self.speed):
            if (self.case == (-1, -1)):
                self.case = self.maze.start
                x, y = self.case
                for line in self.maze.grid:
                    for case in line:
                        case.visited = False
                self.print_start((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("N", False):
                    self.print_wall_N((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("S", False):
                    self.print_wall_S((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("E", False):
                    self.print_wall_E((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("W", False):
                    self.print_wall_W((x + 1) * self.size, (y + 1) * self.size)
                
            else:
                x, y = self.case
                next_case = self.case
                
                self.print_path((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("N", False):
                    self.print_wall_N((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("S", False):
                    self.print_wall_S((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("E", False):
                    self.print_wall_E((x + 1) * self.size, (y + 1) * self.size)
                if self.maze.grid[y][x].walls.get("W", False):
                    self.print_wall_W((x + 1) * self.size, (y + 1) * self.size)

            if self.case == self.maze.end:
                self.print_end((x + 1) * self.size, (y + 1) * self.size)
                self.during_animate = False
                self.case = (-1, -1)
                for line in self.maze.grid:
                    for case in line:
                        case.visited = False
                self.scene_nb = 0
                break

            if not self.maze.grid[y][x].walls.get("N", False):
                if self.maze.grid[y - 1][x].path and not self.maze.grid[y - 1][x].visited:
                    self.maze.grid[y][x].visited = True
                    next_case = (x, y - 1)
            if not self.maze.grid[y][x].walls.get("S", False):
                if self.maze.grid[y + 1][x].path and not self.maze.grid[y + 1][x].visited:
                    self.maze.grid[y][x].visited = True
                    next_case = (x, y + 1)
            if not self.maze.grid[y][x].walls.get("E", False):
                if self.maze.grid[y][x + 1].path and not self.maze.grid[y][x + 1].visited:
                    self.maze.grid[y][x].visited = True
                    next_case = (x + 1, y)
            if not self.maze.grid[y][x].walls.get("W", False):
                if self.maze.grid[y][x - 1].path and not self.maze.grid[y][x - 1].visited:
                    self.maze.grid[y][x].visited = True
                    next_case = (x - 1, y)
            self.case = next_case

    def draw_back(self):
        for y in range((self.size // 2),
                       (self.maze_size[0] * self.size) + (self.size // 2)):
            for x in range((self.size // 2),
                           (self.maze_size[1] * self.size) + (self.size // 2)):
                self.img.put_pixel(y,
                                   x,
                                   self.color_back)

    def print_wall_N(self, x, y):
        for i in range(self.size + 1):
            for j in range(self.wall_size):
                self.img.put_pixel(
                                   (x - (self.size // 2)) + i,
                                   y - (self.size // 2) + j,
                                   self.color_maze)

    def print_wall_E(self, x, y):
        for i in range(self.size + 1):
            for j in range(self.wall_size):
                self.img.put_pixel(
                                       x + (self.size // 2) - j,
                                       (y - (self.size // 2)) + i,
                                       self.color_maze)

    def print_wall_S(self, x, y):
        for i in range(self.size + 1):
            for j in range(self.wall_size):
                self.img.put_pixel(
                                       (x - (self.size // 2)) + i,
                                       y + (self.size // 2) - j,
                                       self.color_maze)

    def print_wall_W(self, x, y):
        for i in range(self.size + 1):
            for j in range(self.wall_size):
                self.img.put_pixel(
                                       x - (self.size // 2) + j,
                                       (y - (self.size // 2)) + i,
                                       self.color_maze)

    def print_icon(self, x, y):
        i = 0
        j = 0
        while ((y - (self.size // 2)) + i <= y + (self.size // 2)):
            j = 0
            while ((x - (self.size // 2) + j <= x + (self.size // 2))):
                self.img.put_pixel(
                                       (x - (self.size // 2)) + j,
                                       (y - (self.size // 2)) + i,
                                       self.color_icon)
                j += 1
            i += 1

    def print_start(self, x, y):
        i = 0
        j = 0
        while ((y - (self.size // 2)) + i <= y + (self.size // 2)):
            j = 0
            while ((x - (self.size // 2) + j <= x + (self.size // 2))):
                self.img.put_pixel(
                                       (x - (self.size // 2)) + j,
                                       (y - (self.size // 2)) + i,
                                       self.color_start)
                j += 1
            i += 1

    def print_end(self, x, y):
        i = 0
        j = 0
        while ((y - (self.size // 2)) + i <= y + (self.size // 2)):
            j = 0
            while ((x - (self.size // 2) + j <= x + (self.size // 2))):
                self.img.put_pixel(
                                       (x - (self.size // 2)) + j,
                                       (y - (self.size // 2)) + i,
                                       self.color_end)
                j += 1
            i += 1

    def print_path(self, x, y):
        i = 0
        j = 0
        while ((y - (self.size // 2)) + i <= y + (self.size // 2)):
            j = 0
            while ((x - (self.size // 2) + j <= x + (self.size // 2))):
                self.img.put_pixel(
                                       (x - (self.size // 2)) + j,
                                       (y - (self.size // 2)) + i,
                                       self.color_path)
                j += 1
            i += 1

    def aff_path(self):
        x = self.size
        y = self.size
        for line in self.maze.grid:
            for case in line:
                if case.path:
                    self.print_path(x, y)
                x += self.size
            x = self.size
            y += self.size

    def cal_size(self, x, y):
        i = 0
        while (x * i <= int(1900 * 0.75) and y * i <= 800):
            i += 1
        self.wall_size = (i - 1) // 8
        if self.wall_size <= 0:
            self.wall_size = 1
        self.speed = 8 - self.wall_size
        return i - 1


def mouse_hook(button, x, y, app):
    if button == 1:
        app.click = 1
    else:
        app.click = 0


def aff_maze(app, maze):
    x = app.size
    y = app.size

    if hasattr(maze, "grid"):
        grid = maze.grid
    else:
        grid = maze

    app.print_start(
        (app.maze.start[0] + 1) * app.size,
        (app.maze.start[1] + 1) * app.size)
    app.print_end(
        (app.maze.end[0] + 1) * app.size,
        (app.maze.end[1] + 1) * app.size)
    for line in grid:
        for case in line:
            walls = None
            if hasattr(case, "wall"):
                walls = case.wall
            elif hasattr(case, "walls"):
                walls = case.walls

            icon = getattr(case, "icon", False)

            if not icon:
                if walls is not None and walls.get("N", False):
                    app.print_wall_N(x, y)
                if walls is not None and walls.get("E", False):
                    app.print_wall_E(x, y)
                if walls is not None and walls.get("S", False):
                    app.print_wall_S(x, y)
                if walls is not None and walls.get("W", False):
                    app.print_wall_W(x, y)
            else:
                app.print_icon(x, y)
            x += app.size
        x = app.size
        y += app.size


def display_maze(maze):
    app = App(maze)
    app.mlx = Mlx()
    app.mlx_ptr = app.mlx.mlx_init()
    app.maze_size = (maze.width, maze.height)
    app.size = app.cal_size(app.maze_size[0], app.maze_size[1])
    app.win_size = app.cal_win_size()
    app.win = app.mlx.mlx_new_window(app.mlx_ptr,
                                     app.win_size[0],
                                     app.win_size[1],
                                     "A-maze-ing")
    app.button["generate"] = Button(app.mlx, app.mlx_ptr, app.win, 350, 400,
                                    150, 60, "Generate")
    app.button["show_path"] = Button(app.mlx, app.mlx_ptr, app.win,
                                     int(app.win_size[0] - 225),
                                     int((app.win_size[1] // 2) - 30),
                                     150, 50, "Show Path"
                                     )
    app.button["color_maze"] = Button(app.mlx, app.mlx_ptr, app.win,
                                      int(app.win_size[0] - 225),
                                      int((app.win_size[1] // 2) + 25),
                                      150, 50, "Change Color"
                                      )
    app.button["generate"] = Button(app.mlx, app.mlx_ptr, app.win,
                                    int(app.win_size[0] - 225),
                                    int((app.win_size[1] // 2) - 85),
                                    150, 50, "Generate"
                                    )
    app.button["exit"] = Button(app.mlx, app.mlx_ptr, app.win,
                                int(app.win_size[0] - 225),
                                int(app.win_size[1] - 70),
                                150, 50, "Exit"
                                )
    app.button["42color"] = Button(app.mlx, app.mlx_ptr, app.win,
                                   int(app.win_size[0] - 225),
                                   int((app.win_size[1] // 2) - 140),
                                   150, 50, "Change 42 color"
                                   )
    app.load_image()
    app.mlx.mlx_hook(app.win, 4, 1 << 2, mouse_hook, app)
    app.mlx.mlx_loop_hook(app.mlx_ptr, app.scene, app)
    app.mlx.mlx_hook(app.win, 33, 0, app.close_win, None)

    app.mlx.mlx_loop(app.mlx_ptr)
