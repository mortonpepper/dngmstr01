"""Main game loop and logic"""
import pygame
from character import Character, CharacterClass
from dungeon import Dungeon, TileType
from combat import Combat
from save_load import GameSave

# Initialize pygame
pygame.init()

# Display settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 20
FPS = 60

# Colors
COLOR_BLACK = (6, 8, 15)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (148, 163, 184)
COLOR_WALL = (45, 55, 72)
COLOR_FLOOR = (22, 27, 38)
COLOR_PLAYER = (0, 127, 255)
COLOR_ENEMY = (255, 50, 50)
COLOR_TREASURE = (255, 215, 0)
COLOR_STAIRS = (100, 200, 100)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Master - Classic RPG")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        
        self.running = True
        self.state = "menu"  # menu, character_select, exploration, combat
        self.party = []
        self.dungeon = None
        self.gold = 0
        self.combat = None
        self.current_actor = 0
        self.save_system = GameSave()
        
        self.message_log = []
        self.max_messages = 10
    
    def add_message(self, message):
        """Add message to log"""
        self.message_log.append(message)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)
    
    def create_default_party(self):
        """Create a default starting party"""
        self.party = [
            Character("Brave", CharacterClass.FIGHTER),
            Character("Wizard", CharacterClass.MAGE),
            Character("Priest", CharacterClass.CLERIC),
            Character("Shadow", CharacterClass.THIEF),
        ]
        self.dungeon = Dungeon(32, 16, level=1)
        self.add_message("Party created! Welcome to the dungeon...")
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    self.handle_menu_input(event)
                elif self.state == "exploration":
                    self.handle_exploration_input(event)
                elif self.state == "combat":
                    self.handle_combat_input(event)
    
    def handle_menu_input(self, event):
        """Handle menu inputs"""
        if event.key == pygame.K_n:  # New game
            self.create_default_party()
            self.state = "exploration"
        elif event.key == pygame.K_l:  # Load game
            party, dungeon, gold = self.save_system.load_game()
            if party:
                self.party = party
                self.dungeon = dungeon
                self.gold = gold
                self.state = "exploration"
                self.add_message("Game loaded!")
            else:
                self.add_message("No save file found!")
        elif event.key == pygame.K_q:  # Quit
            self.running = False
    
    def handle_exploration_input(self, event):
        """Handle exploration inputs"""
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.dungeon.move_player(0, -1)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.dungeon.move_player(0, 1)
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.dungeon.move_player(-1, 0)
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.dungeon.move_player(1, 0)
        
        # Check for enemy encounter
        enemy = self.dungeon.get_enemy_at(self.dungeon.player_x, self.dungeon.player_y)
        if enemy:
            self.start_combat(enemy)
        
        # Check for treasure
        treasure = self.dungeon.get_treasure_at(self.dungeon.player_x, self.dungeon.player_y)
        if treasure:
            self.gold += treasure.value
            self.add_message(f"Found {treasure.value} gold!")
            self.dungeon.remove_treasure(treasure)
        
        # Check stairs
        tile = self.dungeon.get_tile(self.dungeon.player_x, self.dungeon.player_y)
        if tile.type == TileType.STAIRS_DOWN:
            self.next_level()
        
        if event.key == pygame.K_i:  # Inventory
            self.show_inventory()
        elif event.key == pygame.K_RETURN:  # Save
            self.save_system.save_game(self.party, self.dungeon, self.gold)
            self.add_message("Game saved!")
        elif event.key == pygame.K_q:  # Quit
            self.running = False
    
    def handle_combat_input(self, event):
        """Handle combat inputs"""
        if not self.combat or self.combat.combat_over:
            self.state = "exploration"
            if self.combat and self.combat.player_won:
                exp_reward = self.combat.end_combat()
                self.add_message(f"Gained {exp_reward} experience!")
            return
        
        current_char = self.party[self.current_actor]
        
        if event.key == pygame.K_a:  # Attack
            self.combat.player_attack(current_char)
            self.combat.enemy_turn()
            self.current_actor = (self.current_actor + 1) % len([c for c in self.party if c.alive])
        
        elif event.key == pygame.K_s:  # Spells
            if current_char.spells and len(current_char.spells) > 0:
                spell = current_char.spells[0]  # Simple: cast first spell
                self.combat.player_cast_spell(current_char, spell)
                self.combat.enemy_turn()
                self.current_actor = (self.current_actor + 1) % len([c for c in self.party if c.alive])
        
        elif event.key == pygame.K_d:  # Defend
            self.combat.player_defend(current_char)
            self.combat.enemy_turn()
            self.current_actor = (self.current_actor + 1) % len([c for c in self.party if c.alive])
    
    def start_combat(self, enemy):
        """Start combat with an enemy"""
        self.combat = Combat(self.party, enemy)
        self.state = "combat"
        self.current_actor = 0
        self.add_message(f"Battle with {enemy.name}!")
    
    def next_level(self):
        """Proceed to next dungeon level"""
        self.dungeon = Dungeon(32, 16, level=self.dungeon.level + 1)
        self.add_message(f"Welcome to Level {self.dungeon.level}!")
    
    def show_inventory(self):
        """Show inventory info"""
        self.add_message(f"Gold: {self.gold}")
    
    def update(self):
        """Update game state"""
        pass
    
    def render(self):
        """Render the game"""
        self.screen.fill(COLOR_BLACK)
        
        if self.state == "menu":
            self.render_menu()
        elif self.state == "exploration":
            self.render_exploration()
        elif self.state == "combat":
            self.render_combat()
        
        pygame.display.flip()
    
    def render_menu(self):
        """Render main menu"""
        title = self.font_large.render("DUNGEON MASTER", True, COLOR_WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        new_game = self.font_medium.render("(N) New Game", True, COLOR_GRAY)
        load_game = self.font_medium.render("(L) Load Game", True, COLOR_GRAY)
        quit_game = self.font_medium.render("(Q) Quit", True, COLOR_GRAY)
        
        self.screen.blit(new_game, (SCREEN_WIDTH // 2 - new_game.get_width() // 2, 200))
        self.screen.blit(load_game, (SCREEN_WIDTH // 2 - load_game.get_width() // 2, 260))
        self.screen.blit(quit_game, (SCREEN_WIDTH // 2 - quit_game.get_width() // 2, 320))
    
    def render_exploration(self):
        """Render dungeon exploration"""
        # Render dungeon
        dungeon_x = 20
        dungeon_y = 20
        
        for y in range(self.dungeon.height):
            for x in range(self.dungeon.width):
                tile = self.dungeon.tiles[y][x]
                rect = pygame.Rect(dungeon_x + x * TILE_SIZE, dungeon_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if tile.type == TileType.WALL:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(self.screen, COLOR_FLOOR, rect)
                    
                    if tile.type == TileType.STAIRS_DOWN:
                        pygame.draw.rect(self.screen, COLOR_STAIRS, rect)
                
                # Draw enemies
                for enemy in self.dungeon.enemies:
                    if enemy.x == x and enemy.y == y and enemy.alive:
                        pygame.draw.rect(self.screen, COLOR_ENEMY, rect)
                
                # Draw treasures
                for treasure in self.dungeon.treasures:
                    if treasure.x == x and treasure.y == y:
                        pygame.draw.rect(self.screen, COLOR_TREASURE, rect)
                
                # Draw player
                if self.dungeon.player_x == x and self.dungeon.player_y == y:
                    pygame.draw.rect(self.screen, COLOR_PLAYER, rect)
        
        # Render party info
        info_x = dungeon_x + self.dungeon.width * TILE_SIZE + 30
        info_y = dungeon_y
        
        level_text = self.font_medium.render(f"Level {self.dungeon.level}", True, COLOR_WHITE)
        self.screen.blit(level_text, (info_x, info_y))
        
        info_y += 40
        for i, char in enumerate(self.party):
            char_text = self.font_small.render(f"{char.name} ({char.char_class.value})", True, COLOR_WHITE)
            hp_text = self.font_small.render(f"HP: {char.hp}/{char.max_hp}", True, COLOR_GRAY)
            mp_text = self.font_small.render(f"MP: {char.mp}/{char.max_mp}", True, COLOR_GRAY)
            level_text = self.font_small.render(f"Lvl: {char.level}", True, COLOR_GRAY)
            
            self.screen.blit(char_text, (info_x, info_y))
            self.screen.blit(hp_text, (info_x, info_y + 20))
            self.screen.blit(mp_text, (info_x, info_y + 40))
            self.screen.blit(level_text, (info_x, info_y + 60))
            info_y += 90
        
        gold_text = self.font_small.render(f"Gold: {self.gold}", True, COLOR_TREASURE)
        self.screen.blit(gold_text, (info_x, info_y))
        
        # Render message log
        msg_y = SCREEN_HEIGHT - 150
        for message in self.message_log[-5:]:
            msg = self.font_small.render(message, True, COLOR_GRAY)
            self.screen.blit(msg, (20, msg_y))
            msg_y += 25
    
    def render_combat(self):
        """Render combat screen"""
        # Combat info
        combat_text = self.font_large.render("COMBAT!", True, COLOR_ENEMY)
        self.screen.blit(combat_text, (SCREEN_WIDTH // 2 - combat_text.get_width() // 2, 50))
        
        # Enemy info
        enemy_info = self.font_medium.render(
            f"{self.combat.enemy.name} - HP: {self.combat.enemy.hp}/{self.combat.enemy.max_hp}",
            True, COLOR_ENEMY
        )
        self.screen.blit(enemy_info, (SCREEN_WIDTH // 2 - enemy_info.get_width() // 2, 120))
        
        # Party info
        party_y = 200
        for i, char in enumerate(self.party):
            if char.alive:
                color = COLOR_WHITE if i == self.current_actor else COLOR_GRAY
                char_text = self.font_medium.render(
                    f"{char.name}: HP {char.hp}/{char.max_hp} MP {char.mp}/{char.max_mp}",
                    True, color
                )
                self.screen.blit(char_text, (50, party_y))
                party_y += 40
        
        # Combat log
        log_y = SCREEN_HEIGHT - 250
        for message in self.combat.log[-8:]:
            msg = self.font_small.render(message, True, COLOR_GRAY)
            self.screen.blit(msg, (50, log_y))
            log_y += 25
        
        # Controls
        controls_y = SCREEN_HEIGHT - 60
        controls = [
            "(A) Attack",
            "(S) Spells",
            "(D) Defend"
        ]
        for control in controls:
            ctrl = self.font_small.render(control, True, COLOR_GRAY)
            self.screen.blit(ctrl, (50, controls_y))
            controls_y += 25
    
    def run(self):
        """Main game loop"""
        self.state = "menu"
        self.add_message("Welcome to Dungeon Master!")
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
