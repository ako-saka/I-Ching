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


class HexagramPrototype:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("I Ching Hexagram Prototype")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("georgia", 28)
        self.small_font = pygame.font.SysFont("georgia", 20)
        self.large_font = pygame.font.SysFont("georgia", 48)

        self.circle_radius = 34
        self.line_width = 320
        self.line_height = 16
        self.line_gap = 72
        self.top_margin = 510

        self.circle_centers = self._build_circle_positions()
        self.reset_button = pygame.Rect(WIDTH // 2 - 140, 580, 280, 48)

        # State management
        self.current_page = PAGE_LANDING
        self.query_text = ""
        self.input_text = ""
        self.input_rect = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 30, 500, 60)
        self.submit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

        # Animation state
        self.animating_line_index = -1
        self.animation_frame = 0
        self.animation_duration = 40
        self.coin_radius = 40

        self._reset_hexagram()

    def set_query(self, query: str) -> None:
        self.query_text = query
        self.current_page = PAGE_HEXAGRAM
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
        self.animating_line_index = -1
        self.animation_frame = 0

    def run(self) -> None:
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)

    def _update(self) -> None:
        if self.animating_line_index >= 0:
            self.animation_frame += 1
            if self.animation_frame >= self.animation_duration:
                self.revealed[self.animating_line_index] = True
                self.animating_line_index = -1
                self.animation_frame = 0

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
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.current_page = PAGE_LANDING
                        self.input_text = ""
                        self.query_text = ""

    def _handle_landing_events(self, event: pygame.event.EventType) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.input_rect.collidepoint(event.pos):
                self.input_text = ""
            elif self.submit_button.collidepoint(event.pos):
                if self.input_text.strip():
                    self.set_query(self.input_text)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self.set_query(self.input_text)
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode.isprintable():
                if len(self.input_text) < 100:
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

        if self.current_page == PAGE_LANDING:
            self._draw_landing_page()
        elif self.current_page == PAGE_HEXAGRAM:
            self._draw_hexagram_page()

        pygame.display.flip()

    def _draw_landing_page(self) -> None:
        title = self.large_font.render("I Ching", True, TEXT)
        subtitle = self.font.render("Ask a question", True, ACCENT)
        prompt = self.small_font.render("Enter your query below:", True, TEXT)

        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 200)))
        self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 280)))

        # Draw input box
        pygame.draw.rect(self.screen, INPUT_BACKGROUND, self.input_rect, border_radius=8)
        pygame.draw.rect(self.screen, INPUT_BORDER, self.input_rect, width=2, border_radius=8)

        # Draw input text
        input_text_surface = self.small_font.render(self.input_text, True, TEXT)
        self.screen.blit(input_text_surface, (self.input_rect.x + 20, self.input_rect.y + 15))

        # Draw cursor
        cursor_x = self.input_rect.x + 20 + input_text_surface.get_width()
        cursor_y = self.input_rect.y + 15
        pygame.draw.line(self.screen, TEXT, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        # Draw submit button
        submit_hovered = self.submit_button.collidepoint(pygame.mouse.get_pos())
        submit_fill = BUTTON_HOVER if submit_hovered else BUTTON_FILL
        pygame.draw.rect(self.screen, submit_fill, self.submit_button, border_radius=14)
        pygame.draw.rect(self.screen, CIRCLE_OUTLINE, self.submit_button, width=2, border_radius=14)

        submit_label = self.small_font.render("Submit", True, TEXT)
        self.screen.blit(submit_label, submit_label.get_rect(center=self.submit_button.center))

    def _draw_hexagram_page(self) -> None:
        query_label = self.font.render(f"Your question: {self.query_text}", True, TEXT)
        self.screen.blit(query_label, query_label.get_rect(center=(WIDTH // 2, 50)))

        title = self.font.render("Click each circle to reveal the hexagram", True, TEXT)
        self._draw_stack_guides()
        self._draw_hexagram()
        self._draw_reset_button()

        # Draw return instruction
        return_text = self.small_font.render("Press R to ask a new question", True, ACCENT)
        self.screen.blit(return_text, return_text.get_rect(center=(WIDTH // 2, 680)))


    def _draw_stack_guides(self) -> None:
        for line_number, (_, y) in enumerate(self.circle_centers, start=1):
            label = self.small_font.render(str(line_number), True, ACCENT)
            self.screen.blit(label, (200, y - 12))

    def _draw_hexagram(self) -> None:
        for index, center in enumerate(self.circle_centers):
            if self.animating_line_index == index:
                self._draw_coin_flip(center)
            elif self.revealed[index]:
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

    def _draw_coin_flip(self, center: tuple[int, int]) -> None:
        progress = self.animation_frame / self.animation_duration
        
        # Create a flipping effect by scaling the width (x-axis) while maintaining height
        # progress goes from 0 to 1, so we create a wave: 1 -> 0 -> 1
        wave_progress = abs(2 * progress - 1)
        scale_x = wave_progress
        
        # Draw the coin as an ellipse that appears to flip
        coin_width = int(self.coin_radius * 2 * scale_x)
        coin_height = int(self.coin_radius * 2)
        
        if coin_width > 0:
            # Draw coin circle (scaled horizontally)
            pygame.draw.ellipse(self.screen, CIRCLE_FILL, 
                              (center[0] - coin_width // 2, center[1] - coin_height // 2,
                               coin_width, coin_height))
            pygame.draw.ellipse(self.screen, CIRCLE_OUTLINE, 
                              (center[0] - coin_width // 2, center[1] - coin_height // 2,
                               coin_width, coin_height), width=4)
        else:
            # At the very thin point, just draw a line
            pygame.draw.line(self.screen, CIRCLE_OUTLINE, 
                           (center[0], center[1] - self.coin_radius),
                           (center[0], center[1] + self.coin_radius), width=4)

    def _draw_reset_button(self) -> None:
        hovered = self.reset_button.collidepoint(pygame.mouse.get_pos())
        fill = BUTTON_HOVER if hovered else BUTTON_FILL
        pygame.draw.rect(self.screen, fill, self.reset_button, border_radius=14)
        pygame.draw.rect(self.screen, CIRCLE_OUTLINE, self.reset_button, width=2, border_radius=14)

        label = self.small_font.render("Generate New Hexagram", True, TEXT)
        self.screen.blit(label, label.get_rect(center=self.reset_button.center))


if __name__ == "__main__":
    HexagramPrototype().run()
