"""Save and load game state"""
import json
import os
from character import Character, CharacterClass
from dungeon import Dungeon

class GameSave:
    def __init__(self, filename="dungeon_master_save.json"):
        self.filename = filename
    
    def save_game(self, party, dungeon, gold=0):
        """Save game state to file"""
        save_data = {
            'party': [char.to_dict() for char in party],
            'dungeon': dungeon.to_dict(),
            'gold': gold
        }
        
        with open(self.filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"Game saved to {self.filename}")
    
    def load_game(self):
        """Load game state from file"""
        if not os.path.exists(self.filename):
            return None, None, 0
        
        try:
            with open(self.filename, 'r') as f:
                save_data = json.load(f)
            
            # Load party
            party = [Character.from_dict(char_data) for char_data in save_data['party']]
            
            # Load dungeon
            dungeon = Dungeon.from_dict(save_data['dungeon'])
            
            gold = save_data.get('gold', 0)
            
            print(f"Game loaded from {self.filename}")
            return party, dungeon, gold
        
        except Exception as e:
            print(f"Error loading game: {e}")
            return None, None, 0
    
    def delete_save(self):
        """Delete save file"""
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Save file {self.filename} deleted")
