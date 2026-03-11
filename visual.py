#!/usr/bin/env python3
from mlx import Mlx
import random
from maze_generator import Maze, Cell

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
    def __init__(self):
        self.mlx = None
        self.mlx_ptr = None
        self.win = None
        self.maze_size = (0, 0)
        self.img_png = {}
        self.scene_nb = 0
        self.button = {}
        self.click = 0
        self.maze = 0
        self.size = 0
        self.i_color = 0
        self.color_maze = 0xFFFFFF00
        self.color_back = 0xFFBDC3C7
        self.color_icon = 0xFF2ECC71
        self.wall_size = 1

    def add_img(self, name):
        self.img_png[name] = ImgData()

    def close_win(self, _):
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def load_image_pgn(self, name):
        self.add_img(name)
        result = self.mlx.mlx_png_file_to_image(self.mlx_ptr, name)
        self.img_png[name].img, self.img_png[name].width, self.img_png[name].height = result
        self.img_png[name].data, self.img_png[name].bpp, self.img_png[name].sl, self.img_png[name].iformat = self.mlx.mlx_get_data_addr(self.img_png[name].img)

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
                (0xFF000000, 0xFFFFFFFF),

                (0xFF2C3E50, 0xFFECF0F1),
                (0xFF34495E, 0xFFBDC3C7),

                (0xFF1F618D, 0xFFD6EAF8),
                (0xFF154360, 0xFFA9CCE3),

                (0xFF145A32, 0xFFD4EFDF),
                (0xFF196F3D, 0xFFA9DFBF),

                (0xFF7D6608, 0xFFFCF3CF),
                (0xFF7E5109, 0xFFFAD7A0),

                (0xFF641E16, 0xFFF5B7B1),
                (0xFF922B21, 0xFFFADBD8),

                (0xFF4A235A, 0xFFE8DAEF),
                (0xFF5B2C6F, 0xFFD7BDE2),

                (0xFF17202A, 0xFFD5DBDB),
                (0xFF212F3C, 0xFFEAECEE),

                (0xFF0B5345, 0xFFD1F2EB),
                (0xFF0E6251, 0xFFA3E4D7)
            ]
        self.i_color += 1
        if (self.i_color >= len(colors)):
            self.i_color = 0
        self.color_maze = colors[self.i_color][1]
        self.color_back = colors[self.i_color][0]

    def scene(self, _):
        if (self.scene_nb == 0):
            # self.draw_back()
            aff_maze(self, self.maze)
            self.scene_nb = 1
        if (self.scene_nb == 1):
            if self.check("show_path"):
                self.scene_nb = 0
            if self.check("exit"):
                self.close_win(None)
            if self.check("color_maze"):
                self.change_color()
                self.scene_nb = 0
            if self.check("generate"):
                self.scene_nb = 0

    def draw_back(self):
        for y in range((self.size // 2), self.maze_size[0] * self.size + (self.size // 2)):
            for x in range((self.size // 2), self.maze_size[1] * self.size + (self.size // 2)):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win,
                                       x,
                                       y,
                                       self.color_back)

    def print_wall_W(self, x, y):
        for i in range(self.size):
            for j in range(self.wall_size):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win,
                                       (x - (self.size // 2)) + i,
                                       y - (self.size // 2) + j,
                                       self.color_maze)

    def print_wall_S(self, x, y):
        for i in range(self.size):
            for j in range(self.wall_size):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win,
                                       x + (self.size // 2) - j,
                                       (y - (self.size // 2)) + i,
                                       self.color_maze)

    def print_wall_E(self, x, y):
        for i in range(self.size):
            for j in range(self.wall_size):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win,
                                       (x - (self.size // 2)) + i,
                                       y + (self.size // 2) - j,
                                       self.color_maze)

    def print_wall_N(self, x, y):
        for i in range(self.size):
            for j in range(self.wall_size):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win,
                                       x - (self.size // 2) + j,
                                       (y - (self.size // 2)) + i,
                                       self.color_maze)

    def print_icon(self, x, y):
        i = 0
        j = 0
        while ((y - (self.size // 2)) + i <= y + (self.size // 2)):
            j = 0
            while ((x - (self.size // 2) + j <= x + (self.size // 2))):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win,
                                       (x - (self.size // 2)) + j,
                                       (y - (self.size // 2)) + i,
                                       self.color_icon)
                j += 1
            i += 1

    def cal_size(self, x, y):
        i = 0
        while (x * i <= int(1900 * 0.75) and y * i <= 900):
            i += 1
        self.wall_size = (i - 1) // 8
        if self.wall_size <= 0:
            self.wall_size = 1
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
                    app.print_wall_W(x, y)
                if walls is not None and walls.get("E", False):
                    app.print_wall_S(x, y)
                if walls is not None and walls.get("S", False):
                    app.print_wall_E(x, y)
                if walls is not None and walls.get("W", False):
                    app.print_wall_N(x, y)
            else:
                app.print_icon(x, y)
            x += app.size
        x = app.size
        y += app.size


def main():
    app = App()
    app.mlx = Mlx()
    app.mlx_ptr = app.mlx.mlx_init()
    app.maze_size = (30, 30)
    app.size = app.cal_size(app.maze_size[0], app.maze_size[1])
    app.win_size = app.cal_win_size()
    print(app.win_size)
    app.win = app.mlx.mlx_new_window(app.mlx_ptr, app.win_size[0], app.win_size[1], "A-maze-ing")
    app.button["generate"] = Button(app.mlx, app.mlx_ptr, app.win, 350, 400,
                                    150, 60, "Generate")
    app.button["show_path"] = Button(app.mlx, app.mlx_ptr, app.win,
                                     int(app.win_size[0] - 225),
                                     int((app.win_size[1] // 2) - 55),
                                     150, 50, "Show Path"
                                     )
    app.button["color_maze"] = Button(app.mlx, app.mlx_ptr, app.win,
                                      int(app.win_size[0] - 225),
                                      int((app.win_size[1] // 2)),
                                      150, 50, "Change Color"
                                      )
    app.button["generate"] = Button(app.mlx, app.mlx_ptr, app.win,
                                    int(app.win_size[0] - 225),
                                    int((app.win_size[1] // 2) - 110),
                                    150, 50, "Generate"
                                    )
    app.button["exit"] = Button(app.mlx, app.mlx_ptr, app.win,
                                int(app.win_size[0] - 225),
                                int(app.win_size[1] - 95),
                                150, 50, "Exit"
                                )
    maze = Maze(app.maze_size[0], app.maze_size[1], None)
    maze.generate_perfect()
    maze.solve()
    app.maze = maze.grid
    app.mlx.mlx_mouse_hook(app.win, mouse_hook, app)
    app.mlx.mlx_loop_hook(app.mlx_ptr, app.scene, app)
    app.mlx.mlx_hook(app.win, 33, 0, app.close_win, None)

    app.mlx.mlx_loop(app.mlx_ptr)


if (__name__ == "__main__"):
    main()
