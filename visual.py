from mlx import Mlx

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
            self.x + len(self.text) * 6,
            self.y + 20,
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
        self.img_png = {}
        self.scene_nb = 0
        self.button = {}
        self.click = 0
        self.maze = 0
        self.size = 0
        self.color_maze = 0xFF000000

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

    def check(self, name):
        ret, x, y = self.mlx.mlx_mouse_get_pos(self.win)
        self.button[name].update_hover(x, y)
        if (self.button[name].click(self.click, x, y)):
            self.click = 0
            return True
        return False

    def scene(self, _):
        if (self.scene_nb == 0):
            self.draw_image("menu.png")
            if self.check("generate"):
                self.scene_nb = 1
        if (self.scene_nb == 1):
            self.draw_image("maze.png")
            aff_maze(self, self.maze)

    def print_wall_N(self, x, y):
        for i in range(self.size):
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, (x - (self.size // 2)) + i, y - (self.size // 2), self.color_maze)

    def print_wall_E(self, x, y):
        for i in range(self.size):
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x + (self.size // 2), (y - (self.size // 2)) + i, self.color_maze)

    def print_wall_S(self, x, y):
        for i in range(self.size):
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, (x - (self.size // 2)) + i, y + (self.size // 2), self.color_maze)

    def print_wall_W(self, x, y):
        for i in range(self.size):
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x - (self.size // 2), (y - (self.size // 2)) + i, self.color_maze)


def mouse_hook(button, x, y, app):
    if button == 1:
        app.click = 1
    else:
        app.click = 0


def aff_maze(app, maze):
    x = app.size
    y = app.size
    for line in maze:
        for case in line:
            if case.wall["N"]:
                app.print_wall_N(x, y)
            if case.wall["E"]:
                app.print_wall_E(x, y)
            if case.wall["S"]:
                app.print_wall_S(x, y)
            if case.wall["W"]:
                app.print_wall_W(x, y)
            x += app.size
        x = app.size
        y += app.size


def cal_size(x, y):
    i = 0
    while (x * i <= 550 and y * i <= 550):
        i += 1
    return i - 1


def main():
    app = App()
    app.mlx = Mlx()
    app.mlx_ptr = app.mlx.mlx_init()
    app.win = app.mlx.mlx_new_window(app.mlx_ptr, 800, 600, "A-maze-ing")
    app.button["generate"] = Button(app.mlx, app.mlx_ptr, app.win, 350, 400,
                                    150, 60, "Generate")
    app.load_image_pgn("menu.png")
    app.load_image_pgn("maze.png")
    app.size = cal_size(30, 20)
    app.maze = generate_maze(30, 20)

    app.mlx.mlx_mouse_hook(app.win, mouse_hook, app)
    app.mlx.mlx_loop_hook(app.mlx_ptr, app.scene, app)
    app.mlx.mlx_hook(app.win, 33, 0, app.close_win, None)

    app.mlx.mlx_loop(app.mlx_ptr)


if (__name__ == "__main__"):
    main()
