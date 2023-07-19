import pygame as pg
from pygame_textinput import TextInputVisualizer
from help_func import load_font


FONT = load_font(font_size=30, name='bahnschrift.ttf')


class TextInput(TextInputVisualizer):
    def __init__(self, x, y, w, h, color=(0, 0, 0)):
        r, g, b = color
        super().__init__(font_object=FONT,
                         font_color=color,
                         cursor_blink_interval=400,
                         cursor_color=(255 - r, 255 - g, 255 - b))
        self.rect = pg.Rect(x, y, w, h)
        self.size = 25
        self.active = False
        self.color = color
        self.event_saved = ''
        self.timer = 0
        self.splits = []
        self.rows = []

    def update(self, events):
        if self.event_saved and pg.time.get_ticks() - self.timer > 600:
            pg.time.Clock().tick(40)
            events = [self.event_saved] + events
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_active = self.active
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
                if last_active != self.active:
                    r, g, b = self.cursor_color
                    self.cursor_color = (255 - r, 255 - g, 255 - b)
            elif event.type == pg.KEYDOWN and self.active and not self.event_saved:
                self.event_saved = event
                self.timer = pg.time.get_ticks()
            elif event.type == pg.KEYUP:
                if self.active:
                    if self.event_saved:
                        self.event_saved = ''
                    if event.key == pg.K_RETURN:
                        self.splits.append(len(self.value))
        if self.active:
            self.change_text_box()
            super().update(events)

    def get_rows(self):
        rows = ['']
        v = self.value
        if self.splits and len(v) < self.splits[-1]:
            del self.splits[-1]
        for i in range(len(v)):
            if i in self.splits:
                rows.append('')
            if self.font_object.size(rows[-1] + v[i])[0] <= self.rect.width:
                rows[-1] += v[i]
            else:
                rows.append(v[i])
        # print(rows)
        return rows

    def change_text_box(self):
        rows = self.get_rows()
        if len(rows) * self.size > self.rect.height + 8:
            self.size = int(self.size * 0.9 + 1)
        if len(rows) <= 4:
            self.size = 25
        self.font_object = load_font('bahnschrift.ttf', self.size)
        self.rows = []
        for i in range(len(rows)):
            self.rows.append(self.font_object.render(rows[i], True, self.color))

    def draw(self, screen):
        for i in range(len(self.rows)):
            screen.blit(self.rows[i], (self.rect.x, self.rect.y + i * self.size - 8))
        if self.active:
            c = 50, 230, 120
        else:
            c = self.color
        k = 2
        pg.draw.rect(screen, c, (self.rect.x - k, self.rect.y - k, self.rect.w + k + 1, self.rect.h + k + 1), 2)
