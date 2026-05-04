import sys
import pygame
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Callable, Optional

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

COLOR_BG = (30, 30, 30)
COLOR_TEXT = (255, 255, 255)
COLOR_BUTTON_BASE = (50, 50, 50)
COLOR_BUTTON_HOVER = (70, 70, 70)
COLOR_BUTTON_ACTIVE = (100, 100, 100)
FONT_SIZE_TITLE = 72
FONT_SIZE_BTN = 32


class MenuState(Enum):
    MAIN = "main"
    MODE_SELECT = "mode_select" 
    PLAYER_COUNT = "player_count"

# --- Класс Кнопки ---
class Button:
    def __init__(self, text: str, rect: pygame.Rect, action: Callable, font: pygame.font.Font):
        self.text = text
        self.rect = rect
        self.action = action
        self.font = font
        self.is_hovered = False

    def draw(self, surface: pygame.Surface):
        color = COLOR_BUTTON_HOVER if self.is_hovered else COLOR_BUTTON_BASE
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_TEXT, self.rect, 2, border_radius=10) # Рамка
        
        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.action()
                return True
        return False

# --- Менеджер Меню ---
class MenuManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.state = MenuState.MAIN
        self.buttons: List[Button] = []
        
        # Шрифты
        self.title_font = pygame.font.SysFont("arial", FONT_SIZE_TITLE, bold=True)
        self.btn_font = pygame.font.SysFont("arial", FONT_SIZE_BTN)
        
        # Инициализация начального экрана
        self.setup_main_menu()

    def setup_main_menu(self):
        self.state = MenuState.MAIN
        self.buttons = [
            Button("Play", pygame.Rect(300, 250, 200, 50), self.go_to_mode_select, self.btn_font),
            Button("Settings", pygame.Rect(300, 320, 200, 50), self.show_rating, self.btn_font),
            Button("Exit", pygame.Rect(300, 390, 200, 50), self.quit_game, self.btn_font),
        ]

    def go_to_mode_select(self):
        """Переход к выбору Оффлайн/Онлайн"""
        self.state = MenuState.MODE_SELECT
        self.buttons = [
            Button("Offline", pygame.Rect(300, 250, 200, 50), self.go_to_player_count, self.btn_font),
            Button("Online", pygame.Rect(300, 320, 200, 50), self.start_online_stub, self.btn_font),
            Button("Back", pygame.Rect(300, 450, 200, 50), self.setup_main_menu, self.btn_font),
        ]

    def go_to_player_count(self):
        """Выбор количества игроков (Соло/Вдвоем)"""
        self.state = MenuState.PLAYER_COUNT
        self.buttons = [
            Button("Solo", pygame.Rect(300, 250, 200, 50), lambda: self.start_game("solo"), self.btn_font),
            Button("Duo", pygame.Rect(300, 320, 200, 50), lambda: self.start_game("pvp"), self.btn_font),
            Button("Back", pygame.Rect(300, 450, 200, 50), self.go_to_mode_select, self.btn_font),
        ]

    def start_game(self, mode: str):
        print(f"Запуск игры в режиме: {mode}")
        # Здесь будет логика перехода к игровому циклу
        # Например: self.running = False для выхода из цикла меню

    def show_rating(self):
        print("Открыть таблицу рейтингов")

    def start_online_stub(self):
        print("Онлайн режим пока не реализован")

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def update(self, events: List[pygame.event.Event]):
        for event in events:
            for btn in self.buttons:
                if btn.handle_event(event):
                    break # Прерываем обработку, если кнопка нажата

    def draw(self):
        self.screen.fill(COLOR_BG)
        
        # Отрисовка заголовка
        title_text = "Reversi"
        title_surf = self.title_font.render(title_text, True, COLOR_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surf, title_rect)

        # Отрисовка кнопок
        for btn in self.buttons:
            btn.draw(self.screen)

        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Reversi Menu")
    clock = pygame.time.Clock()

    menu = MenuManager(screen)
    
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        menu.update(events)
        menu.draw()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()