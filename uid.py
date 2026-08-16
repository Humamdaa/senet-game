import pygame
import sys
import json
import time
import os
from game.Board import Board
from modes.HumanVsHuman import HumanVsHuman
from modes.human_vs_ai import HumanVsAI
from Utils.RandomStep import Random
from game.Rules import Rules
from game.StateGenerator import StateGenrator

# Initialize PyGame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BOARD_WIDTH = 10 * 60
BOARD_HEIGHT = 3 * 60
SQUARE_SIZE = 60
FPS = 60

# Colors
GAME_BG_COLOR = (53, 56, 75)
TEXT_WHITE = (255, 255, 255)
TEXT_GOLD = (255, 215, 0)
PLAYER_A_COLOR = (220, 20, 60)
PLAYER_B_COLOR = (30, 144, 255)
HIGHLIGHT_COLOR = (255, 215, 0)
LEGAL_MOVE_COLOR = (50, 205, 50, 100)
AI_THINKING_COLOR = (255, 140, 0)
MESSAGE_BOX_BG = (40, 43, 60)
MESSAGE_BOX_BORDER = (60, 63, 80)
FOOTER_TEXT_COLOR = (150, 150, 150)

# --- Asset Loading ---
def load_assets():
    """Loads and scales all game assets, returning them in a dictionary."""
    assets_path = os.path.join(os.path.dirname(__file__), 'assets')
    assets = {}
    
    def load_image(file_name, alpha=True):
        path = os.path.join(assets_path, file_name)
        try:
            image = pygame.image.load(path)
            return image.convert_alpha() if alpha else image.convert()
        except pygame.error:
            print(f"Warning: Could not load image '{file_name}' from '{assets_path}'")
            return None

    # Load logo
    logo_original = load_image('logo.png')
    if logo_original:
        # Main menu logo
        target_h = 250
        aspect_ratio = logo_original.get_width() / logo_original.get_height()
        assets['logo_main'] = pygame.transform.scale(logo_original, (int(target_h * aspect_ratio), target_h))
        # Game screen logo
        target_h = 80
        assets['logo_game'] = pygame.transform.scale(logo_original, (int(target_h * aspect_ratio), target_h))

    # Load player pieces
    assets['player_a'] = pygame.transform.scale(load_image("Chess Piecesw.png"), (SQUARE_SIZE, SQUARE_SIZE))
    assets['player_b'] = pygame.transform.scale(load_image("Chess Pieces.png"), (SQUARE_SIZE, SQUARE_SIZE))

    # Load board backgrounds
    assets['bg_l'] = pygame.transform.scale(load_image("Board-Squaresb.png", alpha=False), (SQUARE_SIZE, SQUARE_SIZE))
    assets['bg_r'] = pygame.transform.scale(load_image("Board-Squaresw.png", alpha=False), (SQUARE_SIZE, SQUARE_SIZE))
    
    # Load special squares
    assets['special_squares'] = {}
    for i in [15, 26, 27, 28, 29, 30]:
        img = load_image(f"senet_bg_{i}.png", alpha=False)
        if img:
            assets['special_squares'][i] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
            
    return assets

# --- UI Helper Functions ---
def draw_text_button(surface, text, hover_text, rect, font, base_color, hover_color):
    """Draws a text-based button that changes color on hover."""
    mouse_pos = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse_pos)
    
    display_text = hover_text if is_hover else text
    display_color = hover_color if is_hover else base_color
    
    text_surf = font.render(display_text, True, display_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

# --- Main Menu Class ---
class MainMenu:
    """Manages the main menu screen and user selections."""
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.running = True
        self.selected_option = None

        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 30)

        # Button data and layout
        self.button_data = [
            ("Human vs Human", "Play Human vs Human", 1),
            ("Human vs AI", "Play Human vs AI", 2),
            ("Exit", "Quit Game", 0)
        ]
        button_width, button_height, button_spacing = 300, 50, 20
        start_y = SCREEN_HEIGHT // 2
        self.buttons_rects = [
            pygame.Rect((SCREEN_WIDTH - button_width) // 2, start_y + i * (button_height + button_spacing), button_width, button_height)
            for i, _ in enumerate(self.button_data)
        ]

    def run(self):
        """Runs the main menu loop."""
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)
        return self.selected_option

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.selected_option = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, (_, _, action_id) in enumerate(self.button_data):
                    if self.buttons_rects[i].collidepoint(event.pos):
                        self.selected_option = action_id
                        self.running = False

    def draw(self):
        self.screen.fill(GAME_BG_COLOR)
        
        # Display logo or title
        if 'logo_main' in self.assets and self.assets['logo_main']:
            logo_rect = self.assets['logo_main'].get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(self.assets['logo_main'], logo_rect)
        else:
            title = self.title_font.render("SENET", True, TEXT_WHITE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))
            subtitle = self.button_font.render("Ancient Egyptian Board Game", True, TEXT_WHITE)
            self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 220)))

        # Draw buttons
        for i, (text, hover_text, _) in enumerate(self.button_data):
            draw_text_button(self.screen, text, hover_text, self.buttons_rects[i], self.button_font, TEXT_WHITE, TEXT_GOLD)

# --- Game UI Class ---
class SenetUI:
    """Manages the main game screen, board, and UI."""
    def __init__(self, screen, assets, game_mode):
        self.screen = screen
        self.assets = assets
        self.game_mode = game_mode
        self.running = True

        # Fonts
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.button_font = pygame.font.SysFont("Arial", 22)

        # UI Layout
        self.board_x = (SCREEN_WIDTH - BOARD_WIDTH) // 2
        self.board_y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2 - 20

        # Game Logic Components
        levels = self.load_levels()
        self.board = Board(levels[0])
        self.rand = Random()
        self.state_gen = StateGenrator(self.board)
        self.game = HumanVsHuman(self.board) if game_mode == 1 else HumanVsAI(self.board)

        # Game State
        self.current_player = self.board.get_current_player()
        self.dice_roll = None
        self.selected_piece = None
        self.message = "Welcome to Senet! Click 'Roll Dice' to start."
        self.game_over = False
        self.legal_moves = []

        # AI State
        self.ai_thinking = False
        self.ai_move_from = None
        self.ai_step = 0
        self.ai_timer = 0
        
        # Button definitions
        self._setup_buttons()

    def _setup_buttons(self):
        action_panel_y = self.board_y + BOARD_HEIGHT + 40
        button_width = 150
        gap = (BOARD_WIDTH - (button_width * 3)) // 2
        self.buttons = {
            "roll": {"rect": pygame.Rect(self.board_x, action_panel_y, button_width, 40), "text": "Roll Dice", "hover_text": "> Roll Dice <"},
            "pass": {"rect": pygame.Rect(self.board_x + button_width + gap, action_panel_y, button_width, 40), "text": "Pass Turn", "hover_text": "> Pass Turn <"},
            "restart": {"rect": pygame.Rect(self.board_x + 2 * (button_width + gap), action_panel_y, button_width, 40), "text": "Restart", "hover_text": "> Restart <"},
            "back_to_menu": {"rect": pygame.Rect(20, 20, 200, 40), "text": "< Main Menu", "hover_text": "< Go to Main Menu"}
        }

    def load_levels(self, path="levels.json"):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)["levels"]

    def run(self):
        """Runs the main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: self.restart_game()
                elif event.key == pygame.K_SPACE and not self.dice_roll and not self.ai_thinking: self.roll_dice()
                elif event.key == pygame.K_ESCAPE: self.running = False

    def handle_click(self, pos):
        if self.game_over:
            if self.buttons["restart"]["rect"].collidepoint(pos): self.restart_game()
            return

        if self.ai_thinking: return

        if self.buttons["back_to_menu"]["rect"].collidepoint(pos):
            self.running = False
            return

        if self.buttons["roll"]["rect"].collidepoint(pos): self.roll_dice()
        elif self.buttons["restart"]["rect"].collidepoint(pos): self.restart_game()
        elif self.buttons["pass"]["rect"].collidepoint(pos) and self.dice_roll:
            if not self.legal_moves: self.switch_player()
            else: self.message = "You have legal moves. You must move a piece."
        
        square_index = self._get_square_from_pos(pos)
        if square_index is not None: self._handle_square_click(square_index)

    def update(self):
        """Update game logic, such as AI turns."""
        if self.ai_thinking:
            self._update_ai_turn()

    def draw(self):
        """Draw all UI elements to the screen."""
        self.screen.fill(GAME_BG_COLOR)
        self._draw_header()
        self._draw_board()
        self._draw_action_panel()
        self._draw_footer()
        self._draw_back_button()

    def _draw_header(self):
        if 'logo_game' in self.assets and self.assets['logo_game']:
            logo_rect = self.assets['logo_game'].get_rect(center=(SCREEN_WIDTH // 2, 60))
            self.screen.blit(self.assets['logo_game'], logo_rect)
        
        info_y = 120
        player_text = "🤖 AI's turn" if self.ai_thinking else f"Current Player: {self.current_player}"
        player_color = AI_THINKING_COLOR if self.ai_thinking else (PLAYER_A_COLOR if self.current_player == 'A' else PLAYER_B_COLOR)
        player_surf = self.font.render(player_text, True, player_color)
        self.screen.blit(player_surf, (self.board_x, info_y))

        dice_text = f"Dice Roll: {self.dice_roll if self.dice_roll else 'Not rolled'}"
        dice_surf = self.font.render(dice_text, True, TEXT_WHITE)
        self.screen.blit(dice_surf, dice_surf.get_rect(right=self.board_x + BOARD_WIDTH, top=info_y))

    def _draw_board(self):
        for i in range(30):
            row, col = i // 10, i % 10
            x = self.board_x + ((9 - col) if row == 1 else col) * SQUARE_SIZE
            y = self.board_y + row * SQUARE_SIZE

            square_img = self.assets['special_squares'].get(i + 1, self.assets['bg_l'] if (i % 2 == 0) else self.assets['bg_r'])
            self.screen.blit(square_img, (x, y))
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)

            if (i + 1) not in self.assets['special_squares']:
                self.screen.blit(self.small_font.render(str(i + 1), True, (0,0,0)), (x + 5, y + 5))

            if self.selected_piece == i and not self.ai_thinking:
                pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
            
            if self.dice_roll and not self.game_over and not self.ai_thinking and any(m["from"] - 1 == i for m in self.legal_moves):
                highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight.fill(LEGAL_MOVE_COLOR)
                self.screen.blit(highlight, (x, y))

            cell_value = self.board.grid[i].get_value()
            if cell_value == 'A': self.screen.blit(self.assets['player_a'], (x, y))
            elif cell_value == 'B': self.screen.blit(self.assets['player_b'], (x, y))

    def _draw_action_panel(self):
        for key in ["roll", "pass", "restart"]:
            button = self.buttons[key]
            draw_text_button(self.screen, button["text"], button["hover_text"], button["rect"], self.button_font, TEXT_WHITE, TEXT_GOLD)

        msg_y = self.buttons["roll"]["rect"].bottom + 20
        msg_rect = pygame.Rect(self.board_x, msg_y, BOARD_WIDTH, 60)
        pygame.draw.rect(self.screen, MESSAGE_BOX_BG, msg_rect, border_radius=10)
        pygame.draw.rect(self.screen, MESSAGE_BOX_BORDER, msg_rect, 2, border_radius=10)
        
        for i, line in enumerate(self._wrap_text(self.message, BOARD_WIDTH - 20)):
            msg_surf = self.small_font.render(line, True, TEXT_WHITE)
            self.screen.blit(msg_surf, (msg_rect.x + 10, msg_rect.y + 10 + i * 25))

    def _draw_footer(self):
        instructions = "How to play: 1. Roll Dice -> 2. Click a piece to move. | Special: 26 (Happy), 27 (Water), 28-30 (End)"
        inst_surf = self.small_font.render(instructions, True, FOOTER_TEXT_COLOR)
        self.screen.blit(inst_surf, inst_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)))

    def _draw_back_button(self):
        button = self.buttons["back_to_menu"]
        draw_text_button(self.screen, button["text"], button["hover_text"], button["rect"], self.button_font, TEXT_WHITE, TEXT_GOLD)

    def _wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = [""]
        for word in words:
            if self.small_font.render(lines[-1] + word, True, TEXT_WHITE).get_width() < max_width:
                lines[-1] += word + " "
            else: lines.append(word + " ")
        return lines

    def _get_square_from_pos(self, pos):
        x, y = pos[0] - self.board_x, pos[1] - self.board_y
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
            return 10 + (9 - col) if row == 1 else row * 10 + col
        return None

    def roll_dice(self):
        if self.dice_roll and not self.game_over:
            self.message = "You already rolled! Move a piece first."
            return
        self.dice_roll = self.rand.roll_distance()
        if hasattr(self.board, 'special_rules'): self.board.special_rules.update_last_roll(self.dice_roll)
        self.message = f"Player {self.current_player} rolled: {self.dice_roll}"
        self.legal_moves = self.state_gen.generate_legal_moves(self.dice_roll)
        if not self.legal_moves:
            self.message += f" - No legal moves. Switching players."
            self.switch_player()
        else:
            self.message += f" - {len(self.legal_moves)} legal moves available."

    def _handle_square_click(self, square_index):
        if self.game_over or not self.dice_roll or (self.game_mode == 2 and self.current_player == 'B'): return
        cell = self.board.grid[square_index]
        if cell.get_value() == self.current_player:
            if any(move["from"] - 1 == square_index for move in self.legal_moves):
                self.selected_piece = square_index
                self._move_piece(square_index)
            else:
                self.message = f"Piece {self._get_piece_number(square_index, self.current_player)} cannot move {self.dice_roll} steps."
        else:
            self.message = "That's not your piece!" if cell.is_player_piece() else "Empty square selected."

    def _move_piece(self, square_index):
        if not self.dice_roll: return
        if Rules.checkMove(self.board, square_index, self.dice_roll):
            self.message = f"Moved piece from square {square_index + 1}"
            Rules.move(self.board, square_index, self.dice_roll)
            if self.board.has_player_won(self.current_player):
                self.game_over = True
                self.message = f"🎉 Player {self.current_player} wins! 🎉"
            else:
                self.switch_player()
        else:
            self.message = f"Invalid move for piece {self._get_piece_number(square_index, self.current_player)}"

    def switch_player(self):
        self.board.switchPlayer()
        self.current_player = self.board.get_current_player()
        self.message = f"Player {self.current_player}'s turn"
        self.dice_roll, self.selected_piece, self.legal_moves = None, None, []
        if self.game_mode == 2 and self.current_player == 'B' and not self.game_over: self.start_ai_turn()

    def start_ai_turn(self):
        self.ai_thinking = True
        self.ai_step = 1
        self.ai_timer = pygame.time.get_ticks() + 1000
        self.message = "🤖 AI's turn..."

    def _update_ai_turn(self):
        if pygame.time.get_ticks() < self.ai_timer: return
        if self.ai_step == 1:
            self.roll_dice()
            self.ai_step = 2
            self.ai_timer = pygame.time.get_ticks() + 1000
        elif self.ai_step == 2:
            if not self.legal_moves: self._end_ai_turn(); return
            self.ai_step = 3
            self.ai_timer = pygame.time.get_ticks() + 1000
        elif self.ai_step == 3:
            from game.GameState import GameState
            state = GameState(self.board, "B")
            move = self.game.ai.decide_move(state, self.dice_roll)
            if move:
                self.ai_move_from = move["from"] - 1
                self.ai_step = 4
                self.ai_timer = pygame.time.get_ticks() + 1500
                self.ai_move = move
            else: self._end_ai_turn()
        elif self.ai_step == 4:
            from game.GameState import GameState
            state = GameState(self.board, "B")
            state.apply_move(self.ai_move)
            if self.board.has_player_won('B'):
                self.game_over = True
                self.message = f"🎉 AI (Player B) wins! 🎉"
            self._end_ai_turn()

    def _end_ai_turn(self):
        self.ai_thinking, self.ai_move_from, self.ai_step = False, None, 0
        if not self.game_over: self.switch_player()

    def _get_piece_number(self, position, player):
        return sum(1 for i in range(position + 1) if self.board.grid[i].get_value() == player)

    def restart_game(self):
        levels = self.load_levels()
        self.board = Board(levels[0])
        self.state_gen = StateGenrator(self.board)
        self.game = HumanVsHuman(self.board) if self.game_mode == 1 else HumanVsAI(self.board)
        self.current_player, self.dice_roll, self.selected_piece = self.board.get_current_player(), None, None
        self.message, self.game_over, self.legal_moves = "Game restarted! Click 'Roll Dice' to start.", False, []
        self._end_ai_turn()

def main():
    """Main entry point for the application."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Senet - Ancient Egyptian Board Game")
    assets = load_assets()

    while True:
        menu = MainMenu(screen, assets)
        game_mode = menu.run()

        if game_mode in [1, 2]:
            game_ui = SenetUI(screen, assets, game_mode)
            game_ui.run()
        else: # Exit condition
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
# Here's a summary of the key changes:
# •
# MainMenu Class: All logic for the main menu has been encapsulated in a new MainMenu class, separating it from the game screen.
# •
# SenetUI Class: This class has been streamlined to focus exclusively on the game board and its interactions. Internal helper methods are now prefixed with an underscore (e.g., _draw_header).
# •
# load_assets Function: A new load_assets function now handles the loading and scaling of all game images, centralizing asset management and reducing code duplication.
# •
# draw_text_button Helper: A reusable draw_text_button function has been implemented to render text-based buttons with hover effects, used by both the main menu and the game screen.
# •
# Main Game Loop: The main entry point (main function) now cleanly manages the flow between the MainMenu and the SenetUI game screen, making the application's state transitions clearer.
# •
# Readability: Docstrings and comments have been added to clarify the purpose of classes and functions, and constants are now consistently grouped.
# This refactoring results in a more organized and SOLID-compliant codebase that is easier to understand and extend.