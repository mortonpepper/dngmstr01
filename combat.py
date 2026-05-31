"""Turn-based combat system"""
import random

class Combat:
    def __init__(self, party, enemy):
        self.party = party
        self.enemy = enemy
        self.turn = 0
        self.log = []
        self.combat_over = False
        self.player_won = False
        
        self._add_log(f"Combat started! You face {enemy.name}!")
    
    def _add_log(self, message):
        """Add message to combat log"""
        self.log.append(message)
    
    def player_attack(self, character, attack_type="normal"):
        """Handle player attack"""
        if not character.alive:
            self._add_log(f"{character.name} is unconscious!")
            return False
        
        if attack_type == "normal":
            # Physical attack
            hit_roll = random.randint(1, 20) + (character.dexterity // 3)
            if hit_roll > self.enemy.max_hp / 2:  # Simple hit calculation
                damage = random.randint(2, 8) + (character.strength // 3)
                self.enemy.take_damage(damage)
                self._add_log(f"{character.name} hits {self.enemy.name} for {damage} damage!")
                
                if self.enemy.hp <= 0:
                    self.combat_over = True
                    self.player_won = True
                    self._add_log(f"Victory! {self.enemy.name} is defeated!")
                    return True
            else:
                self._add_log(f"{character.name} misses!")
                return False
        
        elif attack_type == "spell":
            # Spell attack (handled separately)
            return False
        
        return True
    
    def player_cast_spell(self, character, spell_name):
        """Handle player spell cast"""
        if not character.alive:
            self._add_log(f"{character.name} is unconscious!")
            return False
        
        success, message = character.cast_spell(spell_name)
        if not success:
            self._add_log(message)
            return False
        
        self._add_log(message)
        
        # Apply spell effects
        if spell_name == "Fireball":
            damage = random.randint(6, 12) + character.intelligence // 2
            self.enemy.take_damage(damage)
            self._add_log(f"Fireball hits for {damage} damage!")
            if self.enemy.hp <= 0:
                self.combat_over = True
                self.player_won = True
                self._add_log(f"Victory! {self.enemy.name} is defeated!")
        
        elif spell_name == "Magic Missile":
            damage = random.randint(3, 6) + character.intelligence // 4
            self.enemy.take_damage(damage)
            self._add_log(f"Magic Missile hits for {damage} damage!")
            if self.enemy.hp <= 0:
                self.combat_over = True
                self.player_won = True
                self._add_log(f"Victory! {self.enemy.name} is defeated!")
        
        elif spell_name == "Heal":
            heal_amount = random.randint(3, 8) + character.wisdom // 2
            for char in self.party:
                if char.alive and char.hp < char.max_hp:
                    char.heal(heal_amount)
                    self._add_log(f"{char.name} heals for {heal_amount} HP!")
                    break
        
        elif spell_name == "Holy Strike":
            damage = random.randint(5, 10) + character.wisdom // 3
            self.enemy.take_damage(damage)
            self._add_log(f"Holy Strike hits for {damage} damage!")
            if self.enemy.hp <= 0:
                self.combat_over = True
                self.player_won = True
                self._add_log(f"Victory! {self.enemy.name} is defeated!")
        
        elif spell_name == "Protection":
            self._add_log("Party gains protection! Damage reduced next turn.")
        
        return True
    
    def player_defend(self, character):
        """Handle player defend action"""
        if not character.alive:
            self._add_log(f"{character.name} is unconscious!")
            return False
        self._add_log(f"{character.name} takes a defensive stance!")
        return True
    
    def enemy_turn(self):
        """Handle enemy attack"""
        if not self.enemy.alive:
            return
        
        # Enemy attacks random party member
        alive_members = [c for c in self.party if c.alive]
        if not alive_members:
            self.combat_over = True
            self.player_won = False
            self._add_log("Your party has been defeated!")
            return
        
        target = random.choice(alive_members)
        damage = self.enemy.attack()
        actual_damage = target.take_damage(damage)
        self._add_log(f"{self.enemy.name} attacks {target.name} for {actual_damage} damage!")
        
        if target.hp <= 0:
            self._add_log(f"{target.name} has been defeated!")
            if not any(c.alive for c in self.party):
                self.combat_over = True
                self.player_won = False
                self._add_log("Your party has been defeated!")
    
    def end_combat(self):
        """Handle end of combat rewards"""
        if self.player_won:
            exp_reward = self.enemy.experience_reward
            for character in self.party:
                if character.alive:
                    character.gain_experience(exp_reward)
            self._add_log(f"Party gains {exp_reward} experience points!")
            return exp_reward
        return 0
