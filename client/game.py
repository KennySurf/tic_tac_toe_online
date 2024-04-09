from pygame import Surface, draw, locals, Vector2, Color
import math
# import lib.request as request
import storage

COLOR_BACKGROUND = "#eeeebe"
COLOR_GRID = "gray"

FIELD_SIZE = 14
FRAME_SIZE = 50


class Game:
    def __init__(self):
        # self.url = "https://httpbin.org/anything"
        # self.data = {"prompt": "Привет от сервера!"}
        self.map = [0] * (FIELD_SIZE * FIELD_SIZE)
        self.temp_clr = Color(0)
        self.cell_size = 0
        self.bg = None
        self.bg_dirty = True

    def update_bg(self):
        if not self.bg or self.bg.get_width() != self.bg_size:
            self.bg = Surface((self.bg_size, self.bg_size))

        self.bg.fill(COLOR_BACKGROUND)
        for i in range(15):
            draw.line(self.bg, 'gray', (i * self.cell_size, 0), (i * self.cell_size, self.bg_size), 2)
            draw.line(self.bg, 'gray', (0, i * self.cell_size), (self.bg_size, i * self.cell_size), 2)

        for cell_id in range(len(self.map)):
            self.draw_cell_bg(cell_id)

        self.bg_dirty = False

    def start(self):
        # self.map = [0] * (FIELD_SIZE * FIELD_SIZE)
        self.new_figures = list()
        self.bg_dirty = True

    def keydown(self, key: int):
        pass
        # request.post(self.url, self.data, self.on_answer)

    def mousedown(self, pos: tuple[int, int], button: int):
        cx = (pos[0] - 1) // self.cell_size
        cy = (pos[1] - 1) // self.cell_size

        self.add_figure(button == 1, (cx, cy))

    def calc_stage_size(self, app_size: tuple[int, int]) -> tuple[int, int]:
        self.cell_size = (min(app_size[0], app_size[1]) - 2) // FIELD_SIZE
        self.bg_size = FIELD_SIZE * self.cell_size + 2
        self.fig_radius = self.cell_size // 3
        self.fig_width = self.cell_size // 6
        self.bg_dirty = True
        return (self.bg_size, self.bg_size)

    def update(self, tick: float):
        for fig in self.new_figures[:]:
            fig['anim'] += tick * 0.0025
            if fig['anim'] >= 1:
                self.draw_cell_bg(fig['cell_id'])
                self.new_figures.remove(fig)

    def draw(self, surface: Surface):
        if self.bg_dirty:
            self.update_bg()
        surface.blit(self.bg, (0, 0))
        for fig in self.new_figures:
            draw_func = self.draw_cross if fig['is_cross'] else self.draw_toe
            draw_func(surface, divmod(fig['cell_id'], FIELD_SIZE), math.sin(fig['anim'] * math.pi))

    def add_figure(self, is_cross: bool, cell: tuple[int, int]) -> bool:
        if 0 > cell[0] >= FIELD_SIZE or 0 > cell[1] >= FIELD_SIZE:
            return False
        cell_id = cell[0] * FIELD_SIZE + cell[1]
        if self.map[cell_id]:
            return False
        self.map[cell_id] = 1 if is_cross else 2
        self.new_figures.append({'anim': 0, 'cell_id': cell_id, 'is_cross': is_cross})
        return True

    def draw_cross(self, surface: Surface, cell: tuple[int, int], spawn_anim: float = 0):
        pt = self.cell_pos(cell)
        self.temp_clr.hsla = (20, 40 + int(spawn_anim * 60), 50 - int(spawn_anim * 30))
        r = self.fig_radius * (1 + spawn_anim)
        lv = 0.3530534 * self.fig_width * (1 + spawn_anim)
        draw.polygon(surface, self.temp_clr, [pt - (r - lv, r + lv), pt - (r + lv, r - lv), pt + (r - lv, r + lv), pt + (r + lv, r - lv)])
        draw.polygon(surface, self.temp_clr, [pt - (r - lv, -r - lv), pt - (r + lv, -r + lv), pt + (r - lv, -r - lv), pt + (r + lv, -r + lv)])

    def draw_toe(self, surface: Surface, cell: tuple[int, int], spawn_anim: float = 0):
        pt = self.cell_pos(cell)
        self.temp_clr.hsla = (100, 40 + int(spawn_anim * 60), 50 - int(spawn_anim * 30))
        draw.circle(surface, self.temp_clr, pt, (self.fig_radius + round(self.fig_width / 2)) * (1 + spawn_anim), int(self.fig_width * (1 + spawn_anim)))

    def draw_cell_bg(self, cell_id: int):
        match self.map[cell_id]:
            case 1:
                self.draw_cross(self.bg, divmod(cell_id, FIELD_SIZE))
            case 2:
                self.draw_toe(self.bg, divmod(cell_id, FIELD_SIZE))

    def cell_pos(self, cell: tuple[int, int]) -> Vector2:
        return Vector2((cell[0] + 0.5) * self.cell_size + 1, (cell[1] + 0.5) * self.cell_size + 1)

    # def on_answer(self, response):
    #    self.ts = storage.font.print_surface(response["json"]["prompt"], "black")
