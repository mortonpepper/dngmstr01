# Dungeon Master Clone

A classic dungeon crawler RPG built in Python with Pygame, inspired by the 1987 FTL game.

## Features

- **Party Management**: Create and manage a party of 4 characters with different classes
  - Fighter: High HP and Strength
  - Mage: High Intelligence and Mana for spellcasting
  - Cleric: Healing and Holy magic
  - Thief: High Dexterity and stealth

- **Turn-Based Combat**: Strategic combat system with multiple actions
  - Physical attacks
  - Spellcasting with mana management
  - Defend stance
  - Enemy AI

- **Dungeon Exploration**: Procedurally generated dungeons
  - Grid-based movement
  - Enemy encounters
  - Treasure collection
  - Multiple dungeon levels

- **Character Progression**: RPG progression system
  - Experience and leveling
  - Stat-based gameplay
  - Spell learning

- **Save/Load**: Full game state persistence
  - Save your progress
  - Load previous games
  - JSON-based save format

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

### Main Menu
- **N**: New Game
- **L**: Load Game
- **Q**: Quit

### Exploration
- **Arrow Keys / WASD**: Move around the dungeon
- **I**: Show inventory
- **Enter**: Save game
- **Q**: Quit

### Combat
- **A**: Attack enemy
- **S**: Cast spell
- **D**: Defend
- Characters take turns automatically

## Game Classes

### Character Types
- **Fighter**: Best for tanking and physical damage
- **Mage**: Powerful area spells but fragile
- **Cleric**: Healing and support with moderate damage
- **Thief**: High single-target damage with evasion

### Spells
- **Mage**: Fireball, Magic Missile, Teleport
- **Cleric**: Heal, Holy Strike, Protection
- **Fighter/Thief**: Basic Attack

## Dungeon Levels

Descend through multiple dungeon levels, each with:
- Stronger enemies
- More treasure
- Procedurally generated layouts

## Future Enhancements

- [ ] Advanced spell system with targeting
- [ ] Equipment and item management
- [ ] Boss encounters
- [ ] Dungeon traps and puzzles
- [ ] Multiple game modes (story, endless)
- [ ] Improved graphics and animations
- [ ] Sound and music

## Game Architecture

- `character.py`: Character classes and stats
- `dungeon.py`: Dungeon generation and exploration
- `combat.py`: Turn-based combat system
- `save_load.py`: Game persistence
- `main.py`: Main game loop and rendering

## License

Created as an homage to the classic Dungeon Master (1987).
