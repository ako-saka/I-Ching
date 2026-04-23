import math
import random
import sys

import pygame


WIDTH = 900
HEIGHT = 700
FPS = 60
LINE_COUNT = 6

# Page states
PAGE_LANDING = "landing"
PAGE_HEXAGRAM = "hexagram"

BACKGROUND = (245, 239, 226)
TEXT = (44, 38, 28)
ACCENT = (170, 129, 76)
LINE_COLOR = (34, 31, 27)
CIRCLE_FILL = (252, 249, 243)
CIRCLE_OUTLINE = (121, 92, 53)
BUTTON_FILL = (221, 202, 168)
BUTTON_HOVER = (206, 181, 138)
INPUT_BACKGROUND = (255, 255, 255)
INPUT_BORDER = (121, 92, 53)
SKY_TOP = (245, 205, 153)
SKY_BOTTOM = (60, 48, 81)
GLOW = (255, 226, 176)
MIST = (255, 241, 214)
MOUNTAIN_NEAR = (48, 39, 52)
MOUNTAIN_MID = (83, 61, 78)
MOUNTAIN_FAR = (125, 91, 108)
COIN_FRONT = (240, 213, 126)
COIN_BACK = (198, 109, 86)
COIN_EDGE = (128, 72, 44)


class HexagramPrototype:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("I Ching Hexagram Prototype")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("georgia", 28)
        self.small_font = pygame.font.SysFont("georgia", 20)
        self.large_font = pygame.font.SysFont("georgia", 48)
        self.hero_font = pygame.font.SysFont("georgia", 66, bold=True)

        self.circle_radius = 34
        self.line_width = 320
        self.line_height = 16
        self.line_gap = 72
        self.top_margin = 520
        self.coin_radius = 28
        self.animation_duration = 66

        self.circle_centers = self._build_circle_positions()
        self.reset_button = pygame.Rect(WIDTH // 2 - 140, 605, 280, 48)

        # State management
        self.current_page = PAGE_LANDING
        self.query_text = ""
        self.input_text = ""
        self.input_rect = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 10, 500, 60)
        self.submit_button = pygame.Rect(WIDTH // 2 - 105, HEIGHT // 2 + 110, 210, 52)

        # Animation state
        self.animating_line_index = -1
        self.animation_frame = 0
        self.current_cast = []

        self.orbs = self._build_orbs()
        self.stars = self._build_stars()
        self.time = 0.0
        self.cursor_timer = 0

        self._reset_hexagram()

    def set_query(self, query: str) -> None:
        self.query_text = query.strip()
        self.current_page = PAGE_HEXAGRAM
        self._reset_hexagram()

    def _build_circle_positions(self) -> list[tuple[int, int]]:
        centers: list[tuple[int, int]] = []
        start_y = self.top_margin
        for index in range(LINE_COUNT):
            y = start_y - index * self.line_gap
            centers.append((WIDTH // 2, y))
        return centers

    def _build_orbs(self) -> list[dict[str, float]]:
        orbs = []
        for _ in range(10):
            orbs.append(
                {
                    "x": random.uniform(60, WIDTH - 60),
                    "y": random.uniform(50, HEIGHT - 120),
                    "radius": random.uniform(20, 54),
                    "speed": random.uniform(0.35, 0.9),
                    "phase": random.uniform(0, math.tau),
                }
            )
        return orbs

    def _build_stars(self) -> list[dict[str, float]]:
        stars = []
        for _ in range(44):
            stars.append(
                {
                    "x": random.uniform(0, WIDTH),
                    "y": random.uniform(0, HEIGHT * 0.62),
                    "radius": random.uniform(1.0, 2.8),
                    "phase": random.uniform(0, math.tau),
                    "speed": random.uniform(0.8, 2.2),
                }
            )
        return stars

    def _reset_hexagram(self) -> None:
        self.coin_casts: list[list[bool]] = []
        self.hexagram_lines: list[bool] = []
        for _ in range(LINE_COUNT):
            cast = [random.choice([True, False]) for _ in range(3)]
            self.coin_casts.append(cast)
            heads_count = sum(cast)
            self.hexagram_lines.append(heads_count >= 2)

        self.revealed = [False] * LINE_COUNT
        self.animating_line_index = -1
        self.animation_frame = 0
        self.current_cast = []

    def run(self) -> None:
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

    def _update(self) -> None:
        self.time += 1 / FPS
        self.cursor_timer = (self.cursor_timer + 1) % FPS

        if self.animating_line_index >= 0:
            self.animation_frame += 1
            if self.animation_frame >= self.animation_duration:
                self.revealed[self.animating_line_index] = True
                self.animating_line_index = -1
                self.animation_frame = 0
                self.current_cast = []

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.current_page == PAGE_LANDING:
                self._handle_landing_events(event)
            elif self.current_page == PAGE_HEXAGRAM:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_click(event.pos)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.current_page = PAGE_LANDING
                    self.input_text = ""
                    self.query_text = ""
                    self._reset_hexagram()

    def _handle_landing_events(self, event: pygame.event.EventType) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_button.collidepoint(event.pos) and self.input_text.strip():
                self.set_query(self.input_text)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self.set_query(self.input_text)
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable() and len(self.input_text) < 100:
                self.input_text += event.unicode

    def _handle_click(self, position: tuple[int, int]) -> None:
        if self.reset_button.collidepoint(position):
            self._reset_hexagram()
            return

        for index, center in enumerate(self.circle_centers):
            if self.revealed[index] or self.animating_line_index >= 0:
                continue
            if self._point_in_circle(position, center, self.circle_radius):
                self.animating_line_index = index
                self.animation_frame = 0
                self.current_cast = self.coin_casts[index]
                return

    @staticmethod
    def _point_in_circle(
        point: tuple[int, int], center: tuple[int, int], radius: int
    ) -> bool:
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        return dx * dx + dy * dy <= radius * radius

    def _draw(self) -> None:
        self._draw_background()

        if self.current_page == PAGE_LANDING:
            self._draw_landing_page()
        elif self.current_page == PAGE_HEXAGRAM:
            self._draw_hexagram_page()

        pygame.display.flip()

    def _draw_background(self) -> None:
        self._draw_vertical_gradient(SKY_TOP, SKY_BOTTOM)
        self._draw_celestial_body()
        self._draw_stars()
        self._draw_orbs()
        self._draw_mountains()
        self._draw_mist_band()

    def _draw_vertical_gradient(self, top: tuple[int, int, int], bottom: tuple[int, int, int]) -> None:
        for y in range(HEIGHT):
            blend = y / HEIGHT
            color = (
                int(top[0] + (bottom[0] - top[0]) * blend),
                int(top[1] + (bottom[1] - top[1]) * blend),
                int(top[2] + (bottom[2] - top[2]) * blend),
            )
            pygame.draw.line(self.screen, color, (0, y), (WIDTH, y))

    def _draw_celestial_body(self) -> None:
        halo_surface = pygame.Surface((320, 320), pygame.SRCALPHA)
        for radius, alpha in ((120, 35), (90, 55), (65, 85)):
            pygame.draw.circle(halo_surface, (*GLOW, alpha), (160, 120), radius)
        self.screen.blit(halo_surface, (WIDTH // 2 - 160, 20))
        pygame.draw.circle(self.screen, GLOW, (WIDTH // 2, 140), 46)
        pygame.draw.circle(self.screen, (255, 245, 217), (WIDTH // 2 - 12, 128), 8)

    def _draw_stars(self) -> None:
        for star in self.stars:
            pulse = 0.55 + 0.45 * math.sin(self.time * star["speed"] + star["phase"])
            color = (255, 244, 227, int(100 + 120 * pulse))
            star_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(star_surface, color, (5, 5), max(1, int(star["radius"])))
            self.screen.blit(star_surface, (star["x"], star["y"]))

    def _draw_orbs(self) -> None:
        orb_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for orb in self.orbs:
            x = orb["x"] + math.sin(self.time * orb["speed"] + orb["phase"]) * 18
            y = orb["y"] + math.cos(self.time * (orb["speed"] * 0.7) + orb["phase"]) * 10
            alpha = int(26 + 18 * math.sin(self.time * orb["speed"] + orb["phase"]))
            pygame.draw.circle(orb_surface, (*MIST, max(8, alpha)), (int(x), int(y)), int(orb["radius"]))
        self.screen.blit(orb_surface, (0, 0))

    def _draw_mountains(self) -> None:
        drift = math.sin(self.time * 0.25) * 12
        far_points = [
            (-40 + drift, HEIGHT),
            (90 + drift, 360),
            (220 + drift, 430),
            (360 + drift, 290),
            (510 + drift, 420),
            (690 + drift, 300),
            (940 + drift, HEIGHT),
        ]
        mid_points = [
            (-30 - drift, HEIGHT),
            (120 - drift, 420),
            (240 - drift, 350),
            (380 - drift, 455),
            (540 - drift, 330),
            (730 - drift, 440),
            (930 - drift, HEIGHT),
        ]
        near_points = [
            (-30, HEIGHT),
            (110, 520),
            (240, 430),
            (390, 520),
            (520, 405),
            (700, 500),
            (930, HEIGHT),
        ]
        pygame.draw.polygon(self.screen, MOUNTAIN_FAR, far_points)
        pygame.draw.polygon(self.screen, MOUNTAIN_MID, mid_points)
        pygame.draw.polygon(self.screen, MOUNTAIN_NEAR, near_points)

    def _draw_mist_band(self) -> None:
        mist_surface = pygame.Surface((WIDTH, 160), pygame.SRCALPHA)
        for i in range(6):
            y = 25 + i * 18 + math.sin(self.time * 0.6 + i) * 6
            pygame.draw.ellipse(mist_surface, (*MIST, 35), (-40, int(y), WIDTH + 80, 32))
        self.screen.blit(mist_surface, (0, HEIGHT - 180))

    def _draw_panel(self, rect: pygame.Rect, alpha: int = 170) -> None:
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (28, 24, 33, alpha), panel.get_rect(), border_radius=26)
        pygame.draw.rect(panel, (238, 212, 170, 120), panel.get_rect(), width=2, border_radius=26)
        self.screen.blit(panel, rect.topleft)

    def _draw_landing_page(self) -> None:
        hero_panel = pygame.Rect(110, 90, 680, 470)
        self._draw_panel(hero_panel, alpha=155)

        eyebrow = self.small_font.render("AN ANIMATED DIVINATION PROTOTYPE", True, (244, 221, 178))
        title = self.hero_font.render("Cast the I Ching", True, (255, 246, 227))
        subtitle = self.font.render("Ask a question and reveal your hexagram through a three-coin toss.", True, (237, 218, 187))
        prompt = self.small_font.render("Type your question below to begin.", True, (219, 193, 152))

        self.screen.blit(eyebrow, eyebrow.get_rect(center=(WIDTH // 2, 150)))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 215)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 275)))
        self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 320)))

        self._draw_input_box()
        self._draw_submit_button()

    def _draw_input_box(self) -> None:
        pygame.draw.rect(self.screen, INPUT_BACKGROUND, self.input_rect, border_radius=16)
        pygame.draw.rect(self.screen, (236, 212, 169), self.input_rect, width=2, border_radius=16)

        display_text = self.input_text if self.input_text else "Should I follow this path?"
        color = TEXT if self.input_text else (134, 119, 103)
        input_text_surface = self.small_font.render(display_text, True, color)
        self.screen.blit(input_text_surface, (self.input_rect.x + 18, self.input_rect.y + 18))

        if self.cursor_timer < FPS // 2:
            cursor_x = self.input_rect.x + 18 + input_text_surface.get_width() if self.input_text else self.input_rect.x + 18
            pygame.draw.line(
                self.screen,
                TEXT,
                (cursor_x, self.input_rect.y + 15),
                (cursor_x, self.input_rect.y + 43),
                2,
            )

    def _draw_submit_button(self) -> None:
        submit_hovered = self.submit_button.collidepoint(pygame.mouse.get_pos())
        submit_fill = BUTTON_HOVER if submit_hovered else BUTTON_FILL
        pygame.draw.rect(self.screen, submit_fill, self.submit_button, border_radius=16)
        pygame.draw.rect(self.screen, COIN_EDGE, self.submit_button, width=2, border_radius=16)

        submit_label = self.small_font.render("Begin the casting", True, TEXT)
        self.screen.blit(submit_label, submit_label.get_rect(center=self.submit_button.center))

    def _draw_hexagram_page(self) -> None:
        top_panel = pygame.Rect(70, 28, 760, 110)
        casting_panel = pygame.Rect(85, 145, 730, 450)
        self._draw_panel(top_panel, alpha=160)
        self._draw_panel(casting_panel, alpha=138)

        prompt = self.small_font.render("YOUR QUESTION", True, (240, 212, 170))
        self.screen.blit(prompt, (110, 52))
        for i, line in enumerate(self._wrap_text(self.query_text, self.font, 620)[:2]):
            rendered = self.font.render(line, True, (255, 247, 232))
            self.screen.blit(rendered, (110, 76 + i * 28))

        helper = self.small_font.render("Click each seal to cast a line. Two or three heads become a solid yang line.", True, (226, 203, 171))
        self.screen.blit(helper, helper.get_rect(center=(WIDTH // 2, 175)))

        self._draw_stack_guides()
        self._draw_hexagram()
        self._draw_reset_button()

        return_text = self.small_font.render("Press R to return and ask a new question", True, (240, 212, 170))
        self.screen.blit(return_text, return_text.get_rect(center=(WIDTH // 2, 675)))

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split()
        if not words:
            return [""]
        lines = []
        current = words[0]
        for word in words[1:]:
            trial = f"{current} {word}"
            if font.size(trial)[0] <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def _draw_stack_guides(self) -> None:
        for line_number, (_, y) in enumerate(self.circle_centers, start=1):
            label = self.small_font.render(str(line_number), True, (239, 214, 172))
            self.screen.blit(label, (205, y - 12))

            guide_color = (236, 213, 174)
            pygame.draw.line(self.screen, guide_color, (245, y), (290, y), 1)
            pygame.draw.line(self.screen, guide_color, (610, y), (655, y), 1)

    def _draw_hexagram(self) -> None:
        for index, center in enumerate(self.circle_centers):
            if self.animating_line_index == index:
                self._draw_coin_flip(center)
            elif self.revealed[index]:
                self._draw_line(center[1], self.hexagram_lines[index])
            else:
                self._draw_unrevealed_marker(center)

    def _draw_unrevealed_marker(self, center: tuple[int, int]) -> None:
        pulse = 0.5 + 0.5 * math.sin(self.time * 2.1 + center[1] * 0.03)
        radius = int(self.circle_radius + pulse * 3)
        halo = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(halo, (*GLOW, 34), (radius * 2, radius * 2), radius + 10)
        self.screen.blit(halo, (center[0] - radius * 2, center[1] - radius * 2))
        pygame.draw.circle(self.screen, CIRCLE_FILL, center, radius)
        pygame.draw.circle(self.screen, CIRCLE_OUTLINE, center, radius, width=4)
        pygame.draw.circle(self.screen, COIN_FRONT, center, 10)
        pygame.draw.circle(self.screen, COIN_EDGE, center, 10, width=2)

    def _draw_line(self, y: int, is_solid: bool) -> None:
        left = WIDTH // 2 - self.line_width // 2
        line_surface = pygame.Surface((self.line_width + 20, self.line_height + 20), pygame.SRCALPHA)
        glow_color = (*GLOW, 45)
        pygame.draw.rect(line_surface, glow_color, (0, 5, self.line_width + 10, self.line_height + 10), border_radius=12)
        self.screen.blit(line_surface, (left - 5, y - self.line_height // 2 - 10))

        if is_solid:
            rect = pygame.Rect(left, y - self.line_height // 2, self.line_width, self.line_height)
            pygame.draw.rect(self.screen, LINE_COLOR, rect, border_radius=8)
            pygame.draw.rect(self.screen, (232, 205, 160), rect, width=1, border_radius=8)
            return

        segment_width = 130
        gap = 60
        left_rect = pygame.Rect(
            WIDTH // 2 - gap // 2 - segment_width,
            y - self.line_height // 2,
            segment_width,
            self.line_height,
        )
        right_rect = pygame.Rect(
            WIDTH // 2 + gap // 2,
            y - self.line_height // 2,
            segment_width,
            self.line_height,
        )
        pygame.draw.rect(self.screen, LINE_COLOR, left_rect, border_radius=8)
        pygame.draw.rect(self.screen, LINE_COLOR, right_rect, border_radius=8)
        pygame.draw.rect(self.screen, (232, 205, 160), left_rect, width=1, border_radius=8)
        pygame.draw.rect(self.screen, (232, 205, 160), right_rect, width=1, border_radius=8)

    def _draw_coin_flip(self, center: tuple[int, int]) -> None:
        progress = self.animation_frame / self.animation_duration
        cast_panel = pygame.Rect(318, 210, 264, 122)
        self._draw_panel(cast_panel, alpha=168)

        label = self.small_font.render("Coin casting in motion", True, (252, 238, 212))
        self.screen.blit(label, label.get_rect(center=(WIDTH // 2, 236)))

        start_offsets = (-110, 0, 110)
        end_offsets = (-92, 0, 92)
        for index, toss_is_heads in enumerate(self.current_cast):
            offset_x = self._lerp(start_offsets[index], end_offsets[index], min(1.0, progress * 1.1))
            arc_height = math.sin(progress * math.pi) * 70
            settle = self._ease_out_cubic(min(1.0, progress * 1.3))
            y_offset = -28 - arc_height + (1 - settle) * 16
            wobble = math.sin(progress * math.tau * 3 + index) * 8 * (1 - progress)
            coin_center = (int(center[0] + offset_x + wobble), int(center[1] - 45 + y_offset))

            flip_cycles = 2.5 + index * 0.35
            flip = abs(math.cos(progress * math.pi * flip_cycles))
            face_heads = toss_is_heads if progress > 0.72 else (math.sin(progress * math.pi * flip_cycles) > 0)
            self._draw_coin(coin_center, max(0.08, flip), face_heads, label=progress > 0.78)

        resolution = self.small_font.render(self._cast_label(self.current_cast), True, (241, 215, 175))
        if progress > 0.72:
            self.screen.blit(resolution, resolution.get_rect(center=(WIDTH // 2, center[1] + 54)))

    def _draw_coin(
        self,
        center: tuple[int, int],
        width_scale: float,
        is_heads: bool,
        *,
        label: bool,
    ) -> None:
        coin_width = max(6, int(self.coin_radius * 2 * width_scale))
        coin_height = self.coin_radius * 2
        coin_rect = pygame.Rect(
            center[0] - coin_width // 2,
            center[1] - coin_height // 2,
            coin_width,
            coin_height,
        )
        fill = COIN_FRONT if is_heads else COIN_BACK
        pygame.draw.ellipse(self.screen, fill, coin_rect)
        pygame.draw.ellipse(self.screen, COIN_EDGE, coin_rect, width=3)

        inner_rect = coin_rect.inflate(-10, -10)
        if inner_rect.width > 8:
            pygame.draw.ellipse(self.screen, (*MIST,), inner_rect, width=2)
        if label and width_scale > 0.4:
            glyph = "H" if is_heads else "T"
            coin_label = self.small_font.render(glyph, True, COIN_EDGE)
            self.screen.blit(coin_label, coin_label.get_rect(center=center))

    def _cast_label(self, cast: list[bool]) -> str:
        heads = sum(cast)
        return f"{heads} heads -> {'yang line' if heads >= 2 else 'yin line'}"

    def _draw_reset_button(self) -> None:
        hovered = self.reset_button.collidepoint(pygame.mouse.get_pos())
        fill = BUTTON_HOVER if hovered else BUTTON_FILL
        pygame.draw.rect(self.screen, fill, self.reset_button, border_radius=14)
        pygame.draw.rect(self.screen, COIN_EDGE, self.reset_button, width=2, border_radius=14)

        label = self.small_font.render("Generate New Hexagram", True, TEXT)
        self.screen.blit(label, label.get_rect(center=self.reset_button.center))

    @staticmethod
    def _lerp(start: float, end: float, amount: float) -> float:
        return start + (end - start) * amount

    @staticmethod
    def _ease_out_cubic(value: float) -> float:
        return 1 - pow(1 - value, 3)


if __name__ == "__main__":
    HexagramPrototype().run()
