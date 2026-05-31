"""Dungeon generation and management"""
import random
from enum import Enum

class TileType(Enum):
    WALL = "#"
    FLOOR = "."
    STAIRS_DOWN = ">"
    STAIRS_UP = "<"
    ENEMY = "E"
    TREASURE = "$"
    FOUNTAIN = "F"

class Tile:
    def __init__(self, tile_type):
        self.type = tile_type
        self.explored = False
        self.has_enemy = False
        self.has_treasure = False

class Enemy:
    def __init__(self, name, level, x, y):
        self.name = name
        self.level = level
        self.x = x
        self.y = y
        self.hp = 5 * level
        self.max_hp = self.hp
        self.damage = 2 + level
        self.experience_reward = 10 * level
        self.alive = True
    
    def take_damage(self, damage):
        """Take damage"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
    
    def attack(self):
        """Return damage amount for attack"""
        return random.randint(self.damage - 1, self.damage + 1)

class Treasure:
    def __init__(self, name, value, x, y):
        self.name = name
        self.value = value
        self.x = x
        self.y = y

class Dungeon:
    def __init__(self, width=32, height=16, level=1):
        self.width = width
        self.height = height
        self.level = level
        self.tiles = [[Tile(TileType.WALL) for _ in range(width)] for _ in range(height)]
        self.enemies = []
        self.treasures = []
        
        self.player_x = 5
        self.player_y = 5
        
        self._generate_dungeon()
    
    def _generate_dungeon(self):
        """Generate a simple dungeon layout"""
        # Create main room
        for y in range(3, self.height - 3):
            for x in range(3, self.width - 3):
                self.tiles[y][x] = Tile(TileType.FLOOR)
        
        # Create some corridors and rooms
        for _ in range(5):
            x = random.randint(4, self.width - 4)
            y = random.randint(4, self.height - 4)
            # Carve out a room
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.tiles[ny][nx] = Tile(TileType.FLOOR)
        
        # Place stairs
        self.tiles[2][2] = Tile(TileType.STAIRS_UP)
        self.tiles[self.height - 3][self.width - 3] = Tile(TileType.STAIRS_DOWN)
        
        # Spawn enemies
        for _ in range(3 + self.level):
            x = random.randint(10, self.width - 4)
            y = random.randint(4, self.height - 4)
            if self.tiles[y][x].type == TileType.FLOOR:
                enemy = Enemy(f"Goblin-{_+1}", self.level, x, y)
                self.enemies.append(enemy)
        
        # Spawn treasures
        for _ in range(2 + self.level):
            x = random.randint(4, self.width - 4)
            y = random.randint(4, self.height - 4)
            if self.tiles[y][x].type == TileType.FLOOR:
                treasure = Treasure(f"Gold Pile", 50 * self.level, x, y)
                self.treasures.append(treasure)
    
    def get_tile(self, x, y):
        """Get tile at position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return Tile(TileType.WALL)
    
    def is_walkable(self, x, y):
        """Check if tile is walkable"""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        tile_type = self.tiles[y][x].type
        return tile_type in [TileType.FLOOR, TileType.STAIRS_DOWN, TileType.STAIRS_UP, TileType.FOUNTAIN]
    
    def move_player(self, dx, dy):
        """Move player if possible"""
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        if self.is_walkable(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
            self.tiles[self.player_y][self.player_x].explored = True
            return True
        return False
    
    def get_enemy_at(self, x, y):
        """Get enemy at position"""
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y and enemy.alive:
                return enemy
        return None
    
    def get_treasure_at(self, x, y):
        """Get treasure at position"""
        for treasure in self.treasures:
            if treasure.x == x and treasure.y == y:
                return treasure
        return None
    
    def remove_treasure(self, treasure):
        """Remove collected treasure"""
        if treasure in self.treasures:
            self.treasures.remove(treasure)
    
    def to_dict(self):
        """Convert dungeon to dictionary for saving"""
        return {
            'level': self.level,
            'width': self.width,
            'height': self.height,
            'player_x': self.player_x,
            'player_y': self.player_y,
            'enemies': [
                {
                    'name': e.name,
                    'level': e.level,
                    'x': e.x,
                    'y': e.y,
                    'hp': e.hp,
                    'max_hp': e.max_hp,
                    'alive': e.alive
                } for e in self.enemies
            ]
        }
    
    @staticmethod
    def from_dict(data):
        """Create dungeon from dictionary"""
        dungeon = Dungeon(data['width'], data['height'], data['level'])
        dungeon.player_x = data['player_x']
        dungeon.player_y = data['player_y']
        dungeon.enemies = []
        for e_data in data['enemies']:
            enemy = Enemy(e_data['name'], e_data['level'], e_data['x'], e_data['y'])
            enemy.hp = e_data['hp']
            enemy.alive = e_data['alive']
            dungeon.enemies.append(enemy)
        return dungeon
