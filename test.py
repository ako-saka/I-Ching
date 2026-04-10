import random
import sys
import pygame


WIDTH = 900
HEIGHT = 700
FPS = 60
LINE_COUNT = 6

BACKGROUND = (245, 239, 226)
TEXT = (44, 38, 28)
ACCENT = (170, 129, 76)
LINE_COLOR = (34, 31, 27)
CIRCLE_FILL = (252, 249, 243)
CIRCLE_OUTLINE = (121, 92, 53)
BUTTON_FILL = (221, 202, 168)
BUTTON_HOVER = (206, 181, 138)


class HexagramPrototype:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("I Ching Hexagram Prototype")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("georgia", 28)
        self.small_font = pygame.font.SysFont("georgia", 20)

        self.circle_radius = 34
        self.line_width = 320
        self.line_height = 16
        self.line_gap = 72
        self.top_margin = 510

        self.circle_centers = self._build_circle_positions()
        self.reset_button = pygame.Rect(WIDTH // 2 - 95, 620, 190, 48)

        self._reset_hexagram()

    def _build_circle_positions(self) -> list[tuple[int, int]]:
        centers: list[tuple[int, int]] = []
        start_y = self.top_margin
        for index in range(LINE_COUNT):
            y = start_y - index * self.line_gap
            centers.append((WIDTH // 2, y))
        return centers

    def _reset_hexagram(self) -> None:
        # True means a solid yang line, False means a broken yin line.
        self.hexagram_lines = [random.choice([True, False]) for _ in range(LINE_COUNT)]
        self.revealed = [False] * LINE_COUNT

    def run(self) -> None:
        while True:
            self._handle_events()
            self._draw()
            self.clock.tick(FPS)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)

    def _handle_click(self, position: tuple[int, int]) -> None:
        if self.reset_button.collidepoint(position):
            self._reset_hexagram()
            return

        for index, center in enumerate(self.circle_centers):
            if self.revealed[index]:
                continue
            if self._point_in_circle(position, center, self.circle_radius):
                self.revealed[index] = True
                return

    @staticmethod
    def _point_in_circle(
        point: tuple[int, int], center: tuple[int, int], radius: int
    ) -> bool:
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        return dx * dx + dy * dy <= radius * radius

    def _draw(self) -> None:
        self.screen.fill(BACKGROUND)

        title = self.font.render("Click each circle to reveal the hexagram", True, TEXT)
        subtitle = self.small_font.render(
            "Each revealed line is randomly chosen as solid or broken. Bottom line is first.",
            True,
            TEXT,
        )
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 52)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 92)))

        self._draw_stack_guides()
        self._draw_hexagram()
        self._draw_reset_button()

        pygame.display.flip()

    def _draw_stack_guides(self) -> None:
        for line_number, (_, y) in enumerate(self.circle_centers, start=1):
            label = self.small_font.render(str(line_number), True, ACCENT)
            self.screen.blit(label, (200, y - 12))

    def _draw_hexagram(self) -> None:
        for index, center in enumerate(self.circle_centers):
            if self.revealed[index]:
                self._draw_line(center[1], self.hexagram_lines[index])
            else:
                pygame.draw.circle(self.screen, CIRCLE_FILL, center, self.circle_radius)
                pygame.draw.circle(
                    self.screen, CIRCLE_OUTLINE, center, self.circle_radius, width=4
                )

    def _draw_line(self, y: int, is_solid: bool) -> None:
        left = WIDTH // 2 - self.line_width // 2
        if is_solid:
            rect = pygame.Rect(left, y - self.line_height // 2, self.line_width, self.line_height)
            pygame.draw.rect(self.screen, LINE_COLOR, rect, border_radius=8)
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

    def _draw_reset_button(self) -> None:
        hovered = self.reset_button.collidepoint(pygame.mouse.get_pos())
        fill = BUTTON_HOVER if hovered else BUTTON_FILL
        pygame.draw.rect(self.screen, fill, self.reset_button, border_radius=14)
        pygame.draw.rect(self.screen, CIRCLE_OUTLINE, self.reset_button, width=2, border_radius=14)

        label = self.small_font.render("Generate New Hexagram", True, TEXT)
        self.screen.blit(label, label.get_rect(center=self.reset_button.center))


if __name__ == "__main__":
    HexagramPrototype().run()
