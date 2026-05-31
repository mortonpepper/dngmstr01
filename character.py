"""Character classes for Dungeon Master"""
import random
from enum import Enum

class CharacterClass(Enum):
    FIGHTER = "Fighter"
    MAGE = "Mage"
    CLERIC = "Cleric"
    THIEF = "Thief"

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.level = 1
        self.experience = 0
        
        # Base stats by class
        if char_class == CharacterClass.FIGHTER:
            self.max_hp = 30
            self.max_mp = 5
            self.strength = 18
            self.intelligence = 10
            self.wisdom = 12
            self.dexterity = 12
        elif char_class == CharacterClass.MAGE:
            self.max_hp = 15
            self.max_mp = 25
            self.strength = 8
            self.intelligence = 18
            self.wisdom = 14
            self.dexterity = 14
        elif char_class == CharacterClass.CLERIC:
            self.max_hp = 20
            self.max_mp = 20
            self.strength = 14
            self.intelligence = 12
            self.wisdom = 18
            self.dexterity = 12
        else:  # THIEF
            self.max_hp = 18
            self.max_mp = 10
            self.strength = 12
            self.intelligence = 12
            self.wisdom = 10
            self.dexterity = 18
        
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.armor_class = 10 - (self.dexterity // 3)
        
        # Inventory and spells
        self.inventory = []
        self.spells = self._learn_starting_spells()
        self.alive = True
    
    def _learn_starting_spells(self):
        """Learn starting spells based on class"""
        spells = []
        if self.char_class == CharacterClass.MAGE:
            spells = ["Fireball", "Magic Missile", "Teleport"]
        elif self.char_class == CharacterClass.CLERIC:
            spells = ["Heal", "Holy Strike", "Protection"]
        else:
            spells = ["Attack"]
        return spells
    
    def take_damage(self, damage):
        """Take damage, considering armor class"""
        damage = max(1, damage - (10 - self.armor_class) // 2)
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
        return damage
    
    def heal(self, amount):
        """Heal HP"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def cast_spell(self, spell_name, targets=None):
        """Cast a spell and use mana"""
        spell_costs = {
            "Fireball": 8,
            "Magic Missile": 5,
            "Teleport": 10,
            "Heal": 6,
            "Holy Strike": 7,
            "Protection": 5,
            "Attack": 0
        }
        
        if spell_name not in self.spells:
            return False, "Spell not learned"
        
        cost = spell_costs.get(spell_name, 0)
        if self.mp < cost:
            return False, "Not enough mana"
        
        self.mp -= cost
        return True, f"{self.name} casts {spell_name}!"
    
    def restore_mana(self, amount):
        """Restore mana"""
        self.mp = min(self.max_mp, self.mp + amount)
    
    def gain_experience(self, amount):
        """Gain experience points"""
        self.experience += amount
        # Level up at 100 exp per level
        if self.experience >= 100 * self.level:
            self.level_up()
    
    def level_up(self):
        """Level up the character"""
        self.level += 1
        self.max_hp += 5
        self.max_mp += 3
        self.hp = self.max_hp
        self.mp = self.max_mp
    
    def to_dict(self):
        """Convert character to dictionary for saving"""
        return {
            'name': self.name,
            'class': self.char_class.name,
            'level': self.level,
            'experience': self.experience,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'mp': self.mp,
            'max_mp': self.max_mp,
            'strength': self.strength,
            'intelligence': self.intelligence,
            'wisdom': self.wisdom,
            'dexterity': self.dexterity,
            'armor_class': self.armor_class,
            'inventory': self.inventory,
            'spells': self.spells,
            'alive': self.alive
        }
    
    @staticmethod
    def from_dict(data):
        """Create character from dictionary"""
        char = Character(data['name'], CharacterClass[data['class']])
        char.level = data['level']
        char.experience = data['experience']
        char.hp = data['hp']
        char.max_hp = data['max_hp']
        char.mp = data['mp']
        char.max_mp = data['max_mp']
        char.inventory = data['inventory']
        char.spells = data['spells']
        char.alive = data['alive']
        return char
